"""Package authored source and evidence; never include local game dependencies."""

from pathlib import Path

from zipfile import ZipFile, ZIP_DEFLATED

root=Path(__file__).resolve().parents[1]

output=root/'dist/DndWizard-v0.4.0-source.zip'

folders={'Code','art-source','DndWizard','tools','tests','test-results','docs','.github'}

with ZipFile(output,'w',ZIP_DEFLATED) as archive:

    for p in sorted(root.rglob('*')):

        if not p.is_file(): continue

        rel=p.relative_to(root)

        if len(rel.parts)>1 and rel.parts[0] not in folders: continue

        if any(part in {'__pycache__','.godot','bin','obj'} for part in rel.parts): continue
        if p.suffix in {'.pyc','.pck','.dll','.pdb','.log'}: continue

        if p.name in {'last-case.json','live-cards-failure.txt','raster-jobs.json'}: continue

        archive.write(p,Path('DndWizard')/rel)

print(output)



