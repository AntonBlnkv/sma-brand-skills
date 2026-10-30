"""Map the skill's Higgsfield ids to YOUR workspace (first-run bootstrap + every prompt).

The ids written in SKILL.md and references/*.md are the original ones; they work only for the account that
created them. This script uploads the bundled files (assets/manifest.json) into your own Higgsfield workspace,
records the new ids in a local map, and rewrites any prompt or attachment list to use them.

Usage (run from the skill folder; the map lives in ~/.sma-max-photo/ids.json, or $SMA_MAX_IDS):
  python3 scripts/ids.py status                      what is uploaded / created / missing, and which workspace
  python3 scripts/ids.py workspace WS_ID [NAME]      record the Higgsfield workspace you chose (before uploading)
  python3 scripts/ids.py request [--batch N]         JSON for the Higgsfield media_upload tool: the files still to upload
                                                     (batch N of 20, starting at 1)
  python3 scripts/ids.py put RESPONSE.json           save the media_upload result to a file, then run this: it PUTs each
                                                     file to its upload_url and records the media ids
  python3 scripts/ids.py put-one FILENAME UPLOAD_URL MEDIA_ID URL   the same for one file (values from the result)
  python3 scripts/ids.py confirm-list                media ids to pass to media_confirm (type image)
  python3 scripts/ids.py confirmed ID [ID ...]|--all mark media ids as confirmed after media_confirm said "uploaded"
  python3 scripts/ids.py element KEY                 JSON for manage_reference_elements action=create (KEY: max, mom,
                                                     dad, toddler, woman); create them in this order
  python3 scripts/ids.py set-element KEY NEW_ID      record the new Element id that create returned
  python3 scripts/ids.py get ID_OR_KEY               the id to use now (yours if mapped, else the original + a warning)
  python3 scripts/ids.py map FILE|-                  print FILE (or stdin) with every original id replaced by yours,
                                                     including <<<element>>> tags; use it on every prompt and attach list
Exit code of `map` / `get` is 3 when an id had no mapping (the original was kept): finish the bootstrap first.
"""
import json, os, re, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = json.load(open(os.path.join(HERE, 'assets', 'manifest.json')))
MAP_PATH = os.environ.get('SMA_MAX_IDS', os.path.expanduser('~/.sma-max-photo/ids.json'))
UUID = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')

def load():
    if os.path.exists(MAP_PATH):
        return json.load(open(MAP_PATH))
    return {'workspace': None, 'uploads': {}, 'elements': {}, 'map': {}}

def save(m):
    os.makedirs(os.path.dirname(MAP_PATH), exist_ok=True)
    m['updated'] = time.strftime('%Y-%m-%d %H:%M:%S')
    json.dump(m, open(MAP_PATH, 'w'), indent=1)

def upload_name(key):
    return 'sma_' + re.sub(r'[^A-Za-z0-9]+', '_', key) + '.jpg'

def by_name():
    return {upload_name(u['key']): u for u in MANIFEST['uploads']}

def rebuild_map(m):
    mp = {}
    for u in MANIFEST['uploads']:
        rec = m['uploads'].get(u['key'])
        if rec and rec.get('confirmed'):
            for oid in u['ids']:
                mp[oid] = rec['media_id']
    for e in MANIFEST['elements']:
        if e['key'] in m['elements']:
            mp[e['id']] = m['elements'][e['key']]
    m['map'] = mp

def main(a):
    if not a or a[0] in ('-h', '--help'):
        print(__doc__); return 0 if a else 1
    cmd, rest = a[0], a[1:]
    m = load()
    if cmd == 'status':
        ups = MANIFEST['uploads']
        done = [u for u in ups if m['uploads'].get(u['key'], {}).get('confirmed')]
        pend = [u for u in ups if u['key'] in m['uploads'] and not m['uploads'][u['key']].get('confirmed')]
        print('map file :', MAP_PATH)
        print('workspace:', m.get('workspace') or 'NOT SET (run: ids.py workspace WS_ID)')
        print('uploads  : %d of %d confirmed, %d put but not confirmed' % (len(done), len(ups), len(pend)))
        for e in MANIFEST['elements']:
            print('element  : %-8s %s' % (e['key'].split('.')[1], m['elements'].get(e['key'], 'not created')))
        missing = len(ups) - len(done) + sum(1 for e in MANIFEST['elements'] if e['key'] not in m['elements'])
        print('READY' if missing == 0 else 'NOT READY: %d step(s) left' % missing)
        return 0
    if cmd == 'workspace':
        if not rest: sys.exit('usage: ids.py workspace WS_ID [NAME]')
        if m.get('workspace') and m['workspace']['id'] != rest[0] and (m['uploads'] or m['elements']):
            sys.exit('this map already holds ids from workspace %s; use another map file (SMA_MAX_IDS=...) for a second workspace' % m['workspace']['id'])
        m['workspace'] = {'id': rest[0], 'name': ' '.join(rest[1:]) or None}
        save(m); print('workspace recorded:', m['workspace']); return 0
    if cmd == 'request':
        if not m.get('workspace'): sys.exit('record the workspace first: ids.py workspace WS_ID')
        todo = [u for u in MANIFEST['uploads'] if not m['uploads'].get(u['key'], {}).get('confirmed')]
        n = int(rest[rest.index('--batch') + 1]) if '--batch' in rest else 1
        part = todo[(n - 1) * 20:n * 20]
        if not part: print('nothing left to upload'); return 0
        print(json.dumps({'files': [{'filename': upload_name(u['key']), 'content_type': 'image/jpeg'} for u in part]}))
        print('# batch %d: %d files; %d still to upload in total' % (n, len(part), len(todo)), file=sys.stderr)
        return 0
    if cmd == 'put-one':   # put-one FILENAME UPLOAD_URL MEDIA_ID URL  (for a small media_upload result read on screen)
        if len(rest) < 4: sys.exit('usage: ids.py put-one FILENAME UPLOAD_URL MEDIA_ID URL')
        resp = {'uploads': [{'instructions': '@' + rest[0], 'upload_url': rest[1], 'media_id': rest[2], 'url': rest[3]}]}
        cmd = 'put'; rest = [None]
    if cmd == 'put':
        if not rest: sys.exit('usage: ids.py put RESPONSE.json')
        if rest[0] is not None: resp = json.load(open(rest[0]))
        items = resp.get('uploads', resp if isinstance(resp, list) else [])
        names = by_name(); ok = 0
        for it in items:
            mm = re.search(r'@(\S+?\.jpg)', it.get('instructions', '')) or re.search(r'(sma_[A-Za-z0-9_]+\.jpg)', json.dumps(it))
            fname = mm.group(1) if mm else it.get('filename')
            u = names.get(fname)
            if not u:
                print('skip: cannot tell which file this upload is for:', it.get('media_id')); continue
            data = open(os.path.join(HERE, u['file']), 'rb').read()
            # a plain User-Agent: the upload host's firewall rejects Python's default one (Cloudflare error 1010)
            req = urllib.request.Request(it['upload_url'], data=data, method='PUT', headers={'Content-Type': 'image/jpeg', 'User-Agent': 'sma-max-photo-uploader/1.7'})
            try:
                code = urllib.request.urlopen(req, timeout=120).status
            except urllib.error.HTTPError as e:
                if e.code == 412:   # this file was already uploaded to this slot (e.g. by hand with curl)
                    code = 200
                else:
                    print('FAIL', u['key'], 'HTTP', e.code, e.read()[:120]); continue
            except Exception as e:
                print('FAIL', u['key'], e); continue
            if code == 200:
                m['uploads'][u['key']] = {'media_id': it['media_id'], 'url': it['url'], 'confirmed': False}
                ok += 1; print('put ', u['key'], '->', it['media_id'])
            else:
                print('FAIL', u['key'], 'HTTP', code)
        save(m); print('%d uploaded; now run media_confirm with: ids.py confirm-list' % ok); return 0
    if cmd == 'confirm-list':
        ids = [r['media_id'] for r in m['uploads'].values() if not r.get('confirmed')]
        print(json.dumps(ids[:20])); return 0
    if cmd == 'confirmed':
        ids = set(rest)
        for r in m['uploads'].values():
            if '--all' in ids or r['media_id'] in ids: r['confirmed'] = True
        rebuild_map(m); save(m); print('confirmed; map has %d ids' % len(m['map'])); return 0
    if cmd == 'element':
        key = 'element.' + (rest[0] if rest else '')
        e = next((x for x in MANIFEST['elements'] if x['key'] == key), None)
        if not e: sys.exit('KEY must be one of: max, mom, dad, toddler, woman')
        medias = []
        for k in e['medias']:
            r = m['uploads'].get(k)
            if not r or not r.get('confirmed'): sys.exit('upload and confirm %s first' % k)
            medias.append({'id': r['media_id'], 'url': r['url'], 'type': 'media_input'})
        print(json.dumps({'action': 'create', 'name': e['name'], 'category': e['category'], 'description': e['description'], 'medias': medias}))
        return 0
    if cmd == 'set-element':
        if len(rest) < 2: sys.exit('usage: ids.py set-element KEY NEW_ID')
        key = 'element.' + rest[0]
        if key not in [e['key'] for e in MANIFEST['elements']]: sys.exit('unknown element ' + rest[0])
        if not UUID.fullmatch(rest[1]): sys.exit('NEW_ID must be a uuid')
        m['elements'][key] = rest[1]; rebuild_map(m); save(m); print('recorded', key, '->', rest[1]); return 0
    if cmd in ('get', 'map'):
        rebuild_map(m); mp = m['map']
        orig_by_key = {u['key']: u['ids'][0] for u in MANIFEST['uploads']}
        orig_by_key.update({e['key']: e['id'] for e in MANIFEST['elements']})
        known = set(orig_by_key.values()) | {i for u in MANIFEST['uploads'] for i in u['ids']}
        if cmd == 'get':
            x = rest[0] if rest else sys.exit('usage: ids.py get ID_OR_KEY')
            oid = orig_by_key.get(x, x)
            if oid in mp: print(mp[oid]); return 0
            print(oid); print('warning: %s is not mapped yet; using the original id' % x, file=sys.stderr); return 3
        src = sys.stdin.read() if (not rest or rest[0] == '-') else open(rest[0]).read()
        missing = sorted({i for i in UUID.findall(src) if i in known and i not in mp})
        out = UUID.sub(lambda g: mp.get(g.group(0), g.group(0)), src)
        sys.stdout.write(out)
        if missing:
            print('\nwarning: %d id(s) not mapped yet, originals kept: %s' % (len(missing), ', '.join(missing)), file=sys.stderr); return 3
        return 0
    sys.exit('unknown command; see --help')

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
