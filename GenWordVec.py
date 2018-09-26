import word2vec
import LTPez
import os

vec_model_path = './vec_res/corpusWord2Vec.bin'
tmp_file_path = './tmp_vec.txt'
# rootdir = './ltp_res'
rootdir = './nega_webs'

def genVecFromStr(content):
    with open(tmp_file_path, 'w+') as f:
        f.write(content)
    word2vec.word2vec(tmp_file_path, vec_model_path, size=300, verbose=True)


def genVecFromFile(file):
    word2vec.word2vec(file, vec_model_path, size=300, verbose=True)


if __name__ == '__main__':

    files_list = os.listdir(rootdir)
    for line in files_list:
        filepath = os.path.join(rootdir, line)
        if os.path.isdir(filepath):
            print("dir:" + filepath)
        if os.path.isfile(filepath):
            # if 'context' in filepath:
            #     print("file:" + filepath)
                # vec_model_path = './vec_res/' + filepath[10:-4] + '_vec.bin'
                # genVecFromFile(filepath)
                # model = word2vec.load(vec_model_path)
                # print(vec_model_path)
            print("file:" + filepath[10:-16] + filepath[-10:-4])
