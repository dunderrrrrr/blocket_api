{pkgs}:
pkgs.poetry2nix.mkPoetryEnv {
  python = pkgs.python312;
  projectDir = ./.;
  editablePackageSources.playground = ./.;
  preferWheels = true;
  overrides = pkgs.poetry2nix.overrides.withDefaults (self: super: {
    ### package specific overrides go here...
  });
}
