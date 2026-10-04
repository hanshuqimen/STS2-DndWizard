"""Native texture import avoids the MCP builder's incompatible raw PNG CTEX payload."""
import json, os, shutil, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
GODOT=os.environ.get('GODOT_EXE',r'C:\Tools\Godot\Godot_console.exe')
work=ROOT/'build/native-import'
stage=ROOT/'build/pack'
work.mkdir(parents=True,exist_ok=True)
stage.mkdir(parents=True,exist_ok=True)
shutil.copytree(ROOT/'DndWizard',work/'DndWizard',dirs_exist_ok=True)
(work/'project.godot').write_text('[application]\nconfig/name="WizardAssetImport"\n[rendering]\nrenderer/rendering_method="gl_compatibility"\n',encoding='utf-8')
p=subprocess.run([GODOT,'--headless','--editor','--path',str(work),'--import'],capture_output=True)
(ROOT/'build/native-import.log').write_bytes(p.stdout+p.stderr)
if p.returncode: raise RuntimeError('Godot import failed; see build/native-import.log')
shutil.copytree(work/'DndWizard',stage/'DndWizard',dirs_exist_ok=True)
ctex=stage/'.godot/imported'
ctex.mkdir(parents=True,exist_ok=True)
for f in (work/'.godot/imported').glob('*.ctex'): shutil.copy2(f,ctex/f.name)
print(json.dumps({'source_dir':str(stage),'output_path':str(ROOT/'DndWizard.pck'),'convert_pngs':False},indent=2))
