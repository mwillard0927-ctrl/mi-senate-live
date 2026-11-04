import urllib.request, re, json
out={}
H={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) Chrome/130 Safari/537.36"}
for u in ["https://www.gametimepa.com/elections/results/",
          "https://www.gametimepa.com/elections/results/race/2026-11-03-state_house-PA-39279/",
          "https://www.gametimepa.com/elections/results/2026-11-03/state/PA/",
          "https://www.gametimepa.com/elections/results/2026-11-03/",
          "https://www.pennlive.com/elections/results/"]:
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=30); b=r.read(3_000_000).decode("utf-8","replace")
        out[u]={"status":r.status,"final":r.geturl(),"len":len(b),"title":(re.search(r'<title>(.*?)</title>',b,re.S) or [None,''])[1][:150],
                "links":sorted(set(re.findall(r'href="([^"]*(?:state_house|race)[^"]*)"',b)))[:60],
                "199":[' '.join(b[max(0,m.start()-250):m.start()+250].split()) for m in re.finditer(r'199',b)][:4]}
    except Exception as e: out[u]=repr(e)
json.dump(out,open("probe.json","w"),indent=1)
