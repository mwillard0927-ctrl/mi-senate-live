import json, re, urllib.request, datetime
u = "https://www.nbcnews.com/politics/2026-elections/michigan-senate-results"
req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/130 Safari/537.36"})
b = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
d = json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', b, re.S).group(1))
pp = d["props"]["pageProps"]; race = pp["races"][0]; s = race["summary"]
cands = [{"name": c.get("name") or c.get("lastName"), "last": c.get("lastName"), "party": c.get("party", ""),
          "votes": c.get("votes", 0), "pct": c.get("percentVote", 0), "winner": bool(c.get("isWinner")),
          "call": c.get("callStatus", "")} for c in s.get("candidates", [])]
counties = [{"name": a["name"], "in": a.get("percentIn", 0),
             "lead": max(a["candidates"], key=lambda c: c.get("votes", 0)).get("lastName") if a.get("votes") else None}
            for a in race["areas"]]
out = {"checked": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "source": "NBC News", "sourceUpdated": pp.get("lastModifiedFormatted"),
       "percentIn": s.get("percentInFormatted"), "candidates": cands,
       "countiesReporting": sum(1 for c in counties if c["in"] > 0), "counties": len(counties)}
json.dump(out, open("results.json", "w"), indent=1)
print(out["percentIn"], [(c["last"], c["votes"]) for c in cands[:2]])
