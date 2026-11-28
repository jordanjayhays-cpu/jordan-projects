#!/usr/bin/env python3
"""Did the last N days actually go out? Exits non-zero if anything is wrong.

    POSTIZ_KEY=... python3 pipeline/health.py          # last 7 days
    POSTIZ_KEY=... python3 pipeline/health.py 14

Written after Reddit published nothing for five days while its routine reported
success every morning. The existing watchdog only retries posts that ERRORED
today, so it cannot see the failure mode that actually happened: a post that was
never created at all. There is no error to find, no alert to raise, and the gap
is invisible unless something counts what is missing.

Two checks, both about absence rather than failure:

  MISSING  a channel that normally posts published nothing that day
  ERROR    a post that fired and was rejected by the platform

The expected set of channels is the union of everything seen across the window
rather than a hardcoded list, so connecting or dropping a channel needs no edit
here. A day is only judged once it is in the past; today is reported but never
counted against the exit code, because the day is not over.
"""
import json
import os
import sys
import urllib.request
from collections import Counter
from datetime import date, timedelta

KEY = os.environ["POSTIZ_KEY"]
PIPE = os.path.dirname(os.path.abspath(__file__))
API = "https://api.postiz.com/public/v1/"


sys.path.insert(0, PIPE)
import mcp_parse  # noqa: E402

CA = "/root/.ccr/ca-bundle.crt"


def posts_window(start, end):
    """Every post in the window, in ONE call, via the MCP endpoint.

    Postiz's public REST API started answering 401 to this key on 2026-11-22
    while the MCP endpoint kept working with the very same key, so this is not
    a dead credential and does not wait on a new one. daily_post.py already
    schedules over MCP, which is why the queue kept extending that morning
    while health.py, reddit_daily.py, fix_hook.py and rerender_days.py all
    failed: those four were the REST callers.

    One call for the whole window rather than one per day, because each MCP
    round trip is slower than the REST one it replaces.
    """
    return mcp_parse.call("postsListTool",
                          {"startDate": f"{start}T00:00:00",
                           "endDate": f"{end}T23:59:00"}, KEY, CA)["output"]["posts"]


def plat(p):
    """MCP returns platform flat; REST nested it. Accept either, so this keeps
    working if the REST API comes back and something passes its shape in."""
    return (p.get("platform")
            or (p.get("integration") or {}).get("providerIdentifier") or "?")


def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    today = date.today()
    window = [(today - timedelta(days=i)).isoformat() for i in range(days, -1, -1)]

    by_day = {d: [] for d in window}
    for p in posts_window(window[0], window[-1]):
        d = (p.get("publishDate") or "")[:10]
        if d in by_day:
            by_day[d].append(p)
    schedule = json.load(open(os.path.join(PIPE, "state.json"))).get("schedule", {})

    # What counts as normal: a channel that published on at least a third of the
    # past days. One flaky day should not lower the bar for every day after it.
    seen = Counter()
    for d in window[:-1]:
        for c in {plat(p) for p in by_day[d] if p.get("state") == "PUBLISHED"}:
            seen[c] += 1
    expected = {c for c, n in seen.items() if n >= max(2, len(window) // 3)}

    problems = []

    # Queue depth first, because it fails EARLIEST and hurts most.
    #
    # The daily pipeline schedules roughly two weeks ahead, so when it stopped
    # running on 2026-08-28 nothing looked wrong for fifteen days: the backlog
    # kept publishing on time. The first symptom was a morning with no post at
    # all, by which point the run had been broken for over two weeks.
    #
    # Counting posts cannot catch that. A day with nothing scheduled has no
    # missing channel and no error, it simply is not there. So check the
    # schedule ahead of today rather than the posts behind it.
    ahead = sorted(d for d in schedule if d >= today.isoformat())
    print(f"queue: {len(ahead)} day(s) scheduled from today"
          + (f", through {ahead[-1]}" if ahead else "") + "\n")
    if len(ahead) < 3:
        problems.append((today.isoformat(), [
            f"QUEUE NEARLY EMPTY: only {len(ahead)} day(s) scheduled. The daily "
            f"pipeline is not extending the schedule; run it before a morning "
            f"passes with nothing to post"]))

    print(f"expected channels: {', '.join(sorted(expected)) or '(none seen)'}\n")
    for d in window:
        ps = by_day[d]
        pub = {plat(p) for p in ps if p.get("state") == "PUBLISHED"}
        err = sorted(plat(p) for p in ps if p.get("state") == "ERROR")
        queued = {plat(p) for p in ps if p.get("state") == "QUEUE"}
        missing = sorted(expected - pub - set(err) - queued)
        # The platform's own rejection text. Reddit failed silently for
        # seventeen days because nothing ever printed this, and the whole time
        # the API was returning "that community doesn't exist" in plain words.
        # A failure that does not say why costs far more than one that does.
        why = {}
        for p in ps:
            if p.get("state") == "ERROR" and p.get("error"):
                why.setdefault(plat(p), p["error"])
        notes = []
        if err:
            notes.append("ERROR: " + ", ".join(
                f"{c} ({why[c]})" if c in why else c for c in err))
        if missing:
            notes.append("MISSING: " + ", ".join(missing))
        flag = "  <-- " + "; ".join(notes) if notes else ""
        print(f"{d}  {schedule.get(d, ''):32s} {len(pub)} published{flag}")
        if notes and d != today.isoformat():
            problems.append((d, notes))
        elif d == today.isoformat() and not pub and not err and not queued:
            # Nothing at all today, not even a failure or a queued post: the day
            # was never scheduled. That is the queue running dry.
            #
            # `q` matters. This runs at 06:10 and the posts go out at 08:00, so
            # before then a perfectly healthy day has zero published and four
            # queued. Without the queue check it reported NOTHING SCHEDULED
            # every single morning, which is how a real warning gets ignored.
            problems.append((d, ["NOTHING SCHEDULED TODAY"]))

    print()
    if not problems:
        print(f"clean — {days} days, every expected channel published")
        return
    print(f"{len(problems)} day(s) with problems:")
    for d, notes in problems:
        print(f"  {d}: {'; '.join(notes)}")
    sys.exit(1)


if __name__ == "__main__":
    main()
