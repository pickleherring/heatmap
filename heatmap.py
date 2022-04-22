"""Map the frequency of sex terms across a text.
"""

import pandas
import regex


with open('sex_terms.txt', encoding='utf-8') as f:
    TERMS = set(f.read().split())

SENTENCE_BREAK = regex.compile('(?<=[.?!:;])(?=\W*\s)')
WORD = regex.compile(r'\b\w+\b')

DEFAULT_WINDOW_SIZE = 200


def split_sentences(text):
    """Split a text into sentences.
    
    argument text: str text containing sentences
    
    returns: list of str
    """
    
    return [s.strip() for s in SENTENCE_BREAK.split(text)]


def get_words(text):
    """Extract words from text.
    
    argument text: str text
    
    returns: list of str lowercased words
    """

    return [w.lower() for w in WORD.findall(text)]


def count_terms(text, terms=TERMS):
    """Count target terms in a text.
    
    argument text: str text
    argument terms: set of target terms
    
    returns: int
    """
    
    return sum([(w in TERMS) for w in get_words(text)])


def smooth_counts(counts, window=DEFAULT_WINDOW_SIZE):
    """Smooth a series of counts.
    
    argument counts: list of counts
    argument window: number of counts to average over
    
    returns: pandas.Series of smoothed counts
    """
    
    counts = pandas.Series(counts)
    
    return counts.rolling(window, center=True).mean()
    

def process_text(text, terms=TERMS, window=DEFAULT_WINDOW_SIZE):
    """Run all processing steps on a text.
    
    argument text: str text
    argument terms: set of target terms
    argument window: number of sentences to average over
    
    returns: pandas.DataFrame with columns:
        pos: int ordinal position of sentence in text
        sentence: str raw text of sentence
        count: int term count
        smoothed: float smoothed term count
    """
    
    sentences = split_sentences(text)
    counts = [count_terms(s, terms=terms) for s in sentences]
    
    data = {
        'pos': range(len(sentences)),
        'sentence': sentences,
        'count': counts,
        'smoothed': smooth_counts(counts, window=window)
    }
    
    return pandas.DataFrame(data)
