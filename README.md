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
sudo apt install bc bison ccache curl flex git tar wget aria2

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
   usage: run.py build build [-k {NONE,NEXT,SUKI,RKSU}] [-s/--susfs] [-l/--lxc]

   options:
   -h, --help            show this help message and exit
   -k {NONE,NEXT,SUKI,RKSU}, --ksu {NONE,NEXT,SUKI,RKSU}
                           KernelSU variant (default: NONE)
   -s, --susfs, --no-susfs
                           Enable SUSFS support
   -l, --lxc, --no-lxc   Enable LXC support
   ```

### Build Example

   `KernelSU Next` with `SUSFS` and `LXC` disabled:

   ```bash
   uv run run.py build --ksu NEXT --susfs --no-lxc
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

1. **Fork the repository** to your GitHub account.
2. **Configure secrets**:

   * `GH_TOKEN`: A Personal Access Token (PAT) with repo and workflow read/write permissions for the kernel builder repo and the release repo.

---

## Configuration

> [!WARNING]
> If you plan to build a GKI Kernel for other devices, set `LXC` to `false` or remove function completely as it only supports `xaga` (ESK Kernel).

Customize your build by:

* `config/config.py` – Contains kernel configuration settings.
* `config/manifest.py` – Specifies repository sources and branches.
* `main.py` – The main script responsible for orchestrating the build.

---

## License

This project is distributed under the [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html). See `LICENSE` for details.
