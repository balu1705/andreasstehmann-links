import re
t=open("preischeck/index.html",encoding="utf-8").read()
print(re.findall(r"<h[123][^>]*>([^<]+)",t)[:12])
print([v for v in re.findall(r"(?:const|var|let)\s+([A-Za-z_$][\w$]*)\s*=",t)][:20])
print(re.findall(r"(?:fetch|XMLHttpRequest)\(.{0,60}",t)[:5])
