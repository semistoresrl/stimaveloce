# -*- coding: utf-8 -*-
"""Illustrazioni originali (SVG) in stile flat: auto, moto, casa, perito. Colori del brand."""
OR, BL, NV, BG, SK = "#FF7A1A", "#1F5EFF", "#0B1B3A", "#EEF3FF", "#F2C6A0"


def car(x=0, y=0, s=1, c=BL):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M8 58 Q8 40 26 38 L52 22 Q60 17 72 17 L118 17 Q130 17 138 25 L156 40 Q176 42 178 58 L178 66 Q178 72 172 72 L14 72 Q8 72 8 66Z" fill="{c}"/>'
            '<path d="M58 26 L72 22 L104 22 L104 40 L48 40Z" fill="#DDE7FF"/><path d="M112 22 L130 22 Q136 22 140 27 L151 40 L112 40Z" fill="#DDE7FF"/>'
            f'<rect x="164" y="50" width="12" height="7" rx="3" fill="{OR}"/><rect x="10" y="50" width="10" height="6" rx="3" fill="#FFE2CC"/>'
            f'<circle cx="50" cy="72" r="16" fill="{NV}"/><circle cx="50" cy="72" r="7" fill="#C9D3EA"/>'
            f'<circle cx="140" cy="72" r="16" fill="{NV}"/><circle cx="140" cy="72" r="7" fill="#C9D3EA"/></g>')


def moto(x=0, y=0, s=1, c=OR):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<circle cx="26" cy="62" r="20" fill="none" stroke="{NV}" stroke-width="7"/><circle cx="124" cy="62" r="20" fill="none" stroke="{NV}" stroke-width="7"/>'
            f'<path d="M26 62 L58 36 L96 36 L124 62" fill="none" stroke="{NV}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M50 34 Q60 18 84 20 L102 26 Q108 34 98 40 L62 44 Q50 44 50 34Z" fill="{c}"/>'
            f'<path d="M104 30 L118 14 L128 16" fill="none" stroke="{NV}" stroke-width="5" stroke-linecap="round"/>'
            '<rect x="56" y="28" width="26" height="6" rx="3" fill="#FFE2CC"/></g>')


def house(x=0, y=0, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M10 70 L90 12 L170 70 Z" fill="{OR}"/><rect x="26" y="66" width="128" height="88" rx="6" fill="#fff" stroke="#DDE3F0" stroke-width="3"/>'
            f'<rect x="76" y="104" width="30" height="50" rx="4" fill="{BL}"/><rect x="38" y="84" width="28" height="26" rx="4" fill="#DDE7FF"/><rect x="116" y="84" width="28" height="26" rx="4" fill="#DDE7FF"/>'
            '<path d="M120 20 L120 40 L136 50 L136 20Z" fill="#E3E7F0"/>'
            '<path d="M50 70 q4 10 0 18 q-4 8 0 14" fill="none" stroke="#7FA2FF" stroke-width="4" stroke-linecap="round" opacity=".9"/>'
            '<circle cx="50" cy="108" r="4" fill="#7FA2FF"/></g>')


def perito(x=0, y=0, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="22" y="70" width="56" height="70" rx="22" fill="{BL}"/><rect x="30" y="134" width="16" height="44" rx="7" fill="{NV}"/><rect x="54" y="134" width="16" height="44" rx="7" fill="{NV}"/>'
            f'<circle cx="50" cy="44" r="22" fill="{SK}"/><path d="M28 42 Q30 18 52 18 Q74 18 74 40 Q64 30 48 32 Q36 32 28 42Z" fill="{NV}"/>'
            '<circle cx="43" cy="46" r="2.6" fill="#0B1B3A"/><circle cx="58" cy="46" r="2.6" fill="#0B1B3A"/><path d="M44 56 Q51 61 58 56" fill="none" stroke="#0B1B3A" stroke-width="2.4" stroke-linecap="round"/>'
            f'<rect x="64" y="84" width="40" height="52" rx="6" fill="#fff" stroke="#DDE3F0" stroke-width="3"/><rect x="74" y="78" width="20" height="10" rx="4" fill="{OR}"/>'
            '<path d="M72 100 h24 M72 110 h24 M72 120 h16" stroke="#C9D3EA" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M74 122 l5 5 l10 -12" fill="none" stroke="{OR}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M30 92 Q46 112 66 104" fill="none" stroke="{BL}" stroke-width="12" stroke-linecap="round"/></g>')


def hero_scene():
    return ('<svg class="ill" viewBox="0 0 560 420" role="img" aria-label="Illustrazione: un perito con la cartella accanto a un\'auto, una moto e una casa">'
            '<circle cx="300" cy="200" r="190" fill="#EEF3FF"/><circle cx="440" cy="90" r="46" fill="#FFE2CC"/>'
            '<rect x="40" y="356" width="490" height="10" rx="5" fill="#DDE3F0"/>'
            f'<g class="float">{house(300, 120, 1.2)}</g>'
            f'<g class="float d2">{car(40, 270, 1.15)}</g>'
            f'<g class="float d3">{moto(330, 300, .85)}</g>'
            f'{perito(210, 176, 1.0)}'
            '<g><rect x="430" y="200" width="104" height="44" rx="14" fill="#fff" stroke="#E3E7F0"/><circle cx="452" cy="222" r="9" fill="#14794A"/>'
            '<path d="M448 222 l3 3 l6 -7" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/><text x="468" y="227" font-family="Inter,sans-serif" font-size="13" font-weight="700" fill="#0B1B3A">Foto ok</text></g>'
            '</svg>')


def mini(kind):
    body = {"auto": car(14, 20, .62), "moto": moto(28, 22, .66), "casa": house(30, 6, .55), "perito": perito(50, 0, .52), "medico": perito(50, 0, .52)}[kind]
    return f'<svg class="ill" viewBox="0 0 150 100" aria-hidden="true"><rect width="150" height="100" rx="18" fill="#EEF3FF"/>{body}</svg>'
