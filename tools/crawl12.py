import sys, re, json, time, os, urllib.request
from urllib.parse import urljoin, urldefrag, urlparse
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

OUT = sys.argv[1]
MAXPAGES = int(sys.argv[2]) if len(sys.argv) > 2 else 800
MAXDEPTH = 2
os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0"}
SERVICES = ["azure-sql","postgresql","analysis-services","logic-apps","api-management","service-bus-messaging","event-grid","machine-learning","ai-foundry","ai-services","search","aks","container-apps","virtual-network","defender-for-cloud","cost-management-billing","well-architected","architecture/data-guide","architecture/guide/technology-choices","architecture/framework","devops","developer","azure-resource-manager","templates","virtual-machines","app-service","azure-policy","purview","data-explorer","key-vault", "azure-monitor", "managed-identities-azure-resources", "private-link", "data-factory", "synapse-analytics", "stream-analytics", "azure-functions",
            "role-based-access-control", "event-hubs", "storage/blobs", "storage/common",
            "active-directory", "cosmos-db", "databricks", "azure-resource-manager", "governance"]
SEEDS = """https://learn.microsoft.com/en-us/training/paths/get-started-data-engineering/
https://learn.microsoft.com/en-us/azure/role-based-access-control/overview
https://learn.microsoft.com/en-us/training/modules/intro-to-azure-data-lake-storage
https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview
https://learn.microsoft.com/en-us/azure/data-factory/introduction
https://learn.microsoft.com/en-us/training/paths/data-integration-scale-azure-data-factory/
https://learn.microsoft.com/en-us/azure/data-factory/data-factory-tutorials
https://learn.microsoft.com/en-us/azure/synapse-analytics/overview-what-is
https://learn.microsoft.com/en-us/training/paths/implement-data-streaming-with-asa/
https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-window-functions
https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction""".split()


def norm(u):
    u, _ = urldefrag(u)
    u = u.split("?")[0].rstrip("/")
    return u


def allowed(u):
    p = urlparse(u)
    if p.netloc != "learn.microsoft.com":
        return False
    path = p.path
    if not path.startswith("/en-us/"):
        return False
    rest = path[len("/en-us/"):]
    if rest.startswith(("training/paths/", "training/modules/", "training/support/", "training/courses/", "credentials/")):
        return True
    if rest.startswith(("fabric/","power-bi/","dax/","kusto/","purview/","power-apps/","power-automate/","power-platform/","bicep/","entra/","defender-for-cloud/","azure/ai-foundry/","terraform/","github/","entra/identity/managed-identities-azure-resources/")):
        return True
    if rest.startswith("azure/"):
        r = rest[len("azure/"):]
        return any(r == s or r.startswith(s + "/") for s in SERVICES)
    return False


def fetch(u):
    for _ in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            err = e
            time.sleep(1.5)
    return None


def to_md(soup):
    main = soup.find("main") or soup
    for t in main.select("nav,aside,footer,script,style,svg,button,form,[data-bi-name=feedback-section],.feedback-section"):
        t.decompose()
    lines = []
    for el in main.find_all(["h1", "h2", "h3", "h4", "p", "li", "pre", "tr"]):
        txt = el.get_text(" ", strip=True)
        if not txt:
            continue
        n = el.name
        if n[0] == "h":
            lines.append("\n" + "#" * int(n[1]) + " " + txt)
        elif n == "li":
            lines.append("- " + txt)
        elif n == "pre":
            lines.append("```\n" + el.get_text() + "\n```")
        elif n == "tr":
            lines.append("| " + " | ".join(c.get_text(" ", strip=True) for c in el.find_all(["th", "td"])) + " |")
        else:
            lines.append(txt)
    return "\n".join(lines)


def slug(u):
    return re.sub(r"[^A-Za-z0-9]+", "-", urlparse(u).path.replace("/en-us/", "")).strip("-")[:140]


import os as _o
if _o.environ.get("SEEDS_FILE"):
    SEEDS = [l.strip() for l in open(_o.environ["SEEDS_FILE"]) if l.strip()]
seen = {}
frontier = [(norm(s), 0, "seed") for s in SEEDS]
for s, _, _ in frontier:
    seen[s] = 0
index = []
count = 0
while frontier and count < MAXPAGES:
    batch = frontier[:24]
    frontier = frontier[24:]
    with ThreadPoolExecutor(6) as ex:
        htmls = list(ex.map(lambda t: fetch(t[0]), batch))
    for (u, d, parent), html in zip(batch, htmls):
        if not html:
            index.append((u, d, parent, "FAILED"))
            continue
        try:
            soup = BeautifulSoup(html, "html.parser")
        except Exception:
            index.append((u, d, parent, "FAILED-PARSE"))
            continue
        title = (soup.find("h1").get_text(" ", strip=True) if soup.find("h1") else slug(u))
        links = []
        main = soup.find("main") or soup
        for a in main.find_all("a", href=True):
            v = norm(urljoin(u, a["href"]))
            if allowed(v):
                links.append(v)
        fn = f"d{d}-{slug(u)}.md"
        with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\nSource: {u}\nDepth: {d} (from {parent})\n\n{to_md(soup)}\n")
        index.append((u, d, parent, fn))
        count += 1
        if d < MAXDEPTH:
            for v in dict.fromkeys(links):
                if v not in seen:
                    seen[v] = d + 1
                    frontier.append((v, d + 1, u))
    print(count, len(frontier), flush=True)
    time.sleep(0.5)
with open(os.path.join(OUT, "_INDEX.md"), "w", encoding="utf-8") as f:
    f.write("# Crawl index\n\n")
    for u, d, p, fn in index:
        f.write(f"- d{d} {fn} <- {u}\n")
    if frontier:
        f.write(f"\nNOT CRAWLED (cap {MAXPAGES}): {len(frontier)} queued URLs\n")
print("done", count)
