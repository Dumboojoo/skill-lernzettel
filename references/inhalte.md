# Inhalte schreiben: Themen, drei Stufen, Schnelltests, Abbildungen

Ein vollständiges Beispielthema liegt in `beispiel-thema.html` – vor dem ersten Thema einmal ansehen.

## Inhalt

1. Themen zuschneiden
2. Die drei Erklärstufen
3. Bausteine (HTML-Klassen)
4. Schnelltests
5. Abbildungen als Inline-SVG
6. Fachliche Sorgfalt

---

## 1. Themen zuschneiden

- **Ein Thema = eine Lerneinheit**, die man in 10–20 Minuten verstehen und dann abhaken kann. Zu groß („Plattentektonik“) lässt sich nie guten Gewissens abhaken; zu klein („Moho“) macht die Liste unübersichtlich.
- **Reihenfolge wie im Heft.** Die Lehrkraft baut aufeinander auf; Schüler erkennen ihre Hefteinträge wieder.
- **Kapitel I „Handwerkszeug“**, wenn die Klausur mit Operatoren/Darstellungsformen arbeitet (Oberstufe fast immer): Operatoren & Anforderungsbereiche, Darstellungsformen (Fließschema, Wirkungsgefüge, Skizze, Profil …) – genau so, wie sie im Unterricht eingeführt wurden. Randnotizen der Lehrkraft (z. B. „anhand von M1 = nur Material, ausgehend von M1 = Material + Wissen“) sind Gold wert und gehören hinein.
- **Fallbeispiele aus der alten Klausur** (z. B. „Island“) als eigenes Thema, das in „Genauer“ eine Kurz-Musterlösung der alten Klausur enthält.
- `id` = kurzer Slug ohne Umlaute (`schalenbau`, `wilson`). Die id ist zugleich Speicherschlüssel für das Häkchen – nach dem Veröffentlichen nicht mehr ändern.

## 2. Die drei Erklärstufen

Alle drei Stufen behandeln **denselben Stoff in unterschiedlicher Tiefe** – sie sind keine Fortsetzungen. Wer nur „Einfach“ liest, soll die Kernidee haben; wer nur „Normal“ liest, soll die Klausur bestehen können.

| Stufe | Ziel | Sprache & Umfang | Typische Bausteine |
|---|---|---|---|
| **Einfach** | Kernidee verstehen, „Aha“ | Alltagssprache, kurze Sätze, du-Form, Fachbegriffe nur die wichtigsten und sofort erklärt; ca. 80–150 Wörter | ein Vergleich aus dem Alltag (`.analogy`), kurze Liste, ein Merksatz |
| **Normal** | Heftniveau – das, was in der Klausur reproduziert werden muss | Fachsprache, Definitionen wörtlich nah am Heft, vollständig; ca. 150–350 Wörter | `.def`, Tabellen, Listen, `.box.merke`, Fließschema |
| **Genauer** | Zusammenhänge, Hintergründe, Klausurtechnik | dicht, mit Begründungen „warum“, Verknüpfungen zu anderen Themen (Links `#id`); ca. 150–350 Wörter | Musterlösung zu einer Klausuraufgabe, `.box.tipp`, `.box.fehler`, Profi-Info |

Hinweise:
- **Einfach ist nicht kindisch.** Zielgruppe sind Oberstufenschüler, die den Stoff gerade nicht verstehen – also klare Bilder („wie ein Holzklotz im Wasser“), keine Babysprache.
- **Normal folgt dem Heft.** Wo die Lehrkraft eine Definition vorgegeben hat, diese verwenden (sie wird in der Klausur erwartet). Mitschüler-Lernzettel helfen bei der Struktur, enthalten aber manchmal Fehler.
- **Genauer zeigt, wie man Punkte holt:** Aufbau einer Antwort zu einer typischen Aufgabe, Materialbezug, typische Fehler. Fachlich Tieferes (das im Heft fehlt) als solches kennzeichnen („Fachlich zusätzlich wichtig: …“), damit niemand denkt, es sei Pflichtstoff.

## 3. Bausteine (HTML-Klassen)

Alle Klassen sind in `css/style.css` definiert. Nummer, „Verstanden“-Knopf und Stufen-Tabs ergänzt `js/app.js` automatisch – nicht von Hand einfügen.

```html
<article class="topic" id="slug" data-show="2">
  <header class="topic-head"><h3>Titel</h3></header>
  <div class="level" data-level="1">…</div>
  <div class="level" data-level="2">…</div>
  <div class="level" data-level="3">…</div>
  <figure class="fig">…</figure>        <!-- optional, in allen Stufen sichtbar -->
  <div class="quiz">…</div>
</article>
```

| Baustein | Markup |
|---|---|
| Definition | `<div class="def"><b>Begriff</b> = …</div>` |
| Merkkasten | `<div class="box merke"><span class="box-label">Merke</span>…</div>` |
| Klausur-Tipp | `<div class="box tipp"><span class="box-label">Klausur-Tipp</span>…</div>` |
| Typischer Fehler | `<div class="box fehler"><span class="box-label">Typischer Fehler</span>…</div>` |
| Alltagsvergleich | `<p class="analogy">…</p>` |
| Tabelle | `<div class="tbl"><table><thead>…</thead><tbody><tr><th>Zeilenkopf</th><td>…</td></tr></tbody></table></div>` |
| AFB-Marke | `<span class="afb">I</span>`, `<span class="afb a2">II</span>`, `<span class="afb a3">III</span>` |
| Fließschema | `<p class="flow-title">Überschrift</p><div class="flow"><div class="start">Ausgangspunkt …</div><div>…</div><div class="end">…</div></div>` (Pfeile kommen per CSS) |
| Mehrere Ursachen → Kette | `<div class="flow-row"><div><b>Ursache</b><small>Details</small></div>…</div><div class="flow after-row">…</div>` |
| Stadien/Phasen | `<div class="wilson"><div class="wstage" data-t="div"><span class="n">1</span><b>Name</b>Text<span class="ex">Bsp.: …</span></div>…</div>` (`data-t="div"` rot, `"kon"` blau, ohne = neutral; Legende mit `.legend`) |
| Zeitleiste | `<ul class="timeline"><li><span class="era">Zeit</span><b>Titel</b>Text</li></ul>` |
| 3×3-Raster (z. B. Klima) | `.climate` mit `.h`, `.rh`, `.cell` + Farbklasse – siehe CSS |

Kapitel: `<section class="chapter" id="kap-N" style="--cc:var(--cN)" data-short="Kurztitel" data-msg="Toast-Satz">` mit `.chapter-head` (siehe Vorlage). Es gibt sechs Kapitelfarben `--c1` … `--c6`; bei mehr Kapiteln Farben wiederholen.

## 4. Schnelltests

- 2–3 Fragen pro Thema, je 3 Antworten (selten 4). `data-a` = Index der richtigen Antwort (0-basiert).
- **Position der richtigen Antwort variieren.** Steht sie immer an Stelle A oder B, lernt man das Muster statt des Stoffs.
- Falsche Antworten sind **plausible Fehlvorstellungen** (z. B. „Platten schwimmen auf flüssigem Magma“), keine offensichtlichen Scherze.
- Jede Frage hat eine `.why`-Erklärung – sie wird nach dem Antworten angezeigt und ist der eigentliche Lerneffekt.
- Mindestens eine Frage pro Thema prüft Verständnis (warum/was folgt), nicht nur Begriffe.

## 5. Abbildungen als Inline-SVG

Abbildungen machen den Unterschied zu einem Textdokument. Pro Kapitel 1–3 Stück, dort wo ein Bild mehr sagt (Schichten, Querschnitte, Diagramme, Kreisläufe).

- **Koordinaten vorher ausrechnen**, nicht schätzen: Bei Diagrammen Achsen-Ursprung und Skalierung festlegen (z. B. `x = 64 + km·0,8667`), dann jeden Punkt berechnen. Bei Karten eine einfache Projektion `x = (lon − lon0)·k + 10`, `y = (lat0 − lat)·k + 10` und echte Küsten-/Ortskoordinaten verwenden.
- **Farben, die in Hell und Dunkel funktionieren:**
  - Text und Linien über Klassen: `.fig text` ist automatisch `var(--ink)`; Varianten `.t-mute`, `.t-acc`, `.t-water`, `.t-w` (weiß); Größen `.t-s`, `.t-xs`, `.t-h`, `.t-b`.
  - Linien/Flächen: `class="s-ink"`, `s-mute`, `s-line`, `f-ink`, `f-water`, `f-land`, `f-surface` …
  - Feste Materialfarben (Gestein, Magma …) als Hex-Attribut sind ok; Text **auf** solchen Flächen dann fest dunkel/weiß per `style="fill:#1e1a15"`.
- **Stolperfallen:**
  - `fill="var(--x)"` als Attribut ist unzuverlässig → Klasse oder `style="fill:var(--x)"`.
  - Die CSS-Regel `.fig text{fill:…}` überschreibt `fill="…"`-Attribute → für Sonderfarben `style="fill:…"`.
  - Pfeilspitzen über die gemeinsamen `<marker>` (`url(#arr)`) aus dem `<defs>`-Block am Seitenanfang; neue Marker/Muster dort ergänzen, IDs pro Seite eindeutig.
  - Beschriftungen nicht über Linien legen; bei Platzmangel `viewBox` oben erweitern (z. B. `0 -40 640 320`) und Führungslinien nutzen.
- Bildunterschrift in `<figcaption>` ehrlich: „schematisch“, „nicht maßstabsgetreu“, Quelle der Werte.

## 6. Fachliche Sorgfalt

- Zahlen und Fakten nur übernehmen, wenn sie stimmen. Notizen von Schülern enthalten Rechen- oder Abschreibfehler – Werte aus Diagrammen der Lehrkraft nachrechnen (Beispiel: „45 % liegen 3–6 km tief“ war laut Histogramm 54 %).
- Wo der Unterricht vereinfacht, die Heftversion in „Normal“ lassen und die genauere Erklärung in „Genauer“ ergänzen, statt das Heft zu „korrigieren“.
- Jede bewusste Abweichung vom Heft am Ende dem Nutzer nennen.
