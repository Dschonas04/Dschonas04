#!/usr/bin/env python3
"""Zeichnet die Karten für das Profil-README: Statistik, Sprachen, Serien
und ein paar Spielereien (Terminal, TNT, Server-Schrank).

Warum selbst und nicht github-readme-stats: der öffentliche Dienst dort
antwortet regelmäßig mit 503, und dann steht im Profil ein kaputtes Bild.
Hier läuft die Abfrage im eigenen Arbeitsablauf, das Ergebnis liegt als SVG im
Repository, und es kann nichts ausfallen, was nicht mir gehört.

Jede Karte entsteht zweimal, hell und dunkel: ein SVG im <img> bekommt die
Themenumschaltung von GitHub nicht mit, und eine Fassung, die auf beiden
Untergründen gerade noch geht, ist auf keinem gut. Das README wählt per
#gh-light-mode-only bzw. #gh-dark-mode-only aus.
"""
import datetime
import json
import os
import urllib.request

BENUTZER = os.environ.get("BENUTZER", "Dschonas04")
TOKEN = os.environ["GITHUB_TOKEN"]

THEMEN = {
    "hell": {"akzent": "#c2410c", "schrift": "#57606a", "stark": "#24292f", "linie": "#d0d7de"},
    "dunkel": {"akzent": "#f97316", "schrift": "#9198a1", "stark": "#e6edf3", "linie": "#3d444d"},
}

ABFRAGE = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount weekday } }
      }
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
      totalCount
      nodes {
        name
        isPrivate
        stargazerCount
        languages(first: 12, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    followers { totalCount }
  }
}
"""


def graphql(abfrage, variablen):
    anfrage = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": abfrage, "variables": variablen}).encode(),
        headers={
            "Authorization": "Bearer " + TOKEN,
            "Content-Type": "application/json",
            "User-Agent": "karten.py",
        },
    )
    antwort = json.load(urllib.request.urlopen(anfrage))
    if "errors" in antwort:
        raise SystemExit(antwort["errors"])
    return antwort["data"]


def zahl(n):
    """1234 -> 1.2k. Vierstellige Zahlen sprengen sonst die Spalte."""
    return f"{n / 1000:.1f}k".replace(".0k", "k") if n >= 1000 else str(n)


def kopf(breite, hoehe, titel, t):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}" '
        f'viewBox="0 0 {breite} {hoehe}" role="img" aria-label="{titel}">'
        f'<style>text{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}}</style>'
        f'<rect x="0.5" y="0.5" width="{breite - 1}" height="{hoehe - 1}" rx="7" '
        f'fill="none" stroke="{t["linie"]}"/>'
    )


def statistik_karte(daten, pfad, t):
    b = daten["contributionsCollection"]
    repos = daten["repositories"]["nodes"]
    zeilen = [
        ("Contributions, last year", b["contributionCalendar"]["totalContributions"]),
        ("Commits", b["totalCommitContributions"] + b["restrictedContributionsCount"]),
        ("Pull requests", b["totalPullRequestContributions"]),
        ("Issues", b["totalIssueContributions"]),
        ("Repositories", daten["repositories"]["totalCount"]),
        ("Stars earned", sum(r["stargazerCount"] for r in repos)),
    ]
    akzent, schrift, stark = t["akzent"], t["schrift"], t["stark"]
    # Gleich hoch wie die Nachbarkarte, damit die Reihe bündig ist.
    hoehe = 46 + 6 * 26 + 14
    teile = [kopf(420, hoehe, "GitHub statistics", t)]
    teile.append(f'<text x="22" y="30" font-size="14" font-weight="600" fill="{akzent}">Statistics</text>')
    y = 58
    for name, wert in zeilen:
        teile.append(f'<text x="22" y="{y}" font-size="12.5" fill="{schrift}">{name}</text>')
        teile.append(
            f'<text x="398" y="{y}" font-size="12.5" font-weight="600" '
            f'text-anchor="end" fill="{stark}">{zahl(wert)}</text>'
        )
        y += 26
    teile.append("</svg>")
    open(pfad, "w").write("".join(teile))
    return zeilen


def sprachen_karte(daten, pfad, t, anzahl=7):
    akzent, schrift, stark = t["akzent"], t["schrift"], t["stark"]
    groessen = {}
    farben = {}
    for repo in daten["repositories"]["nodes"]:
        for kante in repo["languages"]["edges"]:
            name = kante["node"]["name"]
            if name in ("Jinja", "Go Template", "Dockerfile", "Makefile"):
                continue
            groessen[name] = groessen.get(name, 0) + kante["size"]
            farben[name] = kante["node"]["color"] or schrift
    oben = sorted(groessen.items(), key=lambda p: -p[1])[:anzahl]
    gesamt = sum(g for _, g in oben) or 1

    breite, rand, balken = 420, 22, 12
    hoehe = 46 + balken + 16 + ((len(oben) + 1) // 2) * 22 + 12
    teile = [kopf(breite, hoehe, "Most used languages", t)]
    teile.append(f'<text x="{rand}" y="30" font-size="14" font-weight="600" fill="{akzent}">Languages</text>')

    # Ein Balken, in dem jede Sprache ihren Anteil bekommt.
    x = rand
    nutz = breite - 2 * rand
    teile.append(f'<clipPath id="r"><rect x="{rand}" y="44" width="{nutz}" height="{balken}" rx="6"/></clipPath>')
    teile.append('<g clip-path="url(#r)">')
    for name, groesse in oben:
        w = nutz * groesse / gesamt
        teile.append(f'<rect x="{x:.1f}" y="44" width="{w:.1f}" height="{balken}" fill="{farben[name]}"/>')
        x += w
    teile.append("</g>")

    y = 44 + balken + 26
    for i, (name, groesse) in enumerate(oben):
        spalte = rand if i % 2 == 0 else rand + nutz / 2
        anteil = 100 * groesse / gesamt
        teile.append(f'<circle cx="{spalte + 5}" cy="{y - 4}" r="5" fill="{farben[name]}"/>')
        teile.append(
            f'<text x="{spalte + 16}" y="{y}" font-size="12" fill="{schrift}">'
            f'{name} <tspan fill="{stark}" font-weight="600">{anteil:.1f}%</tspan></text>'
        )
        if i % 2 == 1:
            y += 22
    if len(oben) % 2 == 1:
        y += 22
    teile.append("</svg>")
    open(pfad, "w").write("".join(teile))
    return oben


def tage(daten):
    """Alle Tage des Kalenders als (Datum, Anzahl, Wochentag), alt nach neu."""
    l = []
    for w in daten["contributionsCollection"]["contributionCalendar"]["weeks"]:
        for d in w["contributionDays"]:
            l.append((d["date"], d["contributionCount"], d["weekday"]))
    return l

def serien_karte(daten, pfad, t):
    import datetime
    l = tage(daten)
    heute = datetime.date.today().isoformat()
    # Aktuelle Serie: heute darf noch leer sein, der Tag ist nicht vorbei.
    aktuell = 0
    for datum, n, _ in reversed(l):
        if datum == heute and n == 0:
            continue
        if n == 0:
            break
        aktuell += 1
    laengste = lauf = 0
    for _, n, _ in l:
        lauf = lauf + 1 if n else 0
        laengste = max(laengste, lauf)
    bester = max(l, key=lambda x: x[1]) if l else ("", 0, 0)
    namen = ["Sundays", "Mondays", "Tuesdays", "Wednesdays", "Thursdays", "Fridays", "Saturdays"]
    je = [0] * 7
    for _, n, wd in l:
        je[wd] += n
    aktive = sum(1 for _, n, _ in l if n)
    zeilen = [
        ("Current streak", f"{aktuell} days"),
        ("Longest streak", f"{laengste} days"),
        ("Active days", f"{aktive} of {len(l)}"),
        ("Best day", f"{bester[1]} on {datetime.date.fromisoformat(bester[0]).strftime('%d %b %Y') if bester[0] else '-'}"),
        ("Busiest on", namen[je.index(max(je))] if any(je) else "-"),
    ]
    akzent, schrift, stark = t["akzent"], t["schrift"], t["stark"]
    # Gleich hoch wie die Nachbarkarte, damit die Reihe bündig ist.
    hoehe = 46 + 6 * 26 + 14
    teile = [kopf(420, hoehe, "Streaks", t)]
    teile.append(f'<text x="22" y="30" font-size="14" font-weight="600" fill="{akzent}">Streaks</text>')
    # Eine kleine Flamme, die bei laufender Serie leuchtet.
    if aktuell:
        teile.append(
            f'<g transform="translate(386 14)"><path d="M6 0C8 5 12 6 12 11a6 6 0 0 1-12 0c0-3 2-4 3-7 1 3 2 3 3 3C6 5 5 3 6 0z" fill="{akzent}">'
            '<animate attributeName="opacity" values="1;.55;1" dur="1.6s" repeatCount="indefinite"/></path></g>'
        )
    y = 58
    for name, wert in zeilen:
        teile.append(f'<text x="22" y="{y}" font-size="12.5" fill="{schrift}">{name}</text>')
        teile.append(f'<text x="398" y="{y}" font-size="12.5" font-weight="600" text-anchor="end" fill="{stark}">{wert}</text>')
        y += 26
    teile.append("</svg>")
    open(pfad, "w").write("".join(teile))
    return zeilen


# ---------------------------------------------------------------------------
# Spielereien: Terminal, TNT, Server-Schrank. Alles reines SVG mit CSS-
# Animation, die GitHub im <img> abspielt, ohne Skript und ohne fremden Dienst.
# ---------------------------------------------------------------------------

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

SPRUECHE = [
    "It works on my homelab.",
    "There is no cloud, it's just my basement.",
    "99 little bugs in the code, take one down, patch it around, 117 little bugs in the code.",
    "sudo make me a sandwich",
    "Weeks of coding can save you hours of planning.",
    "It's not a bug, it's an undocumented feature.",
    "DNS: it's always DNS. Even when it isn't, it's DNS.",
    "git commit -m 'final' && git commit -m 'final final'",
    "A homelab is never finished, only temporarily stable.",
    "Backups are a myth until you need one.",
    "I don't always test my code, but when I do, I do it in production.",
    "rm -rf node_modules && npm install: the modern prayer.",
    "Real programmers count from 0.",
    "Ctrl+C, Ctrl+V: the backbone of software engineering.",
    "Have you tried turning the cluster off and on again?",
    "Go: if err != nil { return err } x 1000",
    "Kubernetes: because one container was too easy.",
    "My code doesn't have bugs, it has surprise features.",
    "TNT is just a very fast terraforming tool.",
    "The best error message is the one that never shows up.",
    "First, solve the problem. Then, write the code. Then, rewrite the code.",
    "Uptime is a lifestyle.",
    "Home is where the WiFi connects automatically.",
    "One does not simply exit vim.",
    "Ansible: because typing the same command on twelve hosts gets old.",
    "There are 10 kinds of people: those who understand binary and those who don't.",
    "Commit early, commit often, rebase never.",
    "The fan noise is a feature. It means it's working.",
]


def terminal_karte(pfad, t, heute):
    """Ein kleines Terminal, das sich beim Laden selbst tippt. Der Spruch
    unter `fortune` wechselt jeden Tag."""
    import datetime
    spruch = SPRUECHE[heute.toordinal() % len(SPRUECHE)]
    hell = t is THEMEN["hell"]
    grund = "#f6f8fa" if hell else "#0d1117"
    leiste = "#eaeef2" if hell else "#161b22"
    gruen = "#1a7f37" if hell else "#3fb950"
    zeilen = [
        ("$ ", "whoami", gruen),
        ("", "jonas: homelab builder, Go + React developer, photographer", t["stark"]),
        ("$ ", "uptime", gruen),
        ("", "self-hosted everything, clouds used: 0, coffee: yes", t["stark"]),
        ("$ ", "fortune", gruen),
        ("", spruch, t["akzent"]),
    ]
    breite, hoehe = 860, 70 + 24 * len(zeilen)
    teile = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}" viewBox="0 0 {breite} {hoehe}" role="img" aria-label="Terminal: {spruch}">',
        f"<style>text{{font-family:{MONO};font-size:13.5px}}"
        ".z{clip-path:inset(0 100% 0 0);animation:tipp var(--d) steps(var(--n)) forwards;animation-delay:var(--v)}"
        "@keyframes tipp{to{clip-path:inset(0 0 0 0)}}"
        ".k{animation:blink 1s step-end infinite}@keyframes blink{50%{opacity:0}}</style>",
        f'<rect x=".5" y=".5" width="{breite - 1}" height="{hoehe - 1}" rx="9" fill="{grund}" stroke="{t["linie"]}"/>',
        f'<path d="M.5 30V9.5a9 9 0 0 1 9-9h{breite - 19}a9 9 0 0 1 9 9V30z" fill="{leiste}"/>',
        '<circle cx="20" cy="15" r="5.5" fill="#ff5f57"/><circle cx="38" cy="15" r="5.5" fill="#febc2e"/><circle cx="56" cy="15" r="5.5" fill="#28c840"/>',
        f'<text x="{breite / 2}" y="19.5" text-anchor="middle" fill="{t["schrift"]}" style="font-size:12px">jonas@homelab: ~</text>',
    ]
    v = 0.3
    y = 56
    for vor, text, farbe in zeilen:
        voll = vor + text
        n = len(voll)
        dauer = 0.03 * n if vor else 0.012 * n
        teile.append(
            f'<g class="z" style="--n:{n};--d:{dauer:.2f}s;--v:{v:.2f}s"><text x="20" y="{y}" fill="{farbe}" xml:space="preserve">'
            f'{vor}<tspan fill="{t["stark"] if vor else farbe}">{text.replace("&", "&amp;").replace("<", "&lt;")}</tspan></text></g>'
        )
        v += dauer + (0.35 if vor else 0.5)
        y += 24
    teile.append(f'<text x="20" y="{y}" fill="{gruen}">$ <tspan class="k" fill="{t["stark"]}">█</tspan></text>')
    teile.append("</svg>")
    open(pfad, "w").write("".join(teile))
    return spruch


def tnt_karte(pfad, t):
    """Ein Block TNT mit brennender Lunte: er blinkt, schwillt an, knallt und
    steht danach wieder da. Endlosschleife von vier Sekunden."""
    breite, hoehe = 860, 150
    px = 6  # Pixelgröße des 16er-Blocks
    ox, oy = breite / 2 - 8 * px, 22
    rot, dunkel, weiss = "#d13b2a", "#8f2216", "#f2f2f2"
    teile = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}" viewBox="0 0 {breite} {hoehe}" role="img" aria-label="A TNT block exploding">',
        "<style>"
        ".b{transform-box:fill-box;transform-origin:center;animation:zuend 4s infinite}"
        "@keyframes zuend{0%,100%{transform:scale(1);opacity:1}10%,30%,50%,70%{filter:brightness(1)}"
        "20%,40%,60%,74%{filter:brightness(2.4)}78%{transform:scale(1.18);opacity:1}80%{transform:scale(1.25);opacity:0}"
        "92%{transform:scale(.6);opacity:0}100%{transform:scale(1);opacity:1}}"
        ".f{transform-box:fill-box;transform-origin:center;animation:feuer 4s infinite;opacity:0}"
        "@keyframes feuer{0%,78%{opacity:0;transform:scale(.2)}82%{opacity:1;transform:scale(1)}95%,100%{opacity:0;transform:scale(1.6)}}"
        ".s{animation:funke .25s steps(2) infinite}@keyframes funke{50%{opacity:.2}}"
        f"text{{font-family:{MONO}}}"
        "</style>",
        '<g class="b">',
    ]
    for zeile in range(16):
        for spalte in range(16):
            if 5 <= zeile <= 10:
                farbe = weiss
            else:
                farbe = rot if (spalte + zeile // 2) % 4 else dunkel
            teile.append(f'<rect x="{ox + spalte * px}" y="{oy + zeile * px}" width="{px}" height="{px}" fill="{farbe}"/>')
    teile.append(
        f'<text x="{ox + 8 * px}" y="{oy + 10.2 * px}" text-anchor="middle" font-size="{4.6 * px}" font-weight="700" fill="#222">TNT</text>'
    )
    teile.append(f'<rect x="{ox + 7.5 * px}" y="{oy - 2 * px}" width="{px}" height="{2 * px}" fill="#555"/>')
    teile.append(f'<circle class="s" cx="{ox + 8 * px}" cy="{oy - 2.4 * px}" r="{0.9 * px}" fill="#ffcc33"/>')
    teile.append("</g>")
    # Der Knall: Ringe und Splitter um die Mitte.
    mx, my = ox + 8 * px, oy + 8 * px
    teile.append(f'<g class="f"><circle cx="{mx}" cy="{my}" r="58" fill="#ffd166" opacity=".55"/>'
                 f'<circle cx="{mx}" cy="{my}" r="38" fill="#ff8c42"/><circle cx="{mx}" cy="{my}" r="20" fill="#fff3b0"/>')
    import math
    for i in range(12):
        w = i * math.pi / 6
        teile.append(f'<rect x="{mx + math.cos(w) * 70 - 5:.1f}" y="{my + math.sin(w) * 52 - 5:.1f}" width="10" height="10" '
                     f'fill="{["#d13b2a", "#f2f2f2", "#ff8c42"][i % 3]}"/>')
    teile.append(f'<text x="{mx}" y="{my + 8}" text-anchor="middle" font-size="26" font-weight="700" fill="#7a1d0f">BOOM</text></g>')
    teile.append("</svg>")
    open(pfad, "w").write("".join(teile))


def schrank_karte(pfad, t):
    """Der Server-Schrank: jede Einheit mit blinkenden Lämpchen, jede in
    ihrem eigenen Takt, damit es nach echtem Betrieb aussieht."""
    import random
    zufall = random.Random(4)
    einheiten = [
        ("pve1", "Proxmox node: VMs, LXC, GPUs for local LLMs"),
        ("pve2", "Proxmox node: Docker host, k3s"),
        ("k3s", "Kubernetes: web apps, CI rollouts"),
        ("docker", "~45 containers: monitoring, SSO, my apps"),
        ("pbs", "Proxmox Backup Server, nightly"),
        ("nas", "Synology, RAID 5: files, media, backups"),
    ]
    hell = t is THEMEN["hell"]
    gehaeuse = "#d0d7de" if hell else "#30363d"
    einschub = "#f6f8fa" if hell else "#161b22"
    breite, h = 860, 30
    hoehe = 46 + h * len(einheiten) + 16
    teile = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}" viewBox="0 0 {breite} {hoehe}" role="img" aria-label="Homelab rack with blinking lights">',
        f"<style>text{{font-family:{MONO};font-size:12.5px}}.l{{animation:an var(--t) steps(1) infinite;animation-delay:var(--v)}}"
        "@keyframes an{50%{opacity:.15}}</style>",
        f'<text x="22" y="28" font-size="14" font-weight="600" fill="{t["akzent"]}" style="font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif">The homelab where all of this runs</text>',
        f'<rect x="14" y="40" width="{breite - 28}" height="{h * len(einheiten) + 12}" rx="6" fill="{gehaeuse}"/>',
    ]
    for i, (name, was) in enumerate(einheiten):
        y = 46 + i * h
        teile.append(f'<rect x="24" y="{y}" width="{breite - 48}" height="{h - 4}" rx="3" fill="{einschub}"/>')
        for s in range(3):
            teile.append(f'<circle cx="{40 + s * 6}" cy="{y + 13}" r="1.6" fill="{t["linie"]}"/>')
        teile.append(f'<text x="70" y="{y + 17.5}" font-weight="700" fill="{t["stark"]}">{name}</text>')
        teile.append(f'<text x="150" y="{y + 17.5}" fill="{t["schrift"]}">{was}</text>')
        for j in range(5):
            farbe = "#3fb950" if j < 3 else ("#f97316" if j == 3 else "#58a6ff")
            dauer = zufall.uniform(0.3, 1.9)
            teile.append(
                f'<rect class="l" style="--t:{dauer:.2f}s;--v:-{zufall.uniform(0, 2):.2f}s" x="{breite - 130 + j * 18}" y="{y + 9}" '
                f'width="9" height="8" rx="1.5" fill="{farbe}"/>'
            )
    teile.append("</svg>")
    open(pfad, "w").write("".join(teile))


if __name__ == "__main__":
    daten = graphql(ABFRAGE, {"login": BENUTZER})["user"]
    for name, t in THEMEN.items():
        zeilen = statistik_karte(daten, f"karten/statistik-{name}.svg", t)
        sprachen = sprachen_karte(daten, f"karten/sprachen-{name}.svg", t)
        serien = serien_karte(daten, f"karten/serien-{name}.svg", t)
        spruch = terminal_karte(f"karten/terminal-{name}.svg", t, datetime.date.today())
        tnt_karte(f"karten/tnt-{name}.svg", t)
        schrank_karte(f"karten/schrank-{name}.svg", t)
    print("Statistik:", ", ".join(f"{n} {w}" for n, w in zeilen))
    print("Sprachen:", ", ".join(n for n, _ in sprachen))
    print("Spruch:", spruch)
    print("Serien:", ", ".join(f"{n} {w}" for n, w in serien))
