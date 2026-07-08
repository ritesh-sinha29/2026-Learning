# Python Environment & Package Management Guide

This guide covers the most popular Python environment and package management tools: **`uv`**, **`Poetry`**, **`Pip + Venv`**, and **`Conda`**. It explains how to install them, use them, and choose the best one for your needs.

---

## 📊 Quick Comparison Matrix

| Feature | `pip` + `venv` (Traditional) | `Poetry` (Workflow Tool) | `uv` (Modern Rust-based) | `Conda` (Data Science) |
| :--- | :--- | :--- | :--- | :--- |
| **Speed** | 🐢 Slow | 🐢 Slow / Medium | ⚡ **Extremely Fast** | 🐢 Slow |
| **Written In** | Python | Python | **Rust** | Python / C |
| **Dependency Resolution** | Basic | Advanced | **Advanced (Rust-fast)** | Advanced (SAT solver) |
| **Lockfile Support** | No (requires `pip-compile`) | Yes (`poetry.lock`) | **Yes (`uv.lock`)** | No (only environment exports) |
| **Python Version Mgmt** | No | No (uses system Python) | **Yes (Automatic download)** | Yes |
| **Standard Compliance** | Low | High (PEP 517/518/621) | **High (PEP 517/518/621)** | Custom ecosystem |
| **Use Case** | Quick scripts | Libraries / Packaging | **General & Web Projects** | Data Science / ML |

---

## ⚡ 1. `uv` (Recommended for Modern Projects)

**`uv`** is an extremely fast, single-binary Python package manager written in Rust. It serves as a drop-in replacement for `pip`, `pip-tools`, `venv`, `poetry`, and `pyenv`.

### 💻 Installation
* **Windows (PowerShell)**:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
* **macOS / Linux**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### 🚀 Common Commands
* **Initialize a new project**:
  ```powershell
  uv init --python 3.13
  ```
* **Add a dependency**:
  ```powershell
  uv add langchain
  ```
* **Add a dev dependency** (testing, formatting, linting):
  ```powershell
  uv add --dev pytest black
  ```
* **Run a file** (automatically creates/syncs `.venv`):
  ```powershell
  uv run main.py
  ```
* **Sync environment** (installs missing packages from `pyproject.toml`):
  ```powershell
  uv sync
  ```
* **Run a one-off tool** (without installing it globally or in project):
  ```powershell
  uvx ruff format .
  ```

> [!TIP]
> **Why `uv` is the best choice today:** It downloads Python versions automatically on demand, resolves dependencies in milliseconds, and uses a unified standard `pyproject.toml` that makes your project highly portable.

---

## 🎼 2. `Poetry` (Best for Packaging & Publishing Libraries)

**`Poetry`** is a complete Python package and dependency manager. It handles dependency resolution, virtual environment creation, package building, and publishing to PyPI.

### 💻 Installation
* **Windows (PowerShell)**:
  ```powershell
  (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
  ```
* **macOS / Linux**:
  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```

### 🚀 Common Commands
* **Initialize interactively in an existing directory**:
  ```powershell
  poetry init
  ```
* **Create a new project structure**:
  ```powershell
  poetry new my-project --src
  ```
* **Add a dependency**:
  ```powershell
  poetry add langchain
  ```
* **Add a dev dependency**:
  ```powershell
  poetry add --group dev pytest
  ```
* **Run a file** (within poetry's virtual environment):
  ```powershell
  poetry run python main.py
  ```
* **Build and publish your package**:
  ```powershell
  poetry build
  poetry publish
  ```

> [!NOTE]
> Poetry requires Python to already be installed on your machine. It excels at building `.whl` and `.tar.gz` files for distribution.

---

## 📦 3. `pip` + `venv` (Traditional / Standard Python Way)

This is Python's built-in toolset. It is simple and requires zero external installations, but lacks modern features like lockfiles and automatic environment syncing.

### 💻 Installation
* Pre-installed with standard Python distributions.

### 🚀 Common Commands
* **Create a virtual environment**:
  ```powershell
  python -m venv .venv
  ```
* **Activate the environment**:
  * *Windows (PowerShell)*:
    ```powershell
    .venv\Scripts\Activate.ps1
    ```
  * *macOS / Linux*:
    ```bash
    source .venv/bin/activate
    ```
* **Install a package**:
  ```powershell
  pip install langchain
  ```
* **Save installed packages**:
  ```powershell
  pip freeze > requirements.txt
  ```
* **Install from a file**:
  ```powershell
  pip install -r requirements.txt
  ```
* **Run a file**:
  ```powershell
  python main.py
  ```

> [!WARNING]
> Standard `pip` does not resolve dependencies cleanly when conflicting sub-dependencies exist, and it can easily break environments if package versions drift.

---

## 🧪 4. `Conda` (Best for Heavy Data Science & ML)

**`Conda`** is a cross-platform package and environment manager. Unlike others, it manages non-Python packages (like C++ libraries, CUDA drivers, and binary packages) directly.

### 💻 Installation
* Download and run the graphical installer for [Miniconda (Recommended)](https://docs.anaconda.com/miniconda/) or [Anaconda](https://www.anaconda.com/).

### 🚀 Common Commands
* **Create a new environment**:
  ```powershell
  conda create -n myenv python=3.13
  ```
* **Activate the environment**:
  ```powershell
  conda activate myenv
  ```
* **Install a package**:
  ```powershell
  conda install numpy scipy pandas
  ```
* **Export environment details**:
  ```powershell
  conda env export > environment.yml
  ```
* **Create environment from file**:
  ```powershell
  conda env create -f environment.yml
  ```

> [!IMPORTANT]
> Use Conda only if you are working on machine learning / deep learning tasks requiring custom non-Python binary builds (like PyTorch with GPU CUDA support) that are complex to install via `pip`.

---

## 🏆 Summary: Which One is Best and Why?

### 🥇 Overall Winner: `uv`
For **90% of general Python and Web applications**, **`uv` is the best choice**. 
* **Rust-based Speed**: You never have to wait for dependencies to download or resolve.
* **No Version Hell**: If a project requires Python 3.12 and another requires 3.13, `uv` downloads and runs them seamlessly in isolation.
* **Zero Boilerplate**: You do not have to manually run activation commands (like `source .venv/bin/activate`) because `uv run` handles activation instantly on-the-fly.

### 🥈 Best for PyPI Library Publishing: `Poetry`
If you are developing a library that you want to **publish on PyPI (Python Package Index)** for other developers to install, **Poetry** is the industry standard. Its build and publish features are extremely robust.

### 🥉 Best for CUDA & ML: `Conda`
If you are doing heavy **deep learning / scientific computing** that requires compiling C/C++ dependencies or dealing with GPU drivers, **Conda** remains the most robust choice for compiling binary dependencies.
