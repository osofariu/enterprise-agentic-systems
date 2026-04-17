# Enterprise Agentic Systems: From Data to Deployment

This training series will guide participants through a realistic client scenario in the manufacturing domain, covering the full lifecycle from initial business and architectural discovery through the design and implementation of a multi-agent system.

## Getting Started

### Install `uv`

`uv` is a fast Python package and project manager. Install it once and use it everywhere — it works the same on macOS and Windows.

**macOS / Linux**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell)**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, restart your terminal and verify with:
```bash
uv --version
```

### Key `uv` commands you'll use

| Command              | What it does                                                                      |
| -------------------- | --------------------------------------------------------------------------------- |
| `uv sync`            | Create the virtual environment and install all dependencies from `pyproject.toml` |
| `uv add <package>`   | Add a new dependency to the project                                               |
| `uv run <script.py>` | Run a Python script inside the managed environment                                |

> You do **not** need to manually activate a virtual environment. `uv run` handles that for you.

### Troubleshooting tips

**`uv` not found after install**
Close and reopen your terminal — the PATH update doesn't take effect in the current session. If it still doesn't work, check that `~/.local/bin` (macOS/Linux) or `%USERPROFILE%\.local\bin` (Windows) is on your PATH.

**`uv sync` doesn't download Python**
This requires a recent version of `uv`. Run `uv self update` to make sure you're on the latest release, then retry.

**Firewall or proxy blocking downloads**
If you're on a corporate network and downloads fail, set your proxy before running any `uv` command:
```bash
export HTTPS_PROXY=http://your-proxy:port   # macOS/Linux
$env:HTTPS_PROXY="http://your-proxy:port"   # Windows PowerShell
```

For anything else, the [uv documentation](https://docs.astral.sh/uv/) is thorough and searchable.

## Tools for data exploration

### Install the `SQLite3 Editor` VSCode extension:

```shell
code --install-extension yy0931.vscode-sqlite3-editor
```

### Install the data exploration tools

Adds jupyter and pandas as project dependencies:

```shell
uv add jupyter pandas
```

### Install the Jupyter extension for VS Code

Gives VS Code the ability to open/render/run notebooks:

```shell
code --install-extension ms-toolsai.jupyter
```



