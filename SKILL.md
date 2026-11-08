---
name: lernzettel-webseite
description: Baut aus Fotos oder Scans von Heftaufschrieben, Lernzetteln, Arbeitsblättern und alten Klausuren eine interaktive Lernzettel-Webseite für GitHub Pages – Themen herausarbeiten und Inhaltsliste, jedes Thema in drei Erklärstufen (Einfach/Normal/Genauer), Abhaken mit Punkten, Rängen und Schnelltests, dazu Übungsklausuren im Stil der Lehrkraft mit Erwartungshorizont. Verwende diesen Skill immer, wenn jemand für eine Klausur, Arbeit, einen Test oder das Abitur lernen will und Unterlagen mitbringt oder eine Lernhilfe möchte – auch bei Formulierungen wie „mach mir einen Lernzettel“, „hier sind meine Heftfotos“, „ich schreib nächste Woche Bio“, „erstell mir Übungsaufgaben im Stil meiner Lehrerin“ oder „Zusammenfassung zum Lernen als Webseite“, egal in welchem Fach.
---

# Lernzettel-Webseite

Aus Schulunterlagen entsteht eine statische Webseite, die man auf GitHub Pages veröffentlichen kann:

```
projekt/
├── index.html              Lernzettel: Inhaltsliste, Kapitel, Themen in 3 Stufen, Schnelltests
├── uebungsklausur-1.html   Übungsklausur im Stil der Lehrkraft + Erwartungshorizont
├── uebungsklausur-2.html
├── css/style.css, css/klausur.css
├── js/app.js, js/klausur.js
├── README.md               Anleitung GitHub Pages
├── .gitignore              schließt den Fotoordner aus
└── <fotoordner>/           Originalfotos – bleiben privat
```

Design und Logik sind fertig (`assets/`); deine Arbeit ist der **Inhalt**: Themen sauber herausarbeiten, verständlich in drei Stufen erklären, gute Testfragen und Übungsklausuren, die sich wie die echte Klausur anfühlen.

## Vorlieben des Nutzers (aus dem ersten Projekt)

- **Keine runden Schriften**, aber schön: Archivo (Überschriften, breit) + IBM Plex Sans/Mono, kantige Elemente, kleine Radien. Das steckt schon in `style.css` – nicht durch Nunito, Quicksand o. Ä. ersetzen.
- Webseite auf **GitHub Pages**, Fortschritt nur im Browser.
- Antworten und Seiten auf **Deutsch**, Schüler duzen.

## Ablauf

Den Nutzer zwischendurch kurz informieren (das Sichten vieler Fotos dauert), aber nicht für Entscheidungen anhalten, die sich aus den Unterlagen ergeben.

### 1. Unterlagen vollständig sichten

Jedes Foto ansehen – auch wenn es viele sind. Inhalte, die man überspringt, fehlen später im Lernzettel. Notiere dabei:

- **Fach, Kurs, Stufe, Thema der Einheit**, Kürzel auf Arbeitsblättern (z. B. „Geo LK · Sch · Reliefsphäre“)
- **Art der Quelle** – sie bestimmt das Gewicht:
  - Heftaufschriebe/Arbeitsblätter der Lehrkraft = verbindlicher Stoff, Definitionen im Wortlaut übernehmen
  - Lernzettel von Mitschülern = gute Struktur, aber Fehler möglich
  - Alte Klausur = zeigt Stil, Operatoren, Punkteverteilung und welche Themen geprüft werden
- Randnotizen der Lehrkraft (z. B. „nicht näher beschreiben“, „anhand vs. ausgehend von“) – sie verraten, worauf es ankommt.
- Namen von Mitschülern und Lehrkraft (für die Datenschutz-Prüfung in Schritt 7).

### 2. Themen herausarbeiten

- 5–7 Kapitel, insgesamt etwa 15–25 Themen, Reihenfolge wie im Heft.
- Wenn die Klausur mit Operatoren arbeitet: Kapitel I „Handwerkszeug“ (Operatoren & AFB, Darstellungsformen).
- Fallbeispiele der alten Klausur als eigenes Thema mit Kurz-Musterlösung.
- Widersprüche und Fehler in den Notizen festhalten – sie kommen am Ende in die Zusammenfassung.

Details zum Zuschnitt: `references/inhalte.md`, Abschnitt 1.

### 3. Projekt aufsetzen

```bash
mkdir -p css js
cp <skill>/assets/css/*.css css/
cp <skill>/assets/js/*.js js/
cp <skill>/assets/templates/index.html index.html
cp <skill>/assets/templates/README.md README.md
cp <skill>/assets/templates/gitignore.txt .gitignore
```

Platzhalter `{{…}}` ersetzen. Wichtig:

- `store` in `window.LERNZETTEL` (im `<head>` jeder Seite gleich): eindeutig pro Projekt, z. B. `'bio-genetik-k1'`. Alle Repos unter `name.github.io` teilen sich einen Browserspeicher – mit gleichem Schlüssel würden sich zwei Lernzettel gegenseitig die Häkchen überschreiben.
- `ranks`: 8 Ränge passend zum Fach, von klein nach groß, Schwellen `0, 0.06, 0.16, 0.30, 0.46, 0.62, 0.80, 1`. Geo-Beispiel: Staubkorn → Sandkorn → Kiesel → Geröll → Findling → Vulkan → Gebirge → Pangäa. Bio z. B.: Nukleotid → Gen → Chromosom → Zelle → Gewebe → Organ → Organismus → Ökosystem.
- `{{SAEULE}}`: Name der Fortschrittssäule, passend zum Fach (Geo: „Bohrkern“, Bio: „DNA-Strang“, Geschichte: „Zeitleiste“ …).
- `{{TITEL_MIT_SHY}}`: Titel mit `&shy;` an einer sinnvollen Trennstelle (großer Hero-Titel bricht sonst auf dem Handy unschön um).

### 4. Inhalte schreiben

Lies zuerst `references/inhalte.md` und das Beispiel `references/beispiel-thema.html`. Kurz:

- **Einfach** = Kernidee mit Alltagsvergleich · **Normal** = Heftniveau, klausurrelevant · **Genauer** = Zusammenhänge, Musterlösung, typische Fehler.
- 2–3 Schnelltest-Fragen pro Thema mit variierter Position der richtigen Antwort.
- 1–3 SVG-Abbildungen pro Kapitel, Koordinaten vorher berechnen.

**Lange Dateien in Etappen schreiben:** Erst `index.html` mit den ersten Kapiteln und einem Marker wie `<!-- WEITERE-KAPITEL -->` anlegen, dann je Kapitel(-paar) den Marker per Edit ersetzen (neuen Marker ans Ende). Eine einzelne riesige Schreibaktion bricht leicht ab, und dann ist alles weg.

### 5. Übungsklausuren

Lies `references/uebungsklausur.md`. Kurz: Stil der Originalklausur analysieren (Kopf, BE, Zeit, Operatoren, Materialmix), dann zwei neue Klausuren mit neuen Fallbeispielen, die sich ergänzen; Materialien selbst zeichnen; Erwartungshorizont mit Punkten pro Aspekt. Vorlage: `assets/templates/uebungsklausur.html`. Auch hier in Etappen schreiben (Blätter 1–4, dann den Erwartungshorizont per Marker anhängen).

Gibt es keine alte Klausur, frag kurz nach Umfang (BE, Minuten) oder nimm einen üblichen Rahmen (z. B. 60 BE / 90 Min. in der Oberstufe) und sag das dem Nutzer.

### 6. Prüfen

```bash
python <skill>/scripts/check_site.py <projekt> --names "Vorname Nachname,Frau X"
```

Das Skript prüft Stufen, Quiz-Antwortindizes, Ankerlinks, BE-/Minutensummen der Klausuren, Erwartungshorizont, Platzhalter-Reste, `.gitignore` und ob Namen auf öffentlichen Seiten stehen. Alle Fehler beheben.

Dann im Browser ansehen:
- Über einen lokalen Server (`python -m http.server 8642`), nicht `file://` – in der Vorschau lädt `file://` oft kein CSS.
- Nach Änderungen kann die Vorschau altes CSS/JS cachen: Dateien per `fetch(url,{cache:'reload'})` neu laden, dann `location.reload()`.
- Abhaken und Schnelltest per JS anklicken und prüfen, ob Punkte und Bohrkern reagieren; `document.documentElement.scrollWidth` mit `clientWidth` vergleichen, um waagerechtes Scrollen zu erkennen; Materialien der Klausuren per Screenshot anschauen (Beschriftungen über Linien? Text in Kästen?).

### 7. Datenschutz & Veröffentlichung

- Der Fotoordner kommt in `.gitignore` – Fotos zeigen oft Namen von Mitschülern, Lehrkraft und Noten.
- Auf den Seiten: keine Namen von Mitschülern, kein Name der Lehrkraft (auch nicht auf den Übungsklausuren). Die Seite ist öffentlich, und eine Klausur mit dem echten Namen kann wie eine offizielle wirken.
- `README.md` erklärt beide Wege (Upload im Browser / Git). Nicht selbst pushen oder ein Repository anlegen, ohne dass der Nutzer das ausdrücklich möchte – anbieten genügt.

### 8. Abschluss

Kurz zusammenfassen:
- Kapitel und Themen (Inhaltsliste in einer Zeile pro Kapitel)
- Was die Spielerei kann (Punkte, Ränge, Säule, Schnelltests)
- Übungsklausuren: Fallbeispiele und abgedeckte Themen
- **Bewusste Abweichungen von den Notizen** (z. B. falsche Zahl korrigiert) und welche Materialwerte schematisch sind
- Was nicht geprüft wurde (z. B. Druckansicht)
- Nächster Schritt: veröffentlichen laut README (anbieten, es zu übernehmen)
