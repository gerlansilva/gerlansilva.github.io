#!/usr/bin/env python3
"""Import ORCID journal articles with or without DOI. Preserve existing hand-curated entries."""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
import json, re
ORCID="0000-0002-9996-9983"
OUT=Path(__file__).resolve().parents[1]/"_publications"/"orcid"
def fetch(url):
    req=Request(url,headers={"Accept":"application/json","User-Agent":"AcademicHomepageORCID/1.0"})
    with urlopen(req,timeout=25) as f:return json.load(f)
def value(obj):return (obj or {}).get("value","") if isinstance(obj,dict) else ""
def qs(x):return json.dumps(str(x or ""),ensure_ascii=False)
def run():
    groups=fetch(f"https://pub.orcid.org/v3.0/{ORCID}/works").get("group",[])
    items=[]
    for group in groups:
        summaries=group.get("work-summary") or []
        journal=[x for x in summaries if x.get("publication-type") in ("journal-article","article","review")]
        if not journal:continue
        s=journal[0]
        title=value((s.get("title") or {}).get("title"))
        if not title:continue
        code=str(s.get("put-code"))
        year=value((s.get("publication-date") or {}).get("year")) or "1900"
        journal_name=value(s.get("journal-title"))
        identifiers=(s.get("external-ids") or {}).get("external-id") or []
        doi=next((x.get("external-id-value","") for x in identifiers if x.get("external-id-type","").lower()=="doi"),"")
        link="https://doi.org/"+doi if doi else value(s.get("url")) or f"https://orcid.org/{ORCID}"
        authors=[]; abstract="";keywords=[]
        try:
            full=fetch(f"https://pub.orcid.org/v3.0/{ORCID}/work/{code}")
            authors=[(" ".join(filter(None,[value((c.get("credit-name") or {})), value((c.get("contributor-orcid") or {}).get("path"))])).strip()) for c in []] # intentionally unused
            authors=[value(c.get("credit-name")) for c in (full.get("contributors") or {}).get("contributor",[]) if value(c.get("credit-name"))]
            abstract=value((full.get("short-description") or {})) if isinstance(full.get("short-description"),dict) else str(full.get("short-description") or "")
        except Exception:pass
        if doi:
            try:
                crossref=fetch("https://api.crossref.org/works/"+quote(doi,safe="")).get("message",{})
                names=[" ".join(filter(None,[a.get("given"),a.get("family")])).strip() for a in crossref.get("author",[])]
                if names:authors=names
                if not journal_name:journal_name=(crossref.get("container-title") or [""])[0]
                if not abstract:abstract=re.sub("<[^>]+>"," ",crossref.get("abstract","")).strip()
                keywords=crossref.get("subject",[]) or []
            except Exception:pass
        if not authors:authors=["Gerlan Silva"]
        items.append((code,title,year,journal_name,doi,link,authors,abstract,keywords))
    if not items:
        print("Nenhum artigo elegível retornado pelo ORCID. Conteúdo existente preservado.")
        return
    OUT.mkdir(parents=True,exist_ok=True)
    for code,title,year,journal,doi,link,authors,abstract,keywords in items:
        lines=["---","title: "+qs(title),"date: "+qs(year+"-01-01"),"pub: "+qs(journal),"pub_date: "+qs(year),"selected: false","source: ORCID","orcid_put_code: "+qs(code),"authors:"]
        lines+=["  - "+qs(a) for a in authors]
        if abstract:lines+=["abstract: "+qs(abstract)]
        if keywords:lines+=["keywords:"]+["  - "+qs(k) for k in keywords]
        lines+=["links:","  DOI: "+qs(link),"---",""]
        (OUT/f"orcid-{code}.md").write_text("\n".join(lines),encoding="utf-8")
    print(f"{len(items)} artigos de periódico importados, incluindo registros sem DOI.")
if __name__=="__main__":run()
