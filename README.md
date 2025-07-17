# GKI Kernel Builder

[![codecov](https://codecov.io/gh/bachnxuan/gki_kernel_builder/graph/badge.svg?token=EYKHK1OOC4)](https://codecov.io/gh/bachnxuan/gki_kernel_builder)

Effortlessly building Android Generic Kernel Image (GKI).

---

## Requirements

* Ubuntu/Debian-based Linux
* Python 3.12+

Install dependencies:

```bash
sudo apt update
sudo apt install bc bison ccache curl flex git tar wget aria2 jq

python3 -m pip install uv
```

---

## Setup Kernel Builder

1. **Clone the repository**:

   ```bash
   git clone https://github.com/bachnxuan/gki_kernel_builder.git
   cd gki_kernel_builder
   ```

2. **Set up venv**:

   ```bash
   uv sync --frozen --no-install-project
   source .venv/bin/activate
   ```

   Once you are finished working with the project, disable the virtual environment (venv) via `deactivate`.

## Build the kernel

Builds are performed via the custom wrapper script `run.py`

### Usage

   ```python
   usage: run.py [-h] {build,clean} ...

   Kernel Builder

   positional arguments:
   {build,clean}
      build        Compile a kernel image
      clean        Remove build artefacts

   options:
   -h, --help     show this help message and exit
   ```

### Build

   ```python
   usage: run.py build build [-v/--verbose] [-k/--ksu {NONE,NEXT,SUKI}] [-s/--susfs] [-l/--lxc]

   options:
   -h, --help            show this help message and exit
   -v, --verbose, --no-verbose
                           Enable verbose output
   -k {NONE,NEXT,SUKI}, --ksu {NONE,NEXT,SUKI}
                           KernelSU variant (default: NONE)
   -s, --susfs, --no-susfs
                           Enable SUSFS support
   ```

### Build Example

   `KernelSU Next` with `SUSFS` and no `LXC`:

   ```bash
   uv run run.py build -k NEXT -s
   ```

   `SukiSU` with `SUSFS` and `LXC` disabled and verbose output:

   ```bash
   uv run run.py build --verbose --ksu SUKI --no-susfs --no-lxc
   ```

### Clean

   ```python
   usage: run.py clean [-h] [-a | --all | --no-all]

   options:
   -h, --help           show this help message and exit
   -a, --all, --no-all  Also delete dist/ (out) directory
   ```

---

## GitHub Workflows

1. **Fork** this repo to your GitHub account.

2. **Add secret** `GH_TOKEN`
   * PAT scopes (read and write): `workflow`, `content`
   * Add PAT access to your release and kernel builder repo
   * Repo → Settings → Secrets → Actions → **New secret**.

3. **Optional Telegram secrets**

> [!NOTE]
> Add the below Telegram secrets below when you want to notify completed build on Telegram.
> The Telegram notify feature can be config via `NOTIFY` on workflows_dispatch and workflows_call input.

   * `TG_BOT_TOKEN` – Telegram Bot Token
   * `TG_CHAT_ID` – Telegram Chat ID

---

## Configuration

> [!WARNING]
> If you plan to build a GKI Kernel for other devices, set `LXC` to `false` or remove function completely as it only supports `xaga` (ESK Kernel).

Customize your build by:

* `config/config.py` – Contains kernel configuration settings.
* `config/manifest.py` – Specifies repository sources and branches.
* `kernel_builder.py` – The main script responsible for orchestrating the build.

---

## License

This project is distributed under the [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html). See `LICENSE` for details.
