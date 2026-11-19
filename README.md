<h1 align="center">Dschonas04</h1>

<p align="center">
  Software developer building self-hosted products for teams.<br>
  Go backends, React and TypeScript frontends, PostgreSQL, shipped as containers.
</p>

<p align="center">
  <img alt="Go" src="https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white">
  <img alt="React" src="https://img.shields.io/badge/React-087EA4?style=flat-square&logo=react&logoColor=white">
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white">
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white">
  <img alt="Kubernetes" src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white">
  <img alt="Kotlin" src="https://img.shields.io/badge/Kotlin-7F52FF?style=flat-square&logo=kotlin&logoColor=white">
  <img alt="Flutter" src="https://img.shields.io/badge/Flutter-02569B?style=flat-square&logo=flutter&logoColor=white">
</p>

---

## Products

Self-hosted, each one a Go backend with PostgreSQL or SQLite, sign-in through
Keycloak (OIDC), shipped as containers for amd64 and arm64.

<table>
  <tr>
    <td width="33%" valign="top">
      <h3><a href="https://github.com/Dschonas04/Nexora">Nexora</a></h3>
      <p><img alt="Release" src="https://img.shields.io/github/v/release/Dschonas04/Nexora?style=flat-square&color=c2410c"></p>
      <p>A wiki with nested pages, backlinks and a knowledge graph. Full text
      search, versions, comments, live co-editing, attachments in S3, an MCP
      server for AI assistants, desktop and Android apps that work offline.</p>
      <p><a href="https://dschonas04.github.io/Nexora/">Project page</a> · <a href="https://nexora.jonasgroll.de">Live demo</a></p>
      <p><sub>Go · React · PostgreSQL</sub></p>
    </td>
    <td width="33%" valign="top">
      <h3><a href="https://github.com/Dschonas04/foodr">Foodr</a></h3>
      <p><img alt="Release" src="https://img.shields.io/github/v/release/Dschonas04/foodr?style=flat-square&color=15803d"></p>
      <p>Meal planner with a food database (BLS 4.0 and Open Food Facts,
      3.4 million products). A local language model picks the week from
      900+ recipes, Foodr adds up shopping list and nutrition; a kitchen view
      and chat for Home Assistant.</p>
      <p><sub>Go · PostgreSQL · Ollama</sub></p>
    </td>
    <td width="33%" valign="top">
      <h3><a href="https://github.com/Dschonas04/captr">Captr</a></h3>
      <p><img alt="Release" src="https://img.shields.io/github/v/release/Dschonas04/captr?style=flat-square&color=7c3aed"></p>
      <p>Photo editing in the browser, in the spirit of Lightroom: RAW, JPEG
      and HEIC, a WebGL2 develop pipeline, masks, a canvas for compositions
      and background removal.</p>
      <p><sub>Go · React · WebGL2 · rembg</sub></p>
    </td>
  </tr>
  <tr>
    <td width="33%" valign="top">
      <h3><a href="https://github.com/Dschonas04/photr">Photr</a></h3>
      <p>Collections of pictures: arrange, design and share them, with share
      links and permissions.</p>
      <p><sub>Go · React</sub></p>
    </td>
    <td width="33%" valign="top">
      <h3><a href="https://github.com/Dschonas04/blankr">Blankr</a></h3>
      <p>A collaborative whiteboard. Live cursors over WebSocket, boards that
      persist, and two share links per board: one to draw, one to watch.</p>
      <p><sub>Go · React</sub></p>
    </td>
    <td width="33%" valign="top">
      <h3><a href="https://github.com/Dschonas04/planr">Planr</a></h3>
      <p>Floor plans and whole houses to scale: storeys, wall build-ups with
      U-values, stairs, roofs, living area, a 3D view, export as DXF, SVG, PNG
      or PDF. Also as a Mac app.</p>
      <p><sub>Go · React · three.js</sub></p>
    </td>
  </tr>
</table>

### In the works

Six more, running in my homelab and not yet public:

| | |
| --- | --- |
| **Ticketr** | Ticket system: queues, priorities with deadlines, internal notes, replies by mail |
| **Pagr** | Content management for websites: Markdown pages and posts, versions, media, sitemap |
| **Meetr** | Video meetings in the browser over WebRTC: rooms by link, waiting room, screen sharing |
| **Forgr** | Git hosting: push and clone over HTTPS with tokens, code browser, diffs, issues |
| **Boardr** | Start page for a homelab: services as tiles with live status checks |
| **Trailr** | Records what users do on Linux machines (SSH, sudo, commands) in a tamper-evident hash chain |

---

## Workshops

Hands-on workshops in German, all in one repository:
[workshop](https://github.com/Dschonas04/workshop). Each workshop is a folder
you work through level by level, with automated tests that confirm when a
level is complete. Texts under CC BY-SA 4.0, code under MIT; CI verifies every
model solution on each change.

| Workshop | Levels | How it is checked |
| --- | --- | --- |
| [Go](https://github.com/Dschonas04/workshop/tree/main/go) | 4 | `go test -race` |
| [React](https://github.com/Dschonas04/workshop/tree/main/react) | 4 | Vitest and the TypeScript compiler |
| [Container](https://github.com/Dschonas04/workshop/tree/main/container) | 5 | Docker, Compose and Podman, a probe per level |
| [Ansible](https://github.com/Dschonas04/workshop/tree/main/ansible) | 4 | Playbooks against your own machine |
| [Terraform / OpenTofu](https://github.com/Dschonas04/workshop/tree/main/terraform) | 4 | Local providers only, no cloud account |
| [Shell](https://github.com/Dschonas04/workshop/tree/main/shell) | 5 | A probe script per level |
| [PowerShell](https://github.com/Dschonas04/workshop/tree/main/powershell) | 8 | Runs your script with input and parameters, starting from zero |


---

## Other projects

| Project | What it is |
| --- | --- |
| [Sendr](https://github.com/Dschonas04/sendr) | Send files to another computer on the same network: no cloud, resume by byte, pinned TLS. One binary for Windows, macOS and Linux. |
| [Managr](https://github.com/Dschonas04/managr) | Running a Minecraft server on Fabric 26.2: loot scaling, quiet mode, donations board and more in one mod. |
| [Fishr](https://github.com/Dschonas04/fishr) | A Fabric mod for fishing with a real fight, 64 kinds of fish, baits and a fish board. |
| [TNT Arsenal](https://github.com/Dschonas04/TNT-Arsenal) | Sixty-four kinds of TNT for Minecraft 26.2, each with hand-drawn textures, from drill and bridge to a nuke with fallout. |

---

## Numbers

<p align="center">
  <img alt="Statistics" src="karten/statistik-hell.svg#gh-light-mode-only">
  <img alt="Streaks" src="karten/serien-hell.svg#gh-light-mode-only">
  <img alt="Statistics" src="karten/statistik-dunkel.svg#gh-dark-mode-only">
  <img alt="Streaks" src="karten/serien-dunkel.svg#gh-dark-mode-only">
</p>

<p align="center">
  <img alt="Languages" src="karten/sprachen-hell.svg#gh-light-mode-only">
  <img alt="Languages" src="karten/sprachen-dunkel.svg#gh-dark-mode-only">
</p>

<p align="center">
  <img alt="A snake eating the contribution graph" src="karten/schlange-hell.svg#gh-light-mode-only">
  <img alt="A snake eating the contribution graph" src="karten/schlange-dunkel.svg#gh-dark-mode-only">
</p>

<p align="center">
  <sub>
    Generated nightly by <a href="karten.py">karten.py</a> in this repository.
    Commits and streaks include private contributions;
    repositories and languages cover public work only.
  </sub>
</p>

---

<p align="center">
  <sub>
    Licensing: Nexora is open core under the AGPL with a few paid extras;
    the other products are under their own licences, see each repository.
  </sub>
</p>
