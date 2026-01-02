import ast
import sys
from pathlib import Path


def get_public_names_from_file(filepath: Path) -> dict[str, Path]:
    with open(filepath) as f:
        tree = ast.parse(f.read())

    public_names = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if not node.name.startswith("_"):
                public_names[node.name] = filepath
        elif isinstance(node, ast.FunctionDef):
            if not node.name.startswith("_"):
                public_names[node.name] = filepath

    return public_names


def get_all_exports(init_file: Path) -> set[str]:
    with open(init_file) as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    if isinstance(node.value, ast.List):
                        return {
                            elt.value  # type: ignore[misc]
                            for elt in node.value.elts
                            if isinstance(elt, ast.Constant)
                        }
    return set()


def main() -> None:
    EXCLUDED_NAMES = {
        "QueryParam",  # internal
        "MobilityAd",  # internal
        "extend",  # internal
        "parse",  # internal
        "url",  # internal
        "get_ad",  # used with api.get_ad()
        "search",  # used with api.search()
        "search_car",  # used with api.search_car()
        "search_boat",  # used with api.search_boat()
        "search_mc",  # used with api.search_mc()
    }

    package_dir = Path("blocket_api")
    init_file = package_dir / "__init__.py"

    source_files = [
        package_dir / "constants.py",
        package_dir / "ad_parser.py",
        package_dir / "blocket.py",
    ]

    if not init_file.exists():
        print(f"Error: {init_file} not found")
        sys.exit(1)

    all_public_names = {}
    for source_file in source_files:
        if source_file.exists():
            names = get_public_names_from_file(source_file)
            all_public_names.update(names)
        else:
            print(f"Warning: {source_file} not found, skipping")

    all_exports = get_all_exports(init_file)

    missing_from_all = {
        name: filepath
        for name, filepath in all_public_names.items()
        if name not in all_exports and name not in EXCLUDED_NAMES
    }

    errors = []

    if missing_from_all:
        for name, filepath in sorted(missing_from_all.items()):
            errors.append(f"  {filepath.relative_to(package_dir.parent)}: {name}")

    if errors:
        print(
            "Make sure to add new public names to __all__ in __init__.py or exclude it:"
        )
        print("\n".join(errors))

        sys.exit(1)

    print(f"✅ All {len(all_public_names)} public names are in __all__")
    sys.exit(0)


if __name__ == "__main__":
    main()
