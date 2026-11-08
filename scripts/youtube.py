#!/usr/bin/env python3
"""YouTube-Videos für Lernzettel finden und prüfen (nur Standardbibliothek).

Suchen – zeigt die Top-Treffer mit ID, Länge, Kanal, Aufrufen und Titel:
    python youtube.py suche "Kettenregel einfach erklärt" [--n 8]

Mehrere Suchen auf einmal (eine Suchanfrage pro Zeile, Ausgabe als JSON):
    python youtube.py suche-datei suchen.txt > treffer.json

Prüfen – jedes YouTube-Link in den HTML-Dateien eines Projekts über die offizielle
oEmbed-Schnittstelle abrufen (existiert das Video, ist es öffentlich, Titel/Kanal):
    python youtube.py pruefe <projektordner>

Exit-Code 1, wenn ein Link nicht (mehr) erreichbar ist.
"""
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9",
    "Cookie": "SOCS=CAI; CONSENT=YES+",
}


def get(url, timeout=20):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError:
        raise
    except urllib.error.URLError as e:
        # python.org-Python auf macOS hat oft keine CA-Zertifikate → curl nutzt die des Systems
        if "CERTIFICATE_VERIFY_FAILED" not in str(e) or not shutil.which("curl"):
            raise
        cmd = ["curl", "-sSfL", "--max-time", str(timeout)]
        for k, v in HEADERS.items():
            cmd += ["-H", f"{k}: {v}"]
        res = subprocess.run(cmd + [url], capture_output=True)
        if res.returncode != 0:
            raise urllib.error.URLError(res.stderr.decode("utf-8", "replace").strip() or f"curl exit {res.returncode}")
        return res.stdout.decode("utf-8", "replace")


def _text(node):
    if not node:
        return ""
    if "simpleText" in node:
        return node["simpleText"]
    return "".join(run.get("text", "") for run in node.get("runs", []))


def _walk(obj):
    if isinstance(obj, dict):
        if "videoRenderer" in obj:
            yield obj["videoRenderer"]
        for v in obj.values():
            yield from _walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk(v)


def suche(query, n=8):
    url = "https://www.youtube.com/results?" + urllib.parse.urlencode({"search_query": query, "hl": "de", "gl": "DE"})
    html = get(url)
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.S)
    if not m:
        raise RuntimeError("Suchergebnis nicht lesbar (Consent-Seite?)")
    data = json.loads(m.group(1))
    out = []
    for v in _walk(data):
        vid = v.get("videoId")
        if not vid or any(o["id"] == vid for o in out):
            continue
        out.append({
            "id": vid,
            "titel": _text(v.get("title")),
            "kanal": _text(v.get("ownerText") or v.get("longBylineText")),
            "laenge": _text(v.get("lengthText")),
            "aufrufe": _text(v.get("viewCountText")),
            "alter": _text(v.get("publishedTimeText")),
        })
        if len(out) >= n:
            break
    return out


def oembed(vid):
    url = "https://www.youtube.com/oembed?" + urllib.parse.urlencode({"url": f"https://www.youtube.com/watch?v={vid}", "format": "json"})
    try:
        return json.loads(get(url))
    except Exception:
        return None


def pruefe(root):
    ids = {}
    for p in sorted(Path(root).glob("*.html")):
        for vid in re.findall(r"youtube\.com/watch\?v=([A-Za-z0-9_-]{11})|youtu\.be/([A-Za-z0-9_-]{11})", p.read_text(encoding="utf-8")):
            vid = vid[0] or vid[1]
            ids.setdefault(vid, set()).add(p.name)
    bad = 0
    for vid, files in ids.items():
        info = oembed(vid)
        if info:
            print(f"  OK      {vid}  {info.get('author_name','?')}: {info.get('title','?')}")
        else:
            bad += 1
            print(f"  FEHLER  {vid}  nicht erreichbar (gelöscht/privat?) – in {', '.join(sorted(files))}")
        time.sleep(0.15)
    print(f"\n{len(ids)} Videos geprüft, {bad} Fehler")
    return bad


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    cmd, arg = sys.argv[1], sys.argv[2]
    n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 8
    if cmd == "suche":
        for t in suche(arg, n):
            print(f"{t['id']}  {t['laenge']:>6}  {t['kanal'][:24]:<24}  {t['aufrufe'][:18]:<18}  {t['titel']}")
    elif cmd == "suche-datei":
        res = {}
        for q in [l.strip() for l in Path(arg).read_text(encoding="utf-8").splitlines() if l.strip()]:
            try:
                res[q] = suche(q, n)
            except Exception as e:
                res[q] = {"fehler": str(e)}
            time.sleep(0.4)
        print(json.dumps(res, ensure_ascii=False, indent=1))
    elif cmd == "pruefe":
        sys.exit(1 if pruefe(arg) else 0)
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
