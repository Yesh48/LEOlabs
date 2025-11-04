"""Minimal MCP-compatible TCP server for Leo Core."""
from __future__ import annotations

import asyncio
import json
from typing import Any, Dict

from leo.db import get_database
from leo.graph import run_audit
from leo.utils.report_utils import state_to_report


class _RequestError(Exception):
    """Internal error to signal invalid requests."""


async def _handle_request(message: Dict[str, Any]) -> Dict[str, Any]:
    method = message.get("method")
    params = message.get("params", {})

    if method == "leo_audit":
        url = params.get("url")
        if not url:
            raise _RequestError("Missing 'url' parameter")
        state = run_audit(url)
        return state_to_report(state)

    if method == "leo_recent":
        limit = int(params.get("limit", 5))
        return get_database().recent_scores(limit=limit)

    raise _RequestError(f"Unknown method: {method}")


async def _client_session(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            try:
                message = json.loads(data.decode("utf-8"))
            except json.JSONDecodeError:
                response = {"error": "invalid_json"}
            else:
                request_id = message.get("id")
                try:
                    result = await _handle_request(message)
                    response = {"id": request_id, "result": result}
                except _RequestError as exc:
                    response = {"id": request_id, "error": str(exc)}
                except Exception as exc:  # pragma: no cover - defensive
                    response = {"id": request_id, "error": f"internal_error: {exc}"}
            writer.write(json.dumps(response).encode("utf-8") + b"\n")
            await writer.drain()
    finally:
        writer.close()
        await writer.wait_closed()


async def _run_server(host: str, port: int) -> None:
    server = await asyncio.start_server(_client_session, host, port)
    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets or [])
    print(f"Leo MCP server listening on {addrs}")
    async with server:
        await server.serve_forever()


def serve(host: str = "0.0.0.0", port: int = 8800) -> None:
    """Blocking helper to run the MCP server."""
    asyncio.run(_run_server(host, port))


__all__ = ["serve"]
