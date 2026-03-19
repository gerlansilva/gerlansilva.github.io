"""
fetch_orcid.py
Busca publicações do ORCID e gera _bibliography/papers.bib
Executado automaticamente pelo GitHub Actions toda segunda-feira.
"""

import json
import os
import re
import urllib.request
from datetime import datetime

ORCID_ID   = "0000-0002-9996-9983"
BASE_URL   = f"https://pub.orcid.org/v3.0/{ORCID_ID}"
OUTPUT     = "_bibliography/papers.bib"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())


def slugify(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def bib_key(title, year, last):
    word = next((slugify(w) for w in title.split() if len(w) > 3), "work")
    return f"{slugify(last)}{year}{word[:10]}"


def get_doi(ext_ids):
    for e in (ext_ids or []):
        if e.get("external-id-type") == "doi":
            return e.get("external-id-value", "")
    return ""


def get_authors(put_code):
    try:
        detail = fetch_json(f"{BASE_URL}/work/{put_code}")
        contribs = detail.get("contributors", {}).get("contributor", [])
        names = [
            c["credit-name"]["value"]
            for c in contribs
            if c.get("credit-name", {}).get("value")
        ]
        return " and ".join(names) if names else ""
    except Exception:
        return ""


def main():
    os.makedirs("_bibliography", exist_ok=True)
    print(f"🔍 Buscando publicações · ORCID: {ORCID_ID}")

    person = fetch_json(f"{BASE_URL}/person")
    first  = person.get("name", {}).get("given-names",  {}).get("value", "")
    last   = person.get("name", {}).get("family-name",  {}).get("value", "")
    full   = f"{first} {last}".strip()
    print(f"👤 {full}")

    works_data = fetch_json(f"{BASE_URL}/works")
    groups     = works_data.get("group", [])
    print(f"📄 {len(groups)} trabalho(s) encontrado(s)")

    entries = []
    for group in groups:
        s         = group.get("work-summary", [{}])[0]
        put_code  = s.get("put-code", "")
        title     = s.get("title", {}).get("title", {}).get("value", "Sem título")
        year      = s.get("publication-date", {}).get("year", {}).get("value", "")
        journal   = (s.get("journal-title") or {}).get("value", "")
        wtype     = s.get("type", "journal-article")
        ext_ids   = s.get("external-ids", {}).get("external-id", [])
        doi       = get_doi(ext_ids)

        authors   = get_authors(put_code) or full
        btype     = "inproceedings" if "conference" in wtype else "article"
        key       = bib_key(title, year, last or "silva")
        vfield    = "booktitle" if btype == "inproceedings" else "journal"

        lines = [f"@{btype}{{{key},"]
        lines.append(f"  title     = {{{title}}},")
        lines.append(f"  author    = {{{authors}}},")
        if journal:
            lines.append(f"  {vfield:<9} = {{{journal}}},")
        if year:
            lines.append(f"  year      = {{{year}}},")
        if doi:
            lines.append(f"  doi       = {{{doi}}},")
            lines.append(f"  url       = {{https://doi.org/{doi}}},")
        lines.append("}")
        entries.append("\n".join(lines))
        print(f"  ✅ {year} — {title[:65]}{'…' if len(title)>65 else ''}")

    header  = (
        f"% Gerado automaticamente via ORCID API\n"
        f"% ORCID : {ORCID_ID}\n"
        f"% Data  : {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
    )
    content = header + "\n\n".join(entries) + "\n"

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n✅ Salvo em: {OUTPUT}  ({len(entries)} entrada(s))")


if __name__ == "__main__":
    main()
