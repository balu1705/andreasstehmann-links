import re,json
t=open("preischeck/index.html",encoding="utf-8").read()
m=re.search(r"const DATA=(\[.*?\])</script>",t,re.S)
d=json.loads(m.group(1))
ds=[x for e in d for x in (e.get("h") or [])[:] ]
print("einträge:",len(d))
print("neueste daten:",max(str(x) for x in ds if x)[:24] if ds else "?")
for e in d[:3]: print(e.get("a"), "| latest:", (e.get("h") or [])[-3:])
