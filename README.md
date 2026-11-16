# Intent Garden website

The public ecosystem map for Intent Garden / Rulerom: Decima‑8, DragonFly,
Liza, WUI and VideoGrace. Russian and English pages share one project dataset.

## Build and preview

Python 3.10 or newer; no third-party packages:

```sh
python3 tools/build.py
python3 -m http.server 8080 --directory _site
```

Open `/ru/` or `/en/`. The root chooses the browser language and offers both links
without JavaScript. `/main/` and `/main_ru/` redirect old bookmarks to the new pages.

- `content/ecosystem.json`: project roles, statuses, links and connections.
- `src/page.html`: the page template.
- `src/assets/`: styles, map interaction and SVG mark.
- `tools/build.py`: the static builder and source of the map geometry.

The map follows the ecosystem sketch. Solid lines represent application/tooling;
dashed lines represent ideas and experiments. They are not a complete dependency
specification. Every project remains readable without JavaScript.

## Publish

GitHub Pages builds and publishes on pushes to `main`; pull requests build without
deploying. A manual run is available in Actions. Custom domain: `intent-garden.org`.

DNS: four A records at `@`, `185.199.108.153`, `185.199.109.153`,
`185.199.110.153`, `185.199.111.153`; `www` is a CNAME to
`intent-garden.github.io`. Enable Enforce HTTPS once GitHub's certificate is ready.

This clean repository contains the new public static website only. The earlier
website and PHP ticket/payment API remain in a separate private repository.
Do not copy its configs, credentials or Git history here. This deployment has no
server-side API or ticket issuance. Licensing of each ecosystem project is separate.

## Analytics

Russian and English pages share Yandex.Metrika counter `106900676` in
`src/page.html`. The tag loads asynchronously; a no-JavaScript pixel is included.
