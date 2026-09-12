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


def posts_on(day):
    url = (f"{API}posts?startDate={day}T00:00:00.000Z&endDate={day}T23:59:59.000Z"
           f"&customer=&display=day&day=0&week=0&month=0&year={day[:4]}")
    d = json.load(urllib.request.urlopen(
        urllib.request.Request(url, headers={"Authorization": KEY,
                 "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}), timeout=60))
    return d.get("posts", d if isinstance(d, list) else [])


def plat(p):
    return (p.get("integration") or {}).get("providerIdentifier") or "?"


def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    today = date.today()
    window = [(today - timedelta(days=i)).isoformat() for i in range(days, -1, -1)]

    by_day = {d: posts_on(d) for d in window}
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
        missing = sorted(expected - pub - set(err))
        notes = []
        if err:
            notes.append("ERROR: " + ", ".join(err))
        if missing:
            notes.append("MISSING: " + ", ".join(missing))
        flag = "  <-- " + "; ".join(notes) if notes else ""
        print(f"{d}  {schedule.get(d, ''):32s} {len(pub)} published{flag}")
        if notes and d != today.isoformat():
            problems.append((d, notes))
        elif notes and d == today.isoformat() and not pub and not err:
            # Nothing at all today, not even a failure: the day was never
            # scheduled. That is the queue running dry, not a run in progress.
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
