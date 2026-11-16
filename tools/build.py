#!/usr/bin/env python3
"""Build the public Intent Garden ecosystem website, with no external packages."""
import argparse
import hashlib
from html import escape
import json
from pathlib import Path
import shutil
from string import Template

ROOT = Path(__file__).resolve().parents[1]
COPY = {
    'ru': {
        'title': 'Intent Garden — экосистема проектов',
        'description': 'Decima, DragonFly, Liza, WUI и VideoGrace: вычисления, язык, интерфейсы и связь. Карта проектов Intent Garden / Rulerom.',
        'skip': 'К содержимому', 'navigation': 'Навигация', 'projects_label': 'Проекты',
        'headline': 'Идеи становятся<br><em>инструментами.</em>',
        'intro': 'Вычисления, язык, интерфейсы и связь. Пять проектов, которые развиваются рядом и помогают проверять друг друга.',
        'map_label': 'Интерактивная карта экосистемы', 'use_label': 'Применение', 'ideas_label': 'Идеи и эксперименты',
        'map_hint': 'Выберите проект на карте',
        'inspector_note': 'Связи имеют разный смысл: общее ядро, инструменты, развитие контрактов или прикладной эксперимент.',
        'projects_eyebrow': '01 / НАПРАВЛЕНИЯ', 'projects_heading': 'У каждого — своя задача.',
        'projects_intro': 'Исследовательский стенд, язык, библиотека и продукт находятся на разных этапах. Здесь — что уже работает и куда ведёт каждый проект.',
        'connections_eyebrow': '02 / СВЯЗИ', 'connections_heading': 'Задачи переходят<br>из проекта в проект.',
        'connections_intro': 'Исследование ставит новые вопросы. Инструмент позволяет поставить опыт. Реальное приложение показывает, что стоит улучшить.',
        'contact_eyebrow': 'ПРОДОЛЖИМ РАЗГОВОР', 'contact_heading': 'Есть задача или идея?',
        'contact_copy': 'Для вопросов об исследованиях, инструментах или совместной работе — напишите нам.',
        'footer_note': 'Открытый код и условия использования — в каждом проекте отдельно.',
        'site': 'Сайт проекта', 'docs': 'Документация', 'code': 'Исходники',
        'research_link': 'Обсудить исследование',
    },
    'en': {
        'title': 'Intent Garden — a connected ecosystem',
        'description': 'Decima, DragonFly, Liza, WUI and VideoGrace: computation, language, interfaces and communication. The Intent Garden / Rulerom project map.',
        'skip': 'Skip to content', 'navigation': 'Navigation', 'projects_label': 'Projects',
        'headline': 'Ideas grow<br><em>into tools.</em>',
        'intro': 'Computation, language, interfaces and communication. Five connected projects, each helping test and develop the others.',
        'map_label': 'Interactive ecosystem map', 'use_label': 'Application', 'ideas_label': 'Ideas and experiments',
        'map_hint': 'Choose a project on the map',
        'inspector_note': 'Each connection has its own meaning: a shared core, tooling, evolving contracts or a practical experiment.',
        'projects_eyebrow': '01 / DIRECTIONS', 'projects_heading': 'A purpose for every project.',
        'projects_intro': 'A research bench, a language, a library and a product are at different stages. Here is what each does and where it is going.',
        'connections_eyebrow': '02 / CONNECTIONS', 'connections_heading': 'Real problems travel<br>between projects.',
        'connections_intro': 'Research raises questions. Tools make experiments possible. Working applications reveal what needs to improve.',
        'contact_eyebrow': 'KEEP THE CONVERSATION GOING', 'contact_heading': 'A problem or an idea?',
        'contact_copy': 'For research, tools or collaboration, get in touch.',
        'footer_note': 'Source availability and terms of use are defined by each project.',
        'site': 'Project website', 'docs': 'Documentation', 'code': 'Source code',
        'research_link': 'Discuss the research',
    },
}
CONNECTION_STORIES = {
    'ru': [
        ('Decima', 'DragonFly', 'Ядро получает конкретную задачу: зрительный поток, две независимые машины и измеримый отклик на движущуюся цель.'),
        ('Liza', 'VideoGrace', 'Сервисный API CAN даёт языку реальный сетевой сценарий. Сейчас это экспериментальный worker и проверка контрактов.'),
        ('WUI', 'VideoGrace', 'Нативный клиент использует общую UI-библиотеку. Найденные в приложении проблемы возвращаются исправлениями в WUI.'),
    ],
    'en': [
        ('Decima', 'DragonFly', 'The core meets a concrete problem: visual input, two independent machines and a measurable response to moving targets.'),
        ('Liza', 'VideoGrace', 'The CAN service API provides a real networking scenario. Today this is an experimental worker and a way to test contracts.'),
        ('WUI', 'VideoGrace', 'The native client uses the shared UI library. Problems found in the application become fixes in WUI.'),
    ],
}
POSITIONS = {
    'decima': (230, 140, 132, 60), 'dragonfly': (675, 130, 144, 63),
    'liza': (235, 355, 128, 62), 'wui': (675, 355, 118, 62),
    'videograce': (450, 565, 177, 66),
}
PATHS = [
    'M365 139 C420 145 469 118 528 126',
    'M230 201 C218 230 220 272 234 292',
    'M332 182 C412 220 513 264 585 313',
    'M263 414 C287 461 316 500 354 513',
    'M646 416 C620 462 588 496 550 513',
]


def links(project, language):
    labels = COPY[language]
    result = ''.join(f'<a href="{escape(item["url"], quote=True)}">{labels[item["label"]]} ↗</a>'
                     for item in project['links'])
    if not result:
        result = f'<a href="mailto:intent@rulerom.com">{labels["research_link"]} ↗</a>'
    return f'<div class="project-links">{result}</div>'


def project_panel(project, language):
    text = project[language]
    return (f'<div style="--project-color:{project["color"]}">'
            f'<div class="project-kicker"><i aria-hidden="true"></i>{escape(text["role"])}</div>'
            f'<h2 id="selected-title">{escape(project["name"])}</h2>'
            f'<p class="project-description">{escape(text["description"])}</p>'
            f'<p class="project-connection">{escape(text["connection"])}</p>'
            f'<span class="project-status">{escape(text["status"])}</span>{links(project, language)}</div>')


def diagram(data, language):
    projects = {p['id']: p for p in data['projects']}
    edges = []
    for edge, route in zip(data['connections'], PATHS, strict=True):
        color = projects[edge['to']]['color']
        edges.append(f'<path class="map-edge {edge["kind"]}" data-from="{edge["from"]}" data-to="{edge["to"]}" '
                     f'd="{route}" style="--edge-color:{color}" marker-end="url(#arrow-{edge["to"]})">'
                     f'<title>{escape(edge[language])}</title></path>')
    markers = ''.join(f'<marker id="arrow-{p["id"]}" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="userSpaceOnUse">'
                      f'<path d="M1 1 L8 5 L1 9" fill="none" stroke="{p["color"]}" stroke-width="1.4"/></marker>' for p in data['projects'])
    nodes = []
    for project in data['projects']:
        pid = project['id']
        x, y, rx, ry = POSITIONS[pid]
        # Slightly asymmetric paths echo the original notebook drawing.
        shape = (f'M{-rx} 0 C{-rx - 8} {-ry * .65} {-rx * .45} {-ry - 8} 0 {-ry} '
                 f'C{rx * .65} {-ry - 5} {rx + 9} {-ry * .45} {rx} 0 '
                 f'C{rx + 3} {ry * .7} {rx * .35} {ry + 6} 0 {ry} '
                 f'C{-rx * .7} {ry + 4} {-rx - 5} {ry * .4} {-rx} 0Z')
        text = project[language]
        label = f'{project["name"]}: {text["role"]}'
        nodes.append(f'<a class="node" href="#project-{pid}" data-project="{pid}" role="button" tabindex="0" '
                     f'aria-label="{escape(label, quote=True)}" aria-current="{str(pid == "decima").lower()}" '
                     f'transform="translate({x} {y})" style="--project-color:{project["color"]};--node-fill:{project["color"]}09">'
                     f'<ellipse class="node-halo" rx="{rx + 17}" ry="{ry + 16}"/>'
                     f'<path class="node-echo" d="{shape}" transform="rotate(-3) scale(1.035)"/>'
                     f'<path class="node-shape" d="{shape}"/>'
                     f'<text class="node-name" text-anchor="middle" y="-1">{escape(project["label"])}</text>'
                     f'<text class="node-role" text-anchor="middle" y="24">{escape(text["role"])}</text></a>')
    description = ('Decima связана с DragonFly, Liza и WUI; Liza и WUI связаны с VideoGrace.' if language == 'ru' else
                   'Decima connects to DragonFly, Liza and WUI; Liza and WUI connect to VideoGrace.')
    return (f'<svg viewBox="0 0 900 650" role="group" aria-labelledby="map-title map-description" xmlns="http://www.w3.org/2000/svg">'
            f'<title id="map-title">{COPY[language]["map_label"]}</title><desc id="map-description">{description}</desc>'
            f'<defs>{markers}</defs>{"".join(edges)}{"".join(nodes)}</svg>')


def build(destination):
    if destination == ROOT or ROOT.is_relative_to(destination) or destination.is_relative_to(ROOT / 'src'):
        raise ValueError('Choose an output directory outside the sources')
    data = json.loads((ROOT / 'content/ecosystem.json').read_text())
    ids = [p['id'] for p in data['projects']]
    if len(set(ids)) != len(ids) or len(ids) != 5:
        raise ValueError('Expected five unique ecosystem projects')
    if len(data['connections']) != len(PATHS):
        raise ValueError('Diagram connections and geometry must agree')
    for edge in data['connections']:
        if edge['from'] not in ids or edge['to'] not in ids:
            raise ValueError('Unknown connection endpoint')
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / 'src/assets', destination / 'assets', dirs_exist_ok=True)
    versions = {kind: hashlib.sha256((ROOT / f'src/assets/site.{kind}').read_bytes()).hexdigest()[:12] for kind in ['css', 'js']}
    template = Template((ROOT / 'src/page.html').read_text())
    for language in COPY:
        values = dict(COPY[language], lang=language, css_version=versions['css'], js_version=versions['js'])
        values.update(ru_current='aria-current="page"' if language == 'ru' else '',
                      en_current='aria-current="page"' if language == 'en' else '',
                      initial_project=project_panel(data['projects'][0], language), diagram=diagram(data, language))
        cards = []
        for index, project in enumerate(data['projects'], 1):
            text = project[language]
            cards.append(f'<article class="project-card" id="project-{project["id"]}" style="--project-color:{project["color"]}">'
                         f'<span class="project-number">0{index} / {escape(text["role"])}</span><h3>{escape(project["name"])}</h3>'
                         f'<p>{escape(text["description"])}</p><span class="project-status">{escape(text["status"])}</span>'
                         f'{links(project, language)}</article>')
        values['project_cards'] = ''.join(cards)
        values['connections'] = ''.join(f'<article class="connection"><div class="connection-route"><span>{a}</span><b aria-hidden="true">→</b><span>{b}</span></div><p>{escape(text)}</p></article>'
                                        for a, b, text in CONNECTION_STORIES[language])
        values['project_data'] = json.dumps({p['id']: {'html': project_panel(p, language)} for p in data['projects']}, ensure_ascii=False).replace('<', '\\u003c')
        page = destination / language / 'index.html'
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(template.substitute(values))
    (destination / 'index.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Intent Garden</title><link rel="icon" href="/assets/mark.svg"><script>location.replace((navigator.language||'en').toLowerCase().startsWith('ru')?'/ru/':'/en/');</script></head><body><h1>Intent Garden</h1><p><a href="/ru/">Русский</a> · <a href="/en/">English</a></p></body></html>''')
    for alias, target in [('main', 'en'), ('main_ru', 'ru'), ('main_zh', 'en')]:
        page = destination / alias / 'index.html'
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(f'<!doctype html><html><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=/{target}/"><title>Intent Garden</title></head><body><a href="/{target}/">Intent Garden</a></body></html>')
    (destination / 'CNAME').write_text('intent-garden.org\n')
    (destination / '.nojekyll').touch()
    (destination / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://intent-garden.org/sitemap.xml\n')
    (destination / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://intent-garden.org/ru/</loc></url><url><loc>https://intent-garden.org/en/</loc></url></urlset>')
    summary = ['# Intent Garden ecosystem', '', 'Intent Garden / Rulerom connects computation, language, interfaces and communication.', '']
    summary += [f'- {p["name"]}: {p["en"]["description"]} Status: {p["en"]["status"]}.' for p in data['projects']]
    summary += ['', 'Relationships distinguish real application from ideas and experiments.', 'Project licenses and source availability are defined individually.']
    (destination / 'llms.txt').write_text('\n'.join(summary) + '\n')
    print(f'Built Intent Garden EN/RU: {len(ids)} projects, {len(data["connections"])} connections → {destination}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / '_site')
    build(parser.parse_args().output.resolve())
