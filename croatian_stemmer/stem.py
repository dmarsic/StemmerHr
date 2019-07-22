#    StemmerHr - Stemmer for Croatian
#    Copyright 2012 Nikola Ljubešić and Ivan Pandžić
#    Copyright 2019 Domagoj Marsic based on Simple Stemmer for Croatian v0.1
#                                  by Nikola Ljubešić and Ivan Pandžić
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""StemmerHr - Stemmer for Croatian

Uses rules to stem Croatian words. See rules_simple.txt.
Stopwords are ignored, see stop.txt.

StemmerHr - Stemmer za hrvatski jezik

Koristi pravila za korjenovanje hrvatskih riječi. Vidi rules_simple.txt.
Zaustavne riječi se ignoriraju, vidi stop.txt.

Usage / Korištenje:

	from croatian_stemmer.stem import StemmerHr

	text = ('I lije na uglu petrolejska lampa '
			'Svjetlost crvenkastožutu ')
	token = 'Balada'

	stemmer = StemmerHr()
	stemmed_tokens = stemmer.stem_text(text)
	stemmed_token = stemmer.stem(token)

	# Alternative / Alternativno:
	stemmed_tokens = stemmer.korjenuj_tekst(text)
	stemmed_token = stemmer.korjenuj(token)

	### Output / Izlaz
	print(stemmed_tokens)
	['i', 'lij', 'na', 'ugl', 'petrolejsk', 'lamp', 'svjetlost',
	'crvenkastožutu']

	print(stemmed_token)
	'balad'
"""

import re
import sys
import logging
from pathlib import Path
from typing import List, Tuple

logger = logging.getLogger(__name__)


class StemmerHr(object):

	ETCDIR = Path('etc')
	RULES_FILE = ETCDIR/'rules_simple.txt'
	STOPWORDS_FILE = ETCDIR/'stop.txt'

	def __init__(
			self,
			explain: bool = False,
			rules_file: str = None,
			stopwords_file: str = None) -> None:
		"""Constructor.

		Rules (pravila) are tuples where first element defines the ending
		of the stem, and the second element defines all suffix forms.
		These are used to remove suffixes.

		Stopwords (zaustavne riječi) define a list of words that are ignored.

		:param explain: Log how the tokens are stemmed.
		:param rules_file: Path to rules file.
		:param stopwords_file: Path to stopwords file.
		"""
		rules_file = rules_file or self.RULES_FILE.as_posix()
		stopwords_file = stopwords_file or self.STOPWORDS_FILE.as_posix()
		self.pravila = self.ucitaj_pravila(rules_file)
		self.stopwords = self.ucitaj_zaustavne_rijeci(stopwords_file)
		self.explain = explain

	def stem_text(self, text: str) -> List[str]:
		"""Alias for `korjenuj_tekst()`."""
		return self.korjenuj_tekst(text)

	def stem(self, token: str) -> str:
		"""Alias for `korjenuj()`."""
		return self.korjenuj(token)

	def ucitaj_pravila(self, rules_file: str) -> List[re.Pattern]:
		"""Load rules from the rules file."""
		pravila = []
		with open(rules_file, 'r') as f:
			for line in f:
				try:
					if line.startswith('#'):
						continue
					tokens = line.strip().split(' ')
					osnova, nastavak = line.strip().split(' ')
					pravilo = re.compile(r'^('+osnova+')('+nastavak+r')$')
					pravila.append(pravilo)
				except ValueError as e:
					logger.error(f'Greška u pravilima, linija: {line}: {e}')
		return pravila

	def ucitaj_zaustavne_rijeci(self, stopwords_file: str) -> List[str]:
		"""Load stopwords from stopwords file."""
		with open(stopwords_file, 'r') as f:
			return list(map(lambda rijec: rijec.strip(), f.readlines()))

	def korjenuj_tekst(self, tekst: str) -> List[str]:
		"""Stem the input tekst into a list of stemmed tokens."""
		korjenovane = []
		pojavnice = re.findall(r'\w+', tekst.lower())
		for pojavnica in pojavnice:
			if pojavnica in self.stopwords:
				if self.explain:
					logger.info(f'{pojavnica} je zaustavna riječ, preskačem.')
				continue
			korjenovane.append(self.korjenuj(pojavnica))
		return korjenovane

	def korjenuj(self, pojavnica: str) -> str:
		"""Stem a single token and return the stemmed form."""
		pojavnica = pojavnica.lower()
		for pravilo in self.pravila:
			dioba = pravilo.match(pojavnica)
			if dioba:
				match = dioba.group(1)
				logger.info(f'"{pojavnica}" odgovara pravilu: {str(pravilo)} -> "{match}"')
				if self.ima_samoglasnik(match) and len(match) > 1:
					logger.info(f'Osnova "{match}" ima samoglasnik, vraćam kao korijen.')
					return match
		logger.info('Nije nađeno pravilo za pojavnicu "{pojavnica}".')
		return pojavnica

	def ima_samoglasnik(self, niz: str) -> bool:
		"""Check if the string contains a vowel."""
		return re.search(r'[aeiouR]', self.istakni_slogotvorno_R(niz)) is not None

	def istakni_slogotvorno_R(self, niz: str) -> str:
		"""Mark 'r' if between two vowels.

		'r' then becomes 'R' in this lowercase string, indicating its
		special function as a vowel.
		"""
		return re.sub(r'(^|[^aeiou])r($|[^aeiou])',r'\1R\2', niz.lower())
