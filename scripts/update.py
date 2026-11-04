import json, urllib.request, urllib.parse, xml.etree.ElementTree as ET, datetime, email.utils
q = 'Michigan Senate El-Sayed Rogers when:1d'
url = 'https://news.google.com/rss/search?' + urllib.parse.urlencode({'q': q, 'hl': 'en-US', 'gl': 'US', 'ceid': 'US:en'})
req = urllib.request.Request(url, headers={'User-Agent': 'mi-senate-live/1.0'})
root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
items = []
for it in root.iter('item'):
    t = it.findtext('title') or ''
    src = it.findtext('source') or ''
    d = email.utils.parsedate_to_datetime(it.findtext('pubDate')).isoformat()
    items.append({'title': t, 'link': it.findtext('link'), 'source': src, 'date': d})
items.sort(key=lambda x: x['date'], reverse=True)
json.dump({'updated': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'items': items[:30]}, open('news.json', 'w'), indent=1)
print(len(items))
