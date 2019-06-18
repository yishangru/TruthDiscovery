import os
# MID Genres Country Year
# ISBN Category Price Year
def domain_histogram_count_for_year(dataset, groupNumber, datasetPath): #
    def read_attribute_value(dataset):
        attribute_set = set()
        attribute_count_dict = dict()

        if dataset == 1:
            attribute_db = open(file=os.path.join(datasetPath, "movie", "ObjectAttributeDB_movie"), mode="r", encoding="utf-8")
            attribute_data_list = attribute_db.readlines()
            for attribute_data in range(len(attribute_data_list)):
                dataSplit = attribute_data_list[attribute_data].strip("\n").split("\t")[1]
                try:
                    year = int(dataSplit)
                    if year > 2100:
                        raise Exception
                    attribute_set.add(year)
                    if year not in attribute_count_dict.keys():
                        attribute_count_dict[year] = 0
                    attribute_count_dict[year] += 1
                except Exception:
                    pass
            attribute_list = list(attribute_set)
            attribute_list.sort()
            return attribute_list, attribute_count_dict
        elif dataset == 0:
            attribute_db = open(file=os.path.join(datasetPath, "book", "ObjectAttributeDB_book"), mode="r", encoding="utf-8")
            attribute_data_list = attribute_db.readlines()
            for attribute_data in range(len(attribute_data_list)):
                dataSplit = attribute_data_list[attribute_data].strip("\n").split("\t")[3]
                try:
                    year = int(dataSplit)
                    if year > 2100:
                        raise Exception
                    attribute_set.add(year)
                    if year not in attribute_count_dict.keys():
                        attribute_count_dict[year] = 0
                    attribute_count_dict[year] += 1
                except Exception:
                    pass
            attribute_list = list(attribute_set)
            attribute_list.sort()
            return attribute_list, attribute_count_dict

    attributeList, attributeCount = read_attribute_value(dataset)
    separation, index_sep = domain_separation(groupNumber, attributeList, attributeCount)
    """
    count = 0
    matlab_attribute = "year" + str(count) + " = ["
    matlab_attribute_count = "count" + str(count) + " = ["
    for attribute in range(len(attributeList)):
        matlab_attribute = matlab_attribute + str(attributeList[attribute]) + ", "
        matlab_attribute_count = matlab_attribute_count + str(attributeCount[attributeList[attribute]]) + ", "
        if count < len(index_sep):
            if attribute == index_sep[count]:
                matlab_attribute = matlab_attribute.strip(" ").strip(",") + "];"
                matlab_attribute_count = matlab_attribute_count.strip(" ").strip(",") + "];"
                print(matlab_attribute)
                print(matlab_attribute_count)
                count += 1
                matlab_attribute = "year" + str(count) + " = ["
                matlab_attribute_count = "count" + str(count) + " = ["
    matlab_attribute = matlab_attribute.strip(" ").strip(",") + "];"
    matlab_attribute_count = matlab_attribute_count.strip(" ").strip(",") + "];"
    print(matlab_attribute)
    print(matlab_attribute_count)
    """
    return separation

def domain_histogram_count_for_price(groupNumber, datasetPath):
    def read_attribute_value():
        attribute_set = set()
        attribute_count_dict = dict()
        attribute_db = open(file=os.path.join(datasetPath, "book", "ObjectAttributeDB_book"), mode="r", encoding="utf-8")
        attribute_data_list = attribute_db.readlines()
        for attribute_data in range(len(attribute_data_list)):
            dataSplit = attribute_data_list[attribute_data].strip("\n").split("\t")[4]
            try:
                price = round(float(dataSplit))
                attribute_set.add(price)
                if price not in attribute_count_dict.keys():
                    attribute_count_dict[price] = 0
                attribute_count_dict[price] += 1
            except Exception:
                pass
        attribute_list = list(attribute_set)
        attribute_list.sort()
        return attribute_list, attribute_count_dict

    attributeList, attributeCount = read_attribute_value()
    separation, index_holder = domain_separation(groupNumber, attributeList, attributeCount)
    #for attribute in attributeList:
    #    print(str(attribute) + " : " + str(attributeCount[attribute]))
    """
    matlab_attribute = "["
    matlab_attribute_count = "["
    for attribute in attributeList:
        matlab_attribute = matlab_attribute + str(attribute) + ", "
        matlab_attribute_count = matlab_attribute_count + str(attributeCount[attribute]) + ", "
    matlab_attribute = matlab_attribute.strip(" ").strip(",") + "]"
    matlab_attribute_count = matlab_attribute_count.strip(" ").strip(",") + "]"
    print(matlab_attribute)
    print(matlab_attribute_count)
    """
    return separation

def domain_separation(group_number, attributeList, attributeCount):
    total_object = 0
    for key in attributeCount.keys():
        total_object = total_object + attributeCount[key]
    group_member_count = int(total_object/group_number)
    separation = list()
    index_sep = list()
    temp_member_count = 0
    for attribute in range(len(attributeList)):
        if temp_member_count + attributeCount[attributeList[attribute]] > group_member_count:
            if temp_member_count < 0.5*group_member_count:
                attribute += 1
            separation.append(attributeList[attribute])
            index_sep.append(attribute)
            temp_member_count = 0
        else:
            temp_member_count = temp_member_count + attributeCount[attributeList[attribute]]
    return separation, index_sep

"""
domain_histogram_count_for_year(1, 6)
print()
domain_histogram_count_for_year(0, 6)
print()
domain_histogram_count_for_price(8)
"""