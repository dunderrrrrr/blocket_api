{
  inputs = {
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    alejandra = {
      url = "github:kamadorueda/alejandra/3.0.0";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs = inputs @ {
    self,
    nixpkgs,
    flake-parts,
    systems,
    poetry2nix,
    alejandra,
    ...
  }:
    flake-parts.lib.mkFlake {inherit inputs;} {
      systems = import systems;
      perSystem = {
        pkgs,
        lib,
        system,
        self',
        ...
      }: let
        poetryEnv = pkgs.callPackage ./. {};
      in {
        _module.args.pkgs = import nixpkgs {
          inherit system;
          overlays = [poetry2nix.overlays.default];
        };

        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.poetry
            poetryEnv
          ];
          POETRY_VIRTUALENVS_IN_PROJECT = true;
          shellHook = ''
            ${lib.getExe pkgs.poetry} env use ${lib.getExe pkgs.python3}
            ${lib.getExe pkgs.poetry} install --all-extras --no-root --sync

            pre-commit install --overwrite
            set -a
            source .env 2> /dev/null
          '';
        };
      };
    };
}
