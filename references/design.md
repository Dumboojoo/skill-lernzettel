# Fachdesign: ein Theme pro Fach

Der Lernzettel soll **zum Fach passen** – ein Mathe-Lernzettel sieht anders aus als einer für Geschichte. Layout, Logik und Bausteine bleiben gleich (`style.css`, `extras.css`, `app.js`); das Aussehen kommt aus **einer** Datei `css/theme.css`, die zuletzt geladen wird.

## Inhalt

1. Vorhandene Themes
2. Schriften – feste Regel
3. Neues Theme für ein Fach bauen
4. Motive nach Fach (Ideen)
5. Prüfen

---

## 1. Vorhandene Themes (`assets/themes/`)

| Datei | Fach | hell / dunkel | Schriften | Fortschrittssäule |
|---|---|---|---|---|
| `erde.css` | Geographie, Geologie | warmes Papier, Höhenlinien / dunkles Gestein | Archivo (breit, Versalien) + IBM Plex | Bohrkern |
| `mathe.css` | Mathematik | Karoheft (Karopapier, Füller-Dunkelblau, Textmarker-Orange) / Tafel (dunkelgrün, Kreidefarben, Karo-Linien) | Inter Tight + Inter + IBM Plex Mono | Wertetabelle „f(x)“ |
| `_vorlage.css` | – | Gerüst mit allen Tokens | – | – |

Passt ein vorhandenes Theme, kopieren: `cp <skill>/assets/themes/mathe.css css/theme.css`. Sonst ein neues bauen (Abschnitt 3) und es **auch im Skill unter `assets/themes/<fach>.css` ablegen**, damit es beim nächsten Mal bereitsteht.

## 2. Schriften – feste Regel

Der Nutzer will **immer eine klare, „cleane“ Schrift, nie etwas Rundliches** – egal welches Fach, auch bei Bio oder Kunst.

**Erlaubt** (Google Fonts, klar und kantig):

| Rolle | Gute Wahl |
|---|---|
| Überschriften | Inter Tight, Archivo, IBM Plex Sans (Condensed), Source Sans 3, Public Sans, Schibsted Grotesk, Instrument Sans |
| Fließtext | Inter, IBM Plex Sans, Source Sans 3, Public Sans |
| Zahlen/Labels | IBM Plex Mono, JetBrains Mono |
| Serifen (nur wenn das Fach es nahelegt, z. B. Geschichte, Deutsch – dann nur für Überschriften) | Source Serif 4, IBM Plex Serif, Newsreader |

**Verboten** (rundlich oder kreisrund-geometrisch – `check_site.py` meldet sie als Fehler): Nunito, Quicksand, Comfortaa, Varela Round, Fredoka, Baloo, M PLUS Rounded, Rubik, Poppins, Montserrat, DM Sans, Manrope, Outfit, Lexend, Barlow, Mulish, Comic-Schriften, Arial/SF Rounded.

Weitere Regeln:
- Formeln bleiben in der KaTeX-Mathe-Schrift (Computer Modern) – das ist richtig so.
- Höchstens zwei Schriftfamilien + eine Mono.
- Schriften werden per `@import` **in der ersten Zeile von `theme.css`** geladen (nicht im HTML). URL vorher testen: `curl -s -o /dev/null -w "%{http_code}" "<url>"` muss 200 liefern – eine falsche Achsenangabe lässt die ganze Anfrage scheitern.
- Hat die Überschriftenschrift keine Breitenachse (alles außer Archivo), `font-stretch:normal` setzen und die Versalien des Grund-Layouts abschalten (siehe `_vorlage.css`). Großbuchstaben-Überschriften wirken nur mit breiter Schrift.
- Enger Zeichenabstand: bei Inter Tight höchstens `-.03em` im großen Titel und `-.012em` bei Themenüberschriften, sonst kleben die Buchstaben.

## 3. Neues Theme bauen

Ausgangspunkt `assets/themes/_vorlage.css`. Vorgehen:

1. **Motiv finden:** Was sieht man im Unterricht dieses Fachs? (Karoheft, Tafel, Laborjournal, Karte, Archivpapier …) Ein Motiv für Hell, eines für Dunkel.
2. **Farben:** `--ink` (Text) dunkel und leicht getönt passend zum Motiv; `--accent` als einzige kräftige Signalfarbe (Fortschritt, aktive Navigation, Untertitel). `--water-ink` muss sich deutlich von `--accent` unterscheiden – Abbildungen benutzen beide Farben nebeneinander (`s-acc`, `s-water`), und Bildunterschriften nennen die Farbe („orange“, „blau“). Wenn sich die Akzentfarbe ändert, die Bildunterschriften prüfen!
3. **Sechs Kapitelfarben** `--c1…--c6`: klar unterscheidbar, in Hell gesättigt mittel, in Dunkel heller/pastellig.
4. **Alle drei Token-Blöcke** füllen (hell, `prefers-color-scheme:dark`, `[data-theme="dark"]`) – sonst wechselt der Theme-Knopf nicht vollständig.
5. **Klausurblätter:** `--paper` und `--paper-line` setzen (Papierfarbe, Linienfarbe der Kästen).
6. **Textur dezent:** Hintergrundmuster (Karo, Linien) mit ca. 4–10 % Deckkraft. Inhalte (Karten, Tabellen) bleiben auf ruhiger `--surface`.
7. **Fortschrittssäule umdeuten** (`.core`): Name `{{SAEULE}}` und Optik passend zum Fach. Die Bohrkern-Spitze (`.core::after`) dann ausblenden.
8. **Hero-Motiv** im HTML (`.hero-topo`, dünne Linien in `currentColor`): Höhenlinien (Geo), Koordinatensystem mit Funktionenschar (Mathe), Strukturformeln (Chemie), Zeitstrahl (Geschichte) … Koordinaten mit einem Skript berechnen.

## 4. Motive nach Fach (Ideen)

| Fach | Hell | Dunkel | Säule | Hero |
|---|---|---|---|---|
| Mathe | Karoheft | Tafel mit Karo | Wertetabelle | Koordinatensystem + Schar |
| Physik | Millimeterpapier | Oszilloskop/Blaupause | Messskala | Feldlinien, Schwingung |
| Chemie | Laborjournal (Linien, Tinte) | Abzug/Labor dunkel | Reagenzglas mit Füllstand | Strukturformeln, Wabenmuster |
| Biologie | Herbarium / Mikroskop-Präparat | dunkles Mikroskopfeld | DNA-Strang | Zellen, Blattadern |
| Geographie | Papier + Höhenlinien (`erde`) | Gestein | Bohrkern | Höhenlinien |
| Geschichte | Archivpapier, Stempelrot | Pergament dunkel | Zeitleiste | Zeitstrahl, Jahreszahlen |
| Deutsch/Englisch | liniertes Schreibheft, Korrekturrot | Notizbuch dunkel | Bücherstapel | Zeilen, Anführungszeichen |

## 5. Prüfen

- `check_site.py` meldet fehlendes `theme.css`, falsche Ladereihenfolge, fehlende Dunkel-Variante und rundliche Schriften.
- Screenshot hell **und** dunkel ansehen (Theme per `data-theme` am `<html>` umschalten).
- `assets/tools/messen.html` meldet, ob die Schriften wirklich geladen wurden und ob auf 390 px waagerecht gescrollt wird – breitere Schriften können Tabellen und Formeln über den Rand schieben.
