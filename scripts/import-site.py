import concurrent.futures, hashlib, json, pathlib, urllib.request
manifest=json.loads(pathlib.Path("site-manifest.json").read_text())
origin="https://quiet-personal-garden-1014.agilechair.chatgpt.site/"
base="/A-Visual-w1/"
def download(item):
    name, expected=item
    request=urllib.request.Request(origin+name,headers={"User-Agent":"Portfolio-Deployment"})
    with urllib.request.urlopen(request, timeout=90) as response:
        data=response.read()
    if hashlib.sha256(data).hexdigest()!=expected:
        raise RuntimeError("Source changed or download failed: "+name)
    if pathlib.Path(name).suffix in [".html",".css",".js"]:
        text=data.decode("utf-8")
        for folder in ["assets","models","drawings","backgrounds","life","certificates"]:
            text=text.replace("/"+folder+"/",base+folder+"/")
        data=text.encode("utf-8")
    target=pathlib.Path("docs")/name
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    list(pool.map(download,manifest.items()))
pathlib.Path("docs/.nojekyll").touch()
print("Imported",len(manifest),"verified website files.")
