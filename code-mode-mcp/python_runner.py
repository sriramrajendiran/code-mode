#!/usr/bin/env python3
"""
Python runner subprocess for code-mode-mcp.

This script is spawned as a child process by the Node.js MCP server to execute
Python code using the 'code-mode' PyPI package (module: utcp_code_mode).

Protocol:
  stdin:  single JSON object:
    {
      "code":     str,   # Python code to execute
      "config":   dict,  # raw UTCP config dict (same as .utcp_config.json contents)
      "root_dir": str,   # filesystem root for resolving relative paths in config
      "timeout":  int    # timeout in seconds (default: 30)
    }

  stdout: single JSON object (one of):
    { "success": true,  "result": <any>,  "logs": [str, ...] }
    { "success": false, "error": str,     "result": null, "logs": [str, ...] }

  stderr: used freely for diagnostics (forwarded to Node's stderr by the parent).
"""

import sys
import json
import asyncio


def main() -> None:
    try:
        raw = sys.stdin.read()
        request = json.loads(raw)
    except Exception as e:
        _write_error(f"Failed to read/parse stdin request: {e}")
        return

    code: str = request.get("code", "")
    config: dict = request.get("config", {})
    root_dir: str = request.get("root_dir", ".")
    timeout: int = int(request.get("timeout", 30))

    try:
        from utcp_code_mode import CodeModeUtcpClient  # noqa: F401
    except ImportError:
        _write_error(
            "The 'code-mode' PyPI package is not installed or not importable. "
            "Install it with: pip install code-mode  "
            "(imported as: from utcp_code_mode import CodeModeUtcpClient)"
        )
        return

    async def run() -> None:
        try:
            client = await CodeModeUtcpClient.create(root_dir=root_dir, config=config)
        except Exception as e:
            _write_error(f"Failed to create CodeModeUtcpClient: {e}")
            return

        try:
            result_dict = await client.call_tool_chain(code=code, timeout=timeout)
            _write_success(
                result=result_dict.get("result"),
                logs=result_dict.get("logs", [])
            )
        except Exception as e:
            _write_error(f"call_tool_chain failed: {e}")

    asyncio.run(run())


def _write_success(result: object, logs: list) -> None:
    response = {
        "success": True,
        "result": _make_json_safe(result),
        "logs": [str(l) for l in logs],
    }
    sys.stdout.write(json.dumps(response))
    sys.stdout.flush()


def _write_error(error: str, logs: list = None) -> None:
    response = {
        "success": False,
        "error": error,
        "result": None,
        "logs": [str(l) for l in (logs or [])],
    }
    sys.stdout.write(json.dumps(response))
    sys.stdout.flush()
    sys.stderr.write(f"[python_runner] ERROR: {error}\n")
    sys.stderr.flush()


def _make_json_safe(value: object) -> object:
    try:
        json.dumps(value)
        return value
    except (TypeError, ValueError):
        return str(value)


if __name__ == "__main__":
    main()
