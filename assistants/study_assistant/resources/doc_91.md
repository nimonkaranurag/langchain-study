[Skip to content](#uv)



* [Highlights](#highlights)
* [Installation](#installation)
* [Projects](#projects)
* [Scripts](#scripts)
* [Tools](#tools)
* [Python versions](#python-versions)
* [The pip interface](#the-pip-interface)
* [Learn more](#learn-more)

# [uv](#uv)

An extremely fast Python package and project manager, written in Rust.

*Installing [Trio](https://trio.readthedocs.io/)'s dependencies with a warm cache.*

## [Highlights](#highlights)

* 🚀 A single tool to replace `pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `twine`, `virtualenv`, and more.
* ⚡️ [10-100x faster](https://github.com/astral-sh/uv/blob/main/BENCHMARKS.md) than `pip`.
* 🗂️ Provides [comprehensive project management](#projects), with a [universal lockfile](concepts/projects/layout/#the-lockfile).
* ❇️ [Runs scripts](#scripts), with support for [inline dependency metadata](guides/scripts/#declaring-script-dependencies).
* 🐍 [Installs and manages](#python-versions) Python versions.
* 🛠️ [Runs and installs](#tools) tools published as Python packages.
* 🔩 Includes a [pip-compatible interface](#the-pip-interface) for a performance boost with a familiar CLI.
* 🏢 Supports Cargo-style [workspaces](concepts/projects/workspaces/) for scalable projects.
* 💾 Disk-space efficient, with a [global cache](concepts/cache/) for dependency deduplication.
* ⏬ Installable without Rust or Python via `curl` or `pip`.
* 🖥️ Supports macOS, Linux, and Windows.

uv is backed by [Astral](https://astral.sh), the creators of [Ruff](https://github.com/astral-sh/ruff).

## [Installation](#installation)

Install uv with our official standalone installer:

```
 $    |  
```

```
PS> powershell -ExecutionPolicy ByPass -c"irm https://astral.sh/uv/install.ps1 | iex"
```

Then, check out the [first steps](getting-started/first-steps/) or read on for a brief overview.

Tip

uv may also be installed with pip, Homebrew, and more. See all of the methods on the [installation page](getting-started/installation/).

## [Projects](#projects)

uv manages project dependencies and environments, with support for lockfiles, workspaces, and more, similar to `rye` or `poetry`:

```
 $   Initialized project `example` at `/home/user/example` $ cd  $   Creating virtual environment at: .venv Resolved 2 packages in 170ms Built example @ file:///home/user/example Prepared 2 packages in 627ms Installed 2 packages in 1ms + example==0.1.0 (from file:///home/user/example) + ruff==0.5.4 $    All checks passed! $  Resolved 2 packages in 0.33ms $  Resolved 2 packages in 0.70msAudited 1 package in 0.02ms
```

See the [project guide](guides/projects/) to get started.

uv also supports building and publishing projects, even if they're not managed with uv. See the [packaging guide](guides/package/) to learn more.

## [Scripts](#scripts)

uv manages dependencies and environments for single-file scripts.

Create a new script and add inline metadata declaring its dependencies:

```
 $ echo  'import requests; print(requests.get("https://astral.sh"))'   $     Updated `example.py`
```

Then, run the script in an isolated virtual environment:

```
 $   Reading inline script metadata from: example.py Installed 5 packages in 12ms 
```

See the [scripts guide](guides/scripts/) to get started.

## [Tools](#tools)

uv executes and installs command-line tools provided by Python packages, similar to `pipx`.

Run a tool in an ephemeral environment using `uvx` (an alias for `uv tool run`):

```
 $   'hello world!' Resolved 1 package in 167ms Installed 1 package in 9ms + pycowsay==0.0.0.2  """ ------------< hello world! > ------------  \ ^__^ \ (oo)\_______ (__)\ )\/\ ||----w |  || ||
```

Install a tool with `uv tool install`:

```
 $    Resolved 1 package in 6ms Installed 1 package in 2ms + ruff==0.5.4Installed 1 executable: ruff $  ruff 0.5.4
```

See the [tools guide](guides/tools/) to get started.

## [Python versions](#python-versions)

uv installs Python and allows quickly switching between versions.

Install multiple Python versions:

```
 $    3  3  3Searching for Python versions matching: Python 3.10Searching for Python versions matching: Python 3.11Searching for Python versions matching: Python 3.12Installed 3 versions in 3.42s + cpython-3.10.14-macos-aarch64-none + cpython-3.11.9-macos-aarch64-none + cpython-3.12.4-macos-aarch64-none
```

Download Python versions as needed:

```
 $    3Using CPython 3.12.0Creating virtual environment at: .venvActivate with: source .venv/bin/activate $      Python 3.8.16 (a9dbdca6fc3286b0addd2240f11d97d8e8de187a, Dec 29 2022, 11:45:30)[PyPy 7.3.11 with GCC Apple LLVM 13.1.6 (clang-1316.0.21.2.5)] on darwinType "help", "copyright", "credits" or "license" for more information.>>>>
```

Use a specific Python version in the current directory:

```
 $    3Pinned `.python-version` to `3.11`
```

See the [installing Python guide](guides/install-python/) to get started.

## [The pip interface](#the-pip-interface)

uv provides a drop-in replacement for common `pip`, `pip-tools`, and `virtualenv` commands.

uv extends their interfaces with advanced features, such as dependency version overrides, platform-independent resolutions, reproducible resolutions, alternative resolution strategies, and more.

Migrate to uv without changing your existing workflows — and experience a 10-100x speedup — with the `uv pip` interface.

Compile requirements into a platform-independent requirements file:

```
 $     \   \   Resolved 43 packages in 12ms
```

Create a virtual environment:

```
 $  Using CPython 3.12.3Creating virtual environment at: .venvActivate with: source .venv/bin/activate
```

Install the locked requirements:

```
 $    Resolved 43 packages in 11ms Installed 43 packages in 208ms + babel==2.15.0 + black==24.4.2 + certifi==2024.7.4 ...
```

See the [pip interface documentation](pip/) to get started.

## [Learn more](#learn-more)

See the [first steps](getting-started/first-steps/) or jump straight to the [guides](guides/) to start using uv.

 