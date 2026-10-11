import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from creatures import CREATURES, portrait_svg, token_svg

OUT = Path(__file__).parent / "out"
SVG = OUT / "svg"; SVG.mkdir(parents=True, exist_ok=True)
PNG = OUT / "png"; PNG.mkdir(parents=True, exist_ok=True)
only = sys.argv[1:]
jobs = []
for slug, (fac, fn) in CREATURES.items():
    if only and slug not in only:
        continue
    fig, focus = fn()
    (SVG / f"{slug}.svg").write_text(portrait_svg(fac, fig, seed=len(slug)))
    (SVG / f"{slug}-token.svg").write_text(token_svg(fac, fig, focus, seed=len(slug)))
    jobs += [{"svg": str(SVG / f"{slug}.svg"), "png": str(PNG / f"{slug}.png"), "size": 1000},
             {"svg": str(SVG / f"{slug}-token.svg"), "png": str(PNG / f"{slug}-token.png"), "size": 512}]
(OUT / "jobs.json").write_text(json.dumps(jobs))
subprocess.run(["node", str(Path(__file__).parent / "render.mjs"), str(OUT / "jobs.json")], check=True)
print("rendered", len(jobs))
