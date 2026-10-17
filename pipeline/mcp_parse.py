#!/usr/bin/env python3
"""Parse a Postiz MCP response body.

Postiz switched the /mcp endpoint to Server Sent Events on 2026-10-15: the
body now comes back as "event: message\\ndata: {...}" with a text/event-stream
content type, even when the request asks for application/json. Before that it
was a bare JSON object. Accept both, so a switch back does not break anything.
"""
import json


def parse(out):
    if isinstance(out, bytes):
        out = out.decode("utf-8", "replace")
    out = out.strip()
    if out.startswith("{"):
        return json.loads(out)
    # SSE: take the last data: line, which carries the JSON-RPC envelope.
    chunks = [ln[5:].strip() for ln in out.splitlines() if ln.startswith("data:")]
    if not chunks:
        raise ValueError(f"not JSON and no SSE data line: {out[:200]!r}")
    return json.loads(chunks[-1])
