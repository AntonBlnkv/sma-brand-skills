"""Build a labelled JPG review board (the team reviews JPG boards only, never HTML).

Usage from Python:
    from board import row, sheet, text
    rows = [row([("frame.png", (0,0,2528,1696), "P02D before"),
                 ("fixed.png", (1050,750,1650,1180), "head after, 100%")], H=520),
            text(["Rule 1 ...", "Rule 2 ..."], W=1800)]
    sheet(rows, "Board title", "out.jpg")
Each cell = (image path, crop box x0,y0,x1,y1 in that image's pixels or None for the whole image, label).
Labels wrap onto up to 2 lines (row(..., label_lines=3) for 3). Cells in a row share height H.

Usage from the command line (run from the skill folder):
    python3 scripts/board.py OUT.jpg "Board title" CELL CELL ... [--row CELL ...] [--note "text"] [--h 520]
    CELL = path=label  or  path@x0,y0,x1,y1=label   (the box crops that image; no box = whole image)
    --row starts a new row; --note adds a line of text under the rows (repeatable).
    Example: python3 scripts/board.py board.jpg "S1 Daylight review" "frame.png=S1 Daylight, full frame" \
             "frame.png@1050,750,1650,1180=Max head 100%" "assets/refs/MX3-TA-5-head-front.jpg=reference TA-5"
Rule: always put Max's head next to the reference head at the same height, cropped from the full-res file.
"""
from PIL import Image, ImageDraw, ImageFont
def _font(n):
    for p in ['/System/Library/Fonts/Supplemental/Arial.ttf','/Library/Fonts/Arial.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
        try: return ImageFont.truetype(p,n)
        except OSError: pass
    return ImageFont.load_default()
F=_font(28); FT=_font(38)
def _wrap(d,txt,font,W):
    words=txt.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=font)<=W-8 or not cur: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines
def row(cells,H=520,label_lines=2):
    LH=34*label_lines+10; ims=[]
    for path,box,label in cells:
        im=Image.open(path).convert('RGB'); im=im.crop(box) if box else im
        im=im.resize((int(im.width*H/im.height),H),Image.LANCZOS)
        c=Image.new('RGB',(im.width,H+LH),'white'); d=ImageDraw.Draw(c)
        lines=_wrap(d,label,F,im.width)
        if len(lines)>label_lines: print('warning: label cut to %d lines: %r (use a shorter label or label_lines=3)'%(label_lines,label))
        for i,l in enumerate(lines[:label_lines]): d.text((4,4+i*34),l,fill='black',font=F)
        c.paste(im,(0,LH)); ims.append(c)
    W=sum(i.width for i in ims)+12*(len(ims)-1); r=Image.new('RGB',(W,H+LH),'white'); x=0
    for i in ims: r.paste(i,(x,0)); x+=i.width+12
    return r
def text(lines,W=1800,size=30):
    f=_font(size); tmp=ImageDraw.Draw(Image.new('RGB',(10,10))); out=[]
    for l in lines: out+= _wrap(tmp,l,f,W) or ['']
    r=Image.new('RGB',(W,len(out)*(size+10)+10),'white'); d=ImageDraw.Draw(r)
    for i,l in enumerate(out): d.text((4,6+i*(size+10)),l,fill='black',font=f)
    return r
def sheet(rows,title,out):
    W=max(r.width for r in rows); H=sum(r.height for r in rows)+20*len(rows)+70
    s=Image.new('RGB',(W+40,H),'white'); ImageDraw.Draw(s).text((20,16),title,fill='black',font=FT); y=70
    for r in rows: s.paste(r,(20,y)); y+=r.height+20
    s.save(out,quality=90); print(out,s.size)

if __name__ == '__main__':
    import sys
    a = sys.argv[1:]
    if len(a) < 3 or a[0] in ('-h', '--help'): print(__doc__); sys.exit(0 if a else 1)
    out, title, rest = a[0], a[1], a[2:]
    H = 520; rows = [[]]; notes = []; i = 0
    while i < len(rest):
        x = rest[i]
        if x == '--row': rows.append([]); i += 1; continue
        if x == '--note': notes.append(rest[i + 1]); i += 2; continue
        if x == '--h': H = int(rest[i + 1]); i += 2; continue
        path, _, label = x.partition('=')
        box = None
        if '@' in path:
            path, b = path.rsplit('@', 1); box = tuple(int(v) for v in b.split(','))
        rows[-1].append((path, box, label or path)); i += 1
    built = [row(r, H=H) for r in rows if r]
    if notes: built.append(text(notes, W=max(r.width for r in built)))
    sheet(built, title, out)
