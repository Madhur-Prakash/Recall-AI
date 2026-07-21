"""
Ollama pre-flight for RecallAI.

`ensure_ollama_model()` runs at import time from `app.py`, so starting the
backend with `uvicorn app:app` first verifies the on-device model configured in
`.env` (`OLLAMA_MODEL`). If the model is missing, an interactive user is prompted
to download it; on confirmation the model is pulled before the server continues.

Behaviour by situation:
    - model installed .............. continue
    - missing, interactive ......... prompt; on "yes" pull then continue, on "no" abort
    - missing, non-interactive ..... pull if OLLAMA_AUTO_PULL is truthy, else warn and continue
    - daemon unreachable ........... abort if interactive (start `ollama serve`), else warn and continue
"""

import os
import sys
from recall_ai.helpers.utils import truthy as _truthy

# Keep console output safe on legacy Windows code pages (cp1252, etc.).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def _installed_model_names(client) -> list:
    """Return the list of model tags currently installed in Ollama."""
    resp = client.list()
    models = getattr(resp, "models", None)
    if models is None and isinstance(resp, dict):
        models = resp.get("models", [])
    names = []
    for m in models or []:
        name = getattr(m, "model", None)
        if name is None and isinstance(m, dict):
            name = m.get("model") or m.get("name")
        if name:
            names.append(name)
    return names


def _is_installed(model: str, names: list) -> bool:
    if model in names:
        return True
    # Tolerate an untagged model name (e.g. "qwen3" matches "qwen3:latest" / "qwen3:8b").
    if ":" not in model:
        return any(n.split(":", 1)[0] == model for n in names)
    return False


def _pull_model(client, model: str) -> None:
    print("\nDownloading '%s' via Ollama - this can take a while...\n" % model)
    last_len = 0
    for progress in client.pull(model, stream=True):
        status = getattr(progress, "status", "") or ""
        total = getattr(progress, "total", None)
        completed = getattr(progress, "completed", None)
        if total and completed:
            pct = completed / total * 100
            done_mb = completed / 1_048_576
            total_mb = total / 1_048_576
            line = f"   {status}: {pct:5.1f}%  ({done_mb:,.0f} / {total_mb:,.0f} MB)"
        else:
            line = f"   {status}..."
        sys.stdout.write("\r" + line.ljust(last_len))
        sys.stdout.flush()
        last_len = len(line)
    sys.stdout.write("\n")
    print("[OK] Model '%s' is ready.\n" % model)


def ensure_ollama_model() -> None:
    """Verify (and optionally download) the configured Ollama model before startup.

    Aborts the process (sys.exit(1)) only when an interactive user cannot proceed;
    stays non-blocking for non-interactive contexts so containers still boot.
    """
    model = os.getenv("OLLAMA_MODEL", "qwen3:8b")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    interactive = sys.stdin.isatty()

    print("RecallAI - checking on-device Ollama model '%s'..." % model)

    try:
        from ollama import Client
    except ImportError:
        print("[x] The 'ollama' Python package is not installed. Run: uv sync  (or pip install ollama)")
        if interactive:
            sys.exit(1)
        return

    client = Client(host=base_url)

    # 1) Is the Ollama daemon reachable?
    try:
        installed = _installed_model_names(client)
    except Exception as exc:
        print("[x] Could not reach the Ollama daemon at %s" % base_url)
        print("    (%s: %s)" % (type(exc).__name__, exc))
        print("    Start it first with:  ollama serve")
        if interactive:
            sys.exit(1)
        print("    Continuing startup anyway (non-interactive).")
        return

    # 2) Already installed?
    if _is_installed(model, installed):
        print("[OK] Ollama model '%s' is available." % model)
        return

    # 3) Missing - decide what to do.
    print("[!] Ollama model '%s' (from .env OLLAMA_MODEL) is not installed." % model)

    if _truthy(os.getenv("OLLAMA_AUTO_PULL")):
        proceed = True
    else:
        answer = None
        if interactive:
            try:
                answer = input("    Download it now? [Y/n]: ").strip().lower()
            except EOFError:
                answer = None  # no usable stdin; fall through to skip
        if answer is None:
            # Non-interactive (Docker/CI) or no stdin: warn but let the server start.
            print("    No interactive input - skipping download.")
            print("    Pull it manually with:  ollama pull %s" % model)
            print("    (or set OLLAMA_AUTO_PULL=true to download automatically at startup)")
            return
        proceed = answer in {"", "y", "yes"}

    if not proceed:
        print("\n[x] '%s' is required to run RecallAI. Aborting startup." % model)
        print("    You can download it later with:  ollama pull %s" % model)
        sys.exit(1)

    # 4) Download, then continue.
    try:
        _pull_model(client, model)
    except Exception as exc:
        print("\n[x] Failed to download '%s': %s: %s" % (model, type(exc).__name__, exc))
        if interactive:
            sys.exit(1)
