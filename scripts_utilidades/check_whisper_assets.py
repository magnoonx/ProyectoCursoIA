import urllib.request, json
req = urllib.request.Request('https://api.github.com/repos/ggerganov/whisper.cpp/releases/latest', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as r:
    data = json.loads(r.read())
print("Tag:", data.get("tag_name"))
for a in data.get("assets", []):
    print("-", a["name"], "->", a["browser_download_url"])
