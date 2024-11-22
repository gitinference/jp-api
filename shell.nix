{ pkgs ? import <nixpkgs> {}}:
let
  fhs = pkgs.buildFHSUserEnv {
    name = "my-fhs-environment";

    targetPkgs = _: [
      pkgs.micromamba
    ];

    profile = ''
      set -e
      eval "$(micromamba shell hook --shell=posix)"
      export MAMBA_ROOT_PREFIX=${builtins.getEnv "PWD"}/.mamba
      if ! test -d $MAMBA_ROOT_PREFIX/envs/jp-api; then
          micromamba create --yes -q -n jp-api
      fi
      micromamba activate jp-api
      micromamba install --yes -f requirements.txt -c conda-forge
      set +e
    '';
  };
in fhs.env