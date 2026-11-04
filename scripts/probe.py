import urllib.request, os
os.makedirs("probe", exist_ok=True)
u="https://www.nbcnews.com/politics/2026-elections/michigan-senate-results"
req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) Chrome/130 Safari/537.36"})
open("probe/nbc.html","wb").write(urllib.request.urlopen(req,timeout=30).read())
