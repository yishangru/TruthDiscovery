import os
import time
import random

Movie_fact_path = "../DataToUse/movie/factDB_movie"
Movie_claim_path = "../DataToUse/movie/claimDB_movie"

Book_fact_path = "../DataToUse/book/factDB_book"
Book_claim_path = "../DataToUse/book/claimDB_book"

test_fact_path = "../DataToUse/test/testDB_fact_movie"
test_claim_path = "../DataToUse/test/testDB_claim_movie"

# initialization LTM
def LTM(alpha_set, beta_set, iterNumber, burninNumber, thinNumber, output_threshold, dataset, datasetPath, outputWritePath):

    def initialization_LTM(alpha_set, beta_set, iterNumber, burninNumber, thinNumber, output_threshold):
        global iterationCount, burninCount, thinCount
        thinCount = thinNumber
        burninCount = burninNumber
        iterationCount = iterNumber

        global beta, alpha
        beta = dict()
        for i in range(2):
            beta[str(i)] = beta_set[1 - i]
        alpha = dict()
        for i in range(2):
            alpha[str(i)] = dict()
            for j in range(2):
                alpha[str(i)][str(j)] = alpha_set[1 - i][1 - j]

        global threshold
        threshold = output_threshold

    # initialization sampling
    def initialization_sampling(dataset, datasetPath):
        def generate_fact_dict(factdict, dataWriteLine):
            dataSplit = dataWriteLine.split("\t")
            factdict[dataSplit[0]] = dict()
            factdict[dataSplit[0]][dataSplit[1]] = dataSplit[2] # BID, MID: Aurthor, Director

        def generate_claim_dict(claimdict, dataWriteLine):
            dataSplit = dataWriteLine.split("\t")
            if dataSplit[0] not in claimdict.keys():
                claimdict[dataSplit[0]] = dict()
            claimdict[dataSplit[0]][dataSplit[1]] = dataSplit[2]

        def generate_truth_dict(factdict):
            def uniform_initialization_truth():
                x = random.uniform(0,1)
                return "1" if x >=0.5 else "0"
            truthdict = dict()
            truth_probability_dict = dict()
            for key in factdict.keys():
                truthdict[key] = uniform_initialization_truth()
                truth_probability_dict[key] = 0
            return truthdict, truth_probability_dict

        factDict = dict()
        claimDict = dict()

        global folder_write
        if dataset == 1: # movie
            folder_write = "movie"
            dataFile = open(file=os.path.join(datasetPath, folder_write, "factDB_movie"), mode="r", encoding="utf-8")
            dataLines = dataFile.readlines()
            for dataLine in range(len(dataLines)):  # MID title year source director
                dataWrite = dataLines[dataLine].strip("\n")
                if not dataLine == 0:
                    generate_fact_dict(factDict, dataWrite)
            dataFile.close()

            dataFile = open(file=os.path.join(datasetPath, folder_write, "claimDB_movie"), mode="r", encoding="utf-8")
            dataLines = dataFile.readlines()
            for dataLine in range(len(dataLines)):  # MID title year source director
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
            dataFile = open(file=os.path.join(datasetPath, "test", "factDB_movie"), mode="r", encoding="utf-8")
            dataLines = dataFile.readlines()
            for dataLine in range(len(dataLines)):  # MID title year source director
                dataWrite = dataLines[dataLine].strip("\n")
                if not dataLine == 0:
                    generate_fact_dict(factDict, dataWrite)
            dataFile.close()

            dataFile = open(file=os.path.join(datasetPath, "test", "claimDB_movie"), mode="r", encoding="utf-8")
            dataLines = dataFile.readlines()
            for dataLine in range(len(dataLines)):  # MID title year source director
                dataWrite = dataLines[dataLine].strip("\n")
                if not dataLine == 0:
                    generate_claim_dict(claimDict, dataWrite)
            dataFile.close()

        def generate_source_matrix(claimDict, truthDict):
            source_matrix = dict()
            for key1 in claimDict.keys(): # fact
                for key2 in claimDict[key1].keys(): # source
                    if key2 not in source_matrix.keys():
                        source_matrix[key2] = dict()
                        for i in range(2):
                            source_matrix[key2][str(i)] = dict()
                            for j in range(2):
                                source_matrix[key2][str(i)][str(j)] = 0
                    source_matrix[key2][truthDict[key1]][claimDict[key1][key2]] += 1
            return source_matrix

        truthDict, truth_probability_dict = generate_truth_dict(factDict)
        sourceMatrix = generate_source_matrix(claimDict, truthDict)
        return factDict, claimDict, truthDict, truth_probability_dict, sourceMatrix

    # perform sampling
    def perform_sampling(dataset):
        global beta, alpha, threshold
        global iterationCount, burninCount, thinCount

        factDict, claimDict, truthDict, truth_probability_dict, sourceMatrix = initialization_sampling(dataset, datasetPath)
        #for key in sourceMatrix:
        #    print(key + ":" + str(sourceMatrix[key]))

        sample_size = iterationCount//thinCount - burninCount//thinCount
        for i in range(1, iterationCount + 1):
            for fact in factDict.keys():
                ptf = beta[truthDict[fact]]
                p_tf = beta[str(1 - int(truthDict[fact]))]
                for key in claimDict[fact]: # source
                    atfoc = alpha[truthDict[fact]][claimDict[fact][key]]
                    atf_oc = alpha[truthDict[fact]][str(1-int(claimDict[fact][key]))]
                    a_tfoc = alpha[str(1-int(truthDict[fact]))][claimDict[fact][key]]
                    a_tf_oc = alpha[str(1 - int(truthDict[fact]))][str(1-int(claimDict[fact][key]))]
                    ntfoc = sourceMatrix[key][truthDict[fact]][claimDict[fact][key]]
                    ntf_oc = sourceMatrix[key][truthDict[fact]][str(1-int(claimDict[fact][key]))]
                    n_tfoc = sourceMatrix[key][str(1-int(truthDict[fact]))][claimDict[fact][key]]
                    n_tf_oc = sourceMatrix[key][str(1-int(truthDict[fact]))][str(1-int(claimDict[fact][key]))]
                    ptf = ptf * (ntfoc - 1 + atfoc)/(ntfoc + ntf_oc - 1 + atfoc + atf_oc)
                    p_tf = p_tf * (n_tfoc + a_tfoc)/(n_tfoc + n_tf_oc + a_tfoc + a_tf_oc)
                if random.uniform(0,1) < p_tf/(ptf + p_tf):
                    truthDict[fact] = str(1-int(truthDict[fact]))
                    for key in claimDict[fact]:
                        sourceMatrix[key][str(1-int(truthDict[fact]))][claimDict[fact][key]] -= 1
                        sourceMatrix[key][truthDict[fact]][claimDict[fact][key]] += 1
                if i > burninCount and i % thinCount == 0:
                    truth_probability_dict[fact] = truth_probability_dict[fact] + int(truthDict[fact])/sample_size

        infer_truth_dict = truth_inference(factDict, truth_probability_dict)
        source_quality_matrix = source_quality_estimation(claimDict, truth_probability_dict)
        return infer_truth_dict, source_quality_matrix

    # infer truth
    def truth_inference(factDict, truth_probability_dict):
        global threshold
        infer_truth_dict = dict()
        for key in truth_probability_dict.keys():
            for object in factDict[key]:
                if object not in infer_truth_dict.keys():
                    infer_truth_dict[object] = list()
                if truth_probability_dict[key] >= threshold:
                    infer_truth_dict[object].append(factDict[key][object])
        return infer_truth_dict

    # source quality estimation
    def source_quality_estimation(claimDict, truth_probability_dict):
        global alpha
        source_quality_final = dict()
        source_quality_matrix = dict()
        for fact in claimDict.keys():
            for source in claimDict[fact].keys():
                if source not in source_quality_matrix.keys():
                    source_quality_final[source] = dict()
                    source_quality_matrix[source] = dict()
                    for i in range(2):
                        source_quality_matrix[source][str(i)] = dict()
                        for j in range(2):
                            source_quality_matrix[source][str(i)][str(j)] = 0
                source_quality_matrix[source]["1"][claimDict[fact][source]] += truth_probability_dict[fact]
                source_quality_matrix[source]["0"][claimDict[fact][source]] += (1 - truth_probability_dict[fact])

        for source in source_quality_final.keys():
            source_quality_final[source]["recall"] = (source_quality_matrix[source]["1"]["1"] + alpha["1"]["1"])/\
                                                     (source_quality_matrix[source]["1"]["1"] + source_quality_matrix[source]["1"]["0"] + alpha["1"]["1"] + alpha["1"]["0"])
            source_quality_final[source]["specificity"] = (source_quality_matrix[source]["0"]["0"] + alpha["0"]["0"])/\
                                                     (source_quality_matrix[source]["0"]["0"] + source_quality_matrix[source]["0"]["1"] + alpha["0"]["0"] + alpha["0"]["1"])
        return source_quality_final


    print("Now for " + str(iterNumber))
    start = time.time()
    initialization_LTM(alpha_set=alpha_set, beta_set=beta_set, iterNumber=iterNumber,
                       burninNumber=burninNumber, thinNumber=thinNumber, output_threshold=output_threshold)
    # initialization_LTM([[10, 10], [80, 8000]], [5, 5], iterNumber=iteration_number_holder[i], burninNumber=burnin_holder[i], thinNumber=thin_holder[i])
    infer_truth_dict, source_quality_matrix = perform_sampling(dataset)
    used_time = time.time() - start

    result_write = open(file=outputWritePath + "/" + folder_write + "/" + "truth_result_LTM_" + str(iterNumber) + "_" + folder_write, mode="w", encoding="utf-8")
    result_write.write("OID\tInferTruth\n")
    for object in infer_truth_dict.keys():
        writeLine = object + "\t"
        for fact in infer_truth_dict[object]:
            writeLine = writeLine + fact + ";"
        writeLine = writeLine.strip(";") + "\n"
        result_write.write(writeLine)
    result_write.write("time_used:" + str(used_time) + "\n")
    result_write.close()

    result_write = open(file=outputWritePath + "/" + folder_write + "/" + "source_result_LTM_" + folder_write + "_" + str(iterNumber), mode="w", encoding="utf-8")
    result_write.write("source\trecall\tspecificity\n")
    for source in source_quality_matrix:
        result_write.write(source + "\t" + str(source_quality_matrix[source]["recall"]) + "\t" + str(
            source_quality_matrix[source]["specificity"]) + "\n")
    result_write.close()

"""
Following method is used for testing the function, 
we first generate a small database to test correctness
"""

"""
iteration_number_holder = [7, 10, 20, 50, 100, 200, 350, 500]
burnin_holder = [2, 2, 5, 10, 20, 50, 75, 100]
thin_holder = [1, 1, 1, 2, 5, 5, 7, 10]
"""

# best parameter set in paper
"""
movie = [[50, 50], [100, 10000]], [10, 10], 50, 10, 2]
book = [[50, 50], [10, 1000]], [10, 10], 50, 10, 2]                                                                              
"""

threshold_set = 0.5
thin_set = 2
burnin_set = 10
iteration_setting = 10
"""
LTM([[50, 50], [10, 1000]], [10, 10], iterNumber=iteration_setting,
    burninNumber=burnin_set, thinNumber=thin_set, output_threshold=threshold_set, dataset=0, 
    datasetPath = "../DataToUse", outputWritePath="./")  # 1 movie, 0 book, -1 test
"""
LTM([[50, 50], [100, 10000]], [10, 10], iterNumber=iteration_setting,
    burninNumber=burnin_set, thinNumber=thin_set, output_threshold=threshold_set, dataset=1,
    datasetPath = "../DataToUse", outputWritePath="./") # 1 movie, 0 book, -1 test