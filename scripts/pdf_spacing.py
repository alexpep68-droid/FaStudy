"""Conservative repairs for whitespace inserted by PDF extraction.

Never change non-whitespace characters, infer words from a dictionary, or join lines.
Only remove a horizontal gap when the encoded glyph sequence agrees exactly and
adjacent letters have no intervening space glyph and are visually contiguous.
"""
import re

def repair_spacing(text, glyphs):
    encoded=[]
    for glyph in glyphs:
        for char in glyph['text']:
            encoded.append((char,glyph))
    visible=[(char,glyph,i) for i,(char,glyph) in enumerate(encoded) if not char.isspace()]
    expected=''.join(c for c in text if not c.isspace())
    if expected!=''.join(c for c,_,_ in visible):
        return text,[],False
    gaps=[];index=-1;i=0
    while i<len(text):
        if not text[i].isspace():index+=1;i+=1;continue
        end=i+1
        while end<len(text) and text[end].isspace():end+=1
        gap=text[i:end]
        if index>=0 and index+1<len(visible) and '\n' not in gap and '\r' not in gap:
            a,ga,ia=visible[index];b,gb,ib=visible[index+1]
            size=min(float(ga.get('size',0)),float(gb.get('size',0)))
            horizontal=float(gb['x0'])-float(ga['x1'])
            same_line=abs(float(ga['top'])-float(gb['top']))<=size*.08
            same_font=ga.get('fontname')==gb.get('fontname') and abs(float(ga.get('size',0))-float(gb.get('size',0)))<.1
            if a.isalpha() and b.isalpha() and ib==ia+1 and size>0 and same_line and same_font and -size*.1<=horizontal<=size*.12:
                gaps.append({'start':i,'end':end,'gap':gap,'left':a,'right':b})
        i=end
    corrected=text
    for gap in reversed(gaps):corrected=corrected[:gap['start']]+corrected[gap['end']:]
    assert ''.join(c for c in corrected if not c.isspace())==expected
    return corrected,gaps,True
