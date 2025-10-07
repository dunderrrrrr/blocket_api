{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };
  outputs = inputs @ {
    self,
    nixpkgs,
    flake-parts,
    ...
  }:
    flake-parts.lib.mkFlake {inherit inputs;} {
      systems = ["x86_64-linux"];
      perSystem = {
        pkgs,
        lib,
        ...
      }: let
        python = pkgs.python3;
      in {
        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.uv
            pkgs.ruff
            python
            (pkgs.writeShellScriptBin "logs" ''
              sudo jq -r '. | "\(.ts | todateiso8601) \(.request.client_ip) \(.request.method) \(.request.uri)"' /var/log/caddy/access-blocket-api.se.log | grep v1
            '')  
            (pkgs.writeShellScriptBin "build" ''
              git pull
              mkdocs build -d /srv/blocket-api/
            '') 

          ];
          shellHook = ''
            uv venv
            source .venv/bin/activate
            uv pip sync requirements.txt
            pre-commit install --overwrite
            set -a
            source .env 2> /dev/null
          '';
        };
      };
    };
}
