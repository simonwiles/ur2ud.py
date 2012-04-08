## ur2ud.py

The most recent version of this program is available at
https://github.com/simonwiles/ur2ud.py/

#### DESCRIPTION:

Converts Indic text romanized according to the ISO15919 conventions into
Devanāgarī.  Inspired in part by John Smith's `ur2ud` (available
[here](http://bombay.indology.info/software/programs/index.html)), and named
in recognition of that fact.

With valid input, ur2ud is functionally equivalent to John Smith's
`ur2ud -s`, and as with the original implementation:

  >  The program does not check that input is valid in terms of ISO15919,
  >  or that UTF-8 input is syntactically valid. Invalid input will cause
  >  unpredictable results. Accented (Vedic) Roman input using acute and
  >  grave accents over vowels will produce correct but unaccented
  >  Devanagari output (the underscore notation for _anudatta_ vowels is
  >  not currently supported, since it is not clear what its Unicode
  >  representation should be).

Note that where Professor Smith's version generally drops invalid input
characters, this program will return them in the result.  I'm currently
of the opinion that this is preferable.

#### ADDITIONAL FUNCTIONALITY:

The program accepts a parameter (`iast`) which instructs it to expect input
romanized according to IAST ([International Alphabet of Sanskrit
Transliteration](http://en.wikipedia.org/wiki/IAST)) instead of
[ISO15919](http://en.wikipedia.org/wiki/ISO_15919).  The most important
differences are that IAST uses 'ṃ' instead of 'ṁ' for the _anusvāra_, and
'ṛ' and 'ṝ' instead of 'r̥' and 'r̥̄' for the short and long retroflex
(_mūrḍhanya_) vowels respectively.

#### TODO:
* convert input to a standard Unicode Normalization form (NFD?)
    -- need to convert the transliteration tables!
* add switches for numerals and JS's skt behaviour (?)
* add switch for accented Roman, or just include it anyway?


#### USAGE:

Usable as a python package:

    from ur2ud import Transliterator
    ur2ud = Transliterator(iast=True)
    devanagari = ur2ud.transliterate(roman)

or from the command line:

    Usage: ur2ud.py

    Read romanized Indic text from STDIN, and write Devanāgarī to STDOUT.

    Options:
      --version   show program's version number and exit
      -h, --help  show this help message and exit
      -i, --iast  Expect IAST input (instead of ISO15919)
