#!/usr/bin/env python3
"""Build Jordan's LinkedIn CRM assets from the raw TSV connection dumps.

Reads  data/connections_part*.tsv   (name <TAB> headline <TAB> connected_on [<TAB> flags])
Writes connections.csv              flat spreadsheet-friendly export
       connections.json             structured records with tags
       crm.db                       SQLite database (table: connections)
       crm.html                     self-contained CRM app (template.html + embedded data)
"""
import csv
import glob
import json
import os
import re
import sqlite3
import unicodedata
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))

MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"], 1)}

TAG_RULES = [
    ("IE / MBA network", r"\bIE Business School\b|\bIE University\b|\bIE Univerity\b|\bIMBA\b|\bIE MBA\b|\bMBA Candidate\b|\bMBA candidate\b|\bMiM\b|\bMIM\b|Master in Management|Masters in Management|International MBA|\bIE\s*'?\d{2}\b|MBA @|MBA at IE|@ ?IE\b|\bBBA Student @ IE\b"),
    ("Founder / CEO", r"\bFounder\b|\bCo-?[Ff]ounder\b|\bCEO\b|\bCTO\b|\bCOO\b|\bCPO\b|\bCMO\b|\bCFO\b|Entrepreneur|\bOwner\b|Fundador|Building\b|Managing Director|Managing Partner"),
    ("Investor / VC", r"Venture Capital\b|\bVC\b|Investor|Private Equity|Angel|Impact Investing|Ventures\b|Investment professional|Redpoint|Apollo\b|Capital Partner"),
    ("Recruiting / Talent", r"[Rr]ecruit|[Tt]alent|[Hh]eadhunt|[Ss]taffing|Executive Search|People Acquisition|Talent Acquisition"),
    ("Sales / BD", r"\bSales\b|Business Development|\bBD\b|BizDev|Account Executive|Account Manager|Partnerships|\bGTM\b|Revenue|Pipeline|Client Development|Commercial\b"),
    ("Marketing / Brand", r"Marketing|\bBrand\b|\bSEO\b|Content|Communications|\bPR\b|Advertis|Growth\b"),
    ("AI / Software", r"\bAI\b|Artificial Intelligence|Software|Engineer|Machine Learning|\bML\b|Data Scien|Developer|DevOps|GenAI|Generative AI|Cloud|SaaS|Tech\b|Automation"),
    ("Finance / Investing", r"Finance|Financial|Banking|Investment|M&A|Equity|CFA\b|FP&A|Wealth|Treasury|Payments|Fintech|FinTech|Private Lender|CPA\b|Mortgage|Loan"),
    ("HR / People", r"\bHR\b|Human Resource|People Ops|PeopleOps|People & Talent|Chief HR|People Leader|Employee Experience"),
    ("Consulting / Strategy", r"Consultant|Consulting|McKinsey|\bBCG\b|Deloitte|Accenture|\bEY\b|KPMG|PwC|Strategy|Strategist|Advisory|Advisor"),
    ("Research / Insights", r"YouGov|Research|Insights|Kantar|Toluna|Harris ?Quest|Veridata|Analyst"),
    ("Real Estate", r"Real [Ee]state|Realtor|Propert|PropTech|\bMRED\b|Escrow"),
    ("Events / Hospitality", r"Events?\b|Hotel|Hospitality|Resort|Travel|Tourism|MICE\b"),
    ("Healthcare / Biotech", r"Health|Medical|Biotech|Pharma|Clinical|Neuro|Nurse|Hospital|\bMD\b|Doctor"),
    ("Legal / Compliance", r"\bLaw\b|Legal|Juris Doctor|J\.?D\.?\b|Attorney|Compliance|AML\b|KYC\b|Counsel|Privacy"),
]

YOUGOV_RE = re.compile(r"YouGov|Harris ?Quest", re.IGNORECASE)
IE_RE = re.compile(TAG_RULES[0][1])
COMPANY_RE = re.compile(r"(?:\bat\b|@|\ben\b|\bna\b)\s+([A-Z][\w&.'’\-]*(?:\s+[A-Z][\w&.'’\-]*){0,4})")


def slugify(text):
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "contact"


def parse_date(raw):
    m = re.match(r"(\w+) (\d{1,2}), (\d{4})", raw.strip())
    if not m:
        raise ValueError(f"Bad date: {raw!r}")
    return datetime(int(m.group(3)), MONTHS[m.group(1)], int(m.group(2)))


def guess_company(headline):
    m = COMPANY_RE.search(headline)
    if m:
        company = m.group(1).strip(" .|,")
        if 2 < len(company) < 60:
            return company
    return ""


def tags_for(headline):
    tags = [tag for tag, pattern in TAG_RULES if re.search(pattern, headline)]
    return tags or ["Other"]


def load_rows():
    rows = []
    for path in sorted(glob.glob(os.path.join(HERE, "data", "connections_part*.tsv"))):
        with open(path, encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                parts = line.split("\t")
                if len(parts) < 3:
                    raise ValueError(f"{path}:{n}: expected >=3 tab-separated fields, got {len(parts)}")
                name, headline, date_raw = parts[0].strip(), parts[1].strip(), parts[2].strip()
                flags = parts[3].strip() if len(parts) > 3 else ""
                dt = parse_date(date_raw)
                rows.append({
                    "name": name,
                    "headline": headline,
                    "connected_on": dt.strftime("%Y-%m-%d"),
                    "connected_on_display": date_raw,
                    "year": dt.year,
                    "flags": flags,
                    "company_guess": guess_company(headline),
                    "tags": tags_for(headline),
                })
    rows.sort(key=lambda r: r["connected_on"], reverse=True)
    seen = {}
    for r in rows:
        base = slugify(r["name"])
        seen[base] = seen.get(base, 0) + 1
        r["id"] = base if seen[base] == 1 else f"{base}-{seen[base]}"
    return rows


def write_csv(rows):
    path = os.path.join(HERE, "connections.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "name", "headline", "connected_on", "year", "flags", "company_guess", "tags"])
        for r in rows:
            w.writerow([r["id"], r["name"], r["headline"], r["connected_on"],
                        r["year"], r["flags"], r["company_guess"], "; ".join(r["tags"])])
    return path


def write_json(rows):
    path = os.path.join(HERE, "connections.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=1)
    return path


def write_sqlite(rows):
    path = os.path.join(HERE, "crm.db")
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    con.execute("""
        CREATE TABLE connections (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            headline TEXT,
            connected_on TEXT,
            year INTEGER,
            flags TEXT,
            company_guess TEXT,
            tags TEXT,
            stage TEXT DEFAULT 'new',
            priority INTEGER DEFAULT 0,
            notes TEXT DEFAULT ''
        )""")
    con.executemany(
        "INSERT INTO connections (id,name,headline,connected_on,year,flags,company_guess,tags) VALUES (?,?,?,?,?,?,?,?)",
        [(r["id"], r["name"], r["headline"], r["connected_on"], r["year"],
          r["flags"], r["company_guess"], "; ".join(r["tags"])) for r in rows])
    con.commit()
    con.close()
    return path


def write_html(rows):
    template_path = os.path.join(HERE, "template.html")
    out_path = os.path.join(HERE, "crm.html")
    with open(template_path, encoding="utf-8") as fh:
        template = fh.read()
    payload = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    html = template.replace("/*__DATA__*/[]", payload)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return out_path


def main():
    rows = load_rows()
    print(f"Parsed {len(rows)} connections "
          f"({rows[-1]['connected_on']} → {rows[0]['connected_on']})")
    for fn in (write_csv, write_json, write_sqlite, write_html):
        print("Wrote", os.path.relpath(fn(rows), HERE))
    from collections import Counter
    counts = Counter(t for r in rows for t in r["tags"])
    print("Top tags:", counts.most_common(10))


if __name__ == "__main__":
    main()
