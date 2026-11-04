import json, re, urllib.request, datetime, os
RACES = {
 "senate": "https://www.nbcnews.com/politics/2026-elections/michigan-senate-results",
 "governor": "https://www.nbcnews.com/politics/2026-elections/michigan-governor-results",
 "pa-governor": "https://www.nbcnews.com/politics/2026-elections/pennsylvania-governor-results",
 "pa-house1": "https://www.nbcnews.com/politics/2026-elections/pennsylvania-us-house-district-1-results",
 "pa-house7": "https://www.nbcnews.com/politics/2026-elections/pennsylvania-us-house-district-7-results",
 "pa-house8": "https://www.nbcnews.com/politics/2026-elections/pennsylvania-us-house-district-8-results",
 "pa-house10": "https://www.nbcnews.com/politics/2026-elections/pennsylvania-us-house-district-10-results",
 "house10": "https://www.nbcnews.com/politics/2026-elections/michigan-us-house-district-10-results",
}
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
def grab(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/130 Safari/537.36"})
    b = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    return json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', b, re.S).group(1))["props"]["pageProps"]
for key, url in RACES.items():
    try:
        pp = grab(url); race = pp["races"][0]; s = race["summary"]
        cands = [{"name": c.get("name") or c.get("lastName"), "last": c.get("lastName"), "party": c.get("party", ""),
                  "votes": c.get("votes", 0), "pct": c.get("percentVote", 0), "winner": bool(c.get("isWinner")),
                  "call": c.get("callStatus", "")} for c in s.get("candidates", [])]
        counties = [{"name": a["name"], "in": a.get("percentIn", 0), "votes": a.get("votes", 0),
                     "c": {c.get("lastName"): c.get("votes", 0) for c in a["candidates"]}} for a in race["areas"]]
        modes = [{"mode": v.get("description"), "votes": v.get("votes", 0),
                  "c": {c.get("lastName"): c.get("percentInt", 0) for c in v.get("candidates", [])}}
                 for v in ((s.get("percentInChart") or {}).get("values") or [])]
        out = {"checked": now, "source": "NBC News", "sourceUpdated": pp.get("lastModifiedFormatted"),
               "title": (pp.get("header") or {}).get("title") if isinstance(pp.get("header"), dict) else None,
               "percentIn": s.get("percentInFormatted"), "candidates": cands, "modes": modes,
               "countiesReporting": sum(1 for c in counties if c["in"] > 0), "counties": len(counties)}
        json.dump(out, open(f"results-{key}.json", "w"), indent=1)
        if key == "senate":
            json.dump(out, open("results.json", "w"), indent=1)
            json.dump({"checked": now, "counties": counties}, open("counties.json", "w"))
        hf = f"history-{key}.json"
        hist = json.load(open(hf)) if os.path.exists(hf) else []
        dem = next((c for c in cands if c["party"] == "dem"), cands[0])
        gop = next((c for c in cands if c["party"] == "gop"), cands[1])
        snap = {"t": now, "d": dem["votes"], "r": gop["votes"], "pin": s.get("percentInFormatted")}
        if not hist or (hist[-1]["d"], hist[-1]["r"]) != (snap["d"], snap["r"]):
            hist.append(snap)
        json.dump(hist[-2000:], open(hf, "w"))
        print(key, out["percentIn"], [(c["last"], c["votes"]) for c in cands[:2]])
    except Exception as e:
        print(key, "ERR", repr(e))
