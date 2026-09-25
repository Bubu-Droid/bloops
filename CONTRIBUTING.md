# Contributer's Guide

This guide will help you set up necessary dev tools for contributing
to this project. It isn't obligatory to set these tools up
for contributing; however, you're strongly recommended to do so ---
if you don't, the CI tests might fail, unless you know exactly
what you're doing, that is.

## Cloning The Repository

```bash
git clone --recursive git@github.com:Bubu-Droid/bloops.git
```

## Installing Dependencies

If you're on Linux, install `asymptote` using your package manager.
If you're on Windows, you need to install `asymptote` and add
the `asy` binary to your `PATH`, good luck. For Arch Linux, you
may run the following command:

```bash
sudo pacman -S asymptote
```

> We need asymptote for testing. If you want to skip the testing
> phase, you have to skip the entire setup of dev tools.

Now, we install project dependencies. You're advised to use `uv`,
it's blazing fast; I'll guide you on how to use it for this project.

```bash
cd bloops/
uv sync
```

Now, we install pre-commit hooks using prek.

```bash
uv run prek install
```

This finishes the installation of all necessary dependencies
for this project.
If you want to manually run tests using `pytest`, use `uv run pytest`.
If you feel overwhelmed by the pre-commit hooks, you may uninstall
them using `uv run prek uninstall`.
Note that pushing with failing pre-commit hooks will inevitably break
CI tests, as the same hooks are run in CI tests for
cross-validation. Please try to avoid this since I'll have to
clean up the mess myself after you open a PR.

> [!NOTE]
> If your formatter/linter is messing with the ones set up in pre-commit
> hooks, you may skip those specific hooks using
> `SKIP=<hook-1>,<hook-2> git commit -m "commit message"`.
> This should ideally not be the case since the set of tools used for the
> hooks are pretty standard.
