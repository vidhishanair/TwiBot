"""A Centrality Summarizer"""

import os
from nltk import tokenize
from utils import *


def centrality(vects):
    """Calculate the centralities of each vector."""

    n = len(vects)

    # For each vector, find the average similarity to all the other
    # vectors. Use reference equality to avoid comparing with self.
    return [(sum([cosine_sim(vect, vect1)
                  for vect1 in vects
                  if vect is not vect1])
             / n)
            for vect in vects]


def gen_centrality_summary(orig_sents, max_words):
    """Given a list of *untokenized* sentences and a threshold summary
    length (in words), return an ordered list of sentences comprising
    the summary."""
    tok_sents = [tokenize.word_tokenize(orig_sent)
                 for orig_sent in orig_sents]
    # TODO: Remove funcwords, etc?
    feat_space = sorted(set().union(*tok_sents))
    vects = [binary_vectorize(feat_space, tok_sent)
             for tok_sent in tok_sents]
    return gen_summary_from_rankings(centrality(vects), tok_sents,
                                     orig_sents, max_words)


def gen_summary_from_rankings(score, tok_sents, orig_sents, max_words):
    ranked_sents = sorted(zip(score, tok_sents, orig_sents), reverse=True)
    summary, tok_summary = [], []
    word_count = 0

    for score, tok_sent, orig_sent in ranked_sents:
        #print tok_sent
        if word_count >= max_words:
            break
        #print(tok_sent,len(tok_sent), is_valid_sent_len(tok_sent))
        if (is_valid_sent_len(tok_sent) and
            not is_repeat(tok_sent, tok_summary)):
            print "hello"
            summary.append(orig_sent)
            tok_summary.append(tok_sent)
            word_count += len(tok_sent)

    return summary    


