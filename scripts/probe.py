import urllib.request, re, json
out={}
H={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) Chrome/130 Safari/537.36","Accept":"*/*"}
for u in ["https://www.electionreturns.pa.gov/",
          "https://www.electionreturns.pa.gov/General/OfficeResults?OfficeID=13&ElectionID=undefined&ElectionType=G&IsActive=1",
          "https://www.electionreturns.pa.gov/api/ElectionReturn/GetElectionsList"]:
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=30); b=r.read(2_000_000).decode("utf-8","replace")
        out[u]={"status":r.status,"len":len(b),"head":b[:600],
                "refs":sorted(set(re.findall(r'(?:src|href)="([^"]+\.js[^"]*)"',b)))[:30],
                "api":sorted(set(re.findall(r'["\'](/?api/[^"\']+)["\']',b)))[:40],
                "199":[b[max(0,m.start()-200):m.start()+200] for m in re.finditer(r'199(th)?',b)][:3]}
    except Exception as e: out[u]=repr(e)
json.dump(out,open("probe.json","w"),indent=1)
