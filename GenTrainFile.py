import os
import word2vec


rootdir = './vec_neg'


if __name__ == '__main__':
    files_list = os.listdir(rootdir)
    file_set = set()
    f = open('./train_data.txt', 'w+')
    for each_file in files_list:
        filepath = os.path.join(rootdir, each_file)

        if os.path.isdir(filepath):
            print("dir:" + filepath)
        if os.path.isfile(filepath):
            # print(filepath)
            # print(filepath.split('_')[1][4:])
            # file_set.add(filepath)  # 787 1418
            f.write()

    print(len(file_set))