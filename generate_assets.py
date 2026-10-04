"""Generate editable SVG sigils and scene files. Raster conversion uses Godot's SVG loader."""
from pathlib import Path
import math, json, shutil
from PIL import Image
from generate_content import CARDS
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'DndWizard'
SOURCE=ROOT/'art-source'
SOURCE.mkdir(exist_ok=True)
for p in ['images/cards','images/powers','images/relics','scenes']:
    (ASSETS/p).mkdir(parents=True,exist_ok=True)

SYMBOLS={
'fire':'<path d="M0 -75 Q65 -10 40 42 Q0 82 -36 42 Q-61 9 -12 -26 Q-25 14 0 12 Q30 -5 0 -75Z"/>',
'bolt':'<path d="M7 -80 L-48 10 L-8 10 L-20 79 L55 -22 L14 -22 L32 -80Z"/>',
'shield':'<path d="M0 -72 L62 -46 L52 18 Q32 61 0 79 Q-32 61 -52 18 L-62 -46Z" fill-opacity=".2"/><path d="M0 -46 V44 M-32 -5 H32" fill="none"/>',
'star':'<path d="M0 -75 L18 -21 L73 -22 L29 13 L45 67 L0 35 L-45 67 L-29 13 L-73 -22 L-18 -21Z" fill-opacity=".25"/>',
'book':'<path d="M0 -45 Q-32 -72 -66 -49 L-66 54 Q-28 34 0 61 Q28 34 66 54 L66 -49 Q32 -72 0 -45Z" fill-opacity=".2"/><path d="M0 -45 V61 M-51 -21 L-16 -11 M-51 0 L-16 10 M16 -11 L51 -21 M16 10 L51 0" fill="none"/>',
'ice':'<path d="M0 -73 V73 M-63 -36 L63 36 M-63 36 L63 -36 M-19 -56 L0 -39 L19 -56 M-19 56 L0 39 L19 56 M-59 -10 L-34 -20 L-39 -48 M59 10 L34 20 L39 48 M39 -48 L34 -20 L59 -10 M-39 48 L-34 20 L-59 10" fill="none"/>',
'eye':'<path d="M-80 0 Q0 -88 80 0 Q0 88 -80 0Z" fill-opacity=".1"/><circle r="29" fill="none"/><circle r="8"/>',
'orb':'<circle r="48" fill-opacity=".3"/><ellipse rx="77" ry="20" transform="rotate(-35)" fill="none"/><path d="M-20 -21 L-2 -32 L22 -11" fill="none"/>',
'missile':'<path d="M-62 47 L18 -32 M-42 67 L38 -12 M-79 20 L1 -59" fill="none"/><path d="M18 -32 L20 -4 L49 -60Z M38 -12 L40 16 L69 -40Z M1 -59 L3 -31 L32 -87Z"/>',
'web':'<path d="M0 -76 V76 M-76 0 H76 M-54 -54 L54 54 M-54 54 L54 -54 M0 -55 L39 -39 L55 0 L39 39 L0 55 L-39 39 L-55 0 L-39 -39Z M0 -28 L20 -20 L28 0 L20 20 L0 28 L-20 20 L-28 0 L-20 -20Z" fill="none"/>',
}
def symbol(c):
    id=c['Id']
    if any(s in id for s in ['Frost','Cold']): return 'ice','#83e4ef'
    if any(s in id for s in ['Fire','Burning','Scorching']): return 'fire','#efac65'
    if any(s in id for s in ['Lightning','Shocking','Thunder']): return 'bolt','#acb7ff'
    if any(s in id for s in ['Armor','Shield','Ward','Counterspell','Mirror','Globe','Life']): return 'shield','#70e3cb'
    if any(s in id for s in ['Recovery','Spellbook','Ritual','Meditation']): return 'book','#dabc78'
    if 'Missile' in id: return 'missile','#c7a4fa'
    if 'Web' in id: return 'web','#c9ceec'
    if any(s in id for s in ['Foresight','TrueStrike']): return 'eye','#f0cf82'
    if any(s in id for s in ['Acid','Witch']): return 'orb','#a4d17a'
    return 'star','#b4b1fa'

def sigil(name,kind,color,idx=0,w=512,h=384):
    stars=''.join(f'<circle cx="{30+(i*73+idx*29)%(w-60)}" cy="{25+(i*43+idx*17)%(h-50)}" r="{1+i%3}" fill="#d8c58b" opacity=".35"/>' for i in range(26))
    rays=''.join(f'<path d="M0 -131 V-142" transform="rotate({a})"/>' for a in range(0,360,30))
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><radialGradient id="b"><stop stop-color="#263451"/><stop offset="1" stop-color="#0d1425"/></radialGradient></defs>
<rect width="{w}" height="{h}" fill="url(#b)"/>{stars}
<g transform="translate({w/2},{h/2})" stroke="{color}" stroke-width="2" fill="none" opacity=".5"><circle r="126"/><circle r="115"/>{rays}<path d="M0 -102 L89 51 L-89 51Z M0 102 L-89 -51 L89 -51Z" transform="rotate({idx*13})" opacity=".25"/></g>
<g transform="translate({w/2},{h/2})" stroke="{color}" stroke-width="5" fill="{color}" stroke-linecap="round" stroke-linejoin="round">{SYMBOLS[kind]}</g>
<path d="M22 55 V22 H55 M{w-55} 22 H{w-22} V55 M22 {h-55} V{h-22} H55 M{w-55} {h-22} H{w-22} V{h-55}" fill="none" stroke="#b79c66" stroke-width="2"/>
</svg>'''
    (SOURCE/(name+'.svg')).write_text(svg,encoding='utf-8')
    return {'source':str(SOURCE/(name+'.svg')),'output':str(ASSETS/'images'/f'{name}.png')}

jobs=[]
for c in CARDS:
    illustration=SOURCE/'illustrations'/(c['Id']+'.png')
    if not illustration.exists(): raise FileNotFoundError(f'Missing required card illustration: {illustration}')
    # Native Godot resampling below keeps image-generation output as source of truth.
    jobs.append({'source':str(illustration),'output':str(ASSETS/'images/cards'/(c['Id']+'.png')),'raster':True})
for folder,items in {'powers':[('SpellSlotsPower','orb'),('ArcaneWardPower','shield'),('EvocationPower','fire'),('MeditationPower','book'),('EmpowerPower','star'),('MirrorImagePower','shield'),('CantripProgressPower','book'),('CantripSpentPower','eye'),('DelayedRecoveryPower','book'),('FocusSpentPower','eye'),('OvercastSpentPower','fire')],'relics':[('Spellbook','book'),('PearlOfPower','orb'),('RunicFocus','star'),('ExpandedGrimoire','book'),('CampfireIncense','fire'),('EfficientFocus','orb')]}.items():
    (SOURCE/folder).mkdir(exist_ok=True)
    for i,(name,kind) in enumerate(items): jobs.append(sigil(folder+'/'+name,kind,'#92d9e7',i,320,320))
jobs.append(sigil('icon','book','#dabe79',0,320,320))
for name,size in [('energy',128),('energy_text',24)]:
    (SOURCE/(name+'.svg')).write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 128 128"><defs><radialGradient id="g"><stop stop-color="#5262aa"/><stop offset="1" stop-color="#16254f"/></radialGradient></defs><circle cx="64" cy="64" r="57" fill="url(#g)" stroke="#e4c780" stroke-width="6"/><circle cx="64" cy="64" r="46" fill="none" stroke="#87dfe9" stroke-width="2"/></svg>''',encoding='utf-8')
    jobs.append({'source':str(SOURCE/(name+'.svg')),'output':str(ASSETS/'images'/f'{name}.png')})
(ROOT/'raster-jobs.json').write_text(json.dumps(jobs),encoding='utf-8')
sprite=SOURCE/'wizard-original.png'
if not sprite.exists():
    raise FileNotFoundError(f"Missing included original sprite: {sprite}")
im=Image.open(sprite).convert('RGBA')
im.thumbnail((640,960),Image.Resampling.LANCZOS)
im.save(ASSETS/'images/wizard.png')

scene='''[gd_scene load_steps=2 format=3]
[ext_resource type="Texture2D" path="res://DndWizard/images/wizard.png" id="1"]
[node name="Wizard" type="Node2D"]
[node name="Visuals" type="Node2D" parent="."]
unique_name_in_owner = true
[node name="Sprite" type="Sprite2D" parent="Visuals"]
position = Vector2(0, -155)
scale = Vector2(0.33, 0.33)
texture = ExtResource("1")
[node name="Bounds" type="Control" parent="."]
unique_name_in_owner = true
offset_left = -95.0
offset_top = -310.0
offset_right = 95.0
mouse_filter = 2
[node name="IntentPos" type="Marker2D" parent="."]
unique_name_in_owner = true
position = Vector2(0, -340)
[node name="CenterPos" type="Marker2D" parent="."]
unique_name_in_owner = true
position = Vector2(0, -150)
[node name="TalkPos" type="Marker2D" parent="."]
unique_name_in_owner = true
position = Vector2(40, -300)
[node name="OrbPos" type="Marker2D" parent="."]
unique_name_in_owner = true
position = Vector2(-100, -180)
'''
(ASSETS/'scenes/wizard.tscn').write_text(scene,encoding='utf-8')
(ASSETS/'scenes/icon.tscn').write_text('''[gd_scene load_steps=2 format=3]
[ext_resource type="Texture2D" path="res://DndWizard/images/icon.png" id="1"]
[node name="WizardIcon" type="TextureRect"]
offset_right = 64.0
offset_bottom = 64.0
texture = ExtResource("1")
expand_mode = 1
stretch_mode = 5
mouse_filter = 2
''',encoding='utf-8')
(ASSETS/'scenes/select.tscn').write_text('''[gd_scene load_steps=2 format=3]
[ext_resource type="Texture2D" path="res://DndWizard/images/wizard.png" id="1"]
[node name="WizardSelect" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
mouse_filter = 2
[node name="Backdrop" type="ColorRect" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
color = Color(0.035, 0.055, 0.10, 1)
mouse_filter = 2
[node name="Wizard" type="TextureRect" parent="."]
layout_mode = 1
anchor_left = 0.37
anchor_right = 0.94
anchor_top = 0.02
anchor_bottom = 0.98
texture = ExtResource("1")
expand_mode = 1
stretch_mode = 5
mouse_filter = 2
''',encoding='utf-8')
print(f'{len(CARDS)} card illustrations and {len(jobs)-len(CARDS)} SVG icons; sprite and scenes prepared.')
