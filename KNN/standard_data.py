# -*- coding: utf-8 -*-
# @Date    : 2017-04-03 16:04:19
# @Author  : Alan Lau (rlalan@outlook.com)
import reader
import fwalker
import bfile


def change_data(files, inputpath):
    trainpath = bfile.buildfile(inputpath+'\\'+'trainingDigits')
    testpath = bfile.buildfile(inputpath+'\\'+'testDigits')
    for file in files:
        ech_name = (file.split('\\'))[-2:]
        new_path = inputpath+'\\'+'\\'.join(ech_name)
        ech_content = reader.readtxt(file, 'utf8')
        new_content = []
        for ech_line in ech_content:
            line_ary = list(ech_line.replace('\n', '').replace('\r', ''))
            new_content.append(' '.join(line_ary))
        print(reader.writetxt(new_path, '\n'.join(new_content), 'utf8'))


def main():
    datapath = r'D:\DevelopmentLanguage\Python\MachineLearning\KNN\lab3_0930\digits'
    inputpath = bfile.buildfile(
        r'D:\DevelopmentLanguage\Python\MachineLearning\KNN\lab3_0930\input_digits')
    files = fwalker.fun(datapath)
    change_data(files, inputpath)

if __name__ == '__main__':
    main()
