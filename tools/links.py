import os, re, sys
ROOT = sys.argv[1]
folders = [("pages","Seed articles (PDP)"),("deep","Docs: depth-2 crawl of PDP links"),("related","Related courses and Learn MCP"),("modules","Modules (course pages)"),("units","Module units (lessons)"),("docs","Official docs: PDP services"),("docs2","Official docs: Fabric, Databricks, Power BI"),("docs3","Official docs: Key Vault, Monitor, Kusto"),("docs4","Official docs: databases, AI, DevOps, networking, security"),("courses2","Courses: Fabric, Databricks, Power BI"),("courses3","Courses: Key Vault, Monitor"),("courses4","Courses: other role topics"),("certs","Certification prep: exams, study guides, courses")]
out = ["# Все ссылки курса Azure\n", "Автоматически собрано из индексов обходов. Формат: заголовок — URL.\n"]
out.append("\n## PDP (источник)\nСм. [00-PDP-Azure-topics.md](00-PDP-Azure-topics.md)\n")
total = 0
for fo, title in folders:
    ip = os.path.join(ROOT, fo, "_INDEX.md")
    items = []
    if fo == "pages":
        for fn in sorted(os.listdir(os.path.join(ROOT, fo))) if os.path.isdir(os.path.join(ROOT, fo)) else []:
            p = os.path.join(ROOT, fo, fn)
            lines = open(p, encoding="utf-8", errors="replace").read().splitlines()[:6]
            url = next((re.search(r"https?://\S+", l).group(0) for l in lines if re.search(r"https?://\S+", l)), "")
            h = next((l.lstrip("# ").strip() for l in lines if l.startswith("#")), fn)
            items.append((fn.replace(".md","") if h.startswith("Source") else h, url, fn))
    elif os.path.exists(ip):
        for line in open(ip, encoding="utf-8"):
            m = re.match(r"- d(\d+) (\S+\.md) <- (\S+)", line)
            if m:
                fn = m.group(2)
                p = os.path.join(ROOT, fo, fn)
                t = fn
                if os.path.exists(p):
                    t = open(p, encoding="utf-8", errors="replace").readline().lstrip("# ").strip() or fn
                items.append((t, m.group(3), fn))
    if not items:
        continue
    total += len(items)
    out.append(f"\n## {title} ({fo}/, {len(items)})\n")
    for t, u, fn in items:
        out.append(f"- [{t}]({u}) — `{fo}/{fn}`")
out.append(f"\n\nВсего страниц: {total}")
open(os.path.join(ROOT, "LINKS.md"), "w", encoding="utf-8").write("\n".join(out))
print("links", total)
