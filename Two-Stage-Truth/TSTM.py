import os
import math
import time
import datetime
from TDM import TDM
from SATM import SATM
from WeightEstimate import estimate_weight

def initialization_data_prepare(dataset, datasetPath):
    def generate_fact_dict(factdict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        factdict[dataSplit[0]] = dict()
        factdict[dataSplit[0]][dataSplit[1]] = dataSplit[2] # BID, MID: Aurthor, Director

    def generate_claim_dict(claimdict, dataWriteLine):
        dataSplit = dataWriteLine.split("\t")
        if dataSplit[0] not in claimdict.keys():
            claimdict[dataSplit[0]] = dict()
        claimdict[dataSplit[0]][dataSplit[1]] = dataSplit[2]

    factDict = dict()
    claimDict = dict()

    if dataset == 1:  # movie
        dataFile = open(file=os.path.join(datasetPath, "movie", "factDB_movie"), mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):  # MID title year source director
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_fact_dict(factDict, dataWrite)
        dataFile.close()

        dataFile = open(file=os.path.join(datasetPath, "movie", "claimDB_movie"), mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):  # MID title year source director
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_claim_dict(claimDict, dataWrite)
        dataFile.close()

    elif dataset == 0:
        dataFile = open(file=os.path.join(datasetPath, "book", "factDB_book"), mode="r", encoding="utf-8")
        dataLines = dataFile.readlines()
        for dataLine in range(len(dataLines)):  # MID title year source director
            dataWrite = dataLines[dataLine].strip("\n")
            if not dataLine == 0:
                generate_fact_dict(factDict, dataWrite)
        dataFile.close()

        dataFile = open(file=os.path.join(datasetPath, "book", "claimDB_book"), mode="r", encoding="utf-8")
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
    return factDict, claimDict

def main_for_TSTM(dataset, ratio, alpha, iteration_SATM, whether_estimate, datasetPath, outputWritePath):
    mapping = dict()
    mapping[0] = "book"
    mapping[1] = "movie"
    mapping[-1] = "test"

    # for TDM
    beta_set = [10, 10]
    thin_number = 1
    burnin_number = 2
    iteration_TDM = 7
    # end for TDM

    # adjust factor
    recall_ad = 0.8
    sp_ad = 0.9

    # for SATM
    veracity = 0.5
    theta = 0.5
    # end for SATM

    fileWrite = mapping[dataset]

    factDict, claimDict = initialization_data_prepare(dataset, datasetPath)

    nowTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
    output_journal = open(file="./journal_" + fileWrite, mode="a+", encoding="utf-8")
    output_journal.write("Experiment on " + nowTime + "\n")

    source_quality_matrix, used_time = TDM(factDict, claimDict, beta_set, iterNumber=iteration_TDM,
                                           burninNumber=burnin_number, thinNumber=thin_number, ratio=ratio)
    result_write = open(file=outputWritePath + "/" + fileWrite + "/source_result_stage1_" + fileWrite, mode="w", encoding="utf-8")
    result_write.write("source\trecall\tspecificity\n")
    for source in source_quality_matrix:
        result_write.write(source + "\t" + str(source_quality_matrix[source]["recall"]) + "\t" + str(
            source_quality_matrix[source]["specificity"]) + "\n")
    result_write.close()

    w_re = list()
    w_sp = list()
    inter_start = time.time()
    if whether_estimate and dataset == 1:
        source_quality_matrix, w_re, w_sp = estimate_weight(source_quality_matrix)

    for source in source_quality_matrix.keys():
        source_quality_matrix[source]["recall"] = math.pow(source_quality_matrix[source]["recall"], recall_ad)
        source_quality_matrix[source]["specificity"] = math.pow(source_quality_matrix[source]["specificity"], sp_ad)
    inter_time = time.time() - inter_start

    if whether_estimate and dataset == 1:
        weight_estimate_write = open(file=outputWritePath + "/" + fileWrite + "/weight_estimate_" + fileWrite, mode="w", encoding="utf-8")
        weight_re = ""
        for weight in w_re:
            weight_re = weight_re + str(weight) + "\t"
        weight_estimate_write.write("RECALL\t" + weight_re.strip("\t") + "\n")
        weight_sp = ""
        for weight in w_sp:
            weight_sp = weight_sp + str(weight) + "\t"
        weight_estimate_write.write("SPECIFICITY\t" + weight_sp.strip("\t") + "\n")
        weight_estimate_write.close()

    inferTruthDict, sourceQualityMatrix, ini_time, itera_time, total_experiment_time = \
        SATM(dataset, factDict, claimDict, source_quality_matrix, alpha, veracity, theta, iteration_SATM, datasetPath)

    output_journal.write("Stage 1 Time:" + str(used_time) + "\n")
    output_journal.write("Inter Stage Time:" + str(inter_time) + "\n")
    output_journal.write("Stage 2 Init Time: " + str(ini_time) + "\n")
    output_journal.write("Stage 2 Iteration Time: " + str(itera_time) + "\n")
    output_journal.write("Stage 2 Time: " + str(total_experiment_time) + "\n")
    output_journal.write("Total Experiment Time: " + str(total_experiment_time + used_time + inter_time) + "\n")
    output_journal.write("\n")
    output_journal.close()

    result_write = open(file=outputWritePath + "/" + fileWrite + "/truth_result_TST_" + fileWrite + "_" + str(int(whether_estimate)),
                        mode="w", encoding="utf-8")
    result_write.write("OID\tInferTruth\n")
    for object in inferTruthDict.keys():
        writeLine = object + "\t"
        for fact in inferTruthDict[object]:
            writeLine = writeLine + fact + ";"
        writeLine = writeLine.strip(";") + "\n"
        result_write.write(writeLine)
    result_write.close()

    result_write = open(file=outputWritePath + "/" + fileWrite + "/" + "source_result_stage2_" + fileWrite + "_" + str(int(whether_estimate)),
                        mode="w", encoding="utf-8")
    result_write.write("source\trecall\tspecificity\n")
    for source in sourceQualityMatrix:
        result_write.write(source + "\t" + str(sourceQualityMatrix[source]["recall"]) + "\t" + str(
            sourceQualityMatrix[source]["specificity"]) + "\n")
    result_write.close()

# alpha 2 for book, 1.5 for movie

"""
dataset = 1
alpha = 1.5
iteration_SATM = 10
whether_estimate = False
ratio_matrix = [1, 1, 1, 99] # 10, 10; 20, 20; 30, 30; 40, 40; 50, 50
main_for_TSTM(dataset=dataset, ratio=ratio_matrix, alpha=alpha, iteration_SATM=iteration_SATM,
              whether_estimate=whether_estimate, datasetPath="../DataToUse", outputWritePath="./")
"""