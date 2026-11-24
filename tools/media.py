import sys, os, re, hashlib, json, time, urllib.request
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

ROOT = sys.argv[1]
FOLDERS = sys.argv[2:]
IMG = os.path.join(ROOT, "media", "images")
VID = os.path.join(ROOT, "media", "videos")
os.makedirs(IMG, exist_ok=True)
os.makedirs(VID, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0"}
VEXT = (".mp4", ".webm", ".mov", ".m4v")


def get(u, binary=False, limit=None):
    for _ in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r:
                data = r.read(limit) if limit else r.read()
                return data if binary else data.decode("utf-8", "replace")
        except Exception:
            time.sleep(1)
    return None


pages = []
for fo in FOLDERS:
    ip = os.path.join(ROOT, fo, "_INDEX.md")
    if not os.path.exists(ip):
        continue
    for line in open(ip, encoding="utf-8"):
        m = re.match(r"- d\d+ (\S+\.md) <- (\S+)", line)
        if m:
            pages.append((fo, m.group(1), m.group(2)))
print("pages", len(pages), flush=True)


def scan(t):
    fo, fn, u = t
    html = get(u)
    if not html:
        return (fo, fn, u, [], [], [])
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception:
        return (fo, fn, u, [], [], [])
    main = soup.find("main") or soup
    imgs, vids, frames = [], [], []
    for im in main.find_all("img"):
        s = im.get("src") or im.get("data-src")
        if s and not s.startswith("data:"):
            imgs.append(urljoin(u, s))
    for v in main.find_all(["video", "source"]):
        s = v.get("src")
        if s and s.lower().split("?")[0].endswith(VEXT):
            vids.append(urljoin(u, s))
    for fr in main.find_all("iframe"):
        s = fr.get("src") or fr.get("data-src")
        if s:
            frames.append(urljoin(u, s))
    for a in main.find_all("a", href=True):
        h = urljoin(u, a["href"])
        if h.lower().split("?")[0].endswith(VEXT):
            vids.append(h)
    return (fo, fn, u, list(dict.fromkeys(imgs)), list(dict.fromkeys(vids)), list(dict.fromkeys(frames)))


with ThreadPoolExecutor(8) as ex:
    scanned = list(ex.map(scan, pages))
print("scanned", flush=True)

allimg = {}
allvid = {}
for fo, fn, u, imgs, vids, frames in scanned:
    for i in imgs:
        allimg.setdefault(i, []).append(fn)
    for v in vids:
        allvid.setdefault(v, []).append(fn)


def name(u, folder):
    p = urlparse(u)
    base = os.path.basename(p.path) or "file"
    h = hashlib.md5(u.encode()).hexdigest()[:8]
    return os.path.join(folder, f"{h}-{re.sub(r'[^A-Za-z0-9._-]', '_', base)[:100]}")


def dl(item):
    u, folder = item
    fp = name(u, folder)
    if os.path.exists(fp) and os.path.getsize(fp) > 0:
        return (u, fp, "exists")
    data = get(u, binary=True, limit=600 * 1024 * 1024)
    if data is None:
        return (u, None, "FAILED")
    open(fp, "wb").write(data)
    return (u, fp, "ok")


jobs = [(u, IMG) for u in allimg] + [(u, VID) for u in allvid]
print("downloads", len(jobs), flush=True)
with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(dl, jobs))
fail = [r for r in res if r[2] == "FAILED"]

with open(os.path.join(ROOT, "media", "_MANIFEST.md"), "a", encoding="utf-8") as f:
    f.write("\n# Media manifest\n\n## Embedded video players (not downloadable directly; open in browser)\n")
    for fo, fn, u, imgs, vids, frames in scanned:
        for fr in frames:
            f.write(f"- {fr}  (page: {u})\n")
    f.write("\n## Downloaded images/videos -> pages\n")
    mp = {u: fp for u, fp, st in res if fp}
    for u, pgs in {**allimg, **allvid}.items():
        if u in mp:
            f.write(f"- {os.path.relpath(mp[u], ROOT)} <- {u} (used in {', '.join(dict.fromkeys(pgs))})\n")
    if fail:
        f.write("\n## Failed\n" + "\n".join(f"- {r[0]}" for r in fail) + "\n")
mp2 = {u: fp for u, fp, st in res if fp}
for fo, fn, u, imgs, vids, frames in scanned:
    block = ""
    for i in imgs:
        if i in mp2:
            block += "![](../media/images/" + os.path.basename(mp2[i]) + ")\n\n"
    for v in vids:
        if v in mp2:
            block += "[Video](../media/videos/" + os.path.basename(mp2[v]) + ")\n\n"
    for fr in frames:
        block += "Embedded video/player: " + fr + "\n\n"
    fpth = os.path.join(ROOT, fo, fn)
    if block and os.path.exists(fpth):
        txt = open(fpth, encoding="utf-8").read()
        if "## Images and media" not in txt:
            open(fpth, "a", encoding="utf-8").write("\n\n## Images and media\n\n" + block)
print("done", len(res), "failed", len(fail))
