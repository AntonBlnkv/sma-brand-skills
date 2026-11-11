"""Smoke test: run every script of the skill from the package, on synthetic frames + the master reference.

Usage:  python3 tests/smoke_test.py [SKILL_DIR]
SKILL_DIR defaults to plugins/sma-max-photo/skills/sma-max-photo next to this file; pass an installed copy
(e.g. ~/.claude/skills/sma-max-photo) to test that instead. Runs in a temp folder, writes nothing else.
Prints one line per script and exits non-zero on the first failure.
"""
import os, subprocess, sys, tempfile
sys.dont_write_bytecode = True  # keep __pycache__ out of the package
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, '..', 'plugins', 'sma-max-photo', 'skills', 'sma-max-photo')
SCRIPTS = os.path.join(SKILL, 'scripts')
MASTER = os.path.join(SKILL, 'assets', 'refs', 'MX3-BO-6-gpt25-sunburst_MASTER.jpg')
for p in (os.path.join(SKILL, 'SKILL.md'), MASTER):
    assert os.path.exists(p), 'missing ' + p

def run(name, *args, env=None):
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, name), *args], cwd=tmp, capture_output=True, text=True,
                       env={**os.environ, **(env or {})})
    if r.returncode:
        print('FAIL', name, r.stderr[-800:]); sys.exit(1)
    print('ok  ', name, '|', r.stdout.strip().splitlines()[-1])
    return r.stdout

tmp = tempfile.mkdtemp(prefix='sma-max-smoke-')
rng = np.random.default_rng(0)
W, H = 900, 600
bg = (np.stack([rng.normal(90, 12, (H, W)), rng.normal(120, 12, (H, W)), rng.normal(95, 12, (H, W))], -1)).clip(0, 255).astype(np.uint8)
Image.fromarray(bg).save(os.path.join(tmp, 'nodog.png'))
withdog = Image.fromarray(bg.copy()); d = ImageDraw.Draw(withdog)
d.ellipse((300, 180, 640, 470), fill=(214, 140, 60))      # an over-orange "Max" (hue ~28, high saturation)
d.ellipse((560, 120, 700, 260), fill=(205, 132, 55))      # his head
withdog.save(os.path.join(tmp, 'withdog.png'))

# 1 max_mask: whole silhouette from WITH / WITHOUT
out = run('max_mask.py', 'withdog.png', 'nodog.png', 'mask.png')
m = np.asarray(Image.open(os.path.join(tmp, 'mask.png'))) > 127
assert m[320, 470] and not m[50, 50], 'mask does not cover the dog'

# 2 recolor_max: move the fur to the evening band with the mask (box = whole frame)
run('recolor_max.py', 'withdog.png', 'x', f'0,0,{W},{H}', 'eve', 'recolored.png', '--mask', 'mask.png')
a = np.asarray(Image.open(os.path.join(tmp, 'recolored.png'))).astype(int)
assert np.abs(a[:40, :40] - bg[:40, :40]).max() <= 2, 'recolor touched the background'  # HSV round-trip rounding only

# 2b recolor_max with the options BEFORE the positional arguments (must give the same result)
run('recolor_max.py', '--mask', 'mask.png', 'withdog.png', 'x', f'0,0,{W},{H}', 'eve', 'recolored2.png')
assert (np.asarray(Image.open(os.path.join(tmp, 'recolored2.png'))) == a.astype(np.uint8)).all(), 'option order changed the result'

# 2c resize_max: cut the dog out of WITH using WITHOUT, put him at 150 px tall with paws at (450, 560)
o = run('resize_max.py', 'nodog.png', 'withdog.png', 'resized.png', '--height', '150', '--feet', '450,560')
r = np.asarray(Image.open(os.path.join(tmp, 'resized.png'))).astype(int)
gold = (r[..., 0] - r[..., 2] > 100)
ys, xs = np.where(gold)
assert abs(ys.max() - 560) <= 4 and abs((ys.max() - ys.min()) - 150) <= 8, ('resize_max put the dog wrong', ys.min(), ys.max())
assert not gold[180:470, 600:640].any() or xs.max() < 600, 'resize_max left the old dog behind'

# 2c' resize_max with --green and --person: green silhouette of the dog, magenta adult standing at x 150..230
gr = Image.fromarray(bg.copy()); dg = ImageDraw.Draw(gr)
dg.ellipse((300, 180, 640, 470), fill=(0, 255, 0)); dg.ellipse((560, 120, 700, 260), fill=(0, 255, 0)); gr.save(os.path.join(tmp, 'green.png'))
pe = Image.fromarray(bg.copy()); ImageDraw.Draw(pe).rectangle((150, 120, 230, 560), fill=(255, 0, 255)); pe.save(os.path.join(tmp, 'person.png'))
o = run('resize_max.py', 'nodog.png', 'withdog.png', 'resized2.png', '--green', 'green.png', '--person', 'person.png', '--side', 'right')
r = np.asarray(Image.open(os.path.join(tmp, 'resized2.png'))).astype(int)
ys, xs = np.where(r[..., 0] - r[..., 2] > 100)
assert abs(ys.max() - 560) <= 6 and abs((ys.max() - ys.min()) - 0.55 * 440) <= 15 and xs.min() > 230, ('--person placement wrong', ys.min(), ys.max(), xs.min())

# 2d ruler
run('ruler.py', 'withdog.png', 'ruler.jpg', '200,100,800,500')
assert os.path.exists(os.path.join(tmp, 'ruler.jpg'))

# 2e twin_board: board with the G1 twin crop and two takes; the golden "Max" must be found in the take
for k in ('G1', 'G3', 'F1', 'L02', 'L05', 'L06', 'L08', 'G4'):
    for f in (f'max-{k}.jpg', f'twin-{k}.jpg'):
        assert os.path.exists(os.path.join(SKILL, 'assets', 'twins', f)), 'missing twin file ' + f
assert os.path.exists(os.path.join(SKILL, 'assets', 'twins', 'medal-ref.jpg')), 'missing medal-ref.jpg'
run('twin_board.py', 'twin_board.jpg', 'G1', 'Smoke', 'withdog.png', 'withdog.png')
assert Image.open(os.path.join(tmp, 'twin_board.jpg')).size[0] > 2000, 'twin_board.py wrote a wrong-size board'

# 3 crop + paste_crop: crop of the master (3:2 grown), "edited" (brightened), pasted back
master = Image.open(MASTER).convert('RGB'); master.save(os.path.join(tmp, 'full.png'))
o = run('crop.py', 'full.png', '300,200,700,500', 'crop.png')
box = tuple(int(v) for v in o.split('box ')[1].split()[0].split(','))
assert abs((box[2] - box[0]) / (box[3] - box[1]) - 1.5) < 0.01, 'crop is not 3:2'
crop = Image.open(os.path.join(tmp, 'crop.png'))
edited = Image.fromarray((np.asarray(crop).astype(int) * 1.05).clip(0, 255).astype(np.uint8))
edited.resize((1200, 800)).save(os.path.join(tmp, 'edited.png'))
run('paste_crop.py', 'full.png', ','.join(map(str, box)), 'edited.png', 'pasted.png', env={'FULL': '1'})
assert Image.open(os.path.join(tmp, 'pasted.png')).size == master.size
run('paste_crop.py', 'full.png', ','.join(map(str, box)), 'edited.png', 'pasted_region.png', env={'REGION': '100,60,300,240'})
pr = np.asarray(Image.open(os.path.join(tmp, 'pasted_region.png'))).astype(int); fo = np.asarray(master).astype(int)
assert (pr[box[1] + 5, box[0] + 5] == fo[box[1] + 5, box[0] + 5]).all(), 'REGION paste changed pixels outside the region'

# 4 colormatch: undo a magenta cast on the master
cast = (np.asarray(master).astype(int) + np.array([18, -10, 14])).clip(0, 255).astype(np.uint8)
Image.fromarray(cast).save(os.path.join(tmp, 'cast.png'))
o = run('colormatch.py', 'full.png', 'cast.png', 'matched.jpg')
before, after = float(o.split('mean before')[1].split()[0]), float(o.split('after')[1].split()[0])
assert after < before, 'colormatch did not reduce the cast'

# 5 board: import and build a labelled sheet
sys.path.insert(0, SCRIPTS); cwd = os.getcwd(); os.chdir(tmp)
from board import row, sheet, text
sheet([row([('full.png', box, 'master crop'), ('pasted.png', box, 'after paste')], H=300), text(['smoke test'], W=900)],
      'sma-max-photo smoke test', os.path.join(tmp, 'board.jpg'))
os.chdir(cwd); print('ok   board.py')
# 5b new helpers: mask check image, read-only fur measurement, board command line, --help everywhere
assert os.path.exists(os.path.join(tmp, 'mask_check.jpg')), 'max_mask.py did not write mask_check.jpg'
o = run('measure_fur.py', MASTER, '0,0,1440,1800', '--style', 'day')
assert 'INSIDE' in o, 'BO-6 master should measure inside the Daylight band'
run('board.py', 'board_cli.jpg', 'CLI board', 'full.png=whole frame', 'full.png@300,200,700,500=crop', '--row', 'pasted.png=after', '--note', 'smoke test')
assert os.path.exists(os.path.join(tmp, 'board_cli.jpg'))
for s in sorted(os.listdir(SCRIPTS)):
    if s.endswith('.py'):
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, s), '--help'], capture_output=True, text=True)
        assert r.returncode == 0 and 'Usage' in r.stdout, s + ' --help does not print its usage'
print('ok   measure_fur.py, board.py CLI, mask_check.jpg, --help on every script')
# 5c size_check.py: the owner's size standards and the place check give the right verdict
for args, code in [(['standing', 'H=1792', 'adult=120,1610', 'max=800,1600'], 0), (['standing', 'H=1792', 'adult=120,1610', 'max=700,1600'], 2),
                   (['standing', 'H=1792', 'adult=120,1610', 'max=800,1700'], 2), (['lying', 'H=1792', 'adulthead=420,560', 'maxhead=900,1130'], 0),
                   (['lying', 'H=1792', 'adulthead=420,560', 'maxhead=900,1180'], 2), (['seated', 'H=1792', 'adult=300,1600', 'shoulder=620', 'max=600,1590'], 2),
                   (['toddler', 'H=1792', 'toddler=700', 'max=640'], 1)]:
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'size_check.py')] + args, capture_output=True, text=True)
    assert r.returncode == code, 'size_check.py %s gave %d, expected %d: %s' % (args, r.returncode, code, r.stdout)
print('ok   size_check.py')

# 6 the prompt skeleton in SKILL.md must match references/prompts.md word for word
import re
S = open(os.path.join(SKILL, 'SKILL.md')).read(); P = open(os.path.join(SKILL, 'references', 'prompts.md')).read()
block = [l for l in P.split('\n') if l.startswith('> {POSE')][0][2:]
assert block in S, 'Max block in SKILL.md differs from prompts.md section 2'
for pat in [r'- Family: `([^`]+)`', r'- Woman driver: `([^`]+)`', r'\*\*Tail:\*\* `([^`]+)`']:
    assert re.search(pat, P).group(1) in S, 'SKILL.md skeleton differs from prompts.md: ' + pat
for code, text in re.findall(r'^\| (EX-\d\d) [^|]+? \| (.+?) \|$', P, re.M):
    assert text in S, 'emotion text differs: ' + code
assert not re.search('[\u0400-\u04FF]', S.replace('Макс', '')), 'non-English text in SKILL.md'
for f in os.listdir(os.path.join(SKILL, 'references')):
    assert not re.search('[\u0400-\u04FF]', open(os.path.join(SKILL, 'references', f)).read()), 'non-English text in ' + f
print('ok   SKILL.md prompt skeleton matches references/prompts.md; no non-English text')
# 7 manifest + ids.py: every bundled file exists, every id in the docs is either in the manifest or listed as not bundled,
#   and the id map rewrites a prompt (with a throw-away map file)
import json
M = json.load(open(os.path.join(SKILL, 'assets', 'manifest.json')))
for u in M['uploads']: assert os.path.exists(os.path.join(SKILL, u['file'])), 'missing bundled file ' + u['file']
known = {i for u in M['uploads'] for i in u['ids']} | {e['id'] for e in M['elements']} | set(M['not_bundled'])
docs = ''.join(open(os.path.join(SKILL, p)).read() for p in ['SKILL.md'] + ['references/' + f for f in os.listdir(os.path.join(SKILL, 'references'))])
stray = sorted(set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', docs)) - known)
assert not stray, 'ids in the docs with no bundled file: %s' % stray
env = {'SMA_MAX_IDS': os.path.join(tmp, 'ids.json')}
fake = {'workspace': {'id': 'test'}, 'uploads': {'max.BO-6': {'media_id': '11111111-1111-4111-8111-111111111111', 'url': 'https://x/y.jpg', 'confirmed': True}},
        'elements': {'element.max': '22222222-2222-4222-8222-222222222222'}, 'map': {}}
json.dump(fake, open(env['SMA_MAX_IDS'], 'w'))
r = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'ids.py'), 'map', '-'], input='<<<01ba1fc5-227c-439d-aa29-47ada4e45545>>> + 3394863f-6981-426a-a55e-6400056a0900',
                   capture_output=True, text=True, env={**os.environ, **env})
assert r.returncode == 0 and '<<<22222222-2222-4222-8222-222222222222>>>' in r.stdout and '11111111-1111-4111-8111-111111111111' in r.stdout, r.stdout + r.stderr
r = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'ids.py'), 'get', 'max.TA-1'], capture_output=True, text=True, env={**os.environ, **env})
assert r.returncode == 3 and 'not mapped' in r.stderr, 'unmapped id must warn and exit 3'
print('ok   manifest (%d files) + ids.py map/get' % len(M['uploads']))
print('ALL OK ->', tmp)
