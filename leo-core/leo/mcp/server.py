"""
leo/mcp/server.py
Model Context Protocol (MCP) server to expose LEO Core tools for GPT-native access.
"""

import json
import asyncio
from leo.graph import run_pipeline
from leo.db import get_recent_scores


async def leo_audit(url: str) -> str:
    """Run full LEO audit and return JSON result."""
    state = run_pipeline(url)
    return json.dumps({
        "url": state.url,
        "metrics": state.metrics,
        "leo_rank": state.leo_rank,
        "suggestions": state.suggestions,
        "timestamp": state.timestamp,
    })


async def leo_recent() -> str:
    """Return recent scores from the DB as JSON."""
    rows = get_recent_scores(10)
    return json.dumps([dict(r) if isinstance(r, dict) else {"url": r[0], "rank": r[1], "timestamp": r[2]} for r in rows])


async def handle_request(reader, writer):
    """Minimal async socket server to process JSON MCP-style requests."""
    while True:
        data = await reader.readline()
        if not data:
            break
        try:
            request = json.loads(data.decode())
            method = request.get("method")
            params = request.get("params", {})

            if method == "leo_audit":
                result = await leo_audit(**params)
            elif method == "leo_recent":
                result = await leo_recent()
            else:
                result = json.dumps({"error": f"Unknown method {method}"})
        except Exception as e:
            result = json.dumps({"error": str(e)})

        writer.write(result.encode() + b"\n")
        await writer.drain()
    writer.close()


def start_mcp_server(port: int = 8800):
    """Launch MCP-compatible socket server."""
    async def main():
        server = await asyncio.start_server(handle_request, "0.0.0.0", port)
        print(f"[MCP] Server running on port {port}")
        async with server:
            await server.serve_forever()

    asyncio.run(main())
