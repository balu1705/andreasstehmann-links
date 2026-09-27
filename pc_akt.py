import re,json
t=open("preischeck/index.html",encoding="utf-8").read()
d=json.loads(re.search(r"const DATA=(\{.*?\});",t,re.S).group(1))
n1=len([k for k,v in d.items() if v["stats"]["min"]==v["stats"]["max"]])
print("ASINs mit nur 1 Preis (min==max):",n1,"von",len(d))
sv=set((v["stats"]["akt"]) for v in d.values());
print("distinct akt-preise:",len(sv))
