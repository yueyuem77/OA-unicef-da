#!/usr/bin/env bash
set -euo pipefail

# -------- settings --------
ENV_NAME="unicef_da_env"
PYTHON_VER="3.11"
REQ_FILE="requirements.txt"
# --------------------------

# 1. Create virtual environment only if it doesn't exist
if [[ ! -d ".venv" ]]; then
  python${PYTHON_VER} -m venv .venv
fi

# 2. Activate the venv
source .venv/bin/activate       # Windows PowerShell: .\.venv\Scripts\Activate.ps1

# 3. Upgrade pip and install requirements (idempotent)
python -m pip install --upgrade pip
if [[ -f "${REQ_FILE}" ]]; then
  pip install -r "${REQ_FILE}"
fi

echo "✅ Environment ready."

