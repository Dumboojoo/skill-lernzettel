#!/usr/bin/env python3
"""Prüft eine Lernzettel-Webseite (index.html + uebungsklausur-*.html) auf typische Fehler.

Aufruf:
    python check_site.py <projektordner> [--names "Vorname Nachname,Frau X"]

--names: kommagetrennte Namen (Mitschüler, Lehrkraft), die auf keiner öffentlichen Seite
         stehen dürfen. Groß-/Kleinschreibung egal.

Exit-Code 1, wenn Fehler gefunden wurden (Warnungen allein ergeben 0).
Nur Standardbibliothek, damit es überall läuft.
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".heic", ".webp", ".gif", ".bmp", ".pdf"}


class Report:
    def __init__(self):
        self.errors, self.warnings, self.ok = [], [], []

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def good(self, msg):
        self.ok.append(msg)

    def print(self):
        for m in self.ok:
            print(f"  OK      {m}")
        for m in self.warnings:
            print(f"  WARNUNG {m}")
        for m in self.errors:
            print(f"  FEHLER  {m}")
        print(f"\n{len(self.errors)} Fehler, {len(self.warnings)} Warnungen")


def num(s):
    return float(s.replace(",", "."))


def check_index(path: Path, r: Report):
    html = path.read_text(encoding="utf-8")
    ids = re.findall(r'\sid="([^"]+)"', html)
    dup = [i for i, c in Counter(ids).items() if c > 1]
    if dup:
        r.err(f"index.html: doppelte ids: {', '.join(dup)}")

    for href in set(re.findall(r'href="#([^"]+)"', html)):
        if href not in ids:
            r.err(f"index.html: Link auf #{href}, aber kein Element mit dieser id")

    chapters = re.findall(r'<section class="chapter"([^>]*)>', html)
    for attrs in chapters:
        cid = re.search(r'id="([^"]+)"', attrs)
        cid = cid.group(1) if cid else "?"
        if "--cc:" not in attrs:
            r.err(f"Kapitel {cid}: style=\"--cc:var(--cN)\" fehlt (Kapitelfarbe)")
        if "data-short" not in attrs:
            r.warn(f"Kapitel {cid}: data-short fehlt (Kurztitel für die Inhaltsliste)")

    topics = list(re.finditer(r'<article class="topic"([^>]*)>(.*?)</article>', html, re.S))
    answer_pos = Counter()
    n_questions = 0
    for m in topics:
        tid = re.search(r'id="([^"]+)"', m.group(1))
        tid = tid.group(1) if tid else "?"
        body = m.group(2)
        if not re.search(r'class="topic-head"', body):
            r.err(f"Thema {tid}: <header class=\"topic-head\"> fehlt")
        for lvl in ("1", "2", "3"):
            if f'data-level="{lvl}"' not in body:
                r.err(f"Thema {tid}: Erklärstufe {lvl} fehlt")
        qs = list(re.finditer(r'<div class="q" data-a="(\d+)"', body))
        if len(qs) < 2:
            r.warn(f"Thema {tid}: nur {len(qs)} Schnelltest-Frage(n) (empfohlen 2–3)")
        for i, q in enumerate(qs):
            n_questions += 1
            end = qs[i + 1].start() if i + 1 < len(qs) else len(body)
            chunk = body[q.end():end]
            a = int(q.group(1))
            ol = re.search(r"<ol>(.*?)</ol>", chunk, re.S)
            n = len(re.findall(r"<li[\s>]", ol.group(1))) if ol else 0
            if n < 2:
                r.err(f"Thema {tid}, Frage {i + 1}: weniger als 2 Antworten")
            elif a >= n:
                r.err(f"Thema {tid}, Frage {i + 1}: data-a=\"{a}\", aber nur {n} Antworten (0-basiert!)")
            if 'class="why"' not in chunk:
                r.warn(f"Thema {tid}, Frage {i + 1}: Erklärung <p class=\"why\"> fehlt")
            answer_pos[a] += 1

    if topics:
        r.good(f"index.html: {len(chapters)} Kapitel, {len(topics)} Themen, {n_questions} Schnelltest-Fragen")
    else:
        r.err("index.html: keine Themen (<article class=\"topic\">) gefunden")
    if n_questions >= 6:
        top, cnt = answer_pos.most_common(1)[0]
        if cnt / n_questions > 0.6:
            r.warn(f"Richtige Antwort steht in {cnt}/{n_questions} Fragen an Position {'ABCD'[top]} – Position stärker variieren")

    if "window.LERNZETTEL" not in html:
        r.warn("index.html: window.LERNZETTEL (store, ranks) fehlt – Fortschritt kollidiert sonst mit anderen Lernzetteln auf github.io")
    for needed in ("css/style.css", "js/app.js"):
        if needed not in html:
            r.err(f"index.html: Verweis auf {needed} fehlt")


def check_exam(path: Path, r: Report):
    html = path.read_text(encoding="utf-8")
    name = path.name
    total_min = re.search(r'<body[^>]*data-minutes="(\d+)"', html)
    mins = [num(x) for x in re.findall(r'<div class="st"[^>]*data-min="([\d.,]+)"', html)]
    be = [num(x) for x in re.findall(r'class="st-be">\(([\d,]+)\s*BE', html)]
    total_be = re.search(r"/\s*\((\d+)\s*BE\)", html)

    if not mins:
        r.err(f"{name}: keine Teilaufgaben (<div class=\"st\" data-min=…>) gefunden")
        return
    if total_min and abs(sum(mins) - int(total_min.group(1))) > 0.01:
        r.err(f"{name}: Minuten der Teilaufgaben = {sum(mins):g}, aber data-minutes = {total_min.group(1)}")
    if len(be) != len(mins):
        r.warn(f"{name}: {len(mins)} Teilaufgaben, aber {len(be)} BE-Angaben (.st-be)")
    if total_be:
        tb = int(total_be.group(1))
        if abs(sum(be) - tb) > 0.01:
            r.err(f"{name}: BE der Teilaufgaben = {sum(be):g}, Gesamt laut Kopf = {tb}")
        sc = re.search(r'class="selfcheck"(.*?)class="sc-result"', html, re.S)
        if sc:
            maxes = [num(x) for x in re.findall(r'<input[^>]*max="([\d.,]+)"', sc.group(1))]
            if abs(sum(maxes) - tb) > 0.01:
                r.err(f"{name}: Selbstbewertung max-Summe = {sum(maxes):g}, Gesamt = {tb}")
            if len(maxes) != len(mins):
                r.warn(f"{name}: {len(maxes)} Eingabefelder in der Selbstbewertung, aber {len(mins)} Teilaufgaben")
        else:
            r.warn(f"{name}: Selbstbewertung (.selfcheck) fehlt")
        sol = [num(x) for x in re.findall(r'<div class="sol">\s*<h3>.*?<span>([\d,]+)\s*BE', html, re.S)]
        if not sol:
            r.warn(f"{name}: Erwartungshorizont (.sol) fehlt")
        elif abs(sum(sol) - tb) > 0.01:
            r.err(f"{name}: Erwartungshorizont-BE = {sum(sol):g}, Gesamt = {tb}")
    else:
        r.warn(f"{name}: Gesamt-BE im Kopf (\"/ (60 BE)\") nicht gefunden")

    mats = re.findall(r"<h3>M(\d+):", html)
    if mats:
        nums = [int(x) for x in mats]
        if nums != list(range(1, len(nums) + 1)):
            r.warn(f"{name}: Materialnummern nicht fortlaufend: {nums}")
    # Nur Aufgabentexte durchsuchen – SVG-Pfade enthalten ebenfalls "M123"
    task_text = " ".join(re.findall(r'<div class="st"[^>]*>(.*?)</div></div>', html, re.S))
    task_text = re.sub(r"<[^>]+>", " ", task_text)
    for ref in sorted(set(re.findall(r"\bM(\d+)\b", task_text)), key=int):
        if mats and int(ref) > max(int(x) for x in mats):
            r.err(f"{name}: Aufgabe verweist auf M{ref}, das es nicht gibt")
    if 'class="sheet solutions"' not in html:
        r.warn(f"{name}: Erwartungshorizont-Blatt fehlt")
    r.good(f"{name}: {len(mins)} Teilaufgaben, {sum(be):g} BE, {sum(mins):g} Min., {len(mats)} Materialien")


def check_privacy(root: Path, r: Report, names):
    gi = root / ".gitignore"
    ignored = []
    if gi.exists():
        ignored = [l.strip().strip("/") for l in gi.read_text(encoding="utf-8").splitlines()
                   if l.strip() and not l.startswith("#")]
    else:
        r.err(".gitignore fehlt – Fotoordner würden mit hochgeladen")

    photo_dirs = set()
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in IMAGE_EXT and ".git" not in p.parts:
            photo_dirs.add(p.relative_to(root).parts[0] if len(p.relative_to(root).parts) > 1 else p.name)
    for d in sorted(photo_dirs):
        if d not in ignored:
            r.err(f"Foto/Scan-Ordner oder -Datei '{d}' steht nicht in .gitignore")
        else:
            r.good(f"'{d}' ist in .gitignore ausgeschlossen")

    public = [p for p in root.rglob("*") if p.is_file() and p.suffix in {".html", ".md", ".js", ".css"}
              and not any(part in ignored or part.startswith(".") for part in p.relative_to(root).parts)]
    for p in public:
        text = p.read_text(encoding="utf-8", errors="ignore")
        if "{{" in text and "}}" in text:
            left = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", text)))
            if left:
                r.err(f"{p.relative_to(root)}: Platzhalter nicht ersetzt: {', '.join(left[:6])}")
        for d in photo_dirs:
            if re.search(rf'(src|href)="{re.escape(d)}/', text):
                r.err(f"{p.relative_to(root)}: verweist auf Datei im privaten Ordner '{d}'")
        for n in names:
            if n and n.lower() in text.lower():
                r.err(f"{p.relative_to(root)}: enthält den Namen „{n}“")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", type=Path)
    ap.add_argument("--names", default="", help="kommagetrennte Namen, die nicht öffentlich auftauchen dürfen")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    root = a.root.resolve()
    r = Report()

    idx = root / "index.html"
    if idx.exists():
        check_index(idx, r)
    else:
        r.err("index.html fehlt")
    exams = sorted(root.glob("uebungsklausur-*.html"))
    if not exams:
        r.warn("keine uebungsklausur-*.html gefunden")
    for e in exams:
        check_exam(e, r)
    for needed in ("css/style.css", "js/app.js", "README.md"):
        if not (root / needed).exists():
            r.err(f"{needed} fehlt")
    if exams:
        for needed in ("css/klausur.css", "js/klausur.js"):
            if not (root / needed).exists():
                r.err(f"{needed} fehlt")
    check_privacy(root, r, [n.strip() for n in a.names.split(",") if n.strip()])

    print(f"Prüfe {root}\n")
    r.print()
    sys.exit(1 if r.errors else 0)


if __name__ == "__main__":
    main()
