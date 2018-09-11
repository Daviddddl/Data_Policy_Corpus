import logging, argparse, sys
from gensim import corpora, models, similarities


def similarity(datapath, querypath, respath):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    class MyCorpus(object):
        def __iter__(self):
            for line in open(datapath):
                yield line.split()

    Corp = MyCorpus()
    dictionary = corpora.Dictionary(Corp)
    corpus = [dictionary.doc2bow(text) for text in Corp]

    tfidf = models.TfidfModel(corpus)

    corpus_tfidf = tfidf[corpus]

    q_file = open(querypath, 'r')
    query = q_file.readline()
    q_file.close()
    vec_bow = dictionary.doc2bow(query.split())
    vec_tfidf = tfidf[vec_bow]

    index = similarities.MatrixSimilarity(corpus_tfidf)
    sims = index[vec_tfidf]

    similarity = list(sims)

    sim_file = open(respath, 'w')
    for i in similarity:
        sim_file.write(str(i) + '\n')
    sim_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='计算文本相似度 工具， 制作者David_狄')
    parser.add_argument('-d', '--datapath', help="The path of doc which need to be calculated.")
    parser.add_argument('-q', '--querypath', help="The path of doc which is standard.")
    parser.add_argument('-r', '--resultpath', help="The path of saved result")
    ARGS = parser.parse_args()

    if ARGS.datapath is not None and ARGS.querypath is not None and ARGS.resultpath is not None:
        similarity(ARGS.datapath, ARGS.querypath, ARGS.resultpath)
    else:
        parser.print_help()
        sys.exit(1)
