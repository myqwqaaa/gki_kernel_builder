# GKI Kernel Builder

Effortlessly building Android Generic Kernel Image (GKI).

---

## Requirements

* Ubuntu/Debian-based Linux
* Python 3.12+

Install dependencies:

```bash
sudo apt update
sudo apt install bc bison ccache curl flex git git-lfs tar wget

python3 -m pip install uv
```

Initialize Git LFS:

```bash
git lfs install
```

---

## Quick Start

### Local Run

1. **Clone the repository**:

   ```bash
   git clone https://github.com/bachnxuan/gki_kernel_builder.git
   cd gki_kernel_builder
   ```

2. **Set up the environment**:

   ```bash
   uv venv        # Create and activate a virtual environment
   uv sync        # Install Python dependencies
   ```

3. **Build the kernel**:

   ```bash
   # Interactive mode
   uv run python3 run.py

   # Non-interactive mode
   KSU=<NONE|NEXT|SUKI> SUSFS=<true|false> LXC=<true|false> LOCAL_RUN="true" uv run python3 -m src.main
   ```

4. **Retrieve artifacts**:

   * Find the boot image and the flashable AnyKernel3 zip in the `dist/` directory.

---

## GitHub Workflows

1. **Fork the repository** to your GitHub account.
2. **Configure secrets** in both this and your release repository:

   * `GH_TOKEN`: A Personal Access Token (PAT) with **repo** and **workflow** read/write permissions.

---

## Configuration

**Important**: If you plan to build a GKI Kernel for other devices, set `LXC` to `false` or remove function completely as it only supports `xaga` (ESK Kernel).

Customize your build by:

* `config/config.py` – Contains kernel configuration settings.
* `config/manifest.py` – Specifies repository sources and branches.
* `main.py` – The main script responsible for orchestrating the build.

---

## License

This project is distributed under the [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html). See `LICENSE` for details.
