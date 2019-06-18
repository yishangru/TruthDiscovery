import os

################## for movie dataset ##################
def remove_single_source_movie(datadirectory, datafile):
    def generate_dict(dataDict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in dataDict.keys():  # title
            dataDict[dataSplit[0]] = dict()
        if dataSplit[1] not in dataDict[dataSplit[0]].keys():  # year
            dataDict[dataSplit[0]][dataSplit[1]] = dict()
        if dataSplit[2] not in dataDict[dataSplit[0]][dataSplit[1]].keys():  # source
            dataDict[dataSplit[0]][dataSplit[1]][dataSplit[2]] = list()
        dataDict[dataSplit[0]][dataSplit[1]][dataSplit[2]].append(dataWriteLine)

    def write_file(dataDict):
        dataWrite = list()
        for key1 in dataDict.keys():
            for key2 in dataDict[key1].keys():
                if not len(dataDict[key1][key2].keys()) == 1:
                    for key3 in dataDict[key1][key2]:
                        for data in dataDict[key1][key2][key3]:
                            dataWrite.append(data)
        return dataWrite

    dataFile = open(file=os.path.abspath(os.path.join(datadirectory, datafile)), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    dataDict = dict()
    fileheader = ""
    for dataLine in range(len(dataLines)):
        dataSplit = dataLines[dataLine].split("\t")
        dataWriteLine = dataSplit[0] + "\t" + dataSplit[3] + "\t" + \
                        dataSplit[2] + "\t" + dataSplit[4] + "\t" + dataSplit[1] + "\n"
        # title + year + source + director + genre
        if dataLine == 0:
            fileheader = dataWriteLine
        else:
            generate_dict(dataDict, dataWriteLine)

    dataSmall = open(file=os.path.abspath(os.path.join("./DataToUse", datafile.split('.')[0], datafile)),
                     mode='w', encoding='utf-8')
    dataWrite = write_file(dataDict)
    dataWrite.insert(0, fileheader)
    dataSmall.writelines(dataWrite)
    dataSmall.close()

def unify_name_convention_movie(datadirectory, datafile):
    def remove_space(data):
        data = data.strip(" ")
        return data

    def deal_with_crawling_character1(data):
        mapping = dict()
        mapping["&#2"] = "'"
        mapping["&#39;"] = "'"
        mapping["&#039;"] = "'"
        mapping["&#193;"] = "Á"
        mapping["&#197;"] = "Å"
        mapping["&#199;"] = "Ç"
        mapping["&#201;"] = "É"
        mapping["&#205;"] = "Í"
        mapping["&#211;"] = "Ó"
        mapping["&#212;"] = "Ô"
        mapping["&#214;"] = "Ö"
        mapping["&#216;"] = "Ø"
        mapping["&#220;"] = "Ü"
        mapping["&#222;"] = "Þ"
        mapping["&#223;"] = "ß"
        mapping["&#224;"] = "à"
        mapping["&#225;"] = "á"
        mapping["&#227;"] = "ã"
        mapping["&#228;"] = "ä"
        mapping["&#229;"] = "å"
        mapping["&#230;"] = "æ"
        mapping["&#231;"] = "ç"
        mapping["&#232;"] = "è"
        mapping["&#233;"] = "é"
        mapping["&#235;"] = "ë"
        mapping["&#236;"] = "ì"
        mapping["&#237;"] = "í"
        mapping["&#238;"] = "î"
        mapping["&#239;"] = "ï"
        mapping["&#240;"] = "ð"
        mapping["&#241;"] = "ñ"
        mapping["&#242;"] = "ò"
        mapping["&#243;"] = "ó"
        mapping["&#244;"] = "ô"
        mapping["&#245;"] = "õ"
        mapping["&#246;"] = "ö"
        mapping["&#248;"] = "ø"
        mapping["&#250;"] = "ú"
        mapping["&#251;"] = "û"
        mapping["&#252;"] = "ü"
        mapping["&#253;"] = "ý"
        mapping[r"\t"] = ""
        mapping[r"\n"] = ""
        mapping["Sr."] = ""
        mapping["Jr."] = ""
        mapping[" and "] = ";"
        mapping[" & "] = ";"
        mapping["&rsquo;"] = r"'"
        mapping["&eacute;"] = "é"
        mapping["&aacute;"] = "á"
        mapping["&ocirc;"] = "ô"
        mapping["&oacute;"] = "ó"
        mapping["&uacute;"] = "u"
        mapping["&oslash;"] = "ø"
        mapping["&ouml;"] = "ö"
        mapping["&uuml;"] = "ü"
        mapping["&iacute;"] = "í"
        mapping["&Ocirc;"] = "Ô"
        mapping["&auml;"] = "ä"
        mapping["&Aacute;"] = "Á"
        mapping["&egrave;"] = "è"
        mapping["&quot;"] = r"'"
        mapping["&aring;"] = "å"
        mapping["&Aring;"] = "Å"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] + mapping[target] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    def deal_with_crawling_character2(data):
        mapping = dict()
        mapping["'01;"] = "É"
        mapping["'05;"] = "Í"
        mapping["'11;"] = "Ó"
        mapping["'12;"] = "Ô"
        mapping["'14;"] = "Ö"
        mapping["'16;"] = "Ø"
        mapping["'20;"] = "Ü"
        mapping["'22;"] = "Þ"
        mapping["'23;"] = "ß"
        mapping["'24;"] = "à"
        mapping["'25;"] = "á"
        mapping["'27;"] = "?"
        mapping["'28;"] = "ä"
        mapping["'29;"] = "å"
        mapping["'30;"] = "æ"
        mapping["'31;"] = "ç"
        mapping["'32;"] = "è"
        mapping["'33;"] = "é"
        mapping["'35;"] = "ë"
        mapping["'36;"] = "ì"
        mapping["'37;"] = "í"
        mapping["'38;"] = "î"
        mapping["'39;"] = "ï"
        mapping["'40;"] = "ð"
        mapping["'41;"] = "ñ"
        mapping["'42;"] = "ò"
        mapping["'43;"] = "ó"
        mapping["'44;"] = "ô"
        mapping["'45;"] = "õ"
        mapping["'46;"] = "?"
        mapping["'48;"] = "ø"
        mapping["'50;"] = "ú"
        mapping["'51;"] = "û"
        mapping["'52;"] = "ü"
        mapping["'53;"] = "z"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    def unify_none(data):
        not_know_set = set(list(["unknown", "Unavailable", "N/A", "Not Specified",
                                 "None", "Unknown", "Various", ""]))
        if data in not_know_set:
            data = "none"
        return data

    def treat_for_source(source, data):
        def comma_issue(data, treat):
            mapping = dict()
            mapping[1] = ";"
            mapping[2] = ""
            target = ","
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[treat] + data[index + len(target):len(data)]
            return data

        def bracket_issue(data):
            if data.find("(")>=0:
                status = -1
                operating_string = ""
                for character in range(len(data)):
                    if data[character] == "(":
                        status = character
                    elif data[character] == ")":
                        status = -1
                    elif status == -1:
                        operating_string = operating_string + data[character]
                data = operating_string
            return data

        if source == "agoodmovietowatch":
            operating_string = ""
            status = -1
            for character in range(len(data)):
                if data[character] == '<':
                    status = character
                elif data[character] == '>':
                    status = -1
                elif status == -1:
                    operating_string = operating_string + data[character]
            data = operating_string

        elif source == "amazon":
            target = " et al."
            index = data.find(target)
            if index >= 0:
                data = data[0:index] if index + len(target) == len(data) \
                    else data[0:index] + data[index + len(target):len(data)]

        elif source == "imdb":
            data = data.replace("See full summary;", "")
            if data.find("\\")>=0:
                status = -1
                operating_string = ""
                for character in range(len(data)):
                    if data[character] == "\\":
                        status = character
                    elif data[character] == ">":
                        status = -1
                    elif status == -1:
                        operating_string = operating_string + data[character]
                data = operating_string

        """
        if source == "ifcfilms":
            for character in range(len(data)):
                if data[character] == "&":
                    data = data.rstrip('&') if character == len(data) - 1 else \
                        data[0:character] + ';' + data[character + 1:len(data)]
        """
        if source in set(list(["flimcrave", "agoodmovietowatch", "goodfilms"])):
            data = comma_issue(data, 1)
        if source in set(list(["1moviesonline", "letterboxd", "allmovie"])):
            data = comma_issue(data, 2)
        if source in set(list(["goodfilms", "amazon", "flimcrave", "letterboxd"])):
            data = bracket_issue(data)

        index = data.find("??")
        if index >= 0:
            data = "none"
        return data

    open_file_name = os.path.abspath(os.path.join(datadirectory, datafile))
    write_file_name = "movie"
    dataFile = open(file=open_file_name, mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    dataWrite = list()
    for dataLine in range(len(dataLines)):
        dataSplit = dataLines[dataLine].split("\t")
        if not dataLine == 0:
            dataSplit[3] = deal_with_crawling_character1(dataSplit[3])
            dataSplit[3] = deal_with_crawling_character2(dataSplit[3])
            dataSplit[3] = treat_for_source(dataSplit[2], dataSplit[3])
            dataSplit[3] = remove_space(dataSplit[3])
            dataSplit[3] = unify_none(dataSplit[3])
            if len(dataSplit[3]) <= 2:
                dataSplit[3] = "none"
        data = ""
        for i in dataSplit:
            data = data + i + "\t"
        dataWrite.append(data.rstrip('\t'))

    dataClean = open(file=os.path.abspath(os.path.join(datadirectory, write_file_name, "Cleaned_" + write_file_name + ".txt")),
                     mode='w', encoding='utf-8')
    dataClean.writelines(dataWrite)
    dataClean.close()

def check_conflict_claim_movie(datadirectory, datafile):
    def generate_conflict_dict(dataConflictDict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in dataConflictDict.keys():  # title
            dataConflictDict[dataSplit[0]] = dict()
        if dataSplit[1] not in dataConflictDict[dataSplit[0]].keys():  # year
            dataConflictDict[dataSplit[0]][dataSplit[1]] = dict()
        if dataSplit[3] not in dataConflictDict[dataSplit[0]][dataSplit[1]].keys():  # director
            dataConflictDict[dataSplit[0]][dataSplit[1]][dataSplit[3]] = list()
        dataConflictDict[dataSplit[0]][dataSplit[1]][dataSplit[3]].append(dataWriteLine)

    def write_conflict_file(dataConflictDict):
        dataWrite = list()
        for key1 in dataConflictDict.keys():
            for key2 in dataConflictDict[key1].keys():
                if not len(dataConflictDict[key1][key2].keys()) == 1:
                    for key3 in dataConflictDict[key1][key2]:
                        for data in dataConflictDict[key1][key2][key3]:
                            dataWrite.append(data)
        return dataWrite

    write_file_name = "movie"
    dataFile = open(file=os.path.abspath(os.path.join(datadirectory, datafile)), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    dataConflictDict = dict()
    fileheader = ""
    for dataLine in range(len(dataLines)):
        # title + year + source + director + genre
        if dataLine == 0:
            fileheader = dataLines[dataLine]
        else:
            generate_conflict_dict(dataConflictDict, dataLines[dataLine])

    dataConflict = open(file=os.path.abspath(os.path.join(datadirectory, "Conflict_" + write_file_name + ".txt")),
                        mode='w',encoding='utf-8')
    dataWrite = write_conflict_file(dataConflictDict)
    dataWrite.insert(0, fileheader)
    dataConflict.writelines(dataWrite)
    dataConflict.close()

def check_name_convention_movie(datadirectory, datafile):
    def generate_source_convention_dict(dataDict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in dataDict.keys():  # source
            dataDict[dataSplit[0]] = list()
        dataDict[dataSplit[0]].append(dataWriteLine)

    def write_file(dataDict):
        dataWrite = list()
        for key1 in dataDict.keys():
            for data in dataDict[key1]:
                dataWrite.append(data)
        return dataWrite

    open_file_name = os.path.abspath(os.path.join(datadirectory, datafile))
    write_file_name = "movie"

    dataFile = open(file=open_file_name, mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    dataDict = dict()
    fileheader = ""
    for dataLine in range(len(dataLines)):
        dataSplit = dataLines[dataLine].split("\t")
        dataWriteLine = dataSplit[2] + "\t" + dataSplit[3] + "\n"
        if dataLine == 0:
            fileheader = dataWriteLine
        else:
            generate_source_convention_dict(dataDict, dataWriteLine)

    dataSmall = open(file=os.path.abspath(os.path.join(datadirectory, write_file_name, "NameConvention_" + write_file_name + ".txt")),
                     mode='w', encoding='utf-8')
    dataWrite = write_file(dataDict)
    dataWrite.insert(0, fileheader)
    dataSmall.writelines(dataWrite)
    dataSmall.close()

def main_for_movie_clean():
    remove_single_source_movie("./Data/movie", "movie.txt")
    unify_name_convention_movie("./DataToUse", "movie.txt")
    check_conflict_claim_movie("./DataToUse", "Cleaned_movie.txt")
    check_name_convention_movie("./DataToUse", "Conflict_movie.txt")
"""
1. 去掉非法符号？
1. -放到前面去,换成空格
2. 不区分大小写
N/A
For "imdb":
    1.\n开头，找最后一个>,把\n到后面的都删掉，如果没有直接删了就行
For "goodfilms":
    1. 逗号转成;进行分割
    2. ()issue
For "agoodmovietowatch":
    1. 逗号转成；进行分割
    2. <>去掉
For "flimcrave":
    1. 逗号转成；进行分割
For "amazon":
    1. remove et al.
    2. " and " --> ;
For "movieinsider":
    1. "" --> none
    2. remove &
"""
################## for movie dataset ##################


################## for book dataset ##################
def combine_dataset_book(datadirectory, writedirectory):
    fileList = os.listdir(datadirectory)
    DataWriteFile = open(file=os.path.abspath(os.path.join(writedirectory, "book.txt")), mode="w", encoding="utf-8")
    for data in range(len(fileList)):
        category = str(fileList[data].split(".")[0])
        DataFile = open(file=os.path.join(datadirectory, fileList[data]), mode="r", encoding="utf-8")
        dataLines = DataFile.readlines()
        if data == 0:
            dataWriteLine = dataLines[0].strip("\n").split("\t")
            DataWriteFile.write(dataWriteLine[0] + "\t" + dataWriteLine[1] + "\t" + \
                                dataWriteLine[6] + "\t" + dataWriteLine[3] + "\t" + "Category" +
                                "\t" + dataWriteLine[12] + "\t" + dataWriteLine[19] + "\n")
        dataWriteLines = list()
        for dataLine in range(1, len(dataLines)):
            dataWriteLine = dataLines[dataLine].strip("\n").split("\t")
            dataInter = dataWriteLine[0] + "\t" + dataWriteLine[1] + "\t" + \
                        dataWriteLine[6] + "\t" + dataWriteLine[3] + "\t" + category + \
                        "\t" + dataWriteLine[12] + "\t" + dataWriteLine[19] + "\n"
            dataWriteLines.append(dataInter)
        DataFile.close()
        DataWriteFile.writelines(dataWriteLines)
    DataWriteFile.close()

def remove_single_source_book(datadirectory, datafile):
    def generate_dict(dataDict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in dataDict.keys():  # isbn
            dataDict[dataSplit[0]] = dict()
        if dataSplit[2] not in dataDict[dataSplit[0]].keys():  # source
            dataDict[dataSplit[0]][dataSplit[2]] = list()
        dataDict[dataSplit[0]][dataSplit[2]].append(dataWriteLine)

    def write_file(dataDict):
        dataWrite = list()
        for key1 in dataDict.keys():
            if not len(dataDict[key1].keys()) == 1:
                for key2 in dataDict[key1]:
                    dataSplit = dataDict[key1][key2][0].split("\t")
                    dataWriteLine = dataSplit[0] + "\t" + dataSplit[1] + "\t" + \
                                dataSplit[2] + "\t" + dataSplit[3] + "\t"
                    for data in dataDict[key1][key2]:
                        dataToWrite = data.split("\t")[4]
                        dataWriteLine = dataWriteLine + dataToWrite + ","
                    dataWriteLine = dataWriteLine.strip(",") + "\t" + dataSplit[5] + "\t" + dataSplit[6]
                    dataWrite.append(dataWriteLine)
        return dataWrite

    dataFile = open(file=os.path.abspath(os.path.join(datadirectory, datafile)), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    dataDict = dict()
    fileheader = ""
    for dataLine in range(len(dataLines)):
        if dataLine == 0:
            fileheader = dataLines[dataLine]
        else:
            generate_dict(dataDict, dataLines[dataLine])

    dataSmall = open(file=os.path.abspath(os.path.join("./DataToUse", datafile.split('.')[0], datafile)),
                     mode='w', encoding='utf-8')
    dataWrite = write_file(dataDict)
    dataWrite.insert(0, fileheader)
    dataSmall.writelines(dataWrite)
    dataSmall.close()

def unify_name_convention_book(datadirectory, datafile):
    # / & . with | ~ ; +
    def remove_bracket(data):
        def remove_target(start, end, data):
            status = -1
            inter_string = ""
            for character in range(len(data)):
                if data[character] == start:
                    status = character
                elif data[character] == end:
                    status = -1
                elif status == -1:
                    inter_string = inter_string + data[character]
            data = inter_string
            return data
        data = remove_target("{", "}", data)
        data = remove_target("(", ")", data)
        data = remove_target("[", "]", data)
        return data

    def deal_with_source(data, source):
        if source == "Castle Rock":
            index = data.find("by")
            if index >= 0:
                data = data[index + 2: len(data)]
        return data

    def remove_character_normal(data, mapping):
        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    def remove_character_lower(data, mapping):
        for target in mapping.keys():
            inter_data = data.lower()
            while (inter_data.find(target) >= 0):
                index = inter_data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
                inter_data = data.lower()
        return data

    def remove_character_at_end(data, target):
        inter_data = data.lower()
        if inter_data.find(target) == len(data) - len(target):
            data = data[0:len(data) - len(target)]
        return data

    def deal_with_gamble_character(data):
        mapping1 = dict()
        mapping1["&#232"] = "è"
        mapping1["&#G"] = ""
        mapping1["&#x308"] = ""
        mapping1["Carlo D&#39"] = ""
        mapping1["Ingrid B&#xf6 Ck,"] = ""
        mapping1["Jean Prouv&#xe9,"] = ""
        mapping1["Ren&#xe9 Hirner,"] = ""
        mapping1["Hirner, Ren&#xe9,"] = ""
        mapping1["Brien; O&#39, Darcy"] = ""
        mapping1["O&#39, Darcy, Brien,"] = ""

        mapping2 = dict()
        mapping2["&#39"] = "'"

        data = remove_character_normal(data, mapping1)
        data = remove_character_normal(data, mapping2)
        return data

    def deal_with_special_case(data):
        mapping = dict()
        mapping["P H Feist"] = ""
        mapping["John, G. Heard, H."] = "John, G.;Heard, H."
        mapping["Adrian;Moore, James R. Desmond"] = "Adrian Desmond;Moore, James R."
        mapping["The Economist"] = "Economist"
        mapping["Kak; Subhash"] = "Subhash Kak"
        mapping["By "] = " "
        data = remove_character_normal(data, mapping)
        return data

    def deal_with_unexpected_character(data, source):
        mapping1 = dict()
        mapping1["&"] = ";"
        mapping1["~"] = ";"
        mapping1["/"] = ";"
        mapping1["  "] = " "
        mapping1["sr."] = ""
        mapping1["jr."] = ""
        mapping1["ph.d."] = ""
        mapping1["phd"] = ""
        mapping1[" the "] = " "
        mapping1["others"] = ""
        mapping1["editors of "] = ""
        mapping1["introductions"] = ""
        mapping1["illustrations"] = ""
        mapping1["drawings"] = ""
        mapping1["edited"] = ""
        mapping1["written"] = ""
        mapping1["designed"] = ""
        mapping1["conceived"] = ""
        mapping1["forewords"] = ""
        mapping1["illustrated"] = ""
        mapping1["photographs"] = ""
        mapping1["translated"] = ""
        mapping1["introduced"] = ""
        mapping1["organized"] = ""
        mapping1["counties"] = ""
        mapping1["architects"] = ""
        mapping1["directors"] = ""

        mapping2 = dict()
        mapping2["executive"] = ""
        mapping2["introduction"] = ""
        mapping2["illustration"] = ""
        mapping2["foreword"] = ""
        mapping2["photograph"] = ""
        mapping2["drawing"] = ""
        mapping2["course devized"] = ""
        mapping2["w/trans"] = ""
        mapping2["professor"] = ""
        mapping2[" an "] = " "
        mapping2["intro"] = ""
        mapping2["other"] = ""
        mapping2["editors"] = ""
        mapping2["director"] = ""
        mapping2["project"] = ""

        mapping3 = dict()
        mapping3[" and "] = ";"
        mapping3[" und "] = ";"
        mapping3["with "] = ";"
        mapping3["ed."] = ""
        mapping3[" ed "] = ""
        mapping3["text"] = ""
        mapping3["editor"] = ""
        if source == "Cambridge Rare Books":
            mapping3[" by "] = ";"
        else:
            mapping3[" by "] = " "

        data = remove_character_lower(data, mapping1)
        data = remove_character_lower(data, mapping2)
        data = remove_character_lower(data, mapping3)
        data = remove_space(data)
        data = remove_character_at_end(data, " by")
        data = remove_character_at_end(data, " ed")
        data = remove_character_at_end(data, " eds")
        data = remove_space(data)
        return data

    def unify_none(data):
        notknownset = set(list(['none', 'no author', 'unknown author', 'imprint unknown', 'not specified', 'various'
                                   'no author stated', 'no author given', 'no author listed', 'no author credited',
                                   'no author noted', 'no listed author', 'no data', 'no stated author', 'no name',
                                   'not available', 'not stated', 'not known', 'author not stated', 'not specified',
                                   '1', 'unknown', 'n/a', 'n / a', 'v/& a', 'not applicable', 'unavailable']))
        inter_data = data.lower()
        for target in notknownset:
            if inter_data.find(target) >= 0:
                data = "none"
                break
        return data

    def remove_space(data):
        data = data.strip(" ")
        while(len(data)>2):
            if not data[len(data)-1].isalpha():
                data = data[0:len(data)-1]
            else:
                break
        while(len(data)>2):
            if not data[0].isalpha():
                data = data[1:len(data)]
            else:
                break
        return data

    def deal_with_separator(data):
        #comma_set = set(list(["Fun_Meister", "Ergodebooks"]))
        #two_comman_set = set(list(["medimops", "Murray Media", ]))
        if data.find(";") == -1 and data.find(",") >= 0:
            data_inter = data.split(",")[0]
            if len(data_inter.strip(" ").split(" ")) > 1:
                for character in range(len(data)):
                    if data[character] == ",":
                        data = data[0:character] + ";" + data[character + 1:len(data)]
            else:
                flag = False
                for character in range(len(data)):
                    if not flag:
                        if data[character] == ",":
                            flag = True
                    else:
                        if data[character] == ",":
                            data = data[0:character] + ";" + data[character + 1:len(data)]
                            flag = False
        if len(data) <= 3:
            data = "none"
        return data

    open_file_name = os.path.abspath(os.path.join(datadirectory, datafile))
    dataFile = open(file=open_file_name, mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    dataWrite = list()
    for dataLine in range(len(dataLines)):
        print(dataLine)
        dataSplit = dataLines[dataLine].split("\t")
        if not dataLine == 0:
            dataSplit[3] = remove_bracket(dataSplit[3])
            dataSplit[3] = deal_with_source(dataSplit[3], dataSplit[2])
            dataSplit[3] = deal_with_gamble_character(dataSplit[3])
            dataSplit[3] = deal_with_special_case(dataSplit[3])
            dataSplit[3] = deal_with_unexpected_character(dataSplit[3], dataSplit[2])
            dataSplit[3] = unify_none(dataSplit[3])
            dataSplit[3] = deal_with_separator(dataSplit[3])
        data = ""
        for i in dataSplit:
            data = data + i + "\t"
        dataWrite.append(data.rstrip('\t'))

    dataClean = open(file=os.path.abspath(os.path.join(datadirectory, "Cleaned_" + datafile.split(".")[0] + ".txt")),
        mode='w', encoding='utf-8')
    dataClean.writelines(dataWrite)
    dataClean.close()

def check_conflict_claim_book(datadirectory, datafile):
    def generate_conflict_dict(dataConflictDict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in dataConflictDict.keys():
            dataConflictDict[dataSplit[0]] = dict()
        if dataSplit[3] not in dataConflictDict[dataSplit[0]].keys():  # director
            dataConflictDict[dataSplit[0]][dataSplit[3]] = list()
        dataConflictDict[dataSplit[0]][dataSplit[3]].append(dataWriteLine)

    def write_conflict_file(dataConflictDict):
        dataWrite = list()
        for key1 in dataConflictDict.keys():
            if not len(dataConflictDict[key1].keys()) == 1:
                for key2 in dataConflictDict[key1]:
                    for data in dataConflictDict[key1][key2]:
                        dataWrite.append(data)
        return dataWrite

    write_file_name = "book"
    dataFile = open(file=os.path.abspath(os.path.join(datadirectory, datafile)), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    dataConflictDict = dict()
    fileheader = ""
    for dataLine in range(len(dataLines)):
        if dataLine == 0:
            fileheader = dataLines[dataLine]
        else:
            generate_conflict_dict(dataConflictDict, dataLines[dataLine])

    dataConflict = open(file=os.path.abspath(os.path.join(datadirectory, "Conflict_" + write_file_name + ".txt")),
                        mode='w',encoding='utf-8')
    dataWrite = write_conflict_file(dataConflictDict)
    dataWrite.insert(0, fileheader)
    dataConflict.writelines(dataWrite)
    dataConflict.close()

def check_name_convention_book(datadirectory, datafile):
    def generate_source_convention_dict(dataDict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in dataDict.keys():  # source
            dataDict[dataSplit[0]] = list()
        dataDict[dataSplit[0]].append(dataWriteLine)

    def write_file(dataDict):
        dataWrite = list()
        for key1 in dataDict.keys():
            for data in dataDict[key1]:
                dataWrite.append(data)
        return dataWrite

    write_file_name = "book"
    dataFile = open(file=os.path.join(datadirectory, datafile), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    dataDict = dict()
    fileheader = ""
    for dataLine in range(len(dataLines)):
        dataSplit = dataLines[dataLine].split("\t")
        dataWriteLine = dataSplit[2] + "\t" + dataSplit[3] + "\n"
        if dataLine == 0:
            fileheader = dataWriteLine
        else:
            generate_source_convention_dict(dataDict, dataWriteLine)

    dataSmall = open(file=os.path.abspath(os.path.join(datadirectory, "NameConvention_" + write_file_name + ".txt")),
                     mode='w', encoding='utf-8')
    dataWrite = write_file(dataDict)
    dataWrite.insert(0, fileheader)
    dataSmall.writelines(dataWrite)
    dataSmall.close()

def main_for_book_clean():
    combine_dataset_book("./Data/book/dataset", "./Data/book")
    remove_single_source_book("./Data/book", "book.txt")
    unify_name_convention_book("./DataToUse/book", "book.txt")
    check_conflict_claim_book("./DataToUse/book", "Cleaned_book.txt")
    check_name_convention_book("./DataToUse/book", "Conflict_book.txt")

################## for book dataset ##################
#main_for_book_clean()