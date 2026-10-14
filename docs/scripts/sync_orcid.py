#!/usr/bin/env python3
"""Sync publicly visible ORCID journal articles into Jekyll publication files.
Only works explicitly marked journal-article are imported; existing curated entries remain intact.
"""
import json, pathlib, re, urllib.request, urllib.parse, time, sys
ORCID="0000-0002-9996-9983"
ROOT=pathlib.Path(__file__).resolve().parents[2]
TARGET=ROOT/"_publications"/"orcid"
API=f"https://pub.orcid.org/v3.0/{ORCID}/works"
def fetch_json(url,headers=None):
    req=urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"GerlanAcademicPortfolio/1.0 (GitHub Actions)",**(headers or {})})
    with urllib.request.urlopen(req,timeout=25) as response:
        return json.load(response)
def getval(x): return (x or {}).get("value","") if isinstance(x,dict) else ""
def yaml_string(s): return json.dumps(str(s or ""),ensure_ascii=False)
def main():
    groups=fetch_json(API).get("group",[])
    works=[]
    for group in groups:
        summaries=group.get("work-summary") or []
        s=next((a for a in summaries if a.get("publication-date")),summaries[0] if summaries else None)
        if not s or s.get("publication-type")!="journal-article": continue
        title=getval((s.get("title") or {}).get("title"))
        if not title: continue
        year=getval((s.get("publication-date") or {}).get("year")) or "1900"
        journal=getval(s.get("journal-title"))
        doi=""
        for x in ((s.get("external-ids") or {}).get("external-id") or []):
            if (x.get("external-id-type") or "").lower()=="doi":
                doi=x.get("external-id-value","");break
        url=f"https://doi.org/{doi}" if doi else getval(s.get("url")) or f"https://orcid.org/{ORCID}"
        authors=["Gerlan Silva da Silva"]
        if doi:
            try:
                meta=fetch_json("https://api.crossref.org/works/"+urllib.parse.quote(doi,safe=""))
                m=meta.get("message",{})
                cross_auth=[(" ".join(filter(None,[a.get("given"),a.get("family")])).strip()) for a in m.get("author",[])]
                if cross_auth: authors=cross_auth
                if not journal: journal=(m.get("container-title") or [""])[0]
            except Exception: pass
        work_id=str(s.get("put-code"))
        works.append((work_id,title,year,journal,url,authors))
    if not works:
        raise SystemExit("Nenhum artigo de periódico recuperado do ORCID; registros existentes preservados.")
    TARGET.mkdir(parents=True,exist_ok=True)
    for put,title,year,journal,url,authors in works:
        content="---\n"+"\n".join([
            "title: "+yaml_string(title),
            "date: "+yaml_string(f"{year}-01-01"),
            "pub: "+yaml_string(journal),
            "pub_date: "+yaml_string(year),
            "selected: false",
            "authors:",
            *["  - "+yaml_string(author) for author in authors],
            "links:",
            "  DOI: "+yaml_string(url),
            "source: ORCID",
            "orcid_put_code: "+yaml_string(put),
        ])+"\n---\n"
        (TARGET/f"orcid-{put}.md").write_text(content,encoding="utf-8")
    print(f"Sincronizados {len(works)} artigos públicos do ORCID.")
if __name__=="__main__":main()
