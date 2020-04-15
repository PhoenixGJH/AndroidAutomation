# coding:utf-8
import os
import sys
import platform


class RemoveTagFile(object):
    path = None

    def removeFile(self, path, remove_list, jump_list):  # path后面要跟/
        self.path = path
        system_test = platform.system()
        if(system_test == 'Windows'):
            path_last = self.path[-1]
            if(path_last != '\\'):
                self.path = self.path+'\\'
        elif(system_test == 'Linux'):
            path_last = self.path[-1]
            if (path_last != '/'):
                self.path = self.path + '/'

        self.remove_file(self.path, self.eachFile(self.path))

    def remove_file(self, path, file_list):
        for filename in file_list:
            dirOrFile = path + filename
            if(os.path.exists(dirOrFile)):  # 判断文件是否存在
                if(filename in jump_list):  # 判断是否是需要跳过的文件或文件夹
                    print("jump: " + dirOrFile)
                    continue

                if(filename in remove_list):    # 如果在移除列表则移除
                    if(os.path.isdir(dirOrFile)):
                        print("delDir: " + dirOrFile)
                        self.del_file(dirOrFile)
                        self.del_dir(dirOrFile)
                    else:
                        if(os.path.exists(dirOrFile)):
                            print("delFile: " + dirOrFile)
                            os.remove(dirOrFile)
                else:   #没有在移除列表：如果是文件就跳过，是文件夹则进入
                    if(os.path.isdir(dirOrFile)):
                        self.remove_file(dirOrFile + "\\", self.eachFile(dirOrFile + "\\"))
            else:
                print(dirOrFile + ' is not exist!')

    def del_file(self, path):  # 递归删除目录及其子目录下的文件
        for i in os.listdir(path):
            path_file = os.path.join(path, i)  # 取文件绝对路径
            if os.path.isfile(path_file):  # 判断是否是文件
                os.remove(path_file)
            else:
                self.del_file(path_file)

    def del_dir(self, path):  # 删除文件夹
        listDirs = os.listdir(path)
        if not listDirs:    # 空文件夹直接删除
            os.removedirs(path)
            return
        for j in os.listdir(path):
            path_file = os.path.join(path, j)  # 取文件绝对路径
            if not os.listdir(path_file):  # 判断文件如果为空
                os.removedirs(path_file)  # 则删除该空文件夹，如果不为空删除会报异常
            else:
                self.del_dir(path_file)

    def eachFile(self, filepath):  # 获取目录下所有文件的名称
        pathDir = os.listdir(filepath)
        list = []
        for allDir in pathDir:
            child = os.path.join('%s%s' % (filepath, allDir))
            fileName = child.replace(filepath, '')
            list.append(fileName)
        return list


if __name__ == '__main__':
    rtf = RemoveTagFile()
    # 以下表示只删除D:\Test\目录下的a文件夹、a.txt文件、b.txt文件
    """
    规则：
    1、remove_list: 需要删除的文件夹
    2、jump_list：需要跳过的文件夹
    """

    path = 'F:\github\Android\AmazingAvatar'
    remove_list = ['build', '.gradle', '.idea', 'bb.txt']  # 要删除的文件名称
    jump_list = ['.git', 'gradle', 'src', 'libs']  # 要保留的文件名称
    rtf.removeFile(path, remove_list, jump_list)
