import unittest
from croatian_stemmer.stem import StemmerHr


class TestStemmerHr(unittest.TestCase):

    def setUp(self):
        self.stemmer = StemmerHr()

    def test_stem(self):
        """Test stemming single tokens."""
        self.assertEqual(self.stemmer.stem(''), '')
        self.assertEqual(self.stemmer.stem('s'), 's')
        self.assertEqual(self.stemmer.stem('S'), 's')

        # Zašao neki momak u šumu Striborovu, a nije znao, da je ono šuma
        # začarana i da se u njoj svakojaka čuda zbivaju. Zbivala se u njoj
        # čuda dobra, ali i naopaka — svakome po zasluzi.
        self.assertEqual(self.stemmer.stem('Zašao'), 'zaša')
        self.assertEqual(self.stemmer.stem('neki'), 'nek')
        self.assertEqual(self.stemmer.stem('momak'), 'momak')
        self.assertEqual(self.stemmer.stem('u'), 'u')
        self.assertEqual(self.stemmer.stem('šumu'), 'šum')
        self.assertEqual(self.stemmer.stem('Striborovu'), 'striborov')
        self.assertEqual(self.stemmer.stem('a'), 'a')
        self.assertEqual(self.stemmer.stem('nije'), 'nij')
        self.assertEqual(self.stemmer.stem('znao'), 'zna')
        self.assertEqual(self.stemmer.stem('da'), 'da')
        self.assertEqual(self.stemmer.stem('je'), 'je')
        self.assertEqual(self.stemmer.stem('ono'), 'on')
        self.assertEqual(self.stemmer.stem('šuma'), 'šum')
        self.assertEqual(self.stemmer.stem('začarana'), 'začaran')
        self.assertEqual(self.stemmer.stem('i'), 'i')
        self.assertEqual(self.stemmer.stem('se'), 'se')
        self.assertEqual(self.stemmer.stem('njoj'), 'njoj')
        self.assertEqual(self.stemmer.stem('svakojaka'), 'svakojak')
        self.assertEqual(self.stemmer.stem('čuda'), 'čud')
        self.assertEqual(self.stemmer.stem('zbivaju'), 'zbiva')
        self.assertEqual(self.stemmer.stem('Zbivala'), 'zbiva')
        self.assertEqual(self.stemmer.stem('dobra'), 'dobr')
        self.assertEqual(self.stemmer.stem('ali'), 'al')
        self.assertEqual(self.stemmer.stem('naopaka'), 'naopak')
        self.assertEqual(self.stemmer.stem('svakome'), 'svak')
        self.assertEqual(self.stemmer.stem('po'), 'po')
        self.assertEqual(self.stemmer.stem('zasluzi'), 'zasluz')

    def test_stem_text(self):
        """Test stemming a document text.

        This applies an alphanumeric tokenizer: Only \w+ regex pattern is
        taken from documents to form tokens.
        """
        document = """Zašao neki momak u šumu Striborovu, a nije znao, da je
            ono šuma začarana i da se u njoj svakojaka čuda zbivaju. Zbivala se
            u njoj čuda dobra, ali i naopaka — svakome po zasluzi."""
        expected = ['zaša', 'nek', 'momak', 'u', 'šum', 'striborov', 'a',
            'nij', 'zna', 'da', 'je', 'on', 'šum', 'začaran', 'i', 'da', 'se',
            'u', 'njoj', 'svakojak', 'čud', 'zbiva', 'zbiva', 'se', 'u',
            'njoj', 'čud', 'dobr', 'al', 'i', 'naopak', 'svak', 'po', 'zasluz'
        ]
        self.assertEqual(self.stemmer.stem_text(document), expected)


if __name__ == '__main__':
    unittest.main()
