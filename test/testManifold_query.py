# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import unittest

from os.path import abspath, dirname
from nlp_sum.my_sum.utils import get_stop_words
from nlp_sum.my_sum.parse.plaintext import PlaintextParser
from nlp_sum.my_sum.method.query_summarizer.manifoldrank import ManifoldRankSummarizer

from nlp_sum.test.utils_for_test import get_cn_sentence_length, get_en_sentence_length


class testLexrank(unittest.TestCase):

    def test_summarizer(self):
        summarizer_en = ManifoldRankSummarizer("english")
        summarizer_en_stem = ManifoldRankSummarizer("english", True)
        summarizer_cn = ManifoldRankSummarizer("chinese")

        data_file_path = abspath(dirname(__file__)) + '/data'
        cn_data_file_path = data_file_path + '/chinese/'
        en_data_file_path = data_file_path + '/english/'
        parser_cn = PlaintextParser("chinese")
        parser_en = PlaintextParser("english")

        document_set_cn = parser_cn.build_documentSet_from_dir(
            cn_data_file_path
        )
        document_set_en = parser_en.build_documentSet_from_dir(
            en_data_file_path
        )

        query_cn = u"科比生涯的最后一个赛季"
        query_en = "a day in the life with org"

        summarizer_cn.stop_words = get_stop_words("chinese")
        summarizer_en.stop_words = get_stop_words("english")
        summarizer_en_stem.stop_words = get_stop_words("english")

        summary_cn_mmr = summarizer_cn(document_set_cn, query_cn, 100, method="MMR")
        summary_cn_mmr_len = sum(get_cn_sentence_length(sentence) for sentence in summary_cn_mmr)
        summary_cn_mmr_text = ''.join(sentence._texts + '。' for sentence in summary_cn_mmr)

        summary_cn_default = summarizer_cn(document_set_cn, query_cn, 100, method="default")
        summary_cn_default_len = sum(get_cn_sentence_length(sentence) for sentence in summary_cn_default)
        summary_cn_default_text = ''.join(sentence._texts + '。' for sentence in summary_cn_default)

        summary_en_mmr = summarizer_en(document_set_en, query_en, 100, method="MMR")
        summary_en_mmr_len = sum(get_en_sentence_length(sentence) for sentence in summary_en_mmr)
        summary_en_mmr_text = ' '.join(sentence._texts for sentence in summary_en_mmr)

        self.assertLessEqual(summary_cn_mmr_len, 100)
        self.assertLessEqual(summary_cn_default_len, 100)
        self.assertLessEqual(summary_en_mmr_len, 100)

        print("--------------------------chinese MMR-----------------------------")
        print(summary_cn_mmr_text)
        print("the summary length is {}".format(summary_cn_mmr_len))
        print("--------------------------chinese default-----------------------------")
        print(summary_cn_default_text)
        print("the summary length is {}".format(summary_cn_default_len))
        print("--------------------------english MMR-----------------------------")
        print(summary_en_mmr_text)
        print("the summary length is {}".format(summary_en_mmr_len))
