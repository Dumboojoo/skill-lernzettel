# Mathe (und andere Fächer mit Formeln)

Erprobt am Lernzettel „Ableitungen“ (Mathe LF, KA 1). Gilt sinngemäß auch für Physik und Chemie.

## Inhalt

1. Formeln mit KaTeX
2. Mathe-Bausteine
3. Funktionsplots mit `scripts/plot.py`
4. Mathe-Klassenarbeiten (Teil A/B, Wahlaufgaben, BE)
5. Notenpunkte nach der Tabelle der Lehrkraft
6. Fachliche Sorgfalt

---

## 1. Formeln mit KaTeX

- Den auskommentierten KaTeX-Block im `<head>` der Vorlagen aktivieren (Version `0.16.9`, jsDelivr). Er rendert `\( … \)` inline und `\[ … \]` abgesetzt.
- **Reihenfolge ist wichtig und schon richtig:** `app.js` (nicht `defer`) baut zuerst Quiz-Knöpfe und Inhaltsverzeichnis, danach rendert KaTeX (`defer`) die ganze Seite – auch Formeln in Quiz-Antworten.
- **Keine Formeln in `<h3>`-Themenüberschriften**: Der Titel wandert als Text in Seitenleiste, Inhaltsliste und Zufallsthema. Stattdessen Unicode: „Graphen von f, f′ und f″“.
- In HTML `<` in Formeln als `&lt;` schreiben, wenn ein Buchstabe folgt (`\(a&lt;b\)`), sonst hält der Browser es für ein Tag.
- **Abgesetzte Formeln kurz halten:** Was nebeneinander in eine Zeile soll, auf dem Handy aber nicht passt, auf mehrere `\[…\]` verteilen (z. B. drei binomische Formeln = drei Zeilen). `.katex-display` scrollt zwar waagerecht, schön ist das nicht.
- Brüche in Fließtext/Tabellen: `\tfrac`, in abgesetzten Formeln `\dfrac`/`\frac`.
- **Prüfen:** Seite headless rendern (`--dump-dom`) und zählen: `class="katex"` (Anzahl Formeln) und `katex-error` (muss 0 sein). Bleibt roher Text `\(` stehen, fehlt ein Begrenzer.

## 2. Mathe-Bausteine

Stehen im Theme `mathe.css` (Formel-Kasten, Rechenweg) bzw. in `extras.css` (Schritte, Übungshinweis):

| Baustein | Markup |
|---|---|
| Formel-Kasten (Karo-Hintergrund) | `<div class="formel"><span class="box-label">Kettenregel</span>\[…\] Erklärung</div>` |
| Rechenweg mit Kommentar | `<div class="rechnung"><p>\(…\) <span class="k">– Kommentar / (1 BE)</span></p>…</div>` |
| Kochrezept | `<ol class="steps"><li>…</li></ol>` (nummerierte Kästchen in Kapitelfarbe) |
| Übungsaufgaben aus dem Buch/Lernkatalog | `<p class="buch"><b>Üben</b> S. 12 Nr. 1, 3 · AB „…“</p>` – steht in allen Stufen, vor dem Quiz |
| zwei Plots nebeneinander | `<figure class="fig"><div class="fig-2">SVG SVG</div><figcaption>…</figcaption></figure>` |

Bewährte Inhalte für Mathe-Themen:
- **Normal**: Definition/Satz im `.def`, Regel im `.formel`, Beispiel-Tabelle „\(f(x)\) | \(f'(x)\)“ mit Aufgaben aus dem Buch/Arbeitsheft.
- **Genauer**: Musterlösung der alten KA mit BE-Angaben im `.rechnung`, „Typischer Fehler“, „Klausur-Tipp“ (Operator → was genau verlangt ist).
- Quizfragen mit Rechnung im `.why` (eine Zeile).
- Liegen nur Lernkatalog und alte KAs vor (keine Hefteinträge): Definitionen in üblicher Schulbuch-Formulierung schreiben und das im Inhaltsblock offen sagen.

## 3. Funktionsplots mit `scripts/plot.py`

Funktionsgraphen nie von Hand schätzen – mit `plot.py` berechnen lassen (Benutzung im Docstring). Bewährt:

- Ein eigenes Skript `figs.py` im **Scratch-Ordner** erzeugt alle SVGs nach `figs/<name>.svg`; im HTML stehen Platzhalter `<!--FIG:name-->`, die ein kleines Python-Skript ersetzt. Bei späteren Korrekturen die fertigen SVGs über ihr eindeutiges `aria-label` austauschen.
- Gleiche Einheiten auf beiden Achsen (`sy` weglassen), wenn Winkel stimmen müssen (Tangente ⟂ Normale).
- Gestapelte Plots \(f, f', f''\) (NEW-Regel): drei `Plot`-Objekte mit gleichem x-Bereich, `origin=False`, eigene `yticks`, in `<g transform="translate(0 y)">` untereinander.
- Beschriftungen nicht auf Kurven legen: Position gegen die Funktionswerte prüfen (Text liegt ~0,4 Einheiten hoch/breit je nach Maßstab) und im Screenshot kontrollieren.
- In Klausuren: `<figure class="st-fig">` (rechts schwebend, 270 px) bzw. `st-fig wide` (volle Breite) innerhalb der Teilaufgabe; Graphen schwarz (`s-ink`), zweiter Graph gestrichelt (`dash="7 4"`), wie auf echten Aufgabenblättern.
- Werte, die Schüler ablesen sollen, auf Gitterpunkte legen (Scheitel, Schnittpunkte, Steigungen 0 oder Steigungsdreiecke mit ganzen Zahlen).

## 4. Mathe-Klassenarbeiten

Typischer Aufbau in der Oberstufe (BW): 90 Min., ca. 48–50 BE. **Teil A ohne Hilfsmittel** (Pflichtaufgaben + **Wahlaufgabe**, von der nur eine zählt), **Teil B mit WTR/Formeldokument**. Punkte stehen als „(2)“ rechts neben jeder Teilaufgabe.

Markup (Klassen aus `extras.css`):

```html
<div class="teil-bar"><b>TEIL A (22 BE)</b><span>Hilfsmittel: keine Hilfsmittel</span></div>
<div class="st" data-min="15" data-label="Pflicht-Aufgabe 2"><div class="st-b">
  <p class="aufg"><span>PFLICHT-Aufgabe 2</span></p>
  <figure class="st-fig">SVG<figcaption>…</figcaption></figure>
  <p>Aufgabentext …</p>
  <ol class="sub">
    <li><span class="sl">a)</span><span><span class="op">Bestimmen</span> Sie …</span><span class="pt">(2)</span></li>
  </ol>
  <span class="st-be">(8 BE / ca. 15 Min.)</span></div></div>
```

- **Eine `.st` pro Aufgabe** (nicht pro Teilaufgabe): Der Timer zeigt „Pflicht-Aufgabe 2“, die Selbstbewertung hat ein Feld pro Aufgabe.
- **Wahlaufgabe = eine `.st`** mit zwei `<div class="wahl">`-Kästen und einem Hinweis `.wahl-hint`; BE und Minuten nur **einmal** zählen (Prüfskript summiert alle `.st-be`).
- Innerhalb einer `.st` nie `</div></div>` außer am Ende (das Prüfskript erkennt daran das Aufgabenende) – Abbildungen deshalb als `<figure>`, nicht als `<div>`.
- Kein `.st-l` nötig, `extras.css` setzt die Teilaufgaben auf volle Breite.
- Am Ende `<p class="viel-erfolg">– Viel Erfolg –</p>`; Infokasten mit `<div class="ex-text">`.
- Lösungen: je Aufgabe ein `.sol` mit `<h3>Pflicht-Aufgabe 1 <span>4 BE</span></h3>`, Punkte pro Schritt in Klammern wie im Lösungsvorschlag der Lehrkraft. Zusätzliche Blöcke (z. B. Umrechnungstabelle) mit `<div class="sol" id="…">`, damit das Prüfskript sie nicht als BE-Block zählt.
- Typische Aufgaben, die die Lehrkraft gern stellt, übernehmen: Ableiten (Ketten-/Produktregel), Werte aus Graphen von \(u\), \(v\) ablesen (\(u(v(x))\), \((u\cdot v)'\)), Monotonie aus gegebenem \(f'\), Funktionenschar, „richtig/falsch – begründe“ über allgemeine Funktionen (Symmetrie, Berühren, Sattelpunkt).
- **Alle Ergebnisse selbst nachrechnen** (Python), bevor sie in den Erwartungshorizont kommen.

## 5. Notenpunkte nach der Tabelle der Lehrkraft

`klausur.js` rechnet standardmäßig mit einer Prozent-Tabelle. Steht in der alten KA eine eigene Umrechnungstabelle, diese übernehmen – als Mindest-BE je Notenpunkt im `<head>` jeder Klausur:

```html
<script>
window.LERNZETTEL={store:'…',np:[[46,15],[43,14],[40,13],[37,12],[35,11],[32,10],[29,9],[27,8],[24,7],[21,6],[19,5],[16,4],[13,3],[11,2],[8,1],[0,0]].map(function(p){return [p[0]/48*100,p[1]];})};
</script>
```

(48 = Gesamt-BE.) Testen: Grenzwerte eintragen (z. B. 24 → 7 NP, 23 → 6 NP). Die Tabelle zusätzlich im Erwartungshorizont abdrucken.

## 6. Fachliche Sorgfalt

- Lösungsvorschläge der Lehrkraft können Lücken haben (z. B. fehlender Fall \(a>2\) bei „Anzahl der Nullstellen in Abhängigkeit von \(a\)“). Ergänzen und dem Nutzer nennen.
- Wo eine Musterlösung nur notwendige Bedingungen zeigt (z. B. \(h'(a)=h''(a)=0\) für „Sattelpunkt“), ehrlich anmerken, dass das für volle Punkte reichte, aber streng genommen nicht hinreichend ist.
- Gegenbeispiele in Beweisaufgaben müssen **alle** Voraussetzungen erfüllen.
