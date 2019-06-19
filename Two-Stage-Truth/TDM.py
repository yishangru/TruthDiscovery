import time
import random

def TDM(factDict, claimDict, beta_set, iterNumber, burninNumber, thinNumber, ratio):
    # initialization TDM
    def initialization_TDM(beta_set, iterNumber, burninNumber, thinNumber):
        global iterationCount, burninCount, thinCount
        thinCount = thinNumber
        burninCount = burninNumber
        iterationCount = iterNumber

        global beta
        beta = dict()
        for i in range(2):
            beta[str(i)] = beta_set[1 - i]

    # initialization sampling
    def initialization_sampling(factDict, claimDict, ratio):
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

        def generate_source_fact_dict(factdict, claimdict):
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
        sourceFactDict = generate_source_fact_dict(factDict, claimDict)
        # ratio as [ 11, 10, 10, 00]
        ratio_sum = sum(ratio)
        mini_ratio = min(ratio)/ratio_sum
        for i in range(len(ratio)):
            ratio[i] = ratio[i]/ratio_sum
        sourceAlphaDict = dict()
        for source in sourceFactDict.keys():
            sourceAlphaDict[source] = dict()
            for i in range(2):
                sourceAlphaDict[source][str(i)] = dict()
            if sourceFactDict[source]*mini_ratio > 5:
                sourceAlphaDict[source]["1"]["1"] = int(sourceFactDict[source]*ratio[0])
                sourceAlphaDict[source]["1"]["0"] = int(sourceFactDict[source]*ratio[1])
                sourceAlphaDict[source]["0"]["1"] = int(sourceFactDict[source]*ratio[2])
                sourceAlphaDict[source]["0"]["0"] = int(sourceFactDict[source]*ratio[3])
            else:
                sourceAlphaDict[source]["1"]["1"] = 5
                sourceAlphaDict[source]["1"]["0"] = 5
                sourceAlphaDict[source]["0"]["1"] = 5
                sourceAlphaDict[source]["0"]["0"] = 99
        return truthDict, truth_probability_dict, sourceMatrix, sourceAlphaDict

    # perform sampling
    def perform_sampling(factDict, claimDict, ratio):
        global beta
        global iterationCount, burninCount, thinCount

        # source quality estimation
        def source_quality_estimation(claimDict, truth_probability_dict, sourceAlphaDict):
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
                source_quality_final[source]["recall"] = (source_quality_matrix[source]["1"]["1"] +
                                                          sourceAlphaDict[source]["1"]["1"]) / \
                                                         (source_quality_matrix[source]["1"]["1"] +
                                                          source_quality_matrix[source]["1"]["0"] +
                                                          sourceAlphaDict[source]["1"]["1"] + sourceAlphaDict[source]["1"][
                                                              "0"])
                source_quality_final[source]["specificity"] = (source_quality_matrix[source]["0"]["0"] +
                                                               sourceAlphaDict[source]["0"]["0"]) / \
                                                              (source_quality_matrix[source]["0"]["0"] +
                                                               source_quality_matrix[source]["0"]["1"] +
                                                               sourceAlphaDict[source]["0"]["0"] +
                                                               sourceAlphaDict[source]["0"]["1"])
            return source_quality_final

        truthDict, truth_probability_dict, sourceMatrix, sourceAlphaDict = initialization_sampling(factDict, claimDict, ratio)
        sample_size = iterationCount//thinCount - burninCount//thinCount
        for i in range(1, iterationCount + 1):
            for fact in factDict.keys():
                ptf = beta[truthDict[fact]]
                p_tf = beta[str(1 - int(truthDict[fact]))]
                for key in claimDict[fact]: # source
                    atfoc = sourceAlphaDict[key][truthDict[fact]][claimDict[fact][key]]
                    atf_oc = sourceAlphaDict[key][truthDict[fact]][str(1-int(claimDict[fact][key]))]
                    a_tfoc = sourceAlphaDict[key][str(1-int(truthDict[fact]))][claimDict[fact][key]]
                    a_tf_oc = sourceAlphaDict[key][str(1 - int(truthDict[fact]))][str(1-int(claimDict[fact][key]))]
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
        source_quality_matrix = source_quality_estimation(claimDict, truth_probability_dict, sourceAlphaDict)
        return source_quality_matrix

    start = time.time()
    initialization_TDM(beta_set=beta_set, iterNumber=iterNumber,
                       burninNumber=burninNumber, thinNumber=thinNumber)
    source_quality_matrix = perform_sampling(factDict, claimDict, ratio)
    used_time = time.time() - start
    return source_quality_matrix, used_time

"""
def main_for_TDM():
    iteration_number_holder = [7, 10, 20, 50, 100, 200, 350, 500]
    burnin_holder = [2, 2, 5, 10, 20, 50, 75, 100]
    thin_holder = [1, 1, 1, 2, 5, 5, 7, 10]

    dataset = 0
    mapping = dict()
    mapping[1] = "TDM_movie_result"
    mapping[0] = "TDM_book_result"
    beta_set = [10, 10]
    #ratio as [11, 10, 10, 00]
    ratio = [1, 1, 1, 99]
    # ratio = [1, 1, 1, 9]

    factDict, claimDict = initialization_data_prepare(dataset)
    for i in range(len(iteration_number_holder)-4):
        print("Now for " + str(iteration_number_holder[i]))
        source_quality_matrix, used_time = TDM(factDict, claimDict, beta_set, iterNumber=iteration_number_holder[i],
            burninNumber=burnin_holder[i], thinNumber=thin_holder[i], ratio=ratio)
        print("Write for " + str(iteration_number_holder[i]))
        result_write = open(file="./" + mapping[dataset] + "/" + "source_result_TDM_" + str(iteration_number_holder[i]), mode="a+",
                            encoding="utf-8")
        result_write.write("source\trecall\tspecificity\n")
        for source in source_quality_matrix:
            result_write.write(source + "\t" + str(source_quality_matrix[source]["recall"]) + "\t" + str(
                source_quality_matrix[source]["specificity"]) + "\n")
        result_write.write("time_used:" + str(used_time) + "\n")
        result_write.close()
#main_for_TDM()
"""