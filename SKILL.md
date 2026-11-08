---
name: lernzettel-webseite
description: Baut aus Fotos oder Scans von Heftaufschrieben, Lernzetteln, Arbeitsblättern und alten Klausuren eine interaktive Lernzettel-Webseite für GitHub Pages im Design des Fachs (z. B. Karoheft/Tafel für Mathe, immer mit klarer, nicht rundlicher Schrift) – Themen herausarbeiten und Inhaltsliste, jedes Thema in drei Erklärstufen (Einfach/Normal/Genauer), Abhaken mit Punkten, Rängen und Schnelltests, dazu Übungsklausuren im Stil der Lehrkraft mit Erwartungshorizont. Verwende diesen Skill immer, wenn jemand für eine Klausur, Arbeit, einen Test oder das Abitur lernen will und Unterlagen mitbringt oder eine Lernhilfe möchte – auch bei Formulierungen wie „mach mir einen Lernzettel“, „hier sind meine Heftfotos“, „ich schreib nächste Woche Bio“, „erstell mir Übungsaufgaben im Stil meiner Lehrerin“ oder „Zusammenfassung zum Lernen als Webseite“, egal in welchem Fach.
---

# Lernzettel-Webseite

Aus Schulunterlagen entsteht eine statische Webseite, die man auf GitHub Pages veröffentlichen kann:

```
projekt/
├── index.html              Lernzettel: Inhaltsliste, Kapitel, Themen in 3 Stufen, Schnelltests
├── uebungsklausur-1.html   Übungsklausur im Stil der Lehrkraft + Erwartungshorizont
├── uebungsklausur-2.html
├── css/style.css, css/klausur.css, css/extras.css
├── css/theme.css           Fachdesign: Farben, Schriften, Motiv (aus assets/themes/)
├── js/app.js, js/klausur.js
├── README.md               Anleitung GitHub Pages
├── .gitignore              schließt den Fotoordner aus
└── <fotoordner>/           Originalfotos – bleiben privat
```

Layout und Logik sind fertig (`assets/`). Deine Arbeit ist der **Inhalt** – Themen sauber herausarbeiten, verständlich in drei Stufen erklären, gute Testfragen und Übungsklausuren, die sich wie die echte Klausur anfühlen – und ein **Design, das zum Fach passt** (`css/theme.css`).

## Vorlieben des Nutzers (aus dem ersten Projekt)

- **Design passend zum Fach.** Jeder Lernzettel bekommt ein Fach-Theme (Mathe = Karoheft/Tafel, Geo = Höhenlinien/Bohrkern …). Vorhandene Themes in `assets/themes/`; für ein neues Fach eines bauen und im Skill ablegen → `references/design.md`. Ein generischer Look, der zu jedem Fach gleich aussieht, gefiel nicht.
- **Immer eine klare, „cleane“ Schrift – nie etwas Rundliches**, egal welches Fach: z. B. Inter/Inter Tight, Archivo, IBM Plex, Source Sans 3. Verboten u. a. Nunito, Quicksand, Comfortaa, Poppins, Montserrat, DM Sans, Rubik (vollständige Liste in `references/design.md`; `check_site.py` meldet sie). Kantige Elemente, kleine Radien.
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
cp <skill>/assets/themes/<fach>.css css/theme.css     # z. B. mathe.css, erde.css – oder neues Theme bauen
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
- **Fachdesign:** Gibt es für das Fach noch kein Theme, jetzt eines nach `references/design.md` bauen (Motiv hell/dunkel, Farben, Schriften, Säule, Hero-Motiv) und zusätzlich unter `<skill>/assets/themes/<fach>.css` speichern. Das Hero-Linienmotiv im HTML (`.hero-topo`) passend ersetzen.
- **Formeln (Mathe, Physik, Chemie):** KaTeX-Block im `<head>` aktivieren und `references/mathe.md` lesen.

### 4. Inhalte schreiben

Lies zuerst `references/inhalte.md` und das Beispiel `references/beispiel-thema.html`. Kurz:

- **Einfach** = Kernidee mit Alltagsvergleich · **Normal** = Heftniveau, klausurrelevant · **Genauer** = Zusammenhänge, Musterlösung, typische Fehler.
- 2–3 Schnelltest-Fragen pro Thema mit variierter Position der richtigen Antwort.
- 1–3 SVG-Abbildungen pro Kapitel, Koordinaten vorher berechnen. Funktionsgraphen mit `scripts/plot.py` erzeugen (`references/mathe.md`, Abschnitt 3).
- Mathe: Formeln, Rechenwege, Formel-Kästen und Übungsangaben aus dem Buch → `references/mathe.md`.

**Lange Dateien in Etappen schreiben:** Erst `index.html` mit den ersten Kapiteln und einem Marker wie `<!-- WEITERE-KAPITEL -->` anlegen, dann je Kapitel(-paar) den Marker per Edit ersetzen (neuen Marker ans Ende). Eine einzelne riesige Schreibaktion bricht leicht ab, und dann ist alles weg.

### 5. Übungsklausuren

Lies `references/uebungsklausur.md`. Kurz: Stil der Originalklausur analysieren (Kopf, BE, Zeit, Operatoren, Materialmix), dann zwei neue Klausuren mit neuen Fallbeispielen, die sich ergänzen; Materialien selbst zeichnen; Erwartungshorizont mit Punkten pro Aspekt. Vorlage: `assets/templates/uebungsklausur.html`. Auch hier in Etappen schreiben (Blätter 1–4, dann den Erwartungshorizont per Marker anhängen).

Mathe-Klassenarbeiten (Teil A ohne/Teil B mit Hilfsmitteln, Wahlaufgaben, Punkte „(2)“ je Teilaufgabe) und die Umrechnungstabelle der Lehrkraft für den Notenrechner: `references/mathe.md`, Abschnitte 4–5.

Gibt es keine alte Klausur, frag kurz nach Umfang (BE, Minuten) oder nimm einen üblichen Rahmen (z. B. 60 BE / 90 Min. in der Oberstufe) und sag das dem Nutzer.

### 6. Prüfen

```bash
python <skill>/scripts/check_site.py <projekt> --names "Vorname Nachname,Frau X"
```

Das Skript prüft Stufen, Quiz-Antwortindizes, Ankerlinks, BE-/Minutensummen der Klausuren, Erwartungshorizont, Platzhalter-Reste, `.gitignore`, ob Namen auf öffentlichen Seiten stehen, ob `css/theme.css` richtig eingebunden ist und ob rundliche Schriften vorkommen. Alle Fehler beheben.

Dann im Browser ansehen:
- Über einen lokalen Server (`python3 -m http.server 8642`, im Hintergrund), nicht `file://` – in der Vorschau lädt `file://` oft kein CSS.
- Nach Änderungen kann die Vorschau altes CSS/JS cachen: Dateien per `fetch(url,{cache:'reload'})` neu laden, dann `location.reload()`.
- **Ohne Vorschau-Tool geht es mit Chrome headless** (`"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --user-data-dir=<scratch>/chrome --virtual-time-budget=20000 …`):
  - `--screenshot=<datei>.png --window-size=1280,1600` für Screenshots; zu einem bestimmten Thema über eine kleine Hilfsseite mit `<iframe>`, die nach dem Laden `scrollBehavior='auto'` setzt und zum Element scrollt (mit smooth scrolling landet der Screenshot mitten in der Animation). Hell **und** dunkel prüfen (`data-theme` am `<html>` setzen).
  - `--dump-dom` + `assets/tools/messen.html` (als `_messen.html` ins Projekt kopieren) misst waagerechtes Scrollen auf 390 px und ob die Schriften geladen sind. Screenshots mit 390 px Fensterbreite täuschen (Chrome hat eine Mindestbreite).
  - Funktionen per JS in einer Hilfsseite testen: Häkchen klicken → Punkte +10, richtige Quizantwort → +5, Notenrechner-Grenzwerte.
  - Alle Hilfsseiten danach löschen – nicht veröffentlichen.
- Materialien der Klausuren per Screenshot anschauen (Beschriftungen über Linien? Text in Kästen?).

### 7. Datenschutz & Veröffentlichung

- Der Fotoordner kommt in `.gitignore` – Fotos zeigen oft Namen von Mitschülern, Lehrkraft und Noten.
- Auf den Seiten: keine Namen von Mitschülern, kein Name der Lehrkraft (auch nicht auf den Übungsklausuren). Die Seite ist öffentlich, und eine Klausur mit dem echten Namen kann wie eine offizielle wirken.
- `README.md` erklärt beide Wege (Upload im Browser / Git). Nicht selbst pushen oder ein Repository anlegen, ohne dass der Nutzer das ausdrücklich möchte – anbieten genügt.
- **Wenn der Nutzer ein Repo nennt und hochladen lassen möchte:** Repo klonen (auch leer) und die Seite direkt darin bauen; die Originalunterlagen bleiben außerhalb. Für Commits im öffentlichen Repo `git config user.email <Name>@users.noreply.github.com` setzen, damit keine private E-Mail öffentlich wird (dem Nutzer sagen). Scheitert `git push` an fehlenden Zugangsdaten (`could not read Username`), nicht nach Tokens suchen – dem Nutzer erklären: Token unter GitHub → Settings → Developer settings anlegen und einmal selbst `git push` im Terminal ausführen; danach speichert der Schlüsselbund den Zugang. GitHub Pages aktiviert der Nutzer unter Settings → Pages (Branch `main`, `/ (root)`).

### 8. Abschluss

Kurz zusammenfassen:
- Kapitel und Themen (Inhaltsliste in einer Zeile pro Kapitel)
- Was die Spielerei kann (Punkte, Ränge, Säule, Schnelltests)
- Übungsklausuren: Fallbeispiele und abgedeckte Themen
- **Bewusste Abweichungen von den Notizen** (z. B. falsche Zahl korrigiert) und welche Materialwerte schematisch sind
- Was nicht geprüft wurde (z. B. Druckansicht)
- Nächster Schritt: veröffentlichen laut README (anbieten, es zu übernehmen)
