Movie_fact_path = "../DataToUse/movie/factDB_movie"
Movie_claim_path = "../DataToUse/movie/claimDB_movie"

Book_fact_path = "../DataToUse/book/factDB_book"
Book_claim_path = "../DataToUse/book/claimDB_book"

test_fact_path = "../DataToUse/test/testDB_fact_movie"
test_claim_path = "../DataToUse/test/testDB_claim_movie"

def source_count(dataset):
    def generate_source_dict(source_set, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[1] not in source_set:
            source_set.add(dataSplit[1])

    source_set = set()
    if dataset == 1:  # movie
        dataFile = open(file=Movie_claim_path, mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):  # MID title year source director
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_source_dict(source_set, dataWrite)
        dataFile.close()

    elif dataset == 0:
        dataFile = open(file=Book_claim_path, mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):  # MID title year source director
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_source_dict(source_set, dataWrite)
        dataFile.close()

    elif dataset == -1:  # this is for testing
        dataFile = open(file=test_claim_path, mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):  # MID title year source director
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_source_dict(source_set, dataWrite)
        dataFile.close()
    print("source: " + str(len(source_set)))

def source_coverage(dataset):
    def generate_fact_dict(factdict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        factdict[dataSplit[0]] = dict()
        factdict[dataSplit[0]][dataSplit[1]] = dataSplit[2]

    def generate_claim_dict(claimdict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in claimdict.keys():
            claimdict[dataSplit[0]] = dict()
        claimdict[dataSplit[0]][dataSplit[1]] = dataSplit[2]

    def generate_object_size(factdict):
        object_set = set()
        for key1 in factdict.keys():
            for key2 in factdict[key1].keys():
                object_set.add(key2)
        return len(object_set)

    def generate_source_object_provide_dict(factdict, claimdict):
        source_object_dict = dict()
        for key1 in claimdict.keys():
            for key2 in claimdict[key1].keys():
                if key2 not in source_object_dict.keys():
                    source_object_dict[key2] = set()
                if claimdict[key1][key2] == "1":
                    for key3 in factdict[key1].keys():
                        source_object_dict[key2].add(key3)
        return source_object_dict

    def generate_source_object_associate_dict(factdict, claimdict):
        def generate_object_fact_dict(factdict):
            object_fact_dict = dict()
            for fact in factdict.keys():
                for object in factdict[fact].keys():
                    if object not in object_fact_dict.keys():
                        object_fact_dict[object] = set()
                    object_fact_dict[object].add(fact)
            return object_fact_dict

        source_object_dict = dict()
        object_fact_dict = generate_object_fact_dict(factdict)
        for fact in claimdict.keys():
            for source in claimdict[fact].keys():
                if source not in source_object_dict.keys():
                    source_object_dict[source] = set()
                for object in factdict[fact].keys():
                    source_object_dict[source].add(object)
        source_fact_dict = dict()
        for source in source_object_dict.keys():
            source_fact_dict[source] = 0
            for object in source_object_dict[source]:
                source_fact_dict[source] += len(object_fact_dict[object])
        return source_fact_dict

    def get_source_object_provide_meta_information(sourceObjectProvidedict):
        max_information_count = -1
        mini_information_count = -1
        for key1 in sourceObjectProvidedict.keys():
            if len(sourceObjectProvidedict[key1]) > max_information_count:
                max_information_count = len(sourceObjectProvidedict[key1])
            if (len(sourceObjectProvidedict[key1]) < mini_information_count) or mini_information_count == -1:
                mini_information_count = len(sourceObjectProvidedict[key1])
        return max_information_count, mini_information_count

    def get_source_object_associate_dict(sourceObjectAssociatedict):
        max_information_count = -1
        mini_information_count = -1
        for key1 in sourceObjectAssociatedict.keys():
            if sourceObjectAssociatedict[key1] > max_information_count:
                max_information_count = sourceObjectAssociatedict[key1]
            if (sourceObjectAssociatedict[key1] < mini_information_count) or mini_information_count == -1:
                mini_information_count = sourceObjectAssociatedict[key1]
        return max_information_count, mini_information_count

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

    object_size = generate_object_size(factDict)
    sourceObjectProvide = generate_source_object_provide_dict(factDict, claimDict)
    sourceObjectAssociate = generate_source_object_associate_dict(factDict, claimDict)
    max_provide, mini_provide = get_source_object_provide_meta_information(sourceObjectProvide)
    max_associate, mini_associate = get_source_object_associate_dict(sourceObjectAssociate)

    print("object: " + str(object_size))
    print("max_provide_info: " + str(max_provide) + " - " + str(max_provide/object_size*100) + "%")
    print("mini_provide_info: " + str(mini_provide) + " - " + str(mini_provide / object_size * 100) + "%")
    print("max_asso_fact: " + str(max_associate))
    print("mini_asso_fact: " + str(mini_associate))

def source_object(dataset):
    def generate_fact_dict(factdict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        factdict[dataSplit[0]] = dict()
        factdict[dataSplit[0]][dataSplit[1]] = dataSplit[2]

    def generate_claim_dict(claimdict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in claimdict.keys():
            claimdict[dataSplit[0]] = dict()
        claimdict[dataSplit[0]][dataSplit[1]] = dataSplit[2]

    def generate_object_fact_dict(factdict, claimdict):
        object_source_dict = dict()
        for key1 in factdict.keys():
            for key2 in factdict[key1].keys():
                if key2 not in object_source_dict.keys():
                    object_source_dict[key2] = set()
                for key3 in claimdict[key1].keys():
                    object_source_dict[key2].add(key3)
        return object_source_dict

    def get_object_source_meta_information(objectSourcedict):
        source_count_number = 0
        for key1 in objectSourcedict.keys():
            source_count_number = source_count_number + len(objectSourcedict[key1])
        source_count_number = source_count_number / len(objectSourcedict)
        return source_count_number

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

    objectSourceDict = generate_object_fact_dict(factDict, claimDict)
    average_source = get_object_source_meta_information(objectSourceDict)
    print("average source for object: " + str(average_source))


dataset_name_dict = dict()
dataset_name_dict[1] = "movie"
dataset_name_dict[0] = "book"
dataset_name_dict[-1] = "test"

dataset_id = 1
print(dataset_name_dict[dataset_id])
source_count(dataset_id)
source_coverage(dataset_id)
source_object(dataset_id)
print()
dataset_id = 0
print(dataset_name_dict[dataset_id])
source_count(dataset_id)
source_coverage(dataset_id)
source_object(dataset_id)