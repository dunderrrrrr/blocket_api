import htpy as h

from docs.components_base import SWAGGER, sidebar_link, sidebar_section


def _resolve(schema: dict, schemas: dict) -> dict:
    if not schema:
        return {}
    if "$ref" in schema:
        return schemas.get(schema["$ref"].split("/")[-1], {})
    if "anyOf" in schema:
        for s in schema["anyOf"]:
            if s.get("type") != "null":
                return _resolve(s, schemas)
    return schema


def _type_label(schema: dict, schemas: dict) -> str:
    s = _resolve(schema, schemas)
    if s.get("type") == "array":
        inner = _resolve(s.get("items", {}), schemas)
        if inner.get("enum"):
            return "array[enum]"
        return f"array[{inner.get('type', 'string')}]"
    return s.get("type", "string")


def _enum_values(schema: dict, schemas: dict) -> list:
    s = _resolve(schema, schemas)
    if s.get("enum"):
        return s["enum"]
    if s.get("type") == "array":
        inner = _resolve(s.get("items", {}), schemas)
        return inner.get("enum", [])
    return []


_ENUM_PREVIEW_COUNT = 5


def _enum_cell(enums: list) -> h.Node:
    if not enums:
        return h.td(".ep-values-cell")["—"]
    if len(enums) <= _ENUM_PREVIEW_COUNT:
        return h.td(".ep-values-cell")[h.div(".ep-values")[[h.code[v] for v in enums]]]

    preview, rest = enums[:_ENUM_PREVIEW_COUNT], enums[_ENUM_PREVIEW_COUNT:]
    return h.td(".ep-values-cell")[
        h.details(".ep-values-toggle")[
            h.div(".ep-values")[[h.code[v] for v in preview]],
            h.div(".ep-values.ep-values-rest")[[h.code[v] for v in rest]],
            h.summary(".ep-values-btn")[
                h.span(".ep-values-btn-more")[f"Show all ({len(enums)}) ▾"],
                h.span(".ep-values-btn-less")["Show less ▴"],
            ],
        ]
    ]


def _param_row(p: dict, schemas: dict) -> h.Node:
    schema = p.get("schema", {})
    required = p.get("required", False)
    in_path = p.get("in") == "path"
    type_label = _type_label(schema, schemas)
    default = _resolve(schema, schemas).get("default", "")
    enums = _enum_values(schema, schemas)

    return h.tr[
        h.td[
            h.code[p["name"]],
            h.span(".param-in-path")["path"] if in_path else "",
        ],
        h.td[
            h.span(".param-required" if required else ".param-optional")[
                "required" if required else "optional"
            ]
        ],
        h.td(".type-code")[type_label],
        h.td[h.code(".default-code")[str(default)] if default != "" else "—"],
        _enum_cell(enums),
    ]


def _slugify(path: str) -> str:
    return path.replace("/", "-").replace("{", "").replace("}", "").lstrip("-")


def _endpoint_block(path: str, op: dict, schemas: dict) -> h.Node:
    params = op.get("parameters", [])
    slug = _slugify(path)
    required_params = [p for p in params if p.get("required")]
    resolved_path = path
    for p in required_params:
        if p.get("in") == "path":
            resolved_path = resolved_path.replace(f"{{{p['name']}}}", "VALUE")
    qs = "&".join(
        f"{p['name']}=VALUE" for p in required_params if p.get("in") != "path"
    )
    curl_url = f"https://blocket-api.se{resolved_path}" + (f"?{qs}" if qs else "")

    return h.div(".ep-block", id=slug)[
        h.div(".ep-block-header")[
            h.span(".method-badge")["GET"],
            h.code(".ep-path")[path],
        ],
        h.p(".ep-summary")[op.get("summary", "")],
        h.div(".endpoint-table")[
            h.table[
                h.thead[
                    h.tr[
                        h.th["Parameter"],
                        h.th["Required"],
                        h.th["Type"],
                        h.th["Default"],
                        h.th["Values"],
                    ]
                ],
                h.tbody[
                    [_param_row(p, schemas) for p in params]
                    if params
                    else h.tr[h.td(colspan="5")["No parameters"]]
                ],
            ]
        ],
        h.div(".ep-curl")[
            h.span(".install-prompt")["$"],
            h.code[f'curl "{curl_url}"'],
        ],
    ]


def _sidebar(paths: dict) -> list[h.Node]:
    links = [
        sidebar_link(
            op.get("summary", path),
            f"#{_slugify(path)}",
        )
        for path, methods in paths.items()
        for op in [methods.get("get", next(iter(methods.values())))]
    ]
    return [
        sidebar_section("Endpoints", links),
        sidebar_section(
            "More",
            [
                sidebar_link("Quickstart", "/quickstart"),
                sidebar_link("Examples", "/examples"),
                sidebar_link("Swagger ↗", SWAGGER),
            ],
        ),
    ]


def render(spec: dict) -> h.Node:
    schemas = spec.get("components", {}).get("schemas", {})
    paths = spec.get("paths", {})

    endpoint_blocks = [
        _endpoint_block(path, methods.get("get", next(iter(methods.values()))), schemas)
        for path, methods in paths.items()
    ]

    swagger_tip = h.div(".ep-swagger-tip")[
        "Autogenerated from ",
        h.a(href=f"{SWAGGER}/openapi.json", target="_blank")["openapi.json"],
        ". Full interactive docs at ",
        h.a(href=SWAGGER, target="_blank")["Swagger ↗"],
        ".",
    ]

    return h.div(style="max-width:1200px;margin:0 auto;")[
        h.div(".doc-layout")[
            h.aside(".sidebar")[_sidebar(paths)],
            h.main[swagger_tip, endpoint_blocks],
        ]
    ]
