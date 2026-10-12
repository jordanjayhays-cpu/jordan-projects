#!/usr/bin/env python3
"""Image generation for storyboard shots, via Postiz's generateImageTool.

This lived in a scratchpad directory until 2026-10-12 and was lost to every
container rebuild, which broke the storyboard path each time. It belongs in the
repo: the mini-movie format is now the daily output, not an experiment.

The Veo video route costs real money and is capped by Postiz credits. Image
generation is a separate pool and is free, which is why a whole film can be
made from stills and a moving camera rather than from clips.

No key is stored here. POSTIZ_KEY comes from the environment, falling back to
/tmp/.pz, the same as every other script in this pipeline.
"""
import json, os, subprocess, time

CA = "/root/.ccr/ca-bundle.crt"


def _key():
    k = os.environ.get("POSTIZ_KEY")
    if k:
        return k.strip()
    try:
        return open("/tmp/.pz").read().strip()
    except OSError:
        raise SystemExit("POSTIZ_KEY not set and /tmp/.pz missing. "
                         "Run pipeline/restore_container.sh <key> first.")


def mcp(name, args, tries=3):
    """Call one Postiz MCP tool. Returns the parsed result, or {'error': ...}.

    Generation takes about thirty seconds a frame and the tunnel drops
    occasionally, so this retries with backoff rather than losing the run.
    """
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                          "params": {"name": name, "arguments": args}})
    last = None
    for attempt in range(tries):
        try:
            out = subprocess.check_output(
                ["curl", "-sS", "--cacert", CA, "-X", "POST",
                 "https://mcp.postiz.com/mcp",
                 "-H", f"Authorization: Bearer {_key()}",
                 "-H", "Content-Type: application/json",
                 "-H", "Accept: application/json, text/event-stream",
                 "-d", payload],
                timeout=300)
            d = json.loads(out)
            body = d["result"]["content"][0]["text"]
            if d["result"].get("isError"):
                return {"error": body[:300]}
            try:
                return json.loads(body)
            except ValueError:
                return {"path": body.strip()}
        except Exception as exc:
            last = exc
            if attempt < tries - 1:
                time.sleep(2 ** attempt)
    return {"error": f"{type(last).__name__}: {str(last)[:200]}"}
