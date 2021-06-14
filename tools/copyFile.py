import shutil


def copyFile(fileName1, fileName2):
    file1 = open(fileName1, 'r')
    file2 = open(fileName2, 'w')

    shutil.copyfileobj(file1, file2)

    file1.close()
    file2.close()
