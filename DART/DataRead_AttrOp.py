# -*- coding:utf-8 -*-
import os
import random

Movie_db_path = "../DataToUse/movie/ToUseDB_movie"
Movie_attribute_path = "../DataToUse/movie/ObjectAttributeDB_movie"
Book_db_path = "../DataToUse/book/ToUseDB_book"
Book_attribute_path = "../DataToUse/book/ObjectAttributeDB_book"
Test_db_path = "../DataToUse/test/testDB_movie"

"""
This part for data read and db operation
Perform attribute operation and aggregate operation
"""
object_source_dict = dict()  # object: {sou: set(dom)}
source_object_dict = dict()  # sou: {object: set()}

object_domain_dict = dict()  # object: {dom: claim_count}
domain_object_dict = dict()  # dom: set(object)
object_main_domain_dict = dict()  # object_id: main_dom_id

object_source_value_dict = dict()  # object_id: {sou_id: {claim: set(), confidence_claimed, confidence_unclaimed}}
object_value_dict = dict() # object {value: veracity}

# obj: {sou:{Claimed: set(), confidence_claimed, confidence_unclaimed}}
# obj: value: veracity_score
def object_source_value_mapping_claimed(object, sou, claim_value):
    if object not in object_value_dict.keys():
        object_value_dict[object] = dict()

    if object not in object_source_value_dict.keys():
        object_source_value_dict[object] = dict()

    if sou not in object_source_value_dict[object].keys():
        object_source_value_dict[object][sou] = dict()
        object_source_value_dict[object][sou]["claimed"] = set()

    if not claim_value == "none":
        if claim_value not in object_value_dict[object].keys():
            object_value_dict[object][claim_value] = -1
        object_source_value_dict[object][sou]["claimed"].add(claim_value)

# output the mapping relation between O and D (identifying the domain richness for source)  obj_n: {dom_n: count} ; dom_n: set(obj_n)
def object_domain_mapping(object, dom):  # consider inference for object domain
    if object in object_value_dict.keys():
        if object not in object_domain_dict.keys():
            object_domain_dict[object] = dict()

        if dom not in domain_object_dict.keys():
            domain_object_dict[dom] = set()
        domain_object_dict[dom].add(object)

        if dom not in object_domain_dict[object]:
            object_domain_dict[object][dom] = 1
        else:
            object_domain_dict[object][dom] += 1

# find main domain for object
def object_main_domain_mapping():
    for key in object_domain_dict.keys():
        main_domain_set = set()
        domain_claim_count = -1
        for dom in object_domain_dict[key].keys():
            if object_domain_dict[key][dom] > domain_claim_count:
                main_domain_set.clear()
                main_domain_set.add(dom)
                domain_claim_count = object_domain_dict[key][dom]
            elif object_domain_dict[key][dom] == domain_claim_count:
                main_domain_set.add(dom)
        if len(main_domain_set) > 1:
            main_domain_set = list(main_domain_set)
            select_dom = random.randint(0,len(main_domain_set)-1) # random choose one as main domain
            object_main_domain_dict[key] = main_domain_set[select_dom]
        elif len(main_domain_set) == 1:
            object_main_domain_dict[key] = main_domain_set.pop()

# output the value sets for each source in object o |O|*|S|
# obj_n: {sou_n: set(dom_id)}; sou_n:set(obj_n)  unique
def object_source_mapping():
    """
    if object not in object_source_dict.keys():
        object_source_dict[object] = dict()
    if sou not in object_source_dict[object].keys():
        object_source_dict[object][sou] = set()
    object_source_dict[object][sou].add(dom)
    """
    for object in object_source_value_dict.keys():
        for sou in object_source_value_dict[object].keys():
            if sou not in source_object_dict.keys():
                source_object_dict[sou] = dict()
            if object_main_domain_dict[object] not in source_object_dict[sou].keys():
                source_object_dict[sou][object_main_domain_dict[object]] = set()
            source_object_dict[sou][object_main_domain_dict[object]].add(object)

def main_for_DART_Data_op(dataset, datasetPath):
    mapping = dict()
    mapping[1] = "movie"
    mapping[0] = "book"

    if dataset == 1:
        dataDB = open(file=os.path.join(datasetPath, mapping[dataset], "ToUseDB_movie"), mode="r", encoding="utf-8")
        dataRead = dataDB.readlines()
        for data in range(len(dataRead)):
            if not data == 0:
                dataSplit = dataRead[data].strip("\n").split("\t")
                object_source_value_mapping_claimed(dataSplit[0], dataSplit[3], dataSplit[4])
        dataDB.close()
        dataDB = open(file=os.path.join(datasetPath, mapping[dataset], "ObjectAttributeDB_movie"), mode="r", encoding="utf-8")
        dataRead = dataDB.readlines()
        for data in range(len(dataRead)):
            if not data == 0:
                dataSplit = dataRead[data].strip("\n").split("\t")
                object_domain_mapping(dataSplit[0], dataSplit[3].split(",")[0])
        dataDB.close()

    elif dataset == 0:
        dataDB = open(file=os.path.join(datasetPath, mapping[dataset], "ToUseDB_book"), mode="r", encoding="utf-8")
        dataRead = dataDB.readlines()
        for data in range(len(dataRead)):
            if not data == 0:
                dataSplit = dataRead[data].strip("\n").split("\t")
                object_source_value_mapping_claimed(dataSplit[0], dataSplit[2], dataSplit[3])
        dataDB.close()
        dataDB = open(file=os.path.join(datasetPath, mapping[dataset], "ObjectAttributeDB_book"), mode="r", encoding="utf-8")
        dataRead = dataDB.readlines()
        for data in range(len(dataRead)):
            if not data == 0:
                dataSplit = dataRead[data].strip("\n").split("\t")
                object_domain_mapping(dataSplit[0], dataSplit[2].split(",")[0])
        dataDB.close()

    object_main_domain_mapping()
    object_source_mapping()
    return mapping[dataset]