import os
import math
import time
from DomainSeparation import domain_histogram_count_for_year
from DomainSeparation import domain_histogram_count_for_price
test_fact_path = "../DataToUse/test/testDB_fact_movie"
test_claim_path = "../DataToUse/test/testDB_claim_movie"

def SATM(dataset, factdict, claimdict, sourceQualityMatrix, alpha, veracity, theta, iterationNumber, datasetPath):
    def generate_object_domain_mapping(dataset, domain_number, object_value_dict, datasetPath):
        def numeric_domain(domain, domain_separation, domain_object_dict, tag):
            try:
                attribute = float(domain)
                for domainSep in range(len(domain_separation)):
                    if attribute - domain_separation[domainSep] <= 0:
                        domain_add = tag + str(domainSep)
                        object_domain_dict[dataLine[0]].add(domain_add)
                        if domain_add not in domain_object_dict.keys():
                            domain_object_dict[domain_add] = set()
                        domain_object_dict[domain_add].add(dataLine[0])
                        break
                    elif domainSep == len(domain_separation) - 1:
                        domain_add = tag + str(domainSep + 1)
                        object_domain_dict[dataLine[0]].add(domain_add)
                        if domain_add not in domain_object_dict.keys():
                            domain_object_dict[domain_add] = set()
                        domain_object_dict[domain_add].add(dataLine[0])
            except Exception:
                pass

        object_domain_dict = dict()
        domain_object_dict = dict()
        if dataset == 0:
            price_separation = domain_histogram_count_for_price(domain_number, datasetPath)
            year_separation = domain_histogram_count_for_year(dataset, domain_number, datasetPath)
            dataRead = open(file=os.path.join(datasetPath, "book", "ObjectAttributeDB_book"), mode="r", encoding="utf-8")
            dataReadList = dataRead.readlines()
            for data in range(len(dataReadList)):  # len(dataReadList)
                if not data == 0:
                    dataLine = dataReadList[data].strip("\n").split("\t")
                    if dataLine[0] not in object_value_dict.keys():
                        continue
                    if dataLine[0] not in object_domain_dict.keys():
                        object_domain_dict[dataLine[0]] = set()
                    CategoryList = dataLine[2].split(",")
                    for category in CategoryList:  # category
                        object_domain_dict[dataLine[0]].add(category)
                        if category not in domain_object_dict.keys():
                            domain_object_dict[category] = set()
                        domain_object_dict[category].add(dataLine[0])
                    numeric_domain(dataLine[3], year_separation, domain_object_dict, "y")
                    numeric_domain(dataLine[4], price_separation, domain_object_dict, "p")
        elif dataset == 1:
            year_separation = domain_histogram_count_for_year(dataset, domain_number, datasetPath)
            dataRead = open(file=os.path.join(datasetPath, "movie", "ObjectAttributeDB_movie"), mode="r", encoding="utf-8")
            dataReadList = dataRead.readlines()
            for data in range(len(dataReadList)):  # len(dataReadList)
                if not data == 0:
                    dataLine = dataReadList[data].strip("\n").split("\t")
                    if dataLine[0] not in object_value_dict.keys():
                        continue
                    if dataLine[0] not in object_domain_dict.keys():
                        object_domain_dict[dataLine[0]] = set()
                    numeric_domain(dataLine[1], year_separation, domain_object_dict, "y")
                    if not dataLine[2] == "":  # country
                        object_domain_dict[dataLine[0]].add(dataLine[2])
                        if dataLine[2] not in domain_object_dict.keys():
                            domain_object_dict[dataLine[2]] = set()
                        domain_object_dict[dataLine[2]].add(dataLine[0])
                    GenreList = dataLine[3].split(",")
                    for genre in GenreList:  # genre
                        object_domain_dict[dataLine[0]].add(genre)
                        if genre not in domain_object_dict.keys():
                            domain_object_dict[genre] = set()
                        domain_object_dict[genre].add(dataLine[0])
        return object_domain_dict, domain_object_dict

    def generate_object_source_value_dict(factdict, claimdict):
        object_value_dict = dict()
        object_source_value_dict = dict()
        for key1 in claimdict.keys():
            for key2 in factdict[key1].keys():  # object only 1
                if key2 not in object_source_value_dict.keys():
                    object_source_value_dict[key2] = dict()
                if key2 not in object_value_dict.keys():
                    object_value_dict[key2] = dict()
                object_value_dict[key2][key1] = -1  # veracity score
                for key3 in claimdict[key1].keys():
                    if key3 not in object_source_value_dict[key2].keys():
                        object_source_value_dict[key2][key3] = dict()
                        object_source_value_dict[key2][key3]["claimed"] = set()
                    if claimdict[key1][key3] == "1":
                        object_source_value_dict[key2][key3]["claimed"].add(key1)
        return object_value_dict, object_source_value_dict

    def generate_source_object_dict(factdict, claimdict):
        source_object_dict = dict()
        for key1 in claimdict.keys():
            for key2 in factdict[key1].keys():
                for key3 in claimdict[key1].keys():
                    if key3 not in source_object_dict.keys():
                        source_object_dict[key3] = set()
                    source_object_dict[key3].add(key2)
        return source_object_dict

    def generate_source_domain_richness_dict(alpha, object_domain_dict, domain_object_dict, source_object_dict):
        domain_data_quantities = dict()  # dom: total quantities of information
        for dom in domain_object_dict.keys():
            domain_data_quantities[dom] = len(domain_object_dict[dom])

        source_domain_global_percent = dict()  # sou: {dom: global percentage}
        for sou in source_object_dict.keys():
            if sou not in source_domain_global_percent.keys():
                source_domain_global_percent[sou] = dict()
            for item in source_object_dict[sou]:
                for dom in object_domain_dict[item]:
                    if dom not in source_domain_global_percent[sou].keys():
                        source_domain_global_percent[sou][dom] = 0
                    source_domain_global_percent[sou][dom] += 1

        for sou in source_domain_global_percent.keys():  # calculate global domain percentage
            for dom in source_domain_global_percent[sou]:
                source_domain_global_percent[sou][dom] = float(
                    source_domain_global_percent[sou][dom] / domain_data_quantities[dom])

        source_domain_richness = dict()  # sou: {dom: richness}
        for sou in source_domain_global_percent.keys():  # calculate global domain richness
            if sou not in source_domain_richness.keys():
                source_domain_richness[sou] = dict()
            for dom in source_domain_global_percent[sou].keys():
                calculate_value = source_domain_global_percent[sou][dom]
                source_domain_richness[sou][dom] = math.sqrt(1 - math.pow((alpha * calculate_value - 1), 2))
        return source_domain_richness

    def generate_source_object_distance_dict(source_domain_richness, source_object_dict, object_domain_dict):
        source_object_distance_dict = dict()
        for sou in source_object_dict.keys():
            if sou not in source_object_distance_dict.keys():
                source_object_distance_dict[sou] = dict()
            for item in source_object_dict[sou]:
                if item not in source_object_distance_dict[sou].keys():
                    source_object_distance_dict[sou][item] = 0
                count_dom = 0
                distance_add = 0
                for dom in object_domain_dict[item]:
                    distance_add = distance_add + source_domain_richness[sou][dom]
                    count_dom = count_dom + 1
                if count_dom == 0:
                    source_object_distance_dict[sou][item] = 1
                else:
                    source_object_distance_dict[sou][item] = distance_add / count_dom
        return source_object_distance_dict

    # This part initialize the veracity score and confidence score
    def initialize_value_veracity_and_confidence(default_veracity_score, object_value_dict, object_source_value_dict):
        for object in object_value_dict.keys():
            for value in object_value_dict[object].keys():
                object_value_dict[object][value] = default_veracity_score
        for object in object_source_value_dict.keys():
            for sou in object_source_value_dict[object]:
                size_value_set = len(object_value_dict[object])
                size_claim_set = len(object_source_value_dict[object][sou]["claimed"])
                if not size_claim_set == 0:
                    object_source_value_dict[object][sou]["claimedConfidence"] = \
                        float((1 - float(
                            (size_value_set - size_claim_set) / math.pow(size_value_set, 2))) / size_claim_set)
                    object_source_value_dict[object][sou]["unclaimedConfidence"] = \
                        float(1 / math.pow(size_value_set, 2))
                else:
                    object_source_value_dict[object][sou]["claimedConfidence"] = 0
                    object_source_value_dict[object][sou]["unclaimedConfidence"] = 0

    # This part calculates veracity score for a value
    def update_veracity_score(object_value_dict, object_source_value_dict, source_object_distance_dict,
                              source_quality_matrix):
        for object in object_source_value_dict:
            for value in object_value_dict[object].keys():
                Prob_value_true = 1
                Prob_value_false = 1
                for sou in object_source_value_dict[object]:
                    if value in object_source_value_dict[object][sou]["claimed"]:
                        factor_power = source_object_distance_dict[sou][object] * object_source_value_dict[object][sou][
                            "claimedConfidence"]
                        Prob_value_true = Prob_value_true * \
                                          math.pow(source_quality_matrix[sou]["recall"], factor_power)
                        Prob_value_false = Prob_value_false * \
                                           math.pow(1 - source_quality_matrix[sou]["recall"], factor_power)

                    else:
                        factor_power = source_object_distance_dict[sou][object] * object_source_value_dict[object][sou][
                            "unclaimedConfidence"]
                        Prob_value_true = Prob_value_true * \
                                          math.pow(1 - source_quality_matrix[sou]["specificity"], factor_power)
                        Prob_value_false = Prob_value_false * \
                                           math.pow(source_quality_matrix[sou]["specificity"], factor_power)
                try:
                    previous_value = object_value_dict[object][value]
                    inter_value = (1 - previous_value) / previous_value * Prob_value_false / Prob_value_true
                    object_value_dict[object][value] = 1 / (1 + inter_value)
                except Exception:
                    object_value_dict[object][value] = 0

    # This part calculated recall for a data source
    def update_source_recall(source_object_dict, object_value_dict, object_source_value_dict, source_quality_matrix):
        for sou in source_quality_matrix.keys():
            true_claim_value_count = 0
            false_claim_value_count = 0
            for object in source_object_dict[sou]:
                for value in object_value_dict[object].keys():
                    if value in object_source_value_dict[object][sou]["claimed"]:
                        #if object_value_dict[object][value] >= 0.5:
                        true_claim_value_count += object_value_dict[object][value]
                    else:
                        #if object_value_dict[object][value] >= 0.5:
                        false_claim_value_count += object_value_dict[object][value]
            source_quality_matrix[sou]["recall"] = float(true_claim_value_count / (true_claim_value_count + false_claim_value_count))

    # This part calculated specificity for a data source
    def update_source_specificity(source_object_dict, object_value_dict, object_source_value_dict,
                                  source_quality_matrix):
        for sou in source_quality_matrix.keys():
            true_claim_value_count = 0
            false_claim_value_count = 0
            for object in source_object_dict[sou]:
                for value in object_value_dict[object]:
                    if value in object_source_value_dict[object][sou]["claimed"]:
                        #if object_value_dict[object][value] < 0.5:
                        false_claim_value_count += (1 - object_value_dict[object][value])
                    else:
                        #if object_value_dict[object][value] < 0.5:
                        true_claim_value_count += (1 - object_value_dict[object][value])
            try:
                inter_value = float(1 - false_claim_value_count / (false_claim_value_count + true_claim_value_count))
                source_quality_matrix[sou]["specificity"] = inter_value
            except Exception:
                print(false_claim_value_count + true_claim_value_count)

    def truth_inference(theta, object_value_dict, fact_dict):
        # write result
        infer_truth_dict = dict()
        for object in object_value_dict.keys():
            if object not in infer_truth_dict.keys():
                infer_truth_dict[object] = list()
            for value in object_value_dict[object].keys():
                if object_value_dict[object][value] >= theta:
                    infer_truth_dict[object].append(fact_dict[value][object])
        return infer_truth_dict


    ini_start_time = time.time()
    objectValueDict, objectSourceValueDict = generate_object_source_value_dict(factdict, claimdict)
    sourceObjectDict = generate_source_object_dict(factdict, claimdict)
    objectDomainDict, domainObjectDict = generate_object_domain_mapping(dataset, 8, objectValueDict, datasetPath)
    sourceDomainRichness = generate_source_domain_richness_dict(alpha, objectDomainDict, domainObjectDict, sourceObjectDict)
    sourceObjectDistanceDict = generate_source_object_distance_dict(sourceDomainRichness, sourceObjectDict,
                                                                    objectDomainDict)
    initialize_value_veracity_and_confidence(default_veracity_score=veracity, object_value_dict=objectValueDict,
                                             object_source_value_dict=objectSourceValueDict)
    ini_time = time.time() - ini_start_time  # output time for initialization

    count_itera = 0
    itera_start = time.time()
    while count_itera < iterationNumber:
        update_veracity_score(object_value_dict=objectValueDict, object_source_value_dict=objectSourceValueDict,
                              source_object_distance_dict=sourceObjectDistanceDict, source_quality_matrix=sourceQualityMatrix)
        update_source_recall(source_object_dict=sourceObjectDict, object_value_dict=objectValueDict,
                             object_source_value_dict=objectSourceValueDict, source_quality_matrix=sourceQualityMatrix)
        update_source_specificity(source_object_dict=sourceObjectDict, object_value_dict=objectValueDict,
                             object_source_value_dict=objectSourceValueDict, source_quality_matrix=sourceQualityMatrix)
        count_itera += 1
    inferTruthDict = truth_inference(theta=theta, object_value_dict=objectValueDict, fact_dict=factdict)
    itera_time = time.time() - itera_start
    total_experiment_time = ini_time + itera_time
    return inferTruthDict, sourceQualityMatrix, ini_time, itera_time, total_experiment_time