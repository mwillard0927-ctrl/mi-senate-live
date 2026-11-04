import urllib.request, re, json, os
urls = [
 "https://www.michigan.gov/ElectionResults",
 "https://mielections.us/election/results/",
 "https://mielections.us/election/results/2026GEN_CENR.html",
 "https://www.politico.com/2026-election/results/michigan/senate/",
 "https://www.nytimes.com/interactive/2026/11/03/us/elections/results-michigan-senate.html",
 "https://www.nbcnews.com/politics/2026-elections/michigan-senate-results",
 "https://www.cnn.com/election/2026/results/michigan/senate",
 "https://apnews.com/projects/election-results-2026/?r=MI",
 "https://www.thv11.com/article/news/politics/elections/live-results-michigan-us-senate-race/507-8c1b9074-93a3-42cd-8eb0-aa3dd9f1ad8e",
 "https://en.wikipedia.org/wiki/2026_United_States_Senate_election_in_Michigan",
]
out = []
for u in urls:
    r = {"url": u}
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/130 Safari/537.36"})
        resp = urllib.request.urlopen(req, timeout=25)
        b = resp.read(3_000_000).decode("utf-8", "replace")
        r["final"] = resp.geturl(); r["status"] = resp.status; r["len"] = len(b)
        r["ctx"] = [b[max(0,m.start()-150):m.start()+250] for m in re.finditer(r"El-?Sayed", b)][:6]
        r["links"] = sorted(set(re.findall(r'(?:href|src)="([^"]*(?:result|json|\.txt|csv|feed)[^"]*)"', b, re.I)))[:60]
    except Exception as e:
        r["err"] = repr(e)
    out.append(r)
os.makedirs("probe", exist_ok=True)
json.dump(out, open("probe/out.json", "w"), indent=1)
