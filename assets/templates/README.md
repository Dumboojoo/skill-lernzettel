# Lernzettel {{TITEL}} ({{FACH}})

Interaktiver Lernzettel als Webseite:

- **{{ANZAHL_THEMEN}} Themen in {{ANZAHL_KAPITEL}} Kapiteln**: {{THEMEN_KURZ}}
- **3 Erklärstufen** pro Thema: Einfach · Normal · Genauer
- **Abhaken & Punkte**: Haken bei verstandenen Themen, Schnelltests, Ränge von „{{RANG_1}}“ bis „{{RANG_8}}“
- **2 Übungsklausuren** im Stil der echten Klausur ({{BE_GESAMT}} BE, {{MINUTEN}} Minuten) mit Timer, Erwartungshorizont und Notenpunkte-Rechner

Der Fortschritt wird nur im eigenen Browser gespeichert (localStorage).

## Dateien

| Datei | Inhalt |
|---|---|
| `index.html` | Lernzettel |
| `uebungsklausur-1.html` | Übungsklausur 1: {{KLAUSUR_1_KURZ}} |
| `uebungsklausur-2.html` | Übungsklausur 2: {{KLAUSUR_2_KURZ}} |
| `css/`, `js/` | Design und Logik |
| `{{FOTO_ORDNER}}/` | Fotos der Originalunterlagen – **wird nicht hochgeladen** (siehe `.gitignore`) |

## Auf GitHub Pages veröffentlichen

### Variante A: im Browser (ohne Git)

1. Auf [github.com](https://github.com) einloggen → oben rechts **+** → **New repository**.
2. Name z. B. `{{REPO_NAME}}`, **Public** auswählen, **Create repository**.
3. Auf der Repo-Seite **uploading an existing file** anklicken.
4. Diese Dateien bzw. Ordner hineinziehen: `index.html`, `uebungsklausur-1.html`, `uebungsklausur-2.html`, den Ordner `css` und den Ordner `js`.
   **Nicht** den Ordner `{{FOTO_ORDNER}}` hochladen – darin sind Fotos mit Namen.
5. Unten **Commit changes** klicken.
6. Im Repo: **Settings → Pages** → bei *Source* „Deploy from a branch“, Branch **main**, Ordner **/ (root)** → **Save**.
7. Nach 1–2 Minuten ist die Seite online unter
   `https://DEIN-NAME.github.io/{{REPO_NAME}}/`

### Variante B: mit Git (Terminal)

```bash
git init
git add .
git commit -m "Lernzettel {{TITEL}}"
git branch -M main
git remote add origin https://github.com/DEIN-NAME/{{REPO_NAME}}.git
git push -u origin main
```

Danach wie oben unter **Settings → Pages** den Branch `main` und `/ (root)` auswählen. Der Ordner `{{FOTO_ORDNER}}/` wird dank `.gitignore` automatisch ausgelassen.

Die Warnungen „LF will be replaced by CRLF“ unter Windows sind harmlos.

## Lokal ansehen

`index.html` doppelklicken. Falls Schriften oder Design fehlen, einen kleinen Server starten:

```bash
python -m http.server 8000
```

und `http://localhost:8000` öffnen.

## Hinweis

Selbst erstellte Lernhilfe, zusammengestellt aus Unterrichtsmaterialien. Die Übungsklausuren sind keine offiziellen Klausuren. Ohne Gewähr – bei Widersprüchen gilt der Hefter.
