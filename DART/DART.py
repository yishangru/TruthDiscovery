# -*- coding:utf-8 -*-
import os
import math
import time
import datetime
import DataRead_AttrOp
from DataRead_AttrOp import main_for_DART_Data_op
"""
Implementation of "Domain-Aware Multi=Truth Discovery form Conflicting Sources"
Start on 2018.10.24 End at 2018.11.02
This paper identifies the diversities in reliability, considering the variance in information richness in specific
domain for different sources.
Realizing this influence, this paper combines the richness factor into a Bayesian based reliability deciding method.
Through performing iteration until reaching stable, the reliability of source can be determined, thus further deciding the
reliability of provided information.
"""

# This part infers domain percent and richness for sources
source_domain_global_percent = dict() # sou: {dom: global percentage}
source_domain_richness = dict() # sou: {dom: richness}
domain_data_quantities = dict() # dom: total quantities of information

def calculate_source_domain_percent():
    for sou in DataRead_AttrOp.source_object_dict.keys():
        if sou not in source_domain_global_percent.keys():
            source_domain_global_percent[sou] = dict()
        for dom in DataRead_AttrOp.source_object_dict[sou]:
            if dom not in source_domain_global_percent[sou].keys():
                source_domain_global_percent[sou][dom] = 0
            if dom not in domain_data_quantities.keys():
                domain_data_quantities[dom] = 0
            source_domain_global_percent[sou][dom] += len(DataRead_AttrOp.source_object_dict[sou][dom])
            domain_data_quantities[dom] += len(DataRead_AttrOp.source_object_dict[sou][dom])

    for sou in source_domain_global_percent.keys():   # calculate global domain percentage
        for dom in source_domain_global_percent[sou]:
            source_domain_global_percent[sou][dom] = float(source_domain_global_percent[sou][dom]/domain_data_quantities[dom])

def calculate_source_domain_richness(alpha):
    for sou in source_domain_global_percent.keys():  # calculate global domain richness
        if sou not in source_domain_richness.keys():
            source_domain_richness[sou] = dict()
        for dom in source_domain_global_percent[sou].keys():
            calculate_value = source_domain_global_percent[sou][dom]
            source_domain_richness[sou][dom] = math.sqrt(1 - math.pow((alpha * calculate_value - 1), 2))
"""
# This part infers the correlation relations between domains
source_inter_domain_influence = dict()  # sou_id: {dom_id: {other_domain_id: other_dom->dom} }
source_inter_domain_object_mapping = dict()  # sou_id: {dom_id: object_id_set()}
source_adjusted_domain_expertise = dict()  # sou_id: {dom_id: adjusted domain expertise}

def calculate_source_inter_domain_influence():
    for sou_id in DataRead_AttrOp.number_source_dict.keys():  # initialize source inter-domain influence and source-domain-object-mapping
        source_inter_domain_influence[sou_id] = dict()
        source_inter_domain_object_mapping[sou_id] = dict()
        for top_dom_id in DataRead_AttrOp.number_domain_dict.keys():
            source_inter_domain_influence[sou_id][top_dom_id] = dict()
            source_inter_domain_object_mapping[sou_id][top_dom_id] = set()
            for sub_dom_id in DataRead_AttrOp.number_domain_dict.keys():
                if not top_dom_id == sub_dom_id:
                    source_inter_domain_influence[sou_id][top_dom_id][sub_dom_id] = 0

    for sou_id in DataRead_AttrOp.number_source_dict.keys():  # find the source - object domain
        for object_id in DataRead_AttrOp.source_object_dict[sou_id]:
            for domain_id in DataRead_AttrOp.object_source_dict[object_id][sou_id]:
                source_inter_domain_object_mapping[sou_id][domain_id].add(object_id)

    for sou_id in source_inter_domain_influence:
        for top_dom_id in source_inter_domain_influence[sou_id]:
            for sub_dom_id in source_inter_domain_influence[sou_id][top_dom_id]:
                intersect_set = source_inter_domain_object_mapping[sou_id][top_dom_id].intersection(source_inter_domain_object_mapping[sou_id][sub_dom_id])
                source_inter_domain_influence[sou_id][top_dom_id][sub_dom_id] = float(len(intersect_set)/len(source_inter_domain_object_mapping[sou_id][sub_dom_id]))

def calculate_source_adjusted_domain_expertise(rou, without):
    for sou_id in DataRead_AttrOp.number_source_dict.keys():
        source_adjusted_domain_expertise[sou_id] = dict()
        for dom_id in DataRead_AttrOp.number_domain_dict.keys():
            inter_domain_expertise = source_domain_richness[sou_id][dom_id]
            for influ_domain in source_inter_domain_influence[sou_id][dom_id].keys():
                inter_domain_expertise = inter_domain_expertise + rou*source_domain_richness[sou_id][influ_domain]*source_inter_domain_influence[sou_id][dom_id][influ_domain]
            if not without:
                source_adjusted_domain_expertise[sou_id][dom_id] = inter_domain_expertise
            else:
                source_adjusted_domain_expertise[sou_id][dom_id] = source_domain_richness[sou_id][dom_id]
"""

# This part initialize the source domain recall and specificity rate
source_domain_recall = dict()  # sou_id: {dom_id: recall}
source_domain_sp = dict()  # sou_id: {dom_id: specificity}

def initialize_rec_sp_source(default_rec, default_sp):
    for sou in source_domain_global_percent.keys():
        source_domain_recall[sou] = dict()
        source_domain_sp[sou] = dict()
        for dom in source_domain_global_percent[sou].keys():
            source_domain_recall[sou][dom] = default_rec
            source_domain_sp[sou][dom] = default_sp

# This part initialize the veracity score and confidence score
def initialize_value_veracity_and_confidence(default_veracity_score):
    for object in DataRead_AttrOp.object_value_dict.keys():
        for value in DataRead_AttrOp.object_value_dict[object].keys():
            DataRead_AttrOp.object_value_dict[object][value] = default_veracity_score
    for object in DataRead_AttrOp.object_source_value_dict.keys():
        for sou in DataRead_AttrOp.object_source_value_dict[object]:
            size_value_set = len(DataRead_AttrOp.object_value_dict[object])
            size_claim_set = len(DataRead_AttrOp.object_source_value_dict[object][sou]["claimed"])
            if not size_claim_set == 0:
                DataRead_AttrOp.object_source_value_dict[object][sou]["claimedConfidence"] = \
                    float((1-float((size_value_set - size_claim_set)/math.pow(size_value_set, 2)))/size_claim_set)
                DataRead_AttrOp.object_source_value_dict[object][sou]["unclaimedConfidence"] = \
                    float(1/math.pow(size_value_set, 2))
            else:
                DataRead_AttrOp.object_source_value_dict[object][sou]["claimedConfidence"] = 0
                DataRead_AttrOp.object_source_value_dict[object][sou]["unclaimedConfidence"] = 0

# This part calculates veracity score for a value
def update_veracity_score():
    for object in DataRead_AttrOp.object_source_value_dict:
        main_dom = DataRead_AttrOp.object_main_domain_dict[object]
        for value in DataRead_AttrOp.object_value_dict[object].keys():
            Prob_value_true = 1
            Prob_value_false = 1
            for sou in DataRead_AttrOp.object_source_value_dict[object]:
                if value in DataRead_AttrOp.object_source_value_dict[object][sou]["claimed"]:
                    factor_power = source_domain_richness[sou][main_dom]*DataRead_AttrOp.object_source_value_dict[object][sou]["claimedConfidence"]
                    Prob_value_true = Prob_value_true * \
                                      math.pow(source_domain_recall[sou][main_dom], factor_power)
                    Prob_value_false = Prob_value_false * \
                                       math.pow(1 - source_domain_recall[sou][main_dom], factor_power)

                else:
                    factor_power = source_domain_richness[sou][main_dom] * DataRead_AttrOp.object_source_value_dict[object][sou]["unclaimedConfidence"]
                    Prob_value_true = Prob_value_true * \
                                      math.pow(1-source_domain_sp[sou][main_dom], factor_power)
                    Prob_value_false = Prob_value_false * \
                                       math.pow(source_domain_sp[sou][main_dom], factor_power)
            # update veracity score
            try:
                previous_value = DataRead_AttrOp.object_value_dict[object][value]
                inter_value = (1-previous_value)/previous_value * Prob_value_false / Prob_value_true
                DataRead_AttrOp.object_value_dict[object][value] = 1/(1 + inter_value)
            except Exception:
                DataRead_AttrOp.object_value_dict[object][value] = 0

# This part calculated recall for a data source
def update_source_recall():
    for sou in source_domain_recall.keys():
        for dom in source_domain_recall[sou]:
            veracity_add = 0
            total_claim_value_count = 0
            for object in DataRead_AttrOp.source_object_dict[sou][dom]:
                for value in DataRead_AttrOp.object_source_value_dict[object][sou]["claimed"]:
                    veracity_add = veracity_add + DataRead_AttrOp.object_value_dict[object][value]
                    total_claim_value_count += 1
            if not total_claim_value_count == 0:
                source_domain_recall[sou][dom] = float(veracity_add/total_claim_value_count)

# This part calculated specificity for a data source
def update_source_specificity():
    for sou in source_domain_sp.keys():
        for dom in source_domain_sp[sou].keys():
            veracity_add = 0
            total_unclaim_value_count = 0
            for object in DataRead_AttrOp.source_object_dict[sou][dom]:
                for value in DataRead_AttrOp.object_value_dict[object]:
                    if value not in DataRead_AttrOp.object_source_value_dict[object][sou]["claimed"]:
                        veracity_add = veracity_add + 1 - DataRead_AttrOp.object_value_dict[object][value]
                        total_unclaim_value_count += 1
            if not total_unclaim_value_count == 0:
                source_domain_sp[sou][dom] = float(veracity_add/total_unclaim_value_count)

# This part writes record for supervising the iteration process
def truth_inference(theta, fileWrite, outputPath):
    # write result
    infer_truth_dict = dict()
    for object in DataRead_AttrOp.object_value_dict.keys():
        if object not in infer_truth_dict.keys():
            infer_truth_dict[object] = list()
        for value in DataRead_AttrOp.object_value_dict[object].keys():
            if DataRead_AttrOp.object_value_dict[object][value] >= theta:
                infer_truth_dict[object].append(value)
    result_write = open(file=outputPath + "/" + fileWrite + "/truth_result_DART_" + fileWrite, mode="w", encoding="utf-8")
    result_write.write("OID\tInferTruth\n")
    for object in infer_truth_dict.keys():
        writeLine = object + "\t"
        for fact in infer_truth_dict[object]:
            writeLine = writeLine + fact + ";"
        writeLine = writeLine.strip(";") + "\n"
        result_write.write(writeLine)

# This part performs the iteration process
# alpha for domain richness; theta for final output threshold; rou for inter-domain, without True NOT inter-domain
# recall for default recall rate; sp for default specificity rate; veracity for default veracity score
def DART(alpha, theta, recall, sp, veracity, iterationNumber, fileWrite, outputWritePath):
    nowTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
    output_journal = open(file="./journal_"+fileWrite, mode="a+", encoding="utf-8")
    output_journal.write("Experiment on " + nowTime + "\n")
    output_journal.write("alpha\ttheta\tre_default\tsp_default\tveracity\titeration\n")
    output_journal.write(str(alpha) + "\t" + str(theta) + "\t" + str(recall) + "\t" + str(sp) + "\t" + str(veracity) + "\t" + str(iterationNumber) + "\n")

    ini_start_time = time.time()
    calculate_source_domain_percent()
    calculate_source_domain_richness(alpha=alpha)

    #calculate_source_inter_domain_influence()
    #calculate_source_adjusted_domain_expertise(rou=rou, without=without)

    initialize_rec_sp_source(default_rec=recall, default_sp=sp)
    initialize_value_veracity_and_confidence(default_veracity_score=veracity)
    ini_time = time.time() - ini_start_time  # output time for initialization
    output_journal.write("Initialize Time: " + str(ini_time) + "\n")

    count_itera = 0
    itera_start = time.time()
    while count_itera < iterationNumber:
        update_veracity_score()
        update_source_recall()
        update_source_specificity()
        count_itera += 1
    truth_inference(theta=theta, fileWrite=fileWrite, outputPath=outputWritePath)
    itera_time = time.time() - itera_start
    output_journal.write("Total Iteration Time: " + str(itera_time) + "\n")
    total_experiment_time = ini_time + itera_time
    output_journal.write("Total Time with Experiment: " + str(total_experiment_time) + "\n")
    output_journal.write("\n")

# in paper movie a = 1, book = 1.5
#file_write = main_for_DART_Data_op(1, os.path.abspath("../ForExperiment/OnServer/DataToUse/test/10k"))
#DART(1, 0.5, 0.9, 0.9, 0.5, 20, file_write, os.path.abspath("./test"))

#file_write = main_for_DART_Data_op(0, os.path.abspath("../DataToUse"))
#DART(1.5, 0.5, 0.8, 0.9, 0.5, 20, file_write, os.path.abspath("./"))