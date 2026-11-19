#!/usr/bin/env python3
"""Zeichnet die Karten für das Profil-README: Statistik, Sprachen und Serien.

Warum selbst und nicht github-readme-stats: der öffentliche Dienst dort
antwortet regelmäßig mit 503, und dann steht im Profil ein kaputtes Bild.
Hier läuft die Abfrage im eigenen Arbeitsablauf, das Ergebnis liegt als SVG im
Repository, und es kann nichts ausfallen, was nicht mir gehört.

Jede Karte entsteht zweimal, hell und dunkel: ein SVG im <img> bekommt die
Themenumschaltung von GitHub nicht mit, und eine Fassung, die auf beiden
Untergründen gerade noch geht, ist auf keinem gut. Das README wählt per
#gh-light-mode-only bzw. #gh-dark-mode-only aus.
"""
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
    hoehe = 46 + len(zeilen) * 26 + 14
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
    hoehe = 46 + len(zeilen) * 26 + 14
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


if __name__ == "__main__":
    daten = graphql(ABFRAGE, {"login": BENUTZER})["user"]
    for name, t in THEMEN.items():
        zeilen = statistik_karte(daten, f"karten/statistik-{name}.svg", t)
        sprachen = sprachen_karte(daten, f"karten/sprachen-{name}.svg", t)
        serien = serien_karte(daten, f"karten/serien-{name}.svg", t)
    print("Statistik:", ", ".join(f"{n} {w}" for n, w in zeilen))
    print("Sprachen:", ", ".join(n for n, _ in sprachen))
    print("Serien:", ", ".join(f"{n} {w}" for n, w in serien))
