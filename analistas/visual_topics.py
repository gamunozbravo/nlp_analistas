# coding: utf-8
"""Modulo para visualizar topicos."""
import datetime
import logging
import os
import sys

from gensim import corpora
from gensim.models.ldamodel import LdaModel
import pyLDAvis
import pyLDAvis.gensim as gvis


def topic_data(n, tipo, dirin, ng):
    """
    Prepara data para visualizacion de topicos

    :param n: int (numero de topicos)
    :param tipo: str (label de tipo de sentimiento)
    :param dirin: str (directorio de entrada)
    :param ng: str (uni, bi, tri, phrase)

    :return: PreparedData
    """
    dictf = os.path.join(dirin, 'dict-{}-{}gram.dict'.format(tipo, ng))
    dictionary = corpora.Dictionary.load(dictf)
    strfmt = 'Diccionario con {} tokens cargado'.format(len(dictionary.keys()))
    logging.info(strfmt)

    bowmm = os.path.join(dirin, 'bow-{}-{}gram.mm'.format(tipo, ng))
    bowcorpus = corpora.MmCorpus(bowmm)

    ldaf = os.path.join(dirin, 'model-{}-{}-{}gram.lda'.format(n, tipo, ng))
    ldamodel = LdaModel.load(ldaf)

    data = gvis.prepare(ldamodel, bowcorpus, dictionary)

    return data


def main():
    """Unificar en main para poder ejecutar despues desde otro script."""
    corrida = "{:%Y-%m-%d-%H%M%S}".format(datetime.datetime.now())

    dir_curr = os.path.abspath('.')
    dir_topi = os.path.join(dir_curr, 'topics', 'es')
    dir_output = os.path.join(dir_curr, 'visuals')
    dir_logs = os.path.join(dir_output, 'logs')
    os.makedirs(dir_logs, exist_ok=True)

    logfile = os.path.join(dir_logs, '{}.log'.format(corrida))
    log_format = '%(asctime)s : %(levelname)s : %(message)s'
    log_datefmt = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(format=log_format, datefmt=log_datefmt,
                        level=logging.INFO, filename=logfile, filemode='w')

    cmds = sys.argv
    nc = len(cmds)
    if nc == 1:
        tipo = 'todos'
    else:
        tipo = cmds[1]

    # visualizacion de topicos
    for n in (5, 10, 20, 40):
        for ng in ('uni', 'bi', 'tri', 'phrase'):
            data = topic_data(n=n, tipo=tipo, dirin=dir_topi, ng=ng)
            strfmt = 'topics-{}-{}-{}gram.html'.format(n, tipo, ng)
            html = os.path.join(dir_output, strfmt)
            pyLDAvis.save_html(data, html)


if __name__ == '__main__':
    main()
