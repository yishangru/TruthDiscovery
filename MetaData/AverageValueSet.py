Movie_fact_path = "../DataToUse/movie/factDB_movie"
Movie_claim_path = "../DataToUse/movie/claimDB_movie"

Book_fact_path = "../DataToUse/book/factDB_book"
Book_claim_path = "../DataToUse/book/claimDB_book"

test_fact_path = "../DataToUse/test/testDB_fact_movie"
test_claim_path = "../DataToUse/test/testDB_claim_movie"

def valueset_count(dataset):
    def generate_fact_dict(factdict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        factdict[dataSplit[0]] = dict()
        factdict[dataSplit[0]][dataSplit[1]] = dataSplit[2]

    def generate_claim_dict(claimdict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in claimdict.keys():
            claimdict[dataSplit[0]] = dict()
        claimdict[dataSplit[0]][dataSplit[1]] = dataSplit[2]

    def generate_object_valueset(factdict, claimdict):
        def generate_fact_object_dict(factdict):
            fact_object_dict = dict()
            for key1 in factdict.keys():
                for key2 in factdict[key1].keys():
                    fact_object_dict[key1] = key2
            return fact_object_dict

        factObjectDict = generate_fact_object_dict(factdict)
        object_source_valueset = dict()
        for key1 in claimdict.keys():
            if factObjectDict[key1] not in object_source_valueset.keys():
                object_source_valueset[factObjectDict[key1]] = dict()
            for key2 in claimdict[key1].keys():
                if key2 not in object_source_valueset[factObjectDict[key1]].keys():
                    object_source_valueset[factObjectDict[key1]][key2] = set()
                if claimdict[key1][key2] == "1":
                    object_source_valueset[factObjectDict[key1]][key2].add(key1)
        object_valueset = dict()
        for key1 in object_source_valueset.keys():
            if key1 not in object_valueset.keys():
                object_valueset[key1] = list()
            for key2 in object_source_valueset[key1].keys():
                flag = True
                for valueset_item in object_valueset[key1]:
                    if len(valueset_item) == len(object_source_valueset[key1][key2]):
                        if len(valueset_item - object_source_valueset[key1][key2]) == 0:
                            flag = False
                            break
                if flag:
                    object_valueset[key1].append(object_source_valueset[key1][key2])
        return object_valueset

    def get_object_valueset_meta_information(objectValueSet):
        object_value_count_number = 0
        for key1 in objectValueSet.keys():
            object_value_count_number = object_value_count_number + len(objectValueSet[key1])
        object_value_count_number = object_value_count_number / len(objectValueSet)
        return object_value_count_number

    factDict = dict()
    claimDict = dict()

    if dataset == 1:  # movie
        dataFile = open(file=Movie_fact_path, mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):  # MID title year source director
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_fact_dict(factDict, dataWrite)
        dataFile.close()

        dataFile = open(file=Movie_claim_path, mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):  # MID title year source director
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_claim_dict(claimDict, dataWrite)
        dataFile.close()

    elif dataset == 0:
        dataFile = open(file=Book_fact_path, mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):  # MID title year source director
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_fact_dict(factDict, dataWrite)
        dataFile.close()

        dataFile = open(file=Book_claim_path, mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):  # MID title year source director
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_claim_dict(claimDict, dataWrite)
        dataFile.close()

    elif dataset == -1:  # this is for testing
        dataFile = open(file=test_fact_path, mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):  # MID title year source director
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_fact_dict(factDict, dataWrite)
        dataFile.close()

        dataFile = open(file=test_claim_path, mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):  # MID title year source director
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_claim_dict(claimDict, dataWrite)
        dataFile.close()

    objectValueSet = generate_object_valueset(factDict, claimDict)
    average_valueset = get_object_valueset_meta_information(objectValueSet)
    print("average valueset: " + str(average_valueset))

dataset_name_dict = dict()
dataset_name_dict[1] = "movie"
dataset_name_dict[0] = "book"
dataset_name_dict[-1] = "test"

dataset_id = 1
print(dataset_name_dict[dataset_id])
valueset_count(dataset_id)
print()
dataset_id = 0
print(dataset_name_dict[dataset_id])
valueset_count(dataset_id)