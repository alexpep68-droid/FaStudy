"""Extract a private draft catalog with conservative glyph-verified spacing."""
from pathlib import Path
import argparse,hashlib,json
from pypdf import PdfReader
import pdfplumber
from pdf_spacing import repair_spacing

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf',type=Path)
    parser.add_argument('--title',required=True)
    parser.add_argument('--language',required=True,choices=['es','en','zh','pt','fr'])
    parser.add_argument('--source-url',default=None)
    parser.add_argument('--permission',default=None)
    parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args()
    if args.out.exists():parser.error('Choose a new output filename; existing catalog is not overwritten')
    reader=PdfReader(args.pdf);entries=[];total=0;unaligned=0
    with pdfplumber.open(args.pdf)as witness:
        if len(reader.pages)!=len(witness.pages):raise ValueError('Page count mismatch')
        for number,(page,other)in enumerate(zip(reader.pages,witness.pages),1):
            original=page.extract_text()or''
            corrected,gaps,aligned=repair_spacing(original,other.chars)
            total+=len(gaps);unaligned+=not aligned
            entries.append(dict(pdfPage=number,printedPage=None,section=None,text=corrected,
                                extractionSpacing={'method':'encoded-glyphs-v1','removedHorizontalGaps':len(gaps),'glyphOrderAligned':aligned}))
            other.close()
    doc=dict(title=args.title,author='Li Hongzhi',language=args.language,languageVerified=False,
             sourceUrl=args.source_url,permission=args.permission,lecture=None,date=None,reviewed=False,
             sha256=hashlib.sha256(args.pdf.read_bytes()).hexdigest(),pages=entries,
             extraction={'base':'pypdf','spacingRepair':'encoded-glyphs-v1','characterChanges':0})
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(dict(version=1,documents=[doc]),ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Draft: {len(entries)} pages; {total} horizontal gaps removed; {unaligned} pages skipped by spacing check. Human review still required.')

if __name__=='__main__':main()
