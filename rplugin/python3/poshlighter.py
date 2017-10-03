#!~/.venv/vim-poshlighter/bin/python3

from spacy.en import English
import neovim

HIGHLIGHT_LINKS = {
    'adj': 'Type', # adjective
    #'adp': FIXME # preposition
    'adv': 'Identifier', # adverb
    #'cconj': FIXME # conjunction
    #'det': FIXME # determiner
    'noun': 'Operator', # noun
    #'num': FIXME # number
    'part': 'Special', # particle, possessives
    #'pron': FIXME # pronoun
    'propn': 'Constant', # proper noun
    #'punct': FIXME # punctuation
    'verb': 'Function', # verb
}

nlp = English(entity=False)

@neovim.plugin
class POSHlighter(object):
    def __init__(self, vim):
        self.vim = vim

    @neovim.function('Verb')
    def verb(self, allowed_pos=None):
        if allowed_pos is None:
            allowed_pos = set(['verb'])
        # clear current syntax
        self.vim.command('syntax clear')
        # set up syntax highlight links
        for pos in allowed_pos:
            if pos in HIGHLIGHT_LINKS:
                self.vim.command('highlight link {} {}\n'.format(pos, HIGHLIGHT_LINKS[pos]))
        # tag current file
        for line_num, line in enumerate(self.vim.current.buffer, start=1):
            doc = nlp(line)
            for sentence in doc.sents:
                for word in sentence:
                    pos = word.pos_.lower()
                    if pos not in allowed_pos:
                        continue
                    start_regex = r'\%{}l\%{}c'.format(line_num, word.idx + 1)
                    end_regex = r'\%{}l\%{}c'.format(line_num, word.idx + len(word) + 1)
                    syntax_line = "syntax region {} start='{}' end='{}' oneline".format(pos, start_regex, end_regex)
                    self.vim.command(syntax_line)
