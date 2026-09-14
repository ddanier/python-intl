default:
    just --list

[unix]
_install-prek:
    #!/usr/bin/env bash
    if ( which prek > /dev/null 2>&1 )
    then
        prek install --prepare-hooks
    else
        echo "-----------------------------------------------------------------"
        echo "prek is not installed - cannot enable prek hooks!"
        echo "Recommendation: Install prek ('brew install prek')."
        echo "-----------------------------------------------------------------"
    fi

[windows]
_install-prek:
    #!powershell.exe
    Write-Host "Please ensure prek hooks are installed using 'prek install --prepare-hooks'"

install: (uv "sync" "--group" "dev") && _install-prek

update: (uv "sync" "--group" "dev")

uv *args:
    uv {{args}}

test *args: (uv "run" "pytest" "--numprocesses=logical" "--cov=python_intl" "--cov-report" "term-missing:skip-covered" args)

test-unit *args: (uv "run" "pytest" "--numprocesses=logical" "--cov=python_intl" "--cov-report" "term-missing:skip-covered" "-m" "unit" args)
test-node *args: (uv "run" "pytest" "--numprocesses=logical" "--cov=python_intl" "--cov-report" "term-missing:skip-covered" "-m" "node" args)

test-all: (uv "run" "tox")

ruff *args: (uv "run" "ruff" "check" "python_intl" "tests" "examples" args)

mypy *args: (uv "run" "mypy" "python_intl" "examples" args)

ty *args: (uv "run" "ty" "check" "python_intl" "examples" args)

basedpyright *args: (uv "run" "basedpyright" "python_intl" "examples" args)

prek: (uv "run" "prek" "run" "--all-files")

lint: ruff ty mypy basedpyright prek

qa: lint test

qa-all: lint test-all

release version: (uv "version" version)
    git add pyproject.toml
    git commit -m "release: 🔖 v$(uv version --short)" --no-verify
    git tag "v$(uv version --short)"
    git push
    git push --tags

version-bump version_bump: (uv "version" "--bump" version_bump)
    git add pyproject.toml
    git commit -m "release: 🔖 v$(uv version --short)" --no-verify
    git tag "v$(uv version --short)"
    git push
    git push --tags
