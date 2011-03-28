
Converts Indic text romanized according to the ISO15919 conventions into Devanāgarī.  Inspired in part by John Smith's ur2ud (available [here](http://bombay.indology.info/software/programs/index.html)), and named in recognition of that fact.

Usable as a python package:

    from ur2ud import ur2ud
    devanagari = ur2ud(roman)

or from the command line:

    Usage: cssmin [--wrap N]

    Read CSS from STDIN, and write compressed CSS to STDOUT.

    Options:
      --version       show program's version number and exit
      -h, --help      show this help message and exit
      -w N, --wrap=N  Wrap output to approximately N chars per line.
      -e, --expand    Expand CSS (insert whitespace to make it readable).


v0.2 now fully compatible with the Java YUI CSS compressor
(i.e., passes all tests at https://github.com/yui/yuicompressor/).
