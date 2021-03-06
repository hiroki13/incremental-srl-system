import cPickle
import gzip

import numpy as np

from vocab import UNDER_BAR, VERB


class Saver(object):
    def __init__(self, argv):
        self.argv = argv

    @staticmethod
    def save_pkl_gz_format(fn, data):
        with gzip.open(fn + '.pkl.gz', 'wb') as gf:
            cPickle.dump(data, gf, cPickle.HIGHEST_PROTOCOL)

    @staticmethod
    def save_key_value_format(fn, keys, values):
        assert len(keys) == len(values)
        if type(values[0]) is not str:
            values = map(lambda v: str(v), values)
        with open(fn + '.txt', 'w') as f:
            for key, value in zip(keys, values):
                print >> f, key.encode('utf-8') + '\t' + value.encode('utf-8')


class CoNLL09Saver(Saver):
    def save_predicted_prop(self, corpus, results, vocab_label):
        """
        :param corpus: 1D: n_sents, 2D: n_words; elem=line
        :param results: 1D: n_sents, 2D: n_prds, 3D: n_words; elem=label id
        :param vocab_label: Vocab()
        """
        argv = self.argv
        if argv.output_fn:
            fn = 'result.' + argv.output_fn + '.txt'
        else:
            fn = 'result.txt'

        assert len(corpus) == len(results), '%d %d' % (len(corpus), len(results))

        f = open(fn, 'w')
        for sent, y_pred_sent in zip(corpus, results):
            labels = [[] for _ in xrange(len(sent))]
            for y_pred_prd in y_pred_sent:
                for i, label_id in enumerate(y_pred_prd):
                    label = vocab_label.get_word(label_id)
                    label = UNDER_BAR if label == VERB else label
                    labels[i].append(label)
            for line, label in zip(sent, labels):
                text = "\t".join(line) + "\t" + "\t".join(label)
                print >> f, text
            print >> f
        f.close()

    def save_isrl_props(self, corpus):
        argv = self.argv
        if argv.output_fn:
            fn = 'conll09.isrl.' + argv.output_fn
        else:
            fn = 'conll09.isrl'

        f = open(fn + '.txt', 'w')
        for index, sent in enumerate(corpus):
            forms = " ".join(sent.forms)
            print >> f, "# %d ||| %s" % (index, forms)

            prds_gold = " ".join([str(p_index) for p_index in sent.prd_indices])
            prds_sys = " ".join([str(p_index) for p_index in sent.prd_indices_sys])
            print >> f, "PRDS ||| %s ||| %s" % (str(prds_gold), str(prds_sys))

            for p_index, props in enumerate(sent.prd_props_sys):
                for j, prop in enumerate(props):
                    print >> f, "-- %d ||| %s" % (p_index, " ".join(prop))
            print >> f
        f.close()
