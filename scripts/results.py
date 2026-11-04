import json, re, urllib.request, datetime, os
u = "https://www.nbcnews.com/politics/2026-elections/michigan-senate-results"
req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/130 Safari/537.36"})
b = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
d = json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', b, re.S).group(1))
pp = d["props"]["pageProps"]; race = pp["races"][0]; s = race["summary"]
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
cands = [{"name": c.get("name") or c.get("lastName"), "last": c.get("lastName"), "party": c.get("party", ""),
          "votes": c.get("votes", 0), "pct": c.get("percentVote", 0), "winner": bool(c.get("isWinner")),
          "call": c.get("callStatus", "")} for c in s.get("candidates", [])]
counties = []
for a in race["areas"]:
    cv = {c.get("lastName"): c.get("votes", 0) for c in a["candidates"]}
    counties.append({"name": a["name"], "in": a.get("percentIn", 0), "votes": a.get("votes", 0), "c": cv})
modes = []
for v in (s.get("percentInChart") or {}).get("values", []) or []:
    modes.append({"mode": v.get("description"), "votes": v.get("votes", 0),
                  "c": {c.get("lastName"): c.get("percentInt", 0) for c in v.get("candidates", [])}})
out = {"checked": now, "source": "NBC News", "sourceUpdated": pp.get("lastModifiedFormatted"),
       "percentIn": s.get("percentInFormatted"), "candidates": cands, "modes": modes,
       "countiesReporting": sum(1 for c in counties if c["in"] > 0), "counties": len(counties)}
json.dump(out, open("results.json", "w"), indent=1)
json.dump({"checked": now, "counties": counties}, open("counties.json", "w"))
# history
hist = []
if os.path.exists("history.json"):
    try: hist = json.load(open("history.json"))
    except Exception: hist = []
v = {c["last"]: c["votes"] for c in cands}
snap = {"t": now, "d": v.get("El-Sayed", 0), "r": v.get("Rogers", 0), "tot": sum(v.values()), "pin": s.get("percentInFormatted")}
if not hist or (hist[-1]["d"], hist[-1]["r"]) != (snap["d"], snap["r"]):
    hist.append(snap)
json.dump(hist[-1500:], open("history.json", "w"))
print(out["percentIn"], len(counties), len(modes), len(hist))
