import base64, concurrent.futures, hashlib, json, pathlib, urllib.request
manifest=json.loads(pathlib.Path("site-manifest.json").read_text())
origin="https://quiet-personal-garden-1014.agilechair.chatgpt.site/"
base="/A-Visual-w1/"
def download(item):
    name, expected=item
    if name=="index.html":
        data=base64.b64decode("PCFkb2N0eXBlIGh0bWw+PGh0bWwgbGFuZz0iemgtQ04iPjxoZWFkPjxtZXRhIGNoYXJzZXQ9IlVURi04Ii8+PG1ldGEgbmFtZT0idmlld3BvcnQiIGNvbnRlbnQ9IndpZHRoPWRldmljZS13aWR0aCwgaW5pdGlhbC1zY2FsZT0xLjAiLz48bWV0YSBuYW1lPSJ0aGVtZS1jb2xvciIgY29udGVudD0iIzEwMWIxYiIvPjxtZXRhIG5hbWU9ImRlc2NyaXB0aW9uIiBjb250ZW50PSLoi4/lrZDpvpnnmoTkuKrkurrkuLvpobXvvJrnlLXmsJToh6rliqjljJbjgIFQTEMg6aG555uu44CBQUkg5bqU55So44CB5a6e5Lmg57uP5Y6G5LiO5Liq5Lq65Yib5L2c44CCIi8+PHRpdGxlPuiLj+WtkOm+mSDCtyDnlLXmsJToh6rliqjljJbkuI4gQUkg5bqU55SoPC90aXRsZT48bGluayByZWw9InByZWNvbm5lY3QiIGhyZWY9Imh0dHBzOi8vZm9udHMuZ29vZ2xlYXBpcy5jb20iLz48bGluayByZWw9InByZWNvbm5lY3QiIGhyZWY9Imh0dHBzOi8vZm9udHMuZ3N0YXRpYy5jb20iIGNyb3Nzb3JpZ2luLz48bGluayBocmVmPSJodHRwczovL2ZvbnRzLmdvb2dsZWFwaXMuY29tL2NzczI/ZmFtaWx5PUludGVyOndnaHRAMzAwOzQwMDs1MDA7NjAwOzcwMCZmYW1pbHk9Tm90bytTYW5zK1NDOndnaHRANDAwOzUwMDs2MDAmZGlzcGxheT1zd2FwIiByZWw9InN0eWxlc2hlZXQiLz4gIDxzY3JpcHQgdHlwZT0ibW9kdWxlIiBjcm9zc29yaWdpbiBzcmM9Ii9hc3NldHMvaW5kZXgtQmY4d1FZUTYuanMiPjwvc2NyaXB0PgogIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgY3Jvc3NvcmlnaW4gaHJlZj0iL2Fzc2V0cy9pbmRleC1CWlFMWm5rdS5jc3MiPgo8L2hlYWQ+PGJvZHk+PGRpdiBpZD0icm9vdCI+PC9kaXY+PC9ib2R5PjwvaHRtbD4NCg==")
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
