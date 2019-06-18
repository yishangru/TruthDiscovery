import os
import time
import datetime

Movie_fact_path = "../DataToUse/movie/factDB_movie"
Movie_claim_path = "../DataToUse/movie/claimDB_movie"

Book_fact_path = "../DataToUse/book/factDB_book"
Book_claim_path = "../DataToUse/book/claimDB_book"

test_fact_path = "../DataToUse/test/testDB_fact_movie"
test_claim_path = "../DataToUse/test/testDB_claim_movie"

def MV(dataset, datasetPath, outputWritePath):
    def generate_fact_dict(factdict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        factdict[dataSplit[0]] = dict()
        factdict[dataSplit[0]][dataSplit[1]] = dataSplit[2] # BID, MID: Aurthor, Director

    def generate_claim_dict(claimdict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in claimdict.keys():
            claimdict[dataSplit[0]] = dict()
        claimdict[dataSplit[0]][dataSplit[1]] = dataSplit[2]

    def generate_object_claim_dict(factDict, claimDict):
        object_claim_count_dict = dict()
        for key1 in claimDict.keys():
            for key2 in factDict[key1].keys():
                if key2 not in object_claim_count_dict.keys():
                    object_claim_count_dict[key2] = dict()
                if key1 not in object_claim_count_dict[key2].keys():
                    object_claim_count_dict[key2][key1] = 0
                for key3 in claimDict[key1].keys():
                    if claimDict[key1][key3] == "1":
                        object_claim_count_dict[key2][key1] += 1
        return object_claim_count_dict

    def generate_truth_dict(objectClaimDict):
        truth_dict = dict()
        for key1 in objectClaimDict.keys():
            if key1 not in truth_dict.keys():
                truth_dict[key1] = list()
            max_value = 0
            for key2 in objectClaimDict[key1].keys():
                if objectClaimDict[key1][key2] > max_value:
                    max_value = objectClaimDict[key1][key2]
            for key2 in objectClaimDict[key1].keys():
                if objectClaimDict[key1][key2] == max_value:
                    truth_dict[key1].append(key2)
        return truth_dict

    def write_truth_dict(factDict, truthDict):
        dataWriteList = list()
        for key1 in truthDict.keys():
            dataWriteLine = key1 + "\t"
            for key2 in truthDict[key1]:
                dataWriteLine = dataWriteLine + factDict[key2][key1] + ";"
            dataWriteLine = dataWriteLine.strip(";") + "\n"
            dataWriteList.append(dataWriteLine)
        return dataWriteList

    factDict = dict()
    claimDict = dict()

    global folder_write
    if dataset == 1: # movie
        folder_write = "movie"
        dataFile = open(file=os.path.join(datasetPath, folder_write, "factDB_movie"), mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_fact_dict(factDict, dataWrite)
        dataFile.close()

        dataFile = open(file=os.path.join(datasetPath, folder_write, "claimDB_movie"), mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_claim_dict(claimDict, dataWrite)
        dataFile.close()

    elif dataset == 0:
        folder_write = "book"
        dataFile = open(file=os.path.join(datasetPath, folder_write, "factDB_book"), mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_fact_dict(factDict, dataWrite)
        dataFile.close()

        dataFile = open(file=os.path.join(datasetPath, folder_write, "claimDB_book"), mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_claim_dict(claimDict, dataWrite)
        dataFile.close()

    elif dataset == -1: # this is for testing
        folder_write = "test"
        dataFile = open(file=test_fact_path, mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_fact_dict(factDict, dataWrite)
        dataFile.close()

        dataFile = open(file=test_claim_path, mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_claim_dict(claimDict, dataWrite)
        dataFile.close()

    start = time.time()
    objectClaimDict = generate_object_claim_dict(factDict, claimDict)
    truthDict = generate_truth_dict(objectClaimDict)
    dataWriteList = write_truth_dict(factDict, truthDict)
    used_time = time.time() - start
    result_write = open(file=outputWritePath + "/" + folder_write + "/" + "truth_result_MV_" + folder_write, mode="w", encoding="utf-8")
    result_write.write("OID\tInferTruth\n")
    result_write.writelines(dataWriteList)
    result_write.close()

    result_write = open(file="./" + "journal_" + folder_write, mode="a+", encoding="utf-8")
    result_write.write("Experiment on " + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M') + "\n")
    result_write.write("Total Time : " + str(used_time) + "\n")
    result_write.close()

"""
MV(1, "../DataToUse/movie", "./")
MV(0, "../DataToUse/book", "./")
"""