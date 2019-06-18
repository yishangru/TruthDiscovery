import os

# combine for movie
def main_combine_for_movie(dataPath, writePath):
    fileList = os.listdir(dataPath)
    fileWrite = open(file=writePath, mode="w", encoding="utf-8")
    for file in fileList:
        fileRead = open(file=os.path.join(dataPath, file), mode="r", encoding="utf-8")
        fileReadList = fileRead.readlines()
        fileWrite.writelines(fileReadList)
        fileRead.close()
    fileWrite.close()

def find_missing_database(dataPath1, dataPath2, writePath):
    def generate_dataDict1(dataLine, dataDict):
        dataSplit = dataLine.split("\t")
        dataDict[dataSplit[0]] = dataLine

    def generate_dataDict2(dataLine, dataDict):
        dataSplit = dataLine.split("\t")
        dataDict[dataSplit[0]] = dataSplit[3]

    def generate_missing_dataDict(dataDict1, dataDict2):
        miss_dict = dict()
        for key1 in dataDict1.keys():
            if key1 not in dataDict2.keys():
                miss_dict[key1] = dataDict1[key1]
            elif dataDict2[key1] == "":
                miss_dict[key1] = dataDict1[key1]
        return miss_dict

    def write_dataDict(dataDict):
        dataWriteList = list()
        for key1 in dataDict.keys():
            dataWriteList.append(dataDict[key1] + "\n")
        return dataWriteList

    fileheader = ""
    validateDB = open(file=dataPath1, mode="r", encoding="utf-8")
    movieList = validateDB.readlines()
    dataDict1 = dict()
    for movieLine in range(len(movieList)):
        dataWrite = movieList[movieLine].strip("\n")
        if not movieLine == 0:
            generate_dataDict1(dataWrite, dataDict1)
    validateDB.close()

    crawledDB = open(file=dataPath2, mode="r", encoding="utf-8")
    movieList = crawledDB.readlines()
    dataDict2 = dict()
    for movieLine in range(len(movieList)):
        dataWrite = movieList[movieLine].strip("\n")
        if movieLine == 0:
            fileheader = dataWrite + "\n"
        else:
            generate_dataDict2(dataWrite, dataDict2)
    crawledDB.close()

    missDict = generate_missing_dataDict(dataDict1, dataDict2)
    dataWriteLines = write_dataDict(missDict)
    fileWrite = open(file=writePath, mode="w", encoding="utf-8")
    dataWriteLines.insert(0, fileheader)
    fileWrite.writelines(dataWriteLines)
    fileWrite.close()

def check_category(dataPath, writePath, position):
    def mapping_uniform(data):
        mapping = dict()
        mapping["musical"] = "music"
        mapping["sitcom"] = "comedy"
        mapping["horror"] = "thriller"
        mapping["suspense"] = "thriller"
        mapping["short"] = "independent"
        mapping["comedy-drame"] = "comedy"
        mapping["science-fiction"] = "science fiction"
        mapping["romantic-comedy"] = "romance-comedy"
        mapping["biography"] = "documentary"
        mapping["film-noir"] = "noir"
        mapping["talk-show"] = "tv"
        mapping["talk show"] = "tv"
        mapping["tv shows"] = "tv"
        mapping["tv-movie"] = "tv"
        mapping["tv movie"] = "tv"
        mapping["road-movie"] = "road"
        mapping["anime"] = "animation"
        mapping["international"] = "foreign"
        mapping["mythological"] = "epic"
        mapping["period piece"] = "history"
        mapping["avant garde experimental"] = "independent"
        if data in mapping.keys():
            data = mapping[data]
        return data
    def generate_attribute_set(dataLine, position, attribute_set):
        dataSplit = dataLine.split("\t")[position].split(",")
        for data in dataSplit:
            inter_data = mapping_uniform(data.lower()).split("-")
            for final in inter_data:
                attribute_set.add(final)

    AttributeDB = open(file=dataPath, mode="r", encoding="utf-8")
    attributeRead = AttributeDB.readlines()
    attributeSet = set()
    for movieLine in range(1, len(attributeRead)):
        dataWrite = attributeRead[movieLine].strip("\n")
        generate_attribute_set(dataWrite, position, attributeSet)
    AttributeDB.close()

    AttributeWrite = open(file=writePath, mode="w", encoding="utf-8")
    AttributeWrite.write(attributeRead[0].strip("\n").split("\t")[position]+"\n")
    for attribute in attributeSet:
        AttributeWrite.write(attribute + "\n")
    AttributeWrite.close()

def combine_attribute_movie_database(dataPath1, position, dataPath2, writePath):
    def generate_dataDict(dataLine, dataDict, writeItemList):
        dataSplit = dataLine.split("\t")
        if dataSplit[0] not in dataDict.keys():
            dataDict[dataSplit[0]] = list()
            for writeItem in writeItemList:
                dataDict[dataSplit[0]].append(dataSplit[writeItem])
        else:
            for dataItem in range(len(dataDict[dataSplit[0]])):
                if dataDict[dataSplit[0]][dataItem] == "":
                    dataDict[dataSplit[0]][dataItem] = dataSplit[writeItemList[dataItem]]
    def combine_dataDict(dataDict1, dataDict2):
        print(len(dataDict1))
        for key1 in dataDict1.keys():
            for appendItem in dataDict2[key1]:
                dataDict1[key1].append(appendItem)
    def unify_attribute_represent(dataDict, position):
        def mapping_uniform(data):
            mapping = dict()
            mapping["musical"] = "music"
            mapping["sitcom"] = "comedy"
            mapping["horror"] = "thriller"
            mapping["suspense"] = "thriller"
            mapping["short"] = "independent"
            mapping["comedy-drame"] = "comedy"
            mapping["science-fiction"] = "science fiction"
            mapping["romantic-comedy"] = "romance-comedy"
            mapping["biography"] = "documentary"
            mapping["film-noir"] = "noir"
            mapping["talk-show"] = "tv"
            mapping["talk show"] = "tv"
            mapping["tv shows"] = "tv"
            mapping["tv-movie"] = "tv"
            mapping["tv movie"] = "tv"
            mapping["road-movie"] = "road"
            mapping["anime"] = "animation"
            mapping["international"] = "foreign"
            mapping["mythological"] = "epic"
            mapping["period piece"] = "history"
            mapping["avant garde experimental"] = "independent"
            if data in mapping.keys():
                data = mapping[data]
            return data
        for key in dataDict.keys():
            attribute_set = set()
            attributeLine = dataDict[key][position]
            dataSplit = attributeLine.split(",")
            for data in dataSplit:
                inter_data = mapping_uniform(data.lower()).split("-")
                for final_data in inter_data:
                    attribute_set.add(final_data)
                writeLine = ""
                for attribute in attribute_set:
                    writeLine = writeLine + attribute + ","
                dataDict[key][position] = writeLine.strip(",")
    def write_dataDict(dataDict):
        dataWriteList = list()
        for key1 in dataDict.keys():
            dataWriteLine = ""
            for writeItem in dataDict[key1]:
                dataWriteLine = dataWriteLine + writeItem + "\t"
            dataWriteList.append(dataWriteLine.strip("\t") + "\n")
        return dataWriteList

    AttributeDB1 = open(file=dataPath1, mode="r", encoding="utf-8")
    attributeList = AttributeDB1.readlines()
    dataDict1 = dict()
    writeItemList1 = list([0, 2, 3])
    fileheader = ""
    for attributeLine in range(len(attributeList)):
        dataWrite = attributeList[attributeLine].strip("\n")
        if attributeLine == 0:
            headerHolder = dataWrite.split("\t")
            for key in writeItemList1:
                fileheader = fileheader + headerHolder[key] + "\t"
        else:
            generate_dataDict(dataWrite, dataDict1, writeItemList1)
    AttributeDB1.close()

    AttributeDB2 = open(file=dataPath2, mode="r", encoding="utf-8")
    attributeList = AttributeDB2.readlines()
    dataDict2 = dict()
    writeItemList2 = list([3])
    for attributeLine in range(len(attributeList)):
        dataWrite = attributeList[attributeLine].strip("\n")
        if attributeLine == 0:
            headerHolder = dataWrite.split("\t")
            for key in writeItemList2:
                fileheader = fileheader + headerHolder[key] + "\t"
        else:
            generate_dataDict(dataWrite, dataDict2, writeItemList2)
    AttributeDB2.close()

    fileheader = fileheader.strip("\t") + "\n"
    combine_dataDict(dataDict1, dataDict2)
    unify_attribute_represent(dataDict1, position)
    dataWriteLines = write_dataDict(dataDict1)
    fileWrite = open(file=writePath, mode="w", encoding="utf-8")
    dataWriteLines.insert(0, fileheader)
    fileWrite.writelines(dataWriteLines)
    fileWrite.close()

    #os.remove(dataPath1)
    #os.remove(dataPath2)

def check_country(dataPath, writePath):
    dataOpen = open(file=dataPath, mode="r", encoding="utf-8")
    dataList = dataOpen.readlines()
    country_set = set()
    for data in range(len(dataList)):
        if not data == 0:
            dataSplit = dataList[data].split("\t")[3]
            if not dataSplit == "\n":
                country_set.add(dataSplit)
    dataOpen.close()
    dataWrite = open(file=writePath, mode="w", encoding="utf-8")
    for country in country_set:
        dataWrite.write(country)
    dataWrite.close()

# for movie db
#find_missing_database("./conflictDB_movie", "./ObjectAttributeDB_movie", "./movie_to_add")
#main_combine_for_movie("./combine", "./ObjectAttributeDB_movie")
#combine_attribute_movie_database("./ObjectAttributeDB_movie", 3, "../DataToUse/movie/object_attribute_DB_movie", "../DataToUse/movie/ObjectAttributeDB_movie")
#check_category("../DataToUse/movie/object_attribute_DB_movie", "./attribute_check", 3)
#check_country("./ObjectAttributeDB_movie", "./country_check")

# combine for book
def combine_attribute_book_database(dataPath1, dataPath2, writePath):
    def generate_dataDict(dataLine, dataDict):
        dataSplit = dataLine.split("\t")
        dataDict[dataSplit[0]] = dataLine
    def write_dataDict(datadict1, datadict2):
        dataWriteList = list()
        for key1 in datadict1.keys():
            dataWriteList.append(datadict2[key1] + "\n")
        return dataWriteList

    AttributeDB1 = open(file=dataPath1, mode="r", encoding="utf-8")
    attributeList = AttributeDB1.readlines()
    dataDict1 = dict()
    for attributeLine in range(len(attributeList)):
        dataWrite = attributeList[attributeLine].strip("\n")
        if not attributeLine == 0:
            generate_dataDict(dataWrite, dataDict1)
    AttributeDB1.close()

    fileheader = ""
    AttributeDB2 = open(file=dataPath2, mode="r", encoding="utf-8")
    attributeList = AttributeDB2.readlines()
    dataDict2 = dict()
    for attributeLine in range(len(attributeList)):
        dataWrite = attributeList[attributeLine].strip("\n")
        if attributeLine == 0:
            fileheader = dataWrite + "\n"
        else:
            generate_dataDict(dataWrite, dataDict2)
    AttributeDB2.close()

    dataWriteLines = write_dataDict(dataDict1, dataDict2)
    fileWrite = open(file=writePath, mode="w", encoding="utf-8")
    dataWriteLines.insert(0, fileheader)
    fileWrite.writelines(dataWriteLines)
    fileWrite.close()

#combine_attribute_book_database("../DataToUse/book/conflictDB_book", "../DataToUse/book/object_attribute_rawDB_book", "../DataToUse/book/ObjectAttributeDB_book")