"""Offline release checks: authored content, localization and asset coverage.

Does not load sts2.dll, contact the game bridge, or start the game.
"""
import hashlib
import json
import re
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from generate_content import CARDS, slug

def main():
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)

    ids = [c['Id'] for c in CARDS]
    check(len(ids) == len(set(ids)), 'Duplicate card identifiers')
    check(json.loads((ROOT/'cards.json').read_text(encoding='utf-8')) == CARDS, 'Stale generated card catalog')
    code = (ROOT/'Code/Cards.g.cs').read_text(encoding='utf-8')
    classes = re.findall(r'public sealed class (\w+)\(', code)
    check(classes == ids, 'Generated C# class list does not match authoring data')
    sources = '\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'Code').glob('*.cs'))
    powers = re.findall(r'public sealed class (\w+) : WizardPower', sources)
    relics = re.findall(r'public sealed class (\w+) : WizardRelic', sources)
    card_vars = {'Damage','Block','BonusDamage','BonusBlock','Draw','Slots','Power','Empower','Mirror','DelayedSlots'}
    tables = {}
    for lang in ('eng','zhs'):
        tables[lang] = {}
        for table in ('cards','powers','relics','characters'):
            tables[lang][table] = json.loads((ROOT/f'DndWizard/localization/{lang}/{table}.json').read_text(encoding='utf-8'))
        for card in CARDS:
            key = 'DNDWIZARD-' + slug(card['Id'])
            for suffix in ('title','description'):
                check(bool(tables[lang]['cards'].get(key+'.'+suffix)), f'{lang}: missing {key}.{suffix}')
            text = tables[lang]['cards'].get(key+'.description', '')
            used = set(re.findall(r'\{(\w+)', text))
            check(used <= card_vars, f'{lang}/{key}: unresolved variables {used-card_vars}')
            check('自动消耗' not in text and 'automatically spends' not in text, f'{key}: stale automatic casting text')
        for group, names in [('powers', powers), ('relics', relics)]:
            for name in names:
                key = 'DNDWIZARD-' + slug(name)
                check(bool(tables[lang][group].get(key+'.description')), f'{lang}: missing {key}')
                check((ROOT/f'DndWizard/images/{group}/{name}.png').is_file(), f'Missing {group} icon: {name}')
    for table in tables['eng']:
        check(tables['eng'][table].keys() == tables['zhs'][table].keys(), f'Localization key mismatch: {table}')
    hashes = []
    originals = []
    for name in ids:
        original = ROOT/f'art-source/illustrations/{name}.png'
        runtime = ROOT/f'DndWizard/images/cards/{name}.png'
        check(original.is_file(), f'Missing original illustration: {name}')
        check(runtime.is_file(), f'Missing runtime illustration: {name}')
        if original.is_file(): originals.append(hashlib.sha256(original.read_bytes()).hexdigest())
        if runtime.is_file():
            with Image.open(runtime) as image:
                check(image.size == (512,384), f'Incorrect dimensions: {name}: {image.size}')
            hashes.append(hashlib.sha256(runtime.read_bytes()).hexdigest())
    check(len(set(hashes)) == len(ids), 'Duplicate runtime card illustrations')
    check(len(set(originals)) == len(ids), 'Duplicate original card illustrations')
    report = {'scope':'offline content and resource validation only; no in-game tests',
              'cards':len(ids), 'unique_card_illustrations':len(set(hashes)),
              'powers':len(powers), 'relics':len(relics), 'languages':list(tables), 'errors':errors}
    output = ROOT/'test-results/v0.4.0-static.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if errors: raise SystemExit(1)

if __name__ == '__main__':
    main()
