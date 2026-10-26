import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('pdf_spacing',Path(__file__).resolve().parents[1]/'scripts/pdf_spacing.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

def glyphs(text,gap_at=None,gap=0):
    result=[];x=0
    for i,char in enumerate(text):
        if i==gap_at:x+=gap
        result.append(dict(text=char,x0=x,x1=x+5,top=10,size=12,fontname='Example'))
        x+=5
    return result

class SpacingTests(unittest.TestCase):
    def test_remove_only_invented_gap(self):
        result,changes,aligned=module.repair_spacing('di oses',glyphs('dioses'))
        self.assertEqual(result,'dioses');self.assertEqual(len(changes),1);self.assertTrue(aligned)
    def test_real_space_is_preserved(self):
        self.assertEqual(module.repair_spacing('de ellos',glyphs('de ellos'))[0],'de ellos')
    def test_positioned_word_space_is_preserved(self):
        self.assertEqual(module.repair_spacing('de ellos',glyphs('deellos',2,4))[0],'de ellos')
    def test_linebreak_and_hyphen_are_preserved(self):
        self.assertEqual(module.repair_spacing('di\noses',glyphs('dioses'))[0],'di\noses')
        self.assertEqual(module.repair_spacing('di- oses',glyphs('di-oses'))[0],'di- oses')
    def test_different_character_order_is_not_repaired(self):
        self.assertEqual(module.repair_spacing('di oses',glyphs('diosos')),('di oses',[],False))
    def test_accented_letters(self):
        self.assertEqual(module.repair_spacing('Debe rías',glyphs('Deberías'))[0],'Deberías')
    def test_different_line_and_font_are_preserved(self):
        g=glyphs('dioses');g[2]['fontname']='Other'
        self.assertEqual(module.repair_spacing('di oses',g)[0],'di oses')
        g=glyphs('dioses');g[2]['top']=30
        self.assertEqual(module.repair_spacing('di oses',g)[0],'di oses')

if __name__=='__main__':unittest.main()
