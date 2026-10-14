#!/usr/bin/env python3
"""Regenerate the README competition table from events.json."""
import json
from pathlib import Path

HERE = Path(__file__).parent
START = "<!-- table:start -->"
END = "<!-- table:end -->"


def fmt_dates(d: str) -> str:
    start, _, end = d.partition("..")
    y, m, day = start.split("-")
    if not end:
        return f"{int(day):02d} {month(m)}"
    ey, em, ed = end.split("-")
    if (m, y) == (em, ey):
        return f"{int(day):02d}–{int(ed):02d} {month(m)}"
    return f"{int(day):02d} {month(m)} – {int(ed):02d} {month(em)}"


def month(m: str) -> str:
    names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return names[int(m)]


def main() -> None:
    data = json.loads((HERE / "events.json").read_text(encoding="utf-8"))
    lines = ["| Dates | Competition | City | Country | Page |",
             "|---|---|---|---|---|"]
    for e in sorted(data["events"], key=lambda x: x["dates"]):
        lines.append(
            f"| {fmt_dates(e['dates'])} | {e['name']} | {e['city']} "
            f"| {e['country']} | [link]({e['url']}) |"
        )
    table = "\n".join(lines)
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    if START in readme and END in readme:
        head, rest = readme.split(START, 1)
        _, tail = rest.split(END, 1)
        readme = f"{head}{START}\n{table}\n{END}{tail}"
    else:
        marker = "## Files"
        table_block = f"{START}\n{table}\n{END}\n\n## Files"
        readme = readme.replace(marker, table_block, 1)
    (HERE / "README.md").write_text(readme, encoding="utf-8")
    print(f"README updated: {len(data['events'])} events")


if __name__ == "__main__":
    main()
