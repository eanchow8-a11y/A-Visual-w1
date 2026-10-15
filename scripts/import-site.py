import concurrent.futures, hashlib, json, pathlib, urllib.request
manifest=json.loads(pathlib.Path("site-manifest.json").read_text())
origin="https://quiet-personal-garden-1014.agilechair.chatgpt.site/"
base="/A-Visual-w1/"
def download(item):
    name, expected=item
    if name=="index.html":
        data="<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"UTF-8\"/><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/><meta name=\"theme-color\" content=\"#101b1b\"/><meta name=\"description\" content=\"苏子龙的个人主页：电气自动化、PLC 项目、AI 应用、实习经历与个人创作。\"/><title>苏子龙 · 电气自动化与 AI 应用</title><link rel=\"preconnect\" href=\"https://fonts.googleapis.com\"/><link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin/><link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+SC:wght@400;500;600&display=swap\" rel=\"stylesheet\"/>  <script type=\"module\" crossorigin src=\"/assets/index-Bf8wQYQ6.js\"></script>\n  <link rel=\"stylesheet\" crossorigin href=\"/assets/index-BZQLZnku.css\">\n</head><body><div id=\"root\"></div></body></html>\n".encode("utf-8")
    else:
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
