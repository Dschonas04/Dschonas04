<h1 align="center">Dschonas04</h1>

<p align="center">
  I build self-hosted tools, and the homelab they run in.<br>
  Go on the inside, React on the outside, PostgreSQL underneath.
</p>

<p align="center">
  <img alt="Go" src="https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white">
  <img alt="React" src="https://img.shields.io/badge/React-087EA4?style=flat-square&logo=react&logoColor=white">
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white">
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white">
  <img alt="Kubernetes" src="https://img.shields.io/badge/k3s-FFC61C?style=flat-square&logo=k3s&logoColor=black">
  <img alt="Ansible" src="https://img.shields.io/badge/Ansible-EE0000?style=flat-square&logo=ansible&logoColor=white">
  <img alt="Proxmox" src="https://img.shields.io/badge/Proxmox-E57000?style=flat-square&logo=proxmox&logoColor=white">
  <img alt="Kotlin" src="https://img.shields.io/badge/Kotlin-7F52FF?style=flat-square&logo=kotlin&logoColor=white">
</p>

---

## Products

Three finished things, each self-hosted, each with accounts, sharing and a
privacy page — not demos.

<table>
  <tr>
    <td width="33%" valign="top">
      <h3><a href="https://github.com/Dschonas04/Nexora">Nexora</a></h3>
      <p>
        <img alt="Stars" src="https://img.shields.io/github/stars/Dschonas04/Nexora?style=flat-square&color=c2410c">
        <img alt="Release" src="https://img.shields.io/github/v/release/Dschonas04/Nexora?style=flat-square&color=c2410c">
      </p>
      <p>A wiki with nested pages, backlinks and a knowledge graph. Full text
      search, versions, comments, attachments in S3, import from Obsidian,
      Notion and Confluence.</p>
      <p>
        <a href="https://dschonas04.github.io/Nexora/">Project page</a> ·
        <a href="https://nexora.jonasgroll.de">Live demo</a>
      </p>
      <p><sub>Go · React · PostgreSQL · two containers plus a database</sub></p>
    </td>
    <td width="33%" valign="top">
      <h3><a href="https://github.com/Dschonas04/Blankr">Blankr</a></h3>
      <p>
        <img alt="Stars" src="https://img.shields.io/github/stars/Dschonas04/Blankr?style=flat-square&color=2383e2">
        <img alt="Release" src="https://img.shields.io/github/v/release/Dschonas04/Blankr?style=flat-square&color=2383e2">
      </p>
      <p>A collaborative whiteboard. Live cursors over WebSocket, boards that
      persist, and two share links per board — one to draw, one to watch.</p>
      <p><sub>Go · React · CRDT-style last-write-wins merge</sub></p>
    </td>
    <td width="33%" valign="top">
      <h3><a href="https://github.com/Dschonas04/Planr">Planr</a></h3>
      <p>
        <img alt="Stars" src="https://img.shields.io/github/stars/Dschonas04/Planr?style=flat-square&color=b45309">
        <img alt="Release" src="https://img.shields.io/github/v/release/Dschonas04/Planr?style=flat-square&color=b45309">
      </p>
      <p>A floor plan editor to scale: walls, doors, windows, furniture, room
      areas, a 3D view, and export as DXF, SVG, PNG or a shareable file.</p>
      <p><sub>Go · React · three.js · server-side export</sub></p>
    </td>
  </tr>
</table>

---

## The homelab

Everything above runs at home, on hardware I can touch. Managed by Ansible
from one control node, backed up nightly to a Proxmox Backup Server.

<p>
  <img alt="Proxmox" src="https://img.shields.io/badge/Hypervisors-2%20%C3%97%20Proxmox-E57000?style=flat-square">
  <img alt="Guests" src="https://img.shields.io/badge/Guests-9%20VMs%20%2B%20LXC-informational?style=flat-square">
  <img alt="Containers" src="https://img.shields.io/badge/Containers-40%2B-2496ED?style=flat-square">
  <img alt="k3s" src="https://img.shields.io/badge/Kubernetes-k3s-FFC61C?style=flat-square">
  <img alt="Ansible" src="https://img.shields.io/badge/Roles-33-EE0000?style=flat-square">
  <img alt="Monitoring" src="https://img.shields.io/badge/Monitoring-Prometheus%20%2B%20Grafana-E6522C?style=flat-square">
  <img alt="SIEM" src="https://img.shields.io/badge/SIEM-Wazuh-005C99?style=flat-square">
  <img alt="SSO" src="https://img.shields.io/badge/SSO-Keycloak-4D4D4D?style=flat-square">
</p>

| Layer | What runs there |
| --- | --- |
| Virtualisation | Two Proxmox hosts, nine guests, GPU passthrough for a local LLM |
| Kubernetes | k3s, carrying the public web services |
| Identity | Keycloak as the single sign-on for every web interface |
| Observability | Prometheus, Grafana, Loki, Alertmanager — and Wazuh for the security side |
| Automation | Ansible, 33 roles, plus self-hosted GitHub runners that build and roll out |
| Backup | Proxmox Backup Server, nightly, plus database dumps to a NAS |

---

## Courses I wrote while learning

Each one is a repository you clone and work through in levels, with tests that
tell you whether the level is done. No slides, no video.

| Course | Levels | How it is checked |
| --- | --- | --- |
| [Go](https://github.com/Dschonas04/Go-Kurs) | 4 | `go test -race` |
| [React](https://github.com/Dschonas04/React-Kurs) | 4 | Vitest and the TypeScript compiler |
| [Container](https://github.com/Dschonas04/Container-Kurs) | 5 | Docker, Compose and Podman, a probe per level |
| [Ansible](https://github.com/Dschonas04/Ansible-Kurs) | 4 | Playbooks against your own machine |
| [Terraform / OpenTofu](https://github.com/Dschonas04/Terraform-Kurs) | 4 | Local providers only, no cloud account |
| [Shell](https://github.com/Dschonas04/Shell-Kurs) | 5 | A probe script per level |
| [PowerShell](https://github.com/Dschonas04/Powershell-Kurs) | 9 | Fill-in tasks, starting from zero |

The material is German — the products are the English part of this profile.

---

## Numbers

<p align="center">
  <img alt="Statistics" src="karten/statistik-hell.svg#gh-light-mode-only">
  <img alt="Languages" src="karten/sprachen-hell.svg#gh-light-mode-only">
  <img alt="Statistics" src="karten/statistik-dunkel.svg#gh-dark-mode-only">
  <img alt="Languages" src="karten/sprachen-dunkel.svg#gh-dark-mode-only">
</p>

<p align="center">
  <sub>
    Both cards are drawn by <a href="karten.py">karten.py</a> in this
    repository and redrawn nightly by a workflow — the usual service for this
    answers 503 often enough that a broken image would be the normal state.
    Private contributions are counted in the commit figure; the repository
    count and the languages are the public ones. Most of my work sits in
    private repositories, so these numbers say less than they look like.
  </sub>
</p>

---

<p align="center">
  <sub>
    Licence note: Nexora, Blankr and Planr are under the Business Source
    License 1.1 — run them yourself, commercially, for free; a handful of
    extras need a key, and each turns into Apache 2.0 on its date.
  </sub>
</p>
