# To make this file, I started with the NLTK PTB tokenizer. Then did the following.
#      - I commented out lines of code that call parts of the NLTK API and copied in the code that is loaded from other files
#      - This process makes a file that runs the PTB tokenizer as a single Python file, using the NLTK implementation
#      - I made this file on Oct 14, 2020 and don't update it based on any changes in NLTK since then


######################################################################################################

# Natural Language Toolkit: Tokenizers
#
# Copyright (C) 2001-2020 NLTK Project
# Author: Edward Loper <edloper@gmail.com>
#         Michael Heilman <mheilman@cmu.edu> (re-port from http://www.cis.upenn.edu/~treebank/tokenizer.sed)
#
# URL: <http://nltk.sourceforge.net>
# For license information, see LICENSE.TXT


r"""

Penn Treebank Tokenizer

The Treebank tokenizer uses regular expressions to tokenize text as in Penn Treebank.
This implementation is a port of the tokenizer sed script written by Robert McIntyre
and available at http://www.cis.upenn.edu/~treebank/tokenizer.sed.
"""

import re

from abc import ABC, abstractmethod

# from nltk.tokenize.destructive import MacIntyreContractions 

class MacIntyreContractions:
    """
    List of contractions adapted from Robert MacIntyre's tokenizer.
    """

    CONTRACTIONS2 = [
        r"(?i)\b(can)(?#X)(not)\b",
        r"(?i)\b(d)(?#X)('ye)\b",
        r"(?i)\b(gim)(?#X)(me)\b",
        r"(?i)\b(gon)(?#X)(na)\b",
        r"(?i)\b(got)(?#X)(ta)\b",
        r"(?i)\b(lem)(?#X)(me)\b",
        r"(?i)\b(mor)(?#X)('n)\b",
        r"(?i)\b(wan)(?#X)(na)\s",
    ]
    CONTRACTIONS3 = [r"(?i) ('t)(?#X)(is)\b", r"(?i) ('t)(?#X)(was)\b"]
    CONTRACTIONS4 = [r"(?i)\b(whad)(dd)(ya)\b", r"(?i)\b(wha)(t)(cha)\b"]

#from nltk.tokenize.api import TokenizerI

class TokenizerI(ABC):
    """
    A processing interface for tokenizing a string.
    Subclasses must define ``tokenize()`` or ``tokenize_sents()`` (or both).
    """

    @abstractmethod
    def tokenize(self, s):
        """
        Return a tokenized copy of *s*.
        :rtype: list of str
        """
        if overridden(self.tokenize_sents):
            return self.tokenize_sents([s])[0]

    def span_tokenize(self, s):
        """
        Identify the tokens using integer offsets ``(start_i, end_i)``,
        where ``s[start_i:end_i]`` is the corresponding token.
        :rtype: iter(tuple(int, int))
        """
        raise NotImplementedError()

    def tokenize_sents(self, strings):
        """
        Apply ``self.tokenize()`` to each element of ``strings``.  I.e.:
            return [self.tokenize(s) for s in strings]
        :rtype: list(list(str))
        """
        return [self.tokenize(s) for s in strings]

    def span_tokenize_sents(self, strings):
        """
        Apply ``self.span_tokenize()`` to each element of ``strings``.  I.e.:
            return [self.span_tokenize(s) for s in strings]
        :rtype: iter(list(tuple(int, int)))
        """
        for s in strings:
            yield list(self.span_tokenize(s))


#from nltk.tokenize.util import align_tokens

def align_tokens(tokens, sentence):
    """
    This module attempt to find the offsets of the tokens in *s*, as a sequence
    of ``(start, end)`` tuples, given the tokens and also the source string.
        >>> from nltk.tokenize import TreebankWordTokenizer
        >>> from nltk.tokenize.util import align_tokens
        >>> s = str("The plane, bound for St Petersburg, crashed in Egypt's "
        ... "Sinai desert just 23 minutes after take-off from Sharm el-Sheikh "
        ... "on Saturday.")
        >>> tokens = TreebankWordTokenizer().tokenize(s)
        >>> expected = [(0, 3), (4, 9), (9, 10), (11, 16), (17, 20), (21, 23),
        ... (24, 34), (34, 35), (36, 43), (44, 46), (47, 52), (52, 54),
        ... (55, 60), (61, 67), (68, 72), (73, 75), (76, 83), (84, 89),
        ... (90, 98), (99, 103), (104, 109), (110, 119), (120, 122),
        ... (123, 131), (131, 132)]
        >>> output = list(align_tokens(tokens, s))
        >>> len(tokens) == len(expected) == len(output)  # Check that length of tokens and tuples are the same.
        True
        >>> expected == list(align_tokens(tokens, s))  # Check that the output is as expected.
        True
        >>> tokens == [s[start:end] for start, end in output]  # Check that the slices of the string corresponds to the tokens.
        True
    :param tokens: The list of strings that are the result of tokenization
    :type tokens: list(str)
    :param sentence: The original string
    :type sentence: str
    :rtype: list(tuple(int,int))
    """
    point = 0
    offsets = []
    for token in tokens:
        try:
            start = sentence.index(token, point)
        except ValueError as e:
            raise ValueError(
                'substring "{}" not found in "{}"'.format(token, sentence)
            ) from e
        point = start + len(token)
        offsets.append((start, point))
    return offsets





class TreebankWordTokenizer(TokenizerI):
    r"""
    The Treebank tokenizer uses regular expressions to tokenize text as in Penn Treebank.
    This is the method that is invoked by ``word_tokenize()``.  It assumes that the
    text has already been segmented into sentences, e.g. using ``sent_tokenize()``.

    This tokenizer performs the following steps:

    - split standard contractions, e.g. ``don't`` -> ``do n't`` and ``they'll`` -> ``they 'll``
    - treat most punctuation characters as separate tokens
    - split off commas and single quotes, when followed by whitespace
    - separate periods that appear at the end of line

        >>> from nltk.tokenize import TreebankWordTokenizer
        >>> s = '''Good muffins cost $3.88\nin New York.  Please buy me\ntwo of them.\nThanks.'''
        >>> TreebankWordTokenizer().tokenize(s)
        ['Good', 'muffins', 'cost', '$', '3.88', 'in', 'New', 'York.', 'Please', 'buy', 'me', 'two', 'of', 'them.', 'Thanks', '.']
        >>> s = "They'll save and invest more."
        >>> TreebankWordTokenizer().tokenize(s)
        ['They', "'ll", 'save', 'and', 'invest', 'more', '.']
        >>> s = "hi, my name can't hello,"
        >>> TreebankWordTokenizer().tokenize(s)
        ['hi', ',', 'my', 'name', 'ca', "n't", 'hello', ',']
    """

    # starting quotes
    STARTING_QUOTES = [
        (re.compile(r"^\""), r"``"),
        (re.compile(r"(``)"), r" \1 "),
        (re.compile(r"([ \(\[{<])(\"|\'{2})"), r"\1 `` "),
    ]

    # punctuation
    PUNCTUATION = [
        (re.compile(r"([:,])([^\d])"), r" \1 \2"),
        (re.compile(r"([:,])$"), r" \1 "),
        (re.compile(r"\.\.\."), r" ... "),
        (re.compile(r"[;@#$%&]"), r" \g<0> "),
        (
            re.compile(r'([^\.])(\.)([\]\)}>"\']*)\s*$'),
            r"\1 \2\3 ",
        ),  # Handles the final period.
        (re.compile(r"[?!]"), r" \g<0> "),
        (re.compile(r"([^'])' "), r"\1 ' "),
    ]

    # Pads parentheses
    PARENS_BRACKETS = (re.compile(r"[\]\[\(\)\{\}\<\>]"), r" \g<0> ")

    # Optionally: Convert parentheses, brackets and converts them to PTB symbols.
    CONVERT_PARENTHESES = [
        (re.compile(r"\("), "-LRB-"),
        (re.compile(r"\)"), "-RRB-"),
        (re.compile(r"\["), "-LSB-"),
        (re.compile(r"\]"), "-RSB-"),
        (re.compile(r"\{"), "-LCB-"),
        (re.compile(r"\}"), "-RCB-"),
    ]

    DOUBLE_DASHES = (re.compile(r"--"), r" -- ")

    # ending quotes
    ENDING_QUOTES = [
        (re.compile(r'"'), " '' "),
        (re.compile(r"(\S)(\'\')"), r"\1 \2 "),
        (re.compile(r"([^' ])('[sS]|'[mM]|'[dD]|') "), r"\1 \2 "),
        (re.compile(r"([^' ])('ll|'LL|'re|'RE|'ve|'VE|n't|N'T) "), r"\1 \2 "),
    ]

    # List of contractions adapted from Robert MacIntyre's tokenizer.
    _contractions = MacIntyreContractions()
    CONTRACTIONS2 = list(map(re.compile, _contractions.CONTRACTIONS2))
    CONTRACTIONS3 = list(map(re.compile, _contractions.CONTRACTIONS3))

    def tokenize(self, text, convert_parentheses=False, return_str=False):
        for regexp, substitution in self.STARTING_QUOTES:
            text = regexp.sub(substitution, text)

        for regexp, substitution in self.PUNCTUATION:
            text = regexp.sub(substitution, text)

        # Handles parentheses.
        regexp, substitution = self.PARENS_BRACKETS
        text = regexp.sub(substitution, text)
        # Optionally convert parentheses
        if convert_parentheses:
            for regexp, substitution in self.CONVERT_PARENTHESES:
                text = regexp.sub(substitution, text)

        # Handles double dash.
        regexp, substitution = self.DOUBLE_DASHES
        text = regexp.sub(substitution, text)

        # add extra space to make things easier
        text = " " + text + " "

        for regexp, substitution in self.ENDING_QUOTES:
            text = regexp.sub(substitution, text)

        for regexp in self.CONTRACTIONS2:
            text = regexp.sub(r" \1 \2 ", text)
        for regexp in self.CONTRACTIONS3:
            text = regexp.sub(r" \1 \2 ", text)

        # We are not using CONTRACTIONS4 since
        # they are also commented out in the SED scripts
        # for regexp in self._contractions.CONTRACTIONS4:
        #     text = regexp.sub(r' \1 \2 \3 ', text)

        return text if return_str else text.split()

    def span_tokenize(self, text):
        r"""
        Uses the post-hoc nltk.tokens.align_tokens to return the offset spans.

            >>> from nltk.tokenize import TreebankWordTokenizer
            >>> s = '''Good muffins cost $3.88\nin New (York).  Please (buy) me\ntwo of them.\n(Thanks).'''
            >>> expected = [(0, 4), (5, 12), (13, 17), (18, 19), (19, 23),
            ... (24, 26), (27, 30), (31, 32), (32, 36), (36, 37), (37, 38),
            ... (40, 46), (47, 48), (48, 51), (51, 52), (53, 55), (56, 59),
            ... (60, 62), (63, 68), (69, 70), (70, 76), (76, 77), (77, 78)]
            >>> list(TreebankWordTokenizer().span_tokenize(s)) == expected
            True
            >>> expected = ['Good', 'muffins', 'cost', '$', '3.88', 'in',
            ... 'New', '(', 'York', ')', '.', 'Please', '(', 'buy', ')',
            ... 'me', 'two', 'of', 'them.', '(', 'Thanks', ')', '.']
            >>> [s[start:end] for start, end in TreebankWordTokenizer().span_tokenize(s)] == expected
            True

            Additional example
            >>> from nltk.tokenize import TreebankWordTokenizer
            >>> s = '''I said, "I'd like to buy some ''good muffins" which cost $3.88\n each in New (York)."'''
            >>> expected = [(0, 1), (2, 6), (6, 7), (8, 9), (9, 10), (10, 12),
            ... (13, 17), (18, 20), (21, 24), (25, 29), (30, 32), (32, 36),
            ... (37, 44), (44, 45), (46, 51), (52, 56), (57, 58), (58, 62),
            ... (64, 68), (69, 71), (72, 75), (76, 77), (77, 81), (81, 82),
            ... (82, 83), (83, 84)]
            >>> list(TreebankWordTokenizer().span_tokenize(s)) == expected
            True
            >>> expected = ['I', 'said', ',', '"', 'I', "'d", 'like', 'to',
            ... 'buy', 'some', "''", "good", 'muffins', '"', 'which', 'cost',
            ... '$', '3.88', 'each', 'in', 'New', '(', 'York', ')', '.', '"']
            >>> [s[start:end] for start, end in TreebankWordTokenizer().span_tokenize(s)] == expected
            True

        """
        raw_tokens = self.tokenize(text)

        # Convert converted quotes back to original double quotes
        # Do this only if original text contains double quote(s) or double
        # single-quotes (because '' might be transformed to `` if it is
        # treated as starting quotes).
        if ('"' in text) or ("''" in text):
            # Find double quotes and converted quotes
            matched = [m.group() for m in re.finditer(r"``|'{2}|\"", text)]

            # Replace converted quotes back to double quotes
            tokens = [
                matched.pop(0) if tok in ['"', "``", "''"] else tok
                for tok in raw_tokens
            ]
        else:
            tokens = raw_tokens

        for tok in align_tokens(tokens, text):
            yield tok


class TreebankWordDetokenizer(TokenizerI):
    r"""
    The Treebank detokenizer uses the reverse regex operations corresponding to
    the Treebank tokenizer's regexes.

    Note:
    - There're additional assumption mades when undoing the padding of [;@#$%&]
      punctuation symbols that isn't presupposed in the TreebankTokenizer.
    - There're additional regexes added in reversing the parentheses tokenization,
       - the r'([\]\)\}\>])\s([:;,.])' removes the additional right padding added
         to the closing parentheses precedding [:;,.].
    - It's not possible to return the original whitespaces as they were because
      there wasn't explicit records of where '\n', '\t' or '\s' were removed at
      the text.split() operation.

        >>> from nltk.tokenize.treebank import TreebankWordTokenizer, TreebankWordDetokenizer
        >>> s = '''Good muffins cost $3.88\nin New York.  Please buy me\ntwo of them.\nThanks.'''
        >>> d = TreebankWordDetokenizer()
        >>> t = TreebankWordTokenizer()
        >>> toks = t.tokenize(s)
        >>> d.detokenize(toks)
        'Good muffins cost $3.88 in New York. Please buy me two of them. Thanks.'

    The MXPOST parentheses substitution can be undone using the `convert_parentheses`
    parameter:

    >>> s = '''Good muffins cost $3.88\nin New (York).  Please (buy) me\ntwo of them.\n(Thanks).'''
    >>> expected_tokens = ['Good', 'muffins', 'cost', '$', '3.88', 'in',
    ... 'New', '-LRB-', 'York', '-RRB-', '.', 'Please', '-LRB-', 'buy',
    ... '-RRB-', 'me', 'two', 'of', 'them.', '-LRB-', 'Thanks', '-RRB-', '.']
    >>> expected_tokens == t.tokenize(s, convert_parentheses=True)
    True
    >>> expected_detoken = 'Good muffins cost $3.88 in New (York). Please (buy) me two of them. (Thanks).'
    >>> expected_detoken == d.detokenize(t.tokenize(s, convert_parentheses=True), convert_parentheses=True)
    True

    During tokenization it's safe to add more spaces but during detokenization,
    simply undoing the padding doesn't really help.

    - During tokenization, left and right pad is added to [!?], when
      detokenizing, only left shift the [!?] is needed.
      Thus (re.compile(r'\s([?!])'), r'\g<1>')

    - During tokenization [:,] are left and right padded but when detokenizing,
      only left shift is necessary and we keep right pad after comma/colon
      if the string after is a non-digit.
      Thus (re.compile(r'\s([:,])\s([^\d])'), r'\1 \2')

    >>> from nltk.tokenize.treebank import TreebankWordDetokenizer
    >>> toks = ['hello', ',', 'i', 'ca', "n't", 'feel', 'my', 'feet', '!', 'Help', '!', '!']
    >>> twd = TreebankWordDetokenizer()
    >>> twd.detokenize(toks)
    "hello, i can't feel my feet! Help!!"

    >>> toks = ['hello', ',', 'i', "can't", 'feel', ';', 'my', 'feet', '!',
    ... 'Help', '!', '!', 'He', 'said', ':', 'Help', ',', 'help', '?', '!']
    >>> twd.detokenize(toks)
    "hello, i can't feel; my feet! Help!! He said: Help, help?!"
    """

    _contractions = MacIntyreContractions()
    CONTRACTIONS2 = [
        re.compile(pattern.replace("(?#X)", r"\s"))
        for pattern in _contractions.CONTRACTIONS2
    ]
    CONTRACTIONS3 = [
        re.compile(pattern.replace("(?#X)", r"\s"))
        for pattern in _contractions.CONTRACTIONS3
    ]

    # ending quotes
    ENDING_QUOTES = [
        (re.compile(r"([^' ])\s('ll|'LL|'re|'RE|'ve|'VE|n't|N'T) "), r"\1\2 "),
        (re.compile(r"([^' ])\s('[sS]|'[mM]|'[dD]|') "), r"\1\2 "),
        (re.compile(r"(\S)(\'\')"), r"\1\2 "),
        (re.compile(r" '' "), '"'),
    ]

    # Handles double dashes
    DOUBLE_DASHES = (re.compile(r" -- "), r"--")

    # Optionally: Convert parentheses, brackets and converts them from PTB symbols.
    CONVERT_PARENTHESES = [
        (re.compile("-LRB-"), "("),
        (re.compile("-RRB-"), ")"),
        (re.compile("-LSB-"), "["),
        (re.compile("-RSB-"), "]"),
        (re.compile("-LCB-"), "{"),
        (re.compile("-RCB-"), "}"),
    ]

    # Undo padding on parentheses.
    PARENS_BRACKETS = [
        (re.compile(r"\s([\[\(\{\<])\s"), r" \g<1>"),
        (re.compile(r"\s([\]\)\}\>])\s"), r"\g<1> "),
        (re.compile(r"([\]\)\}\>])\s([:;,.])"), r"\1\2"),
    ]

    # punctuation
    PUNCTUATION = [
        (re.compile(r"([^'])\s'\s"), r"\1' "),
        (re.compile(r"\s([?!])"), r"\g<1>"),  # Strip left pad for [?!]
        # (re.compile(r'\s([?!])\s'), r'\g<1>'),
        (re.compile(r'([^\.])\s(\.)([\]\)}>"\']*)\s*$'), r"\1\2\3"),
        # When tokenizing, [;@#$%&] are padded with whitespace regardless of
        # whether there are spaces before or after them.
        # But during detokenization, we need to distinguish between left/right
        # pad, so we split this up.
        (re.compile(r"\s([#$])\s"), r" \g<1>"),  # Left pad.
        (re.compile(r"\s([;%])\s"), r"\g<1> "),  # Right pad.
        (re.compile(r"\s([&*])\s"), r" \g<1> "),  # Unknown pad.
        (re.compile(r"\s\.\.\.\s"), r"..."),
        (re.compile(r"\s([:,])\s$"), r"\1"),
        (
            re.compile(r"\s([:,])\s([^\d])"),
            r"\1 \2",
        )  # Keep right pad after comma/colon before non-digits.
        # (re.compile(r'\s([:,])\s([^\d])'), r'\1\2')
    ]

    # starting quotes
    STARTING_QUOTES = [
        (re.compile(r"([ (\[{<])\s``"), r'\1"'),
        (re.compile(r"\s(``)\s"), r"\1"),
        (re.compile(r"^``"), r"\""),
    ]

    def tokenize(self, tokens, convert_parentheses=False):
        """
        Treebank detokenizer, created by undoing the regexes from
        the TreebankWordTokenizer.tokenize.

        :param tokens: A list of strings, i.e. tokenized text.
        :type tokens: list(str)
        :return: str
        """
        text = " ".join(tokens)
        # Reverse the contractions regexes.
        # Note: CONTRACTIONS4 are not used in tokenization.
        for regexp in self.CONTRACTIONS3:
            text = regexp.sub(r"\1\2", text)
        for regexp in self.CONTRACTIONS2:
            text = regexp.sub(r"\1\2", text)

        # Reverse the regexes applied for ending quotes.
        for regexp, substitution in self.ENDING_QUOTES:
            text = regexp.sub(substitution, text)

        # Undo the space padding.
        text = text.strip()

        # Reverse the padding on double dashes.
        regexp, substitution = self.DOUBLE_DASHES
        text = regexp.sub(substitution, text)

        if convert_parentheses:
            for regexp, substitution in self.CONVERT_PARENTHESES:
                text = regexp.sub(substitution, text)

        # Reverse the padding regexes applied for parenthesis/brackets.
        for regexp, substitution in self.PARENS_BRACKETS:
            text = regexp.sub(substitution, text)

        # Reverse the regexes applied for punctuations.
        for regexp, substitution in self.PUNCTUATION:
            text = regexp.sub(substitution, text)

        # Reverse the regexes applied for starting quotes.
        for regexp, substitution in self.STARTING_QUOTES:
            text = regexp.sub(substitution, text)

        return text.strip()

    def detokenize(self, tokens, convert_parentheses=False):
        """ Duck-typing the abstract *tokenize()*."""
        return self.tokenize(tokens, convert_parentheses)

if __name__ == "__main__":

    tok = TreebankWordTokenizer()
    tok.tokenize("Hello this is a tokenizer")