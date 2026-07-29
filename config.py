"""
Central place for loading Azure OpenAI credentials.

Checks st.secrets first (used when deployed on Streamlit Community Cloud),
then falls back to a local .env file (used during local development).
This way app.py and utils/ never need to change between local and deployed.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # no-op if .env doesn't exist, harmless in deployment


def _get(key: str, default: str = "") -> str:
    # Try Streamlit secrets first (only works inside a Streamlit runtime)
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)


AZURE_OPENAI_API_KEY = _get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = _get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = _get("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = _get("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")


def validate_config():
    """Call this at app startup so missing keys fail loudly with a clear message."""
    missing = [
        name for name, val in [
            ("AZURE_OPENAI_API_KEY", AZURE_OPENAI_API_KEY),
            ("AZURE_OPENAI_ENDPOINT", AZURE_OPENAI_ENDPOINT),
            ("AZURE_OPENAI_DEPLOYMENT_NAME", AZURE_OPENAI_DEPLOYMENT_NAME),
        ] if not val
    ]
    if missing:
        raise EnvironmentError(
            f"Missing required config values: {', '.join(missing)}. "
            f"Check your .env file (local) or Streamlit secrets (deployed)."
        )