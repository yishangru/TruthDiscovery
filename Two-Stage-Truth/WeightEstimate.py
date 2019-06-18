import math
import numpy as np

def estimate_weight(sourceQualityMatrix):
    sourceAttribute = open(file="../DataToUse/movie/sourceAttributeDB_movie", mode="r", encoding="utf-8")
    dataRead = sourceAttribute.readlines()
    source_list = list()
    attribute_list = list()
    for data in range(len(dataRead)):
        if not data == 0:
            dataSplit = dataRead[data].strip("\n").split("\t")
            for attribute in range(len(dataSplit)):
                if not attribute == 0:
                    attribute_list[attribute - 1].append(float(dataSplit[attribute]))
                else:
                    source_list.append(dataSplit[attribute])
        else:
            attribute_length = len(dataRead[data].strip("\n").split("\t"))
            for count in range(attribute_length - 1):
                attribute_list.append(list())
    # fill unknown value
    count_known = 0
    add_all_value = 0
    fill_attribute_index = 5
    for attribute in range(len(attribute_list[fill_attribute_index])):
        if not attribute_list[fill_attribute_index][attribute] == -1:
            count_known += 1
            add_all_value = add_all_value + attribute_list[fill_attribute_index][attribute]
    for attribute in range(len(attribute_list[fill_attribute_index])):
        if attribute_list[fill_attribute_index][attribute] == -1:
            attribute_list[fill_attribute_index][attribute] = add_all_value / count_known

    # normalize to normal distribution
    no_need_normalization = set(list([len(attribute_list) - 1, len(attribute_list) - 2]))
    for attribute in range(len(attribute_list)):
        if not attribute in no_need_normalization:
            average_value = sum(attribute_list[attribute]) / len(attribute_list[attribute])
            std_value = 0
            for attribute_value in range(len(attribute_list[attribute])):
                std_value = std_value + math.pow(attribute_list[attribute][attribute_value] - average_value, 2)
            std_value = math.sqrt(std_value / len(attribute_list[attribute]))
            for attribute_value in range(len(attribute_list[attribute])):
                attribute_list[attribute][attribute_value] = (attribute_list[attribute][
                                                                  attribute_value] - average_value) / std_value

    sp_quality = list()
    for source in source_list:
        sp_quality.append(sourceQualityMatrix[source]["specificity"])
    recall_quality = list()
    for source in source_list:
        recall_quality.append(sourceQualityMatrix[source]["recall"])
    y_sp = np.array(sp_quality).T
    y_re = np.array(recall_quality).T
    X_T = np.array(attribute_list)
    X = X_T.T

    inverse_result = np.dot(np.linalg.inv(np.dot(X_T, X)), X_T)
    w_re = np.dot(inverse_result, y_re)
    w_sp = np.dot(inverse_result, y_sp)

    adjusted_recall = np.dot(X, w_re)
    adjusted_specificity = np.dot(X, w_sp)
    for source in range(len(source_list)):
        adjusted_re_value = adjusted_recall[source]
        if adjusted_re_value >= 1:
            adjusted_re_value = max([sourceQualityMatrix[source_list[source]]["recall"], 0.95])
        sourceQualityMatrix[source_list[source]]["recall"] = adjusted_re_value
        adjusted_sp_value = adjusted_specificity[source]
        if adjusted_sp_value >= 1:
            adjusted_sp_value = max([sourceQualityMatrix[source_list[source]]["specificity"], 0.95])
        sourceQualityMatrix[source_list[source]]["specificity"] = adjusted_sp_value
    return sourceQualityMatrix, w_re, w_sp

"""
sourceQualityMatrix = dict()
sourceQuality = open(file="./TDM_movie_result/source_result_TDM_7", mode="r", encoding="utf-8")
dataRead = sourceQuality.readlines()
for data in range(len(dataRead)):
    if (not data == 0) and not (data == len(dataRead) - 1):
        dataSplit = dataRead[data].strip("\n").split("\t")
        sourceQualityMatrix[dataSplit[0]] = dict()
        sourceQualityMatrix[dataSplit[0]]["recall"] = float(dataSplit[1])
        sourceQualityMatrix[dataSplit[0]]["specificity"] = float(dataSplit[2])
sourceQuality.close()
sourceQualityMatrix, w_re, w_sp = estimate_weight(sourceQualityMatrix)
for source in sourceQualityMatrix:
    print(source + str(sourceQualityMatrix[source]))
"""