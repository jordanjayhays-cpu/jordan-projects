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


def body(d):
    """Pull the tool result out of a JSON-RPC envelope, or say why we cannot.

    A failed call comes back as {"error": {...}} with no "result", which used
    to surface as KeyError: 'result' and told nobody anything.
    """
    if "result" not in d:
        err = d.get("error") or d
        raise RuntimeError(f"postiz mcp error: {json.dumps(err)[:300]}")
    text = d["result"]["content"][0]["text"]
    if d["result"].get("isError"):
        raise RuntimeError(f"postiz mcp tool error: {text[:300]}")
    return text


def call(name, args, key, ca, tries=3, timeout=300):
    """One Postiz MCP tool call, with retries. Returns the parsed tool output.

    The endpoint answers with a JSON-RPC error now and then (seen 2026-10-22,
    where daily_post.py lost a day to it and the identical call from
    reddit_daily.py succeeded fifteen minutes later), and the tunnel drops. A
    single unretried blip should not cost a day of posting.
    """
    import subprocess, time
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                          "params": {"name": name, "arguments": args}})
    last = None
    for attempt in range(tries):
        try:
            out = subprocess.check_output(
                ["curl", "-sS", "--cacert", ca, "-X", "POST",
                 "https://mcp.postiz.com/mcp",
                 "-H", f"Authorization: Bearer {key}",
                 "-H", "Content-Type: application/json",
                 "-H", "Accept: application/json, text/event-stream",
                 "-d", payload], timeout=timeout)
            text = body(parse(out))
            try:
                return json.loads(text)
            except ValueError:
                return text
        except Exception as e:
            last = e
            if attempt < tries - 1:
                time.sleep(2 ** attempt * 3)
    raise last
