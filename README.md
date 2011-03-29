
Converts Indic text romanized according to the ISO15919 conventions into Devanāgarī.  Inspired in part by John Smith's `ur2ud` (available [here](http://bombay.indology.info/software/programs/index.html)), and named in recognition of that fact.

With valid input, ur2ud is functionally equivalent to John Smith's
`ur2ud -s`, and as with the original implementation:

  >  The program does not check that input is valid in terms of ISO 15919,
  >  or that UTF-8 input is syntactically valid. Invalid input will cause
  >  unpredictable results. Accented (Vedic) Roman input using acute and
  >  grave accents over vowels will produce correct but unaccented
  >  Devanagari output (the underscore notation for anudatta vowels is
  >  not currently supported, since it is not clear what its Unicode
  >  representation should be).

Note that where Professor Smith's version generally drops invalid input
characters, this program will return them in the result.  I'm currently
of the opinion that this is preferable, but could be persuaded to change
my mind.

TODO:
 * allow IAST or ISA15919 (or either??)
 * add switches for numerals and JS's skt behaviour (?)
 * add switch for accented Roman, or just include it anyway?



Usable as a python package:

    from ur2ud import ur2ud
    devanagari = ur2ud(roman)

or from the command line:

    Usage: ur2ud.py

    Read romanized Indic text from STDIN, and write Devanāgarī to STDOUT.

    Options:
      --version   show program's version number and exit
      -h, --help  show this help message and exit
