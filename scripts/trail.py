#!/usr/bin/env python3
"""Decision trail with explicit run and span timing.

  trail.py run-start <file> <run>               [--at ISO]
  trail.py run-end   <file> <run>               [--at ISO]
  trail.py start     <file> <run> <span> <phase> [--at ISO]
  trail.py end       <file> <run> <span>        [--at ISO]
  trail.py note      <file> <run> <phase> <decision> <why> <evidence> <result> [--at ISO]
  trail.py report    <file>

Spans may overlap (review and CI waiting together). `active wall` is the union
of span intervals; phase totals overlap and do not sum to wall time. Time
between runs is never counted. --at takes an ISO 8601 time with a UTC offset.
"""

import csv
import sys
from datetime import datetime
from pathlib import Path

HEADER = ["ts", "run", "event", "span", "phase", "decision", "why", "evidence", "result"]
ARITY = {"run-start": 1, "run-end": 1, "start": 3, "end": 2, "note": 6}


class TrailError(Exception):
    pass


def clean(cell: str) -> str:
    cell = " ".join(cell.replace("\t", " ").splitlines()).strip()
    # Spreadsheet apps execute cells that start with these characters.
    return "'" + cell if cell[:1] in ("=", "+", "-", "@") else cell


def parse_time(value: str) -> datetime:
    try:
        moment = datetime.fromisoformat(value)
    except ValueError as error:
        raise TrailError(f"bad timestamp {value!r}") from error
    if moment.utcoffset() is None:
        raise TrailError(f"timestamp {value!r} needs a UTC offset")
    return moment


def read(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def replay(rows: list[dict[str, str]]) -> dict:
    """Validate events in order and return runs with closed spans and open items."""
    runs: dict[str, dict] = {}
    for row in rows:
        run_id, event, span = row["run"], row["event"], row["span"]
        ts = parse_time(row["ts"])
        run = runs.get(run_id)
        if event == "run-start":
            if run is not None:
                raise TrailError(f"run {run_id} started twice")
            runs[run_id] = {"start": ts, "latest": ts, "end": None, "open": {}, "spans": []}
            continue
        if run is None:
            raise TrailError(f"run {run_id} has events before run-start")
        if run["end"] is not None:
            raise TrailError(f"run {run_id} has events after run-end")
        if ts < run["start"]:
            raise TrailError(f"{event} at {row['ts']} is before run {run_id} started")
        if event == "start":
            if span in run["open"]:
                raise TrailError(f"span {span} is already open in run {run_id}")
            run["open"][span] = (ts, row["phase"])
        elif event == "end":
            if span not in run["open"]:
                raise TrailError(f"span {span} is not open in run {run_id}")
            started, phase = run["open"][span]
            if ts < started:
                raise TrailError(f"span {span} ends at {row['ts']}, before it started")
            del run["open"][span]
            run["spans"].append((started, ts, phase))
        elif event == "run-end":
            if run["open"]:
                raise TrailError(f"run {run_id} ends with open spans: {', '.join(run['open'])}")
            if ts < run["latest"]:
                raise TrailError(f"run {run_id} ends before its latest event")
            run["end"] = ts
        elif event != "note":
            raise TrailError(f"unknown event {event!r}")
        run["latest"] = max(run["latest"], ts)
    return runs


def append(path: Path, run: str, event: str, fields: list[str], at: str | None) -> None:
    ts = parse_time(at) if at else datetime.now().astimezone()
    span, phase, decision, why, evidence, result = "", "", "", "", "", ""
    if event == "start":
        span, phase = fields[0], fields[1]
    elif event == "end":
        span = fields[0]
    elif event == "note":
        phase, decision, why, evidence, result = fields
    row = [ts.isoformat(timespec="seconds"), run, event, span, phase, decision, why, evidence, result]
    row = [row[0]] + [clean(cell) for cell in row[1:]]
    replay(read(path) + [dict(zip(HEADER, row))])
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        if not path.exists() or path.stat().st_size == 0:
            writer.writerow(HEADER)
        writer.writerow(row)


def union_minutes(intervals: list[tuple[datetime, datetime]]) -> float:
    total, current_start, current_end = 0.0, None, None
    for start, end in sorted(intervals):
        if current_end is None or start > current_end:
            if current_end is not None:
                total += (current_end - current_start).total_seconds()
            current_start, current_end = start, end
        else:
            current_end = max(current_end, end)
    if current_end is not None:
        total += (current_end - current_start).total_seconds()
    return total / 60


def report(path: Path) -> int:
    runs = replay(read(path))
    incomplete = [
        f"run {run_id}" + (f" (open spans: {', '.join(run['open'])})" if run["open"] else "")
        for run_id, run in runs.items()
        if run["end"] is None
    ]
    if incomplete:
        raise TrailError("incomplete: " + "; ".join(incomplete))
    phases: dict[str, float] = {}
    elapsed_all = wall_all = 0.0
    for run_id, run in runs.items():
        elapsed = (run["end"] - run["start"]).total_seconds() / 60
        wall = union_minutes([(start, end) for start, end, _ in run["spans"]])
        elapsed_all += elapsed
        wall_all += wall
        print(f"run {run_id}: elapsed {elapsed:.1f} min, active wall {wall:.1f} min")
        for start, end, phase in run["spans"]:
            phases[phase] = phases.get(phase, 0.0) + (end - start).total_seconds() / 60
    print(f"all runs: elapsed {elapsed_all:.1f} min, active wall {wall_all:.1f} min")
    print("phase totals (spans overlap; these do not sum to wall time):")
    for phase, minutes in sorted(phases.items(), key=lambda item: -item[1]):
        print(f"{phase}\t{minutes:.1f} min")
    return 0


def main(argv: list[str]) -> int:
    args = argv[1:]
    at = None
    if "--at" in args:
        index = args.index("--at")
        if index + 1 >= len(args):
            print("--at needs a value", file=sys.stderr)
            return 2
        at = args[index + 1]
        del args[index : index + 2]
    try:
        if len(args) == 2 and args[0] == "report" and at is None:
            return report(Path(args[1]))
        if args and args[0] in ARITY and len(args) == 2 + ARITY[args[0]]:
            append(Path(args[1]), args[2], args[0], args[3:], at)
            return 0
    except TrailError as error:
        print(f"trail: {error}", file=sys.stderr)
        return 1
    print(__doc__.strip(), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
