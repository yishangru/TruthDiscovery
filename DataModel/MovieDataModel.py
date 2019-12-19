import os
import random
moviedatapath = "../DataCleaning/DataToUse/movie/Cleaned_movie.txt"
moviesource_attribute = "../DataCleaning/DataToUse/movie/movie_source_attribute.txt"

#raw database for movie, [movie_id, object, Source, cast]
def generate_raw_database_movie(datapath):
    def generate_data_dict(dataDict, dataWriteLine):
        def treat_values(dataline):
            def remove_space(data):
                data = data.strip(" ")
                return data

            def remove_dot(data):
                data = data.replace(".", " ")
                operating_string = ""
                status = -1
                for character in range(len(data)):
                    if status == -1:
                        operating_string = operating_string + data[character]
                        if data[character] == " ":
                            status = character
                    else:
                        if data[character].isalpha():
                            operating_string = operating_string + data[character]
                            status = -1
                data = operating_string
                return data

            def uniform_representation(data):
                data = data.replace("-", " ")
                if len(data)<=2:
                    data = "none"
                return data

            value_input_list = dataline.split(";")
            value_output_list = list()
            for data in value_input_list:
                inter_data = remove_dot(data)
                inter_data = remove_space(inter_data)
                inter_data = uniform_representation(inter_data)
                if not inter_data == "":
                    value_output_list.append(inter_data)
            return value_output_list

        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in dataDict.keys():  # title
            dataDict[dataSplit[0]] = dict()
        if dataSplit[1] not in dataDict[dataSplit[0]].keys():  # year
            dataDict[dataSplit[0]][dataSplit[1]] = dict()
        if dataSplit[2] not in dataDict[dataSplit[0]][dataSplit[1]].keys():  # source
            dataDict[dataSplit[0]][dataSplit[1]][dataSplit[2]] = dict()
            dataDict[dataSplit[0]][dataSplit[1]][dataSplit[2]]['genres'] = set()
            dataDict[dataSplit[0]][dataSplit[1]][dataSplit[2]]['values'] = treat_values(dataSplit[3])
        dataDict[dataSplit[0]][dataSplit[1]][dataSplit[2]]['genres'].add(dataSplit[4])

    def write_raw_database(dataDict):
        dataWrite = list()
        primary_key = 1
        for key1 in dataDict.keys():  # title
            for key2 in dataDict[key1].keys(): # year
                for key3 in dataDict[key1][key2].keys(): # source
                    generated_data_inter = str(primary_key) + "\t" + key1 + "\t" + \
                                     key2 + "\t" + key3 + "\t"
                    for value in dataDict[key1][key2][key3]['values']:
                        generated_data = generated_data_inter + value + "\n"
                        dataWrite.append(generated_data)
                primary_key += 1
        return dataWrite

    def write_genre_attribute(dataDict):
        dataWrite = list()
        primary_key = 1
        for key1 in dataDict.keys():  # title
            for key2 in dataDict[key1].keys():  # year
                generated_data = str(primary_key) + "\t" + key1 + \
                                       "\t" + key2 + "\t"
                genres_set = set()
                for key3 in dataDict[key1][key2].keys():  # source
                    for genre in dataDict[key1][key2][key3]['genres']:
                        genres_set.add(genre)
                for genre in genres_set:
                    generated_data = generated_data + genre + ","
                generated_data = generated_data.strip(",") + "\n"
                dataWrite.append(generated_data)
                primary_key += 1
        return dataWrite

    write_file_name = "movie"
    dataFile = open(file=os.path.abspath(datapath), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    dataDict = dict()
    fileheader_raw = "MID\t"
    fileheader_genre = "MID\t"
    for dataLine in range(len(dataLines)): # title + year + source + director + genreataLine == 0:
        dataWrite = dataLines[dataLine].strip("\n")
        if dataLine == 0:
            db_title = dataWrite.split("\t")
            for title in range(len(db_title)-1):
                fileheader_raw = fileheader_raw + db_title[title] + "\t"
            fileheader_raw = fileheader_raw.strip("\t") + "\n"
            for title in range(len(db_title)-3):
                fileheader_genre = fileheader_genre + db_title[title] + "\t"
            fileheader_genre = fileheader_genre + db_title[len(db_title)-1] + "\n"
        else:
            generate_data_dict(dataDict, dataWrite)

    rawDatabase = open(file="../DataToUse/" + write_file_name + "/rawDB_" + write_file_name, mode='w', encoding='utf-8')
    dataWrite = write_raw_database(dataDict)
    dataWrite.insert(0, fileheader_raw)
    rawDatabase.writelines(dataWrite)
    rawDatabase.close()

    genreDatabase = open(file="../DataToUse/" + write_file_name + "/object_attribute_rawDB_" + write_file_name, mode='w', encoding='utf-8')
    dataWrite = write_genre_attribute(dataDict)
    dataWrite.insert(0, fileheader_genre)
    genreDatabase.writelines(dataWrite)
    genreDatabase.close()

    dataFile.close()

#unified raw database for movie, [movie_id, object, Source, cast]
def generate_unified_raw_database_movie(datapath):
    def generate_unified_dict(dataDict, factDict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in factDict.keys():
            factDict[dataSplit[0]] = set()
        tag = True
        for data in factDict[dataSplit[0]]:
            data_inter = set(data.split(" "))
            new_inter = set(dataSplit[4].split(" "))
            if len(data_inter - new_inter) == 0:
                dataSplit[4] = data
                tag = False
                break
        if tag:
            factDict[dataSplit[0]].add(dataSplit[4])

        if dataSplit[0] not in dataDict.keys():  # MID
            dataDict[dataSplit[0]] = list()
        data_write = ""
        for data in dataSplit:
            data_write = data_write + data + "\t"
        dataDict[dataSplit[0]].append(data_write.strip("\t")+"\n")

    def remove_all_none(dataDict, factDict):
        for key1 in factDict.keys():
            if len(factDict[key1]) == 1 and ("none" in factDict[key1]):
                dataDict.pop(key1)

    def write_unified_database(dataDict):
        dataWrite = list()
        for key1 in dataDict.keys():
            for data in dataDict[key1]:
                dataWrite.append(data)
        return dataWrite

    write_file_name = "movie"
    dataFile = open(file=os.path.abspath(datapath), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    dataDict = dict()
    factDict = dict()
    raw_unified_header = ""
    for dataLine in range(len(dataLines)): # MID title year source director
        dataWrite = dataLines[dataLine].strip("\n")
        if dataLine == 0:
            raw_unified_header = dataWrite + "\n"
        else:
            generate_unified_dict(dataDict, factDict, dataWrite)

    remove_all_none(dataDict, factDict)
    unifiedRawDatabase = open(file="../DataToUse/" + write_file_name + "/unified_rawDB_" + write_file_name, mode='w', encoding='utf-8')
    dataWrite = write_unified_database(dataDict)
    dataWrite.insert(0, raw_unified_header)
    unifiedRawDatabase.writelines(dataWrite)
    unifiedRawDatabase.close()

    dataFile.close()
    os.remove(datapath)

#fact database for movie, [F_id, movie_id, cast]
def generate_fact_database(movie_raw_path, write_path):
    def generate_fact_dict(dataDict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in dataDict.keys():
            dataDict[dataSplit[0]] = set()
        if not dataSplit[4] == "none":
            dataDict[dataSplit[0]].add(dataSplit[4])

    def write_fact_database(dataDict):
        dataWrite = list()
        fact_id = 1
        for key1 in dataDict.keys():
            for fact in dataDict[key1]:
                generated_data = str(fact_id) + "\t" + key1 + "\t" + \
                                   fact + "\n"
                dataWrite.append(generated_data)
                fact_id += 1
        return dataWrite

    dataFile = open(file=os.path.abspath(movie_raw_path), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    dataDict = dict()
    fileheader_fact = "FID\t"
    for dataLine in range(len(dataLines)): # MID title year source director
        dataWrite = dataLines[dataLine].strip("\n")
        if dataLine == 0:
            header = dataWrite.split("\t")
            fileheader_fact = fileheader_fact + header[0] + "\t" + header[4] + "\n"
        else:
            generate_fact_dict(dataDict, dataWrite)

    factDatabase = open(file=os.path.abspath(write_path), mode='w', encoding='utf-8')
    dataWrite = write_fact_database(dataDict)
    dataWrite.insert(0, fileheader_fact)
    factDatabase.writelines(dataWrite)
    factDatabase.close()

# claim database for movie, [F-id, Source, Observation]
def generate_claim_database(movie_raw_path, fact_path, write_path):
    def generate_data_dict(dataDict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in dataDict.keys():
            dataDict[dataSplit[0]] = dict()
        if dataSplit[3] not in dataDict[dataSplit[0]].keys():
            dataDict[dataSplit[0]][dataSplit[3]] = set()
        if not dataSplit[4] == "none":
            dataDict[dataSplit[0]][dataSplit[3]].add(dataSplit[4])

    def generate_fact_dict(factDict, dataWriteLine): #MID: F_id: director
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[1] not in factDict.keys():
            factDict[dataSplit[1]] = dict()
        factDict[dataSplit[1]][dataSplit[0]] = dataSplit[2]

    def generate_claim_dict(dataDict, factDict, claim_dict):
        for key1 in dataDict.keys(): # M_id
            for key2 in factDict[key1].keys(): #F_id
                if key2 not in claim_dict.keys():
                    claim_dict[key2] = dict()
                for key3 in dataDict[key1].keys(): #source
                    if factDict[key1][key2] in dataDict[key1][key3]:
                        claim_dict[key2][key3] = 1
                    else:
                        claim_dict[key2][key3] = 0

    def write_claim_database(claimDict):
        dataWrite = list()
        for key1 in claimDict.keys():
            for key2 in claimDict[key1].keys():
                generated_data = key1 + "\t" + key2 + "\t" + str(claimDict[key1][key2]) + "\n"
                dataWrite.append(generated_data)
        return dataWrite

    dataFile = open(file=os.path.abspath(movie_raw_path), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    dataDict = dict()
    for dataLine in range(len(dataLines)): # MID title year source director
        dataWrite = dataLines[dataLine].strip("\n")
        if not dataLine == 0:
            generate_data_dict(dataDict, dataWrite)
    dataFile.close()

    dataFile = open(file=os.path.abspath(fact_path), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    factDict = dict()
    for dataLine in range(len(dataLines)): # MID title year source director
        dataWrite = dataLines[dataLine].strip("\n")
        if not dataLine == 0:
            generate_fact_dict(factDict, dataWrite)

    file_header = "FID\t" + "Source\t" + "Observation\n"
    claimDict = dict()
    generate_claim_dict(dataDict, factDict, claimDict)
    claimDatabase = open(file=os.path.abspath(write_path), mode='w', encoding='utf-8')
    dataWrite = write_claim_database(claimDict)
    dataWrite.insert(0, file_header)
    claimDatabase.writelines(dataWrite)
    claimDatabase.close()

# conflict database for movie, [MID, title, year]
def generate_conflict_database(movie_raw_path, fact_path, claim_path):
    def generate_data_dict(dataDict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in dataDict.keys():
            dataDict[dataSplit[0]] = dataSplit[1] + "\t" + dataSplit[2]

    def generate_fact_dict(factDict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        factDict[dataSplit[0]] = dataSplit[1]

    def generate_claim_dict(claimDict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in claimDict.keys():
            claimDict[dataSplit[0]] = set()
        claimDict[dataSplit[0]].add(dataSplit[2])

    def generate_conflict_dict(claimDict, factDict, dataDict):
        def find_conflict_fact(claimDict):
            conflict_fact = list()
            for key in claimDict.keys():
                if not len(claimDict[key]) == 1:
                    conflict_fact.append(key)
            return conflict_fact

        def find_conflict_movie(factDict, conflict_fact):
            conflict_movie = set()
            for fact_id in conflict_fact:
                conflict_movie.add(factDict[fact_id])
            return conflict_movie

        conflictDict = dict()
        conflict_facts = find_conflict_fact(claimDict)
        conflict_movies = find_conflict_movie(factDict, conflict_facts)
        for conflict_movie in conflict_movies:
            conflictDict[conflict_movie] = dataDict[conflict_movie]
        return conflictDict

    def write_conflict_file(conflictDict):
        dataWrite = list()
        for key in conflictDict.keys():
            data = key + "\t" + conflictDict[key] + "\n"
            dataWrite.append(data)
        return dataWrite

    write_file_name = "movie"
    dataFile = open(file=os.path.abspath(movie_raw_path), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    dataDict = dict()
    for dataLine in range(len(dataLines)): # MID title year source director
        dataWrite = dataLines[dataLine].strip("\n")
        if not dataLine == 0:
            generate_data_dict(dataDict, dataWrite)
    dataFile.close()

    dataFile = open(file=os.path.abspath(fact_path), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    factDict = dict()
    for dataLine in range(len(dataLines)): # MID title year source director
        dataWrite = dataLines[dataLine].strip("\n")
        if not dataLine == 0:
            generate_fact_dict(factDict, dataWrite)
    dataFile.close()

    dataFile = open(file=os.path.abspath(claim_path), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    claimDict = dict()
    for dataLine in range(len(dataLines)): # MID title year source director
        dataWrite = dataLines[dataLine].strip("\n")
        if not dataLine == 0:
            generate_claim_dict(claimDict, dataWrite)
    dataFile.close()

    conflictDict = generate_conflict_dict(claimDict, factDict, dataDict)
    file_header = "MID\t" + "title\t" + "year\n"
    dataConflict = open(file=os.path.abspath("conflictDB_" + write_file_name), mode='w',encoding='utf-8')
    dataWrite = write_conflict_file(conflictDict)
    dataWrite.insert(0, file_header)
    dataConflict.writelines(dataWrite)
    dataConflict.close()

# select only conflict data
def generate_only_conflict_db(movie_raw_path, movie_conflict_path):
    def generate_data_dict(dataDict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in dataDict.keys():
            dataDict[dataSplit[0]] = list()
        dataDict[dataSplit[0]].append(dataWriteLine)

    def generate_selected_set(dataWriteLine, selected_set):
        dataSplit = dataWriteLine.split("\t")
        selected_set.add(dataSplit[0])

    def write_testDB_file(dataDict, selected_set):
        dataWrite = list()
        for key in dataDict.keys():
            if key in selected_set:
                for row in dataDict[key]:
                    data = row + "\n"
                    dataWrite.append(data)
        return dataWrite

    dataFile = open(file=os.path.abspath(movie_raw_path), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    dataDict = dict()
    file_header = dataLines[0]
    for dataLine in range(len(dataLines)): # MID title year source director
        dataWrite = dataLines[dataLine].strip("\n")
        if not dataLine == 0:
            generate_data_dict(dataDict, dataWrite)
    dataFile.close()

    selected_set = set()
    dataFile = open(file=os.path.abspath(movie_conflict_path), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    for dataLine in range(len(dataLines)): # MID title year source director
        dataWrite = dataLines[dataLine].strip("\n")
        if not dataLine == 0:
            generate_selected_set(dataWrite, selected_set)
    dataFile.close()

    write_file_name = "movie"
    dataConflict = open(file=os.path.abspath("ToUseDB_" + write_file_name), mode='w',encoding='utf-8')
    dataWrite = write_testDB_file(dataDict, selected_set)
    dataWrite.insert(0, file_header)
    dataConflict.writelines(dataWrite)
    dataConflict.close()

# generate_validation_db
def generate_samll_test_db(movie_raw_path, movie_attribute_path, movie_conflict_path, data_write_path, attribute_write_path, size_test_db):
    def generate_data_dict(dataDict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in dataDict.keys():
            dataDict[dataSplit[0]] = list()
        dataDict[dataSplit[0]].append(dataWriteLine)

    def generate_selected_set(dataWriteLine, selected_set):
        dataSplit = dataWriteLine.split("\t")
        selected_set.add(dataSplit[0])

    def write_testDB_file(dataDict, selected_set):
        dataWrite = list()
        for key in dataDict.keys():
            if key in selected_set:
                for row in dataDict[key]:
                    data = row + "\n"
                    dataWrite.append(data)
        return dataWrite

    dataFile = open(file=os.path.abspath(movie_raw_path), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    dataDict = dict()
    file_header_data = dataLines[0]
    for dataLine in range(len(dataLines)): # MID title year source director
        dataWrite = dataLines[dataLine].strip("\n")
        if not dataLine == 0:
            generate_data_dict(dataDict, dataWrite)
    dataFile.close()

    dataFile = open(file=os.path.abspath(movie_attribute_path), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    attributeDict = dict()
    file_header_attribute = dataLines[0]
    for dataLine in range(len(dataLines)): # MID title year source director
        dataWrite = dataLines[dataLine].strip("\n")
        if not dataLine == 0:
            generate_data_dict(attributeDict, dataWrite)
    dataFile.close()

    selected_set = set()
    dataFile = open(file=os.path.abspath(movie_conflict_path), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    selected_line_numbers = set()
    while(len(selected_line_numbers) < size_test_db):
        selected_line = int(random.uniform(1, len(dataLines)))
        selected_line_numbers.add(selected_line)
    for dataLine in selected_line_numbers: # MID title year source director
        dataWrite = dataLines[dataLine].strip("\n")
        if not dataLine == 0:
            generate_selected_set(dataWrite, selected_set)
    dataFile.close()

    dataConflict = open(file=os.path.abspath(data_write_path), mode='w',encoding='utf-8')
    dataWrite = write_testDB_file(dataDict, selected_set)
    dataWrite.insert(0, file_header_data)
    dataConflict.writelines(dataWrite)
    dataConflict.close()

    dataConflict = open(file=os.path.abspath(attribute_write_path), mode='w',encoding='utf-8')
    dataWrite = write_testDB_file(attributeDict, selected_set)
    dataWrite.insert(0, file_header_attribute)
    dataConflict.writelines(dataWrite)
    dataConflict.close()

# small test database for movie
def generate_validation_db(movie_conflict_path, write_path, size_test_db):
    dataFile = open(file=os.path.abspath(movie_conflict_path), mode='r', encoding='utf-8')
    dataLines = dataFile.readlines()
    file_header = dataLines[0]
    selected_line_numbers = set()
    while(len(selected_line_numbers) < size_test_db):
        selected_line = int(random.uniform(1, len(dataLines)))
        selected_line_numbers.add(selected_line)
    dataWrite = list()
    for dataLine in selected_line_numbers: # MID title year
        dataWrite.append(dataLines[dataLine])
    dataFile.close()

    dataConflict = open(file=os.path.abspath(write_path), mode='w',encoding='utf-8')
    dataWrite.insert(0, file_header)
    dataConflict.writelines(dataWrite)
    dataConflict.close()

"""
# for raw movie database
generate_raw_database_movie(moviedatapath)
generate_unified_raw_database_movie("../DataToUse/movie/rawDB_movie")
generate_fact_database("../DataToUse/movie/unified_rawDB_movie", "../DataToUse/movie/factDB_movie")
generate_claim_database("../DataToUse/movie/unified_rawDB_movie", "../DataToUse/movie/factDB_movie", "../DataToUse/movie/claimDB_movie")
generate_conflict_database("../DataToUse/movie/unified_rawDB_movie", "../DataToUse/movie/factDB_movie", "../DataToUse/movie/claimDB_movie")
"""

"""
# for formal movie database
generate_only_conflict_db("../DataToUse/movie/unified_rawDB_movie", "../DataToUse/movie/conflictDB_movie")
generate_fact_database("../DataToUse/movie/ToUseDB_movie", "../DataToUse/movie/factDB_movie")
generate_claim_database("../DataToUse/movie/ToUseDB_movie", "../DataToUse/movie/factDB_movie", "../DataToUse/movie/claimDB_movie")
"""

"""
# for validation movie database
generate_validation_db("../DataToUse/movie/conflictDB_movie", "../DataToUse/movie/validation_movie", 320)
"""


mapping = dict()
"""
mapping[2000] = "2k"
mapping[4000] = "4k"
mapping[6000] = "6k"
mapping[8000] = "8k"
mapping[10000] = "10k"
"""
mapping[50] = "50"

for size in mapping.keys():
    generate_samll_test_db("../DataToUse/movie/ToUseDB_movie", "../DataToUse/movie/ObjectAttributeDB_movie",
                           "../DataToUse/movie/conflictDB_movie", "../DataToUse/test/" + mapping[size] + "/ToUseDB_movie",
                           "../DataToUse/test/" + mapping[size] + "/ObjectAttributeDB_movie", size)
    generate_fact_database("../DataToUse/test/" + mapping[size] + "/ToUseDB_movie", "../DataToUse/test/" + mapping[size] + "/factDB_movie")
    generate_claim_database("../DataToUse/test/" + mapping[size] + "/ToUseDB_movie", "../DataToUse/test/" + mapping[size] + "/factDB_movie",
                            "../DataToUse/test/" + mapping[size] + "/claimDB_movie")