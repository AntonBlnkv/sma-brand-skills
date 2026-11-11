"""Pre-show size and place check for one take of the twin method (pipeline §A0 step 6d). Read-only, no model.

Read the y values (full-frame pixels) off the ruler first: python3 scripts/ruler.py TAKE.png RULER.jpg
Then give them here; the script applies the owner's standard for the card and prints PASS, CHECK or DROP.

Usage:
  python3 scripts/size_check.py standing H=1792 adult=120,1610 max=760,1600
      Max sitting beside a standing adult (also leash). adult=CROWN,SHOES  max=CROWN,PAWS  H=frame height.
      Max's crown as a share of the adult's height: target 0.52-0.56, accept from 0.46, DROP from 0.57.
  python3 scripts/size_check.py seated H=1792 adult=300,1600 shoulder=620 max=700,1590
      Max sitting beside a seated adult. adult=CROWN,FEET; shoulder=y of the adult's shoulders. DROP if his crown
      is above her shoulders.
  python3 scripts/size_check.py lying H=1792 adulthead=420,560 maxhead=900,1130 adultfeet=1500 maxpaws=1520
      Max lying. adulthead / maxhead = CROWN,CHIN of the nearest adult's head and of Max's head (ears not counted).
      Ratio target 1.6-1.8, accept 1.3-1.5, DROP from 1.95.
  python3 scripts/size_check.py toddler H=1792 toddler=700 max=640 adultfeet=1500 maxpaws=1510
      Max sitting beside a toddler: toddler / max = y of the top of each head. CHECK if Max's crown is above the
      toddler's by more than 3% of the frame height, DROP above 8%.
Place, every card: Max's paws (maxpaws, or the second max value) more than 2% of H below the adult's shoes or feet
means he stands nearer the camera than the people: DROP. Give adultfeet= and maxpaws= on lying and toddler takes.
Exit code 0 = PASS, 1 = CHECK (show it, with the number in the note), 2 = DROP (do not show; generate a new take).
"""
import sys


def pair(s):
    a, b = s.split(','); return float(a), float(b)


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__); return 0 if argv else 1
    card, kv = argv[0], dict(a.split('=', 1) for a in argv[1:])
    H = float(kv['H']); notes, verdict = [], 0

    def worst(v, note):
        nonlocal verdict
        verdict = max(verdict, v); notes.append(note)

    def place(feet, paws):
        off = (paws - feet) / H
        if off > 0.02: worst(2, 'paws %.1f%% of the frame below the people\'s feet: Max is nearer the camera' % (100 * off))
        else: notes.append('place ok (paws %+.1f%% of the frame vs the feet)' % (100 * off))

    if card == 'standing':
        ac, af = pair(kv['adult']); mc, mp = pair(kv['max'])
        r = (af - mc) / (af - ac)
        if r >= 0.57: worst(2, 'crown at %.2f of her height: bigger than canon (drop from 0.57)' % r)
        elif 0.52 <= r <= 0.56: notes.append('crown at %.2f of her height: on target' % r)
        elif r >= 0.46: worst(1, 'crown at %.2f of her height: accept range' % r)
        else: worst(1, 'crown at %.2f of her height: small, below the accept range' % r)
        place(af, mp)
    elif card == 'seated':
        ac, af = pair(kv['adult']); mc, mp = pair(kv['max']); sh = float(kv['shoulder'])
        if mc < sh: worst(2, 'crown above her shoulders')
        else: notes.append('crown below her shoulders')
        place(af, mp)
    elif card == 'lying':
        a1, a2 = pair(kv['adulthead']); m1, m2 = pair(kv['maxhead'])
        r = (m2 - m1) / (a2 - a1)
        if r >= 1.95: worst(2, 'head ratio %.2f: too big (drop from 1.95)' % r)
        elif 1.6 <= r <= 1.8: notes.append('head ratio %.2f: on target' % r)
        elif 1.3 <= r < 1.6: worst(1, 'head ratio %.2f: accept range' % r)
        else: worst(1, 'head ratio %.2f: outside target, judge by eye' % r)
        if 'adultfeet' in kv and 'maxpaws' in kv: place(float(kv['adultfeet']), float(kv['maxpaws']))
    elif card == 'toddler':
        d = (float(kv['toddler']) - float(kv['max'])) / H
        if d > 0.08: worst(2, 'crown %.1f%% of the frame above the toddler\'s head' % (100 * d))
        elif d > 0.03: worst(1, 'crown %.1f%% of the frame above the toddler\'s head: a little big' % (100 * d))
        else: notes.append('crown at or below the toddler\'s head')
        if 'adultfeet' in kv and 'maxpaws' in kv: place(float(kv['adultfeet']), float(kv['maxpaws']))
    else:
        print('unknown card %r: standing | seated | lying | toddler' % card); return 2
    print(['PASS', 'CHECK', 'DROP'][verdict] + ': ' + '; '.join(notes))
    return verdict


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
