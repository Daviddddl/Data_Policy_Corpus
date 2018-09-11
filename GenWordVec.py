import word2vec
import LTPez

vec_model_path = './data/corpusWord2Vec.bin'
tmp_file_path = './data/tmp.txt'


def genVecFromStr(content):
    with open(tmp_file_path, 'w+') as f:
        f.write(content)
    word2vec.word2vec(tmp_file_path, vec_model_path, size=300, verbose=True)


def genVecFromFile(file):
    word2vec.word2vec(file, vec_model_path, size=300, verbose=True)


if __name__ == '__main__':

    genVecFromFile('./data/ltpres.txt')
    model = word2vec.load(vec_model_path)
    print(model.vectors)
