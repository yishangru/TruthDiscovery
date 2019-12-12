import os
import collections

# maintain ISBN_10, ISBN_13, authors, seller, used, publish_date, price, main-category, categories
def preprocess_for_book(datadirectory, writedirectory, requiredAttributes, combineName):
    # reduce not necessary attributes
    fileList = os.listdir(datadirectory)
    DataWriteFile = open(file=os.path.abspath(os.path.join(writedirectory, combineName + "inter")), mode="w", encoding="utf-8")
    BookCategoryDict = collections.defaultdict(lambda: collections.defaultdict(int))
    for data in range(len(fileList)):
        category = str(fileList[data].split(".")[0])  # get the catgeory of data
        dataLines = open(file=os.path.join(datadirectory, fileList[data]), mode="r", encoding="utf-8").readlines()
        if data == 0:
            dataReadLine = dataLines[0].strip("\n").split("\t")
            DataWriteFile.write("\t".join([dataReadLine[requiredAttribute] for requiredAttribute in requiredAttributes]) + "\t" + "category" + "\n")
        for i in range(1, len(dataLines)):
            dataReadLine = dataLines[i].strip("\n").split("\t")
            BookCategoryDict[int(dataReadLine[1])][category] += 1
            DataWriteFile.write("\t".join([dataReadLine[requiredAttribute] for requiredAttribute in requiredAttributes]) + "\t" + category + "\n")
    DataWriteFile.close()

    # add category information for book
    DataReadFile = open(file=os.path.abspath(os.path.join(writedirectory, combineName + "inter")), mode="r", encoding="utf-8")
    BookInfoLines = DataReadFile.readlines()
    DataWriteFile = open(file=os.path.abspath(os.path.join(writedirectory, combineName)), mode="w", encoding="utf-8")
    BookInfoLines[0] = BookInfoLines[0].strip("\n") + "\t" + "main_category" + "\n"
    for i in range(1, len(BookInfoLines)):
        main_category = max(BookCategoryDict[int(BookInfoLines[i].split()[1])], key=(lambda x: BookCategoryDict[int(BookInfoLines[i].split()[1])][x]))
        BookInfoLines[i] = BookInfoLines[i].strip("\n") + "\t" + main_category + "\n"
    DataWriteFile.writelines(BookInfoLines)
    DataWriteFile.close()
    DataReadFile.close()
    os.remove(os.path.abspath(os.path.join(writedirectory, combineName + "inter")))

# maintain title, genre, source, year, director
def preprocess_for_movie(dataPath, writedirectory, requiredAttributes, combineName):
    # reduce not necessary attributes
    DataWriteFile = open(file=os.path.abspath(os.path.join(writedirectory, combineName)), mode="w", encoding="utf-8")
    dataLines = open(file=os.path.abspath(dataPath), mode="r", encoding="utf-8").readlines()
    dataReadLine = dataLines[0].strip("\n").split("\t")
    DataWriteFile.write("\t".join([dataReadLine[requiredAttribute] for requiredAttribute in requiredAttributes]) + "\n")
    for i in range(1, len(dataLines)):
        dataReadLine = dataLines[i].strip("\n").split("\t")
        DataWriteFile.write("\t".join([dataReadLine[requiredAttribute] for requiredAttribute in requiredAttributes]) + "\n")
    DataWriteFile.close()

""" use for prepocessing the data set downloaded from XueLing's Link """
#preprocess_for_book("../Data/book/dataset", "../Data/book", [0, 1, 3, 6, 10, 12, 19], "book.txt")
#preprocess_for_movie("../Data/movie/dataset/movie.txt", "../Data/movie", [0, 1, 2, 3, 4], "movie.txt")