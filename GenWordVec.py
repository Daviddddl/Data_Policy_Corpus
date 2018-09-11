import word2vec
import LTPez

vec_model_path = './data/corpusWord2Vec.bin'
tmp_file_path = './data/tmp.txt'


def genWord4Vec(content):
    with open(tmp_file_path, 'w+') as f:
        f.write(content)
    word2vec.word2vec(tmp_file_path, vec_model_path, size=300, verbose=True)


if __name__ == '__main__':

    LTPez.LTP_parse_content()
    genWord4Vec('大家 好！')
    model = word2vec.load(vec_model_path)
    print(model.vectors)
    indexes = model.cosine(u'我')
    for index in indexes[0]:
        print(model.vocab[index])
