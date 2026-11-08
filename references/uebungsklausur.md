# Übungsklausuren im Stil der Lehrkraft

Ziel: Klausuren, die sich anfühlen wie die echte – gleiche Optik, gleiche Punkteverteilung, gleiche Operatoren, gleicher Materialmix –, aber mit **neuen Raumbeispielen bzw. Inhalten**, die andere Themen des Lernzettels abdecken.

## Inhalt

1. Stil der Originalklausur analysieren
2. Neue Klausuren planen
3. Materialien bauen
4. Erwartungshorizont & Selbstbewertung
5. Markup-Referenz
6. Was nicht hineingehört

---

## 1. Stil der Originalklausur analysieren

Vor dem Schreiben eine Stil-Notiz anlegen (nur für dich), z. B.:

| Merkmal | Beispiel (Geo LK, Klausur 2024) |
|---|---|
| Kopf | Tabelle „Geo LK · Kürzel · Geo-Klausur Nr. 1 · Reliefsphäre“, Logo links schräg |
| Infokasten | „Auf eine sorgfältige Darstellung und korrekte Rechtschreibung ist zu achten.“, Name, Datum, Punkte / (60 BE), Notenpunkte, Mündliche Selbsteinschätzung |
| Umfang | 60 BE, 90 Min.; Aufgabe 1 = 50 BE / 70 Min. (Fallbeispiel), Aufgabe 2 = 10 BE / 20 Min. (anderes Teilgebiet, ein Diagramm) |
| Teilaufgaben | a)–e) mit „(xBE / ca. y Min.)“; BE grob 10/16/16/4/4 |
| Operatoren | fett; oft zwei pro Teilaufgabe („Erläutern … und erklären …“); eine Darstellungsaufgabe mit vorgegebenem Startsatz („Beginnen Sie mit …“) |
| Materialien | M1–M6: Karte, Blockbild/Profil, Fachtext, Fachdiskussion (Pro/Contra), Diagramm; Quellenangaben darunter |
| Einleitung | Kurzer Text mit gelb markierten Schlüsselbegriffen |
| Schluss | Kasten „Operatoren-Liste“ mit AFB |

Achte auch auf Kleinigkeiten wie Material-Verweise („(M1, unterstützend M2)“), Zeitmanagement-Angaben und ob die Lehrkraft Fachdiskussionen/Kontroversen einbaut – das gehört zum Stil.

## 2. Neue Klausuren planen

- **Gleiche Struktur, neuer Fall.** Jede Klausur bekommt ein neues Raumbeispiel/Fallbeispiel, das möglichst viele *andere* Lernzettel-Themen abfragt als die Originalklausur. Zwei Klausuren sollen sich untereinander ergänzen (z. B. eine divergente, eine konvergente Plattengrenze; zwei verschiedene Verwitterungsarten in Aufgabe 2).
- **Punkte und Zeit stimmig:** Summe der BE = Gesamt-BE, Summe der Minuten = Gesamtzeit; Zeit ≈ proportional zu den BE. Das Prüfskript kontrolliert das.
- **AFB-Mischung wie im Original:** wenige BE für AFB I, Großteil AFB II, eine AFB-III-Aufgabe (beurteilen/erörtern) wenn das Original eine hat.
- **Eine Darstellungsaufgabe** (Fließschema/Wirkungsgefüge/Skizze) mit vorgegebenem Startsatz, wenn das Original eine hat.
- Jede Teilaufgabe muss sich mit den Materialien plus Lernzettel-Wissen lösen lassen – vorher selbst die Lösung skizzieren.

## 3. Materialien bauen

Alle Materialien sind selbst erstellt – keine Scans aus Schulbüchern (Urheberrecht), keine Fotos aus den Unterlagen.

- **Karten:** stark vereinfachte Inline-SVG mit echter Geometrie. Projektion festlegen (`x = (lon − lon0)·k + 10`, `y = (lat0 − lat)·k + 10`), echte Koordinaten von Küstenpunkten, Städten, Vulkanen, Epizentren einsetzen, Legende + Maßstab (1° Breite ≈ 111 km). Quelle: „Eigene, stark vereinfachte Darstellung“.
- **Profile/Blockbilder:** schematisch, mit Beschriftungen und Führungslinien; Hinweis „schematisch, überhöht“.
- **Diagramme:** Achsen, Einheiten, Gitter, Legende. Werte entweder belegbar (Literaturwerte, gerundet) oder klar als „schematisch, vereinfachte Werte“ gekennzeichnet. Nie erfundene Zahlen als echte Messreihe ausgeben.
- **Sachtexte:** 120–200 Wörter, sachlich, mit 3–5 verwertbaren Fakten. Nur Fakten, bei denen du dir sicher bist; im Zweifel weglassen oder vorsichtig formulieren („mehrere Meter“, „rund 60 km“).
- **Tabellen/Steckbriefe:** gut für Vergleichsaufgaben (z. B. zwei Vulkane), aber die Zuordnung nicht verraten, wenn sie die Aufgabe ist.
- **Rechenmaterial** (z. B. Weg-Zeit-Diagramm): Werte so wählen, dass sie aufgehen und konsistent sind (z. B. alle Ankunftszeiten passen zu einer gemeinsamen Herdzeit). Hilfslinie für das Ablesen anbieten.
- Farben/Theme wie in `inhalte.md`, Abschnitt 5. In Klausurblättern gilt die Regel `.mat svg text{fill:var(--ink)}` – Sonderfarben per `style="fill:…"`.

## 4. Erwartungshorizont & Selbstbewertung

- Pro Teilaufgabe eine `.sol`-Box: Überschrift mit BE und AFB, darunter die erwarteten Aspekte als Liste mit Punkten in Klammern; Summe = BE der Teilaufgabe.
- Materialbezug ausdrücklich nennen („M5: Rukwa 1910 M 7,4 …“).
- Bei Darstellungsaufgaben: Hinweis zur Aufteilung Darstellung/Inhalt + ein vollständiges Muster-Fließschema (`.flow`).
- Bei AFB III: Pro- und Contra-Aspekte + „begründetes Urteil“ als eigener Punkt.
- Selbstbewertung: ein Eingabefeld je Teilaufgabe (`max` = BE). `js/klausur.js` rechnet Summe, Prozent und Notenpunkte (übliche Oberstufen-Tabelle, als Richtwert gekennzeichnet).

## 5. Markup-Referenz

Gerüst: `assets/templates/uebungsklausur.html`.

| Element | Zweck |
|---|---|
| `<body class="exam" data-minutes="90">` | Gesamtzeit für den Timer |
| `.ex-head` + `.ex-logo` | Kopftabelle, Logo-Kasten schräg links (kleines fachpassendes Piktogramm statt Original-Logo) |
| `.ex-info` mit `.field` | Infokasten mit Linien zum Ausfüllen |
| `.task-bar` | „Aufgabe 1 · (50 BE) · Zeitmanagement“ |
| `.intro` mit `<mark>` | Einleitung mit Markierungen |
| `.st[data-min][data-label]` | Teilaufgabe; Timer hebt die aktuelle hervor |
| `.op` | fetter Operator |
| `.st-be` | „(10 BE / ca. 15 Min.)“ – dieses Format liest das Prüfskript |
| `.mats` > `.mat` / `.mat.wide` | Materialraster (2 Spalten / volle Breite) |
| `.mat-text.mat-box`, `.steck`, `.steck-row` | Sachtext im Kasten, Steckbriefe |
| `.src` | Quellenzeile |
| `.oplist` | Operatoren-Liste (nur die verwendeten Operatoren) |
| `.sheet.solutions` | Erwartungshorizont, per Button einblendbar |
| `.selfcheck` > `.sc-grid input[max]` | Selbstbewertung |

Jedes `.sheet` ist ein Druckblatt (A4). Material-Reihenfolge M1, M2, … so auf die Blätter verteilen, dass die Nummern fortlaufend sind und große Abbildungen `.wide` bekommen (kleine SVG-Schrift wird in halber Breite unlesbar).

## 6. Was nicht hineingehört

- **Kein Name der Lehrkraft** (auch nicht „Viel Erfolg wünscht euch Frau …“) und keine Namen von Mitschülern: Die Seite ist öffentlich, und eine Klausur mit dem echten Namen kann wie eine offizielle aussehen. Stattdessen „Viel Erfolg!“ und der Hinweis „Selbst erstellte Übungsklausur … keine offizielle Klausur“.
- Kein Nachbau des Original-Logos (z. B. Comic-Figur der Lehrkraft) – ein eigenes kleines Piktogramm im selben Kasten genügt als Wiedererkennung.
- Keine wörtlich übernommenen Materialien aus der Originalklausur.
