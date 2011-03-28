#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""

   The program does not check that input is valid in terms of ISO 15919,
   or that UTF-8 input is syntactically valid. Invalid input will cause
   unpredictable results. Accented (Vedic) Roman input using acute and
   grave accents over vowels will produce correct but unaccented
   Devanagari output (the underscore notation for anudatta vowels is
   not currently supported, since it is not clear what its Unicode
   representation should be).


    attempting to be functionally equivalent to John Smith's `ur2ud -s`

    TODO:
    * spaces -- omitted after consonants and before avagraha (complicated?)
      (all okay, I think)
    * apostrophe
        * apostrophe preceeding anusvāra ==> anusvāra + avagraha
        * [:vowel:]\s* + apostrophe ==> [:vowel:] + avagraha
            (natural by-product of correctly dealing with spaces?)
    * allow IAST or ISA15919 (or either??)
    * add switches for numerals and JS's skt behaviour (?)

"""

TRSL_SCHEMES = ['IAST', 'ISO15919']

# h ubar: no Unicode Devanagari char
# h ubreve: no Unicode Devanagari char


ACCENTED_INITIAL_VOWELS = {
    u'\u00E0':              [0x0905],           # a grave
    u'\u00E1':              [0x0905],           # a acute
    u'\u00EC':              [0x0907],           # i grave
    u'\u00ED':              [0x0907],           # i acute
    u'\u00F9':              [0x0909],           # u grave
    u'\u00FA':              [0x0909],           # u acute
    u'\u00E8':              [0x090F],           # e grave
    u'\u00E9':              [0x090F],           # e acute
    u'\u00F2':              [0x0913],           # o grave
    u'\u00F3':              [0x0913],           # o acute
}

ACCENTED_COMBINING_VOWELS = {
    u'\u00EC':              [0x093F],           # i grave
    u'\u00ED':              [0x093F],           # i acute
    u'\u00F9':              [0x0941],           # u grave
    u'\u00FA':              [0x0941],           # u acute
    u'\u00E8':              [0x0947],           # e grave
    u'\u00E9':              [0x0947],           # e acute
    u'\u00F2':              [0x094B],           # o grave
    u'\u00F3':              [0x094B],           # o acute
}

COMBINING_VOWELS = {
    u'a':                   [],
    u'i':                   [0x093F],
    u'u':                   [0x0941],
    u'e':                   [0x0947],
    u'o':                   [0x094B],
    u'ai':                  [0x0948],
    u'au':                  [0x094C],
    u'\u00EA':              [0x0945],           # e circ
    u'\u00F4':              [0x0949],           # o circ
    u'\u00E3':              [0x0901],           # a tilde
    u'\u00F5':              [0x094B, 0x0902],   # o tilde
    u'\u0101':              [0x093E],           # a macron
    u'\u1EBD':              [0x0947, 0x0902],   # e tilde
    u'\u012B':              [0x0940],           # i macron
    u'\u016B':              [0x0942],           # u macron
    u'\u0129':              [0x093F, 0x0902],   # i tilde
    u'\u0169':              [0x0941, 0x0901],   # u tilde
    u'a\u0129':             [0x0948, 0x0902],   # ai tilde
    u'a\u0169':             [0x094C, 0x0902],   # au tilde
    u'\u0101\u0303':        [0x093E, 0x0901],   # a mactil
    u'\u012B\u0303':        [0x0940, 0x0902],   # i mactil
    u'\u016B\u0303':        [0x0942, 0x0901],   # u mactil
    u'\u0101\u0300':        [0x093E],           # a macgrv
    u'\u0101\u0301':        [0x093E],           # a macac
    u'\u012B\u0300':        [0x0940],           # i macgrv
    u'\u012B\u0301':        [0x0940],           # i macac
    u'\u016B\u0300':        [0x0942],           # u macgrv
    u'\u016B\u0301':        [0x0942],           # u macac
    u'l\u0325':             [0x0962],           # l uring
    u'r\u0325':             [0x0943],           # r uring
    u'l\u0325\u0304':       [0x0963],           # l uringmac
    u'r\u0325\u0304':       [0x0944],           # r uringmac
    u'l\u0325\u0300':       [0x0962],           # l uringgrv
    u'l\u0325\u0301':       [0x0962],           # l uringac
    u'r\u0325\u0300':       [0x0943],           # r uringgrv
    u'r\u0325\u0301':       [0x0943],           # r uringac
    u'l\u0325\u0304\u0300': [0x0963],           # l uringmacgrv
    u'l\u0325\u0304\u0301': [0x0963],           # l uringmacac
    u'r\u0325\u0304\u0300': [0x0944],           # r uringmacgrv
    u'r\u0325\u0304\u0301': [0x0944],           # r uringmacac
}

INITIAL_VOWELS = {
    u'a':                   [0x0905],
    u'i':                   [0x0907],
    u'u':                   [0x0909],
    u'e':                   [0x090F],
    u'o':                   [0x0913],
    u'ai':                  [0x0910],
    u'au':                  [0x0914],
    u'\u00EA':              [0x090D],           # e circ
    u'\u00F4':              [0x0911],           # o circ
    u'\u00E3':              [0x0905, 0x0901],   # a tilde
    u'\u00F5':              [0x0913, 0x0902],   # o tilde
    u'\u0101':              [0x0906],           # a macron
    u'\u1EBD':              [0x090F, 0x0901],   # e tilde
    u'\u012B':              [0x0908],           # i macron
    u'\u016B':              [0x090A],           # u macron
    u'\u0129':              [0x0907, 0x0901],   # i tilde
    u'\u0169':              [0x0909, 0x0901],   # u tilde
    u'a\u0129':             [0x0910, 0x0902],   # ai tilde
    u'a\u0169':             [0x0914, 0x0902],   # au tilde
    u'\u0101\u0303':        [0x0906, 0x0901],   # a mactil
    u'\u012B\u0303':        [0x0908, 0x0902],   # i mactil
    u'\u016B\u0303':        [0x090A, 0x0901],   # u mactil
    u'\u0101\u0300':        [0x0906],           # a macgrv
    u'\u0101\u0301':        [0x0906],           # a macac
    u'\u012B\u0300':        [0x0908],           # i macgrv
    u'\u012B\u0301':        [0x0908],           # i macac
    u'\u016B\u0300':        [0x090A],           # u macgrv
    u'\u016B\u0301':        [0x090A],           # u macac
    u'l\u0325':             [0x090C],           # l uring
    u'r\u0325':             [0x090B],           # r uring
    u'l\u0325\u0304':       [0x0961],           # l uringmac
    u'r\u0325\u0304':       [0x0960],           # r uringmac
    u'l\u0325\u0300':       [0x090C],           # l uringgrv
    u'l\u0325\u0301':       [0x090C],           # l uringac
    u'r\u0325\u0300':       [0x090B],           # r uringgrv
    u'r\u0325\u0301':       [0x090B],           # r uringac
    u'l\u0325\u0304\u0300': [0x0961],           # l uringmacgrv
    u'l\u0325\u0304\u0301': [0x0961],           # l uringmacac
    u'r\u0325\u0304\u0300': [0x0960],           # r uringmacgrv
    u'r\u0325\u0304\u0301': [0x0960],           # r uringmacac
}

DIACRITICS = {
    u'\u1E41':              [0x0902],        # m odot (anusvāra)
    u'\u1E25':              [0x0903],        # h udot (visarga)
    u'm\u0310':             [0x0901],        # m cand (candrabhindu/anunāsika)
}

CONSONANTS = {
    u'k':                   [0x0915],
    u'q':                   [0x0958],
    u'kh':                  [0x0916],
    u'g':                   [0x0917],
    u'gh':                  [0x0918],
    u'c':                   [0x091A],
    u'ch':                  [0x091B],
    u'j':                   [0x091C],
    u'z':                   [0x095B],
    u'jh':                  [0x091D],
    u't':                   [0x0924],
    u'th':                  [0x0925],
    u'd':                   [0x0926],
    u'dh':                  [0x0927],
    u'n':                   [0x0928],
    u'p':                   [0x092A],
    u'ph':                  [0x092B],
    u'f':                   [0x095E],
    u'b':                   [0x092C],
    u'bh':                  [0x092D],
    u'm':                   [0x092E],
    u'y':                   [0x092F],
    u'r':                   [0x0930],
    u'l':                   [0x0932],
    u'v':                   [0x0935],
    u's':                   [0x0938],
    u'h':                   [0x0939],
    u'\u00F1':              [0x091E],           # n tilde
    u'\u0121':              [0x095A],           # g odot
    u'\u1E45':              [0x0919],           # n odot
    u'\u1E6D':              [0x091F],           # t udot
    u'\u1E6Dh':             [0x0920],           # th udot
    u'\u1E0D':              [0x0921],           # d udot
    u'\u1E0Dh':             [0x0922],           # dh udot
    u'\u1E5B':              [0x095C],           # r udot
    u'\u1E5Bh':             [0x095D],           # rh udot
    u'\u1E47':              [0x0923],           # n udot
    u'\u1E49':              [0x0929],           # n ubar
    u'\u1E37':              [0x0933],           # l udot
    u'\u1E3B':              [0x0934],           # l ubar
    u'\u015B':              [0x0936],           # s acute
    u'\u1E63':              [0x0937],           # s udot
    u'\u1E8F':              [0x095F],           # y odot
    u'r\u0306':             [0x0931],           # r breve
    u'k\u200D\u0331':       [0x0959],           # kh ubar
}

# remember to add the virāma if immediately after a consonant!
NUMERALS = {
    u'0':  [0x0966],
    u'1':  [0x0967],
    u'2':  [0x0968],
    u'3':  [0x0969],
    u'4':  [0x096A],
    u'5':  [0x096B],
    u'6':  [0x096C],
    u'7':  [0x096D],
    u'8':  [0x096E],
    u'9':  [0x096F],
}

VIRAMA = 0x094D
AVAGRAHA = 0x093D
ANUSVARA = 0x0902


def ur2ud(text):
    """ DOCSTRING """

    transliterables = CONSONANTS.keys() + COMBINING_VOWELS.keys() + ['']
    INITIAL_VOWELS.update(DIACRITICS)
    INITIAL_VOWELS['\''] = [AVAGRAHA]

    text = text.lower()

    state = [0]
    devanagari = []
    stop = len(text)
    i = 0

    def test_char(token):
        """ DOCSTRING """

        if token == ' \'' and state[0] == 1:
            state[0] = 0
            return True

        if token == '\' ' and state[0] == 1:
            devanagari.append(' ')
            state[0] = 0
            return True

        if token == u'\'ṁ':
            devanagari.append(
                    ''.join([unichr(int(k)) for k in [ANUSVARA, AVAGRAHA]]))
            state[0] = 0
            return True

        if token in CONSONANTS:
            if state[0] == 1:
                devanagari.append(unichr(int(VIRAMA)))
            devanagari.append(
                    ''.join([unichr(int(k)) for k in CONSONANTS[token]]))
            state[0] = 1
            return True

        if state[0] < 1 and token in INITIAL_VOWELS:
            devanagari.append(
                    ''.join([unichr(int(k)) for k in INITIAL_VOWELS[token]]))
            return True

        if state[0] == 1 and token in COMBINING_VOWELS:
            devanagari.append(
                    ''.join([unichr(int(k)) for k in COMBINING_VOWELS[token]]))
            state[0] = 0
            return True

        return False

    while (i < stop):

        token = text[i:i + 2]

        if test_char(token):
            i += 2
            continue

        token = text[i]
        if token == ' ' and (
            (state[0] == 1 and text[i + 1:i + 2] in transliterables) or
                    (state[0] < 1 and text[i + 1:i + 2] == '\'')):
            i += 1
            continue

        if token == '\'' and (text[i + 1:i + 2] not in transliterables):
            i += 1
            state[0] = 0
            continue

        if test_char(token):
            i += 1
            continue

        if state[0] == 1:
            devanagari.append(unichr(int(VIRAMA)))

        devanagari.append(token)
        state[0] = -1
        i += 1

    if state[0] == 1:
        devanagari.append(unichr(int(VIRAMA)))

    return ''.join(devanagari)


if __name__ == '__main__':
    import sys
    sys.stdout.write(ur2ud(sys.stdin.read().decode('utf-8')).encode('utf-8'))