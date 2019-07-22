# StemmerHr

Stemmer for Croatian language.

## Usage

```python
from croatian_stemmer.stem import StemmerHr

stemmer = StemmerHr()

stemmer.stem('priče')
# output: 'prič'

stemmer.stem_text('Priče iz davnine')
# output: ['prič', 'iz', 'davnin']
```

## Testing

Testing is based on `unittest`.

```python
python test/test_simple.py
```

## Licence

GNU Lesser General Public License v3. See COPYING.txt and COPYING.LESSER.txt.
