import os
import random
import datetime
# movie truth
movie_truth_path = "../DataToUse/movie/truth_crawled_movie"

TSTM_movie_truth_path = "../Two-Stage-Truth/movie/truth_result_TST_movie_0"
TSTM_source_movie_truth_path = "../Two-Stage-Truth/movie/truth_result_TST_movie_1"
LTM_movie_truth_path = "../LTM/movie/truth_result_LTM_50_movie"
MV_movie_truth_path = "../MajorityVote/movie/truth_result_MV_movie"
SRV_movie_truth_path = "../SourceReliabilityVote/movie/truth_result_SRV_movie"
DART_movie_truth_path = "../DART/movie/truth_result_DART_movie"

# book truth
book_truth_path = "../DataToUse/book/truth_crawled_book"

LTM_book_truth_path = "../LTM/book/truth_result_LTM_50_book"
DART_book_truth_path = "../DART/book/truth_result_DART_book"
TSTM_book_truth_path = "../Two-Stage-Truth/book/truth_result_TST_book"
MV_book_truth_path = "../MajorityVote/book/truth_result_MV_book"
SRV_book_truth_path = "../SourceReliabilityVote/book/truth_result_SRV_book"
# 大小写均一化，分隔符去掉 for movie, . - 去掉
random_set = set()
def main_compare_truth(dataset, model_compare, tag):
    def compare_truth_dict(truth_dict, model_truth_dict):
        find = 0
        missing = 0
        error = 0
        for key in truth_dict.keys():
            truth_set = truth_dict[key]
            model_set = model_truth_dict[key]
            truth_find_set = set()
            model_find_set = set()
            for truth in truth_set:
                inter_truth = set(truth.split(" "))
                for model_truth in model_set:
                    inter_model_truth = set(model_truth.split(" "))
                    if len(inter_truth) == len(inter_truth):
                        if len(inter_truth - inter_model_truth) == 0:
                            truth_find_set.add(truth)
                            model_find_set.add(model_truth)
            find = find + len(truth_find_set)
            missing_set = truth_set - truth_find_set
            error_set = model_set - model_find_set
            missing = missing + len(missing_set)
            error = error + len(error_set)

        recall = find / (find + missing)
        precision = find / (find + error)
        f1_measure = 2 * recall * precision / (recall + precision)
        return recall, precision, f1_measure

    global random_set
    truth_dict = dict()
    model_truth_dict = dict()

    if dataset == 1:
        TruthData = open(file=movie_truth_path, mode="r", encoding="utf-8")
        truthRead = TruthData.readlines()
        if tag:
            random_set = set()
            while(len(random_set) < 180):
                selected_line = int(random.uniform(1, len(truthRead)))
                random_set.add(selected_line)
        for truth in random_set:
            if not truth == 0:
                dataTruth = truthRead[truth].strip("\n").split("\t")
                if dataTruth[0] not in truth_dict.keys():
                    truth_dict[dataTruth[0]] = set()
                directorData = dataTruth[3]
                directorData = directorData.replace(".", " ").replace("-", " ")
                director_list = directorData.split(";")
                for director in director_list:
                    directorInfo = director.strip(" ").lower()
                    while(directorInfo.find("  ") >= 0):
                        directorInfo = directorInfo.replace("  ", " ")
                    truth_dict[dataTruth[0]].add(directorInfo)
                truth_dict[dataTruth[0]].add("")
                truth_dict[dataTruth[0]].remove("")
        TruthData.close()

        ModelTruth = open(file=model_compare, mode="r", encoding="utf-8")
        truthRead = ModelTruth.readlines()
        for truth in range(len(truthRead)):
            if not truth == 0:
                dataTruth = truthRead[truth].strip("\n").split("\t")
                if not dataTruth[0] in truth_dict.keys():
                    continue
                if dataTruth[0] not in model_truth_dict.keys():
                    model_truth_dict[dataTruth[0]] = set()
                directorData = dataTruth[1]
                director_list = directorData.split(";")
                for director in director_list:
                    directorInfo = director.strip(" ").lower()
                    model_truth_dict[dataTruth[0]].add(directorInfo)
                model_truth_dict[dataTruth[0]].add("")
                model_truth_dict[dataTruth[0]].remove("")
    elif dataset == 0:
        TruthData = open(file=book_truth_path, mode="r", encoding="utf-8")
        truthRead = TruthData.readlines()
        if tag:
            random_set = set()
            while(len(random_set) < 200):
                selected_line = int(random.uniform(1, len(truthRead)))
                random_set.add(selected_line)
        for truth in random_set:
            if not truth == 0:
                dataTruth = truthRead[truth].strip("\n").split("\t")
                if dataTruth[0] not in truth_dict.keys():
                    truth_dict[dataTruth[0]] = set()
                authorData = dataTruth[2]
                authorData = authorData.replace(".", " ").replace("-", " ")
                author_list = authorData.split(";")
                for author in author_list:
                    authorInfo = author.strip(" ").lower()
                    while (authorInfo.find("  ") >= 0):
                        authorInfo = authorInfo.replace("  ", " ")
                    truth_dict[dataTruth[0]].add(authorInfo)
                truth_dict[dataTruth[0]].add("")
                truth_dict[dataTruth[0]].remove("")
        TruthData.close()

        ModelTruth = open(file=model_compare, mode="r", encoding="utf-8")
        truthRead = ModelTruth.readlines()
        for truth in range(len(truthRead)):
            if not truth == 0:
                dataTruth = truthRead[truth].strip("\n").split("\t")
                if not dataTruth[0] in truth_dict.keys():
                    continue
                if dataTruth[0] not in model_truth_dict.keys():
                    model_truth_dict[dataTruth[0]] = set()
                authorData = dataTruth[1]
                author_list = authorData.split(";")
                for author in author_list:
                    authorInfo = author.strip(" ").lower()
                    model_truth_dict[dataTruth[0]].add(authorInfo)
                model_truth_dict[dataTruth[0]].add("")
                model_truth_dict[dataTruth[0]].remove("")
    recall, precision, f1_measure = compare_truth_dict(truth_dict, model_truth_dict)
    return recall, precision, f1_measure

"""
dataset = 1
if dataset == 1:
    fileWrite = "movie"
    model_compare = open(file=fileWrite + "_model_compare", mode='w', encoding='utf-8')
    model_compare.write(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M') + "\n")
    model_compare.write("Model\tRecall\tPrecision\tF1-Score\n")
    recall, precision, f1_measure = main_compare_truth(dataset, TSTM_movie_truth_path)
    model_compare.write("RAW TSTM\t" + str(recall) + "\t" + str(precision) + "\t" + str(f1_measure) + "\n")
    recall, precision, f1_measure = main_compare_truth(dataset, TSTM_source_movie_truth_path)
    model_compare.write("Attr TSTM\t" + str(recall) + "\t" + str(precision) + "\t" + str(f1_measure) + "\n")
    recall, precision, f1_measure = main_compare_truth(dataset, DART_movie_truth_path)
    model_compare.write("DART\t" + str(recall) + "\t" + str(precision) + "\t" + str(f1_measure) + "\n")
    recall, precision, f1_measure = main_compare_truth(dataset, LTM_movie_truth_path)
    model_compare.write("LTM\t" + str(recall) + "\t" + str(precision) + "\t" + str(f1_measure) + "\n")
    recall, precision, f1_measure = main_compare_truth(dataset, SRV_movie_truth_path)
    model_compare.write("SRV\t" + str(recall) + "\t" + str(precision) + "\t" + str(f1_measure) + "\n")
    recall, precision, f1_measure = main_compare_truth(dataset, MV_movie_truth_path)
    model_compare.write("MV\t" + str(recall) + "\t" + str(precision) + "\t" + str(f1_measure) + "\n")
    #recall, precision, f1_measure = main_compare_truth(dataset, TSTM_TOP_movie_truth_path)
    #model_compare.write("DART\t" + str(recall) + "\t" + str(precision) + "\t" + str(f1_measure) + "\n")
elif dataset == 0:
    fileWrite = "book"
    model_compare = open(file=fileWrite + "_model_compare", mode='w', encoding='utf-8')
    model_compare.write(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M') + "\n")
    model_compare.write("Model\tRecall\tPrecision\tF1-Score\n")
    recall, precision, f1_measure = main_compare_truth(dataset, TSTM_book_truth_path)
    model_compare.write("TSTM\t" + str(recall) + "\t" + str(precision) + "\t" + str(f1_measure) + "\n")
    recall, precision, f1_measure = main_compare_truth(dataset, DART_book_truth_path)
    model_compare.write("DART\t" + str(recall) + "\t" + str(precision) + "\t" + str(f1_measure) + "\n")
    recall, precision, f1_measure = main_compare_truth(dataset, LTM_book_truth_path)
    model_compare.write("LTM\t" + str(recall) + "\t" + str(precision) + "\t" + str(f1_measure) + "\n")
    recall, precision, f1_measure = main_compare_truth(dataset, SRV_book_truth_path)
    model_compare.write("SRV\t" + str(recall) + "\t" + str(precision) + "\t" + str(f1_measure) + "\n")
    recall, precision, f1_measure = main_compare_truth(dataset, MV_book_truth_path)
    model_compare.write("MV\t" + str(recall) + "\t" + str(precision) + "\t" + str(f1_measure) + "\n")
    # recall, precision, f1_measure = main_compare_truth(dataset, TSTM_TOP_book_truth_path)
    # model_compare.write("DART\t" + str(recall) + "\t" + str(precision) + "\t" + str(f1_measure) + "\n")
"""

def check_for_model_movie():
    model_name = ["DART", "LTM", "MajorityVote", "SourceReliabilityVote", "Two-Stage-Truth", "Two-Stage-Truth"]
    model_file = ["DART", "LTM", "MV", "SRV", "TST", "TST"]

    recall_movie = list()
    precision_movie = list()
    f1_measure_movie = list()

    total_recall_list = list()
    total_precision_list = list()
    total_f1_list = list()
    for count in range(10):
        tag = True
        total_recall_list.append(dict())
        total_precision_list.append(dict())
        total_f1_list.append(dict())
        attr = False
        for model in range(len(model_name)):
            last_item = "_movie"
            if model_name[model] == "Two-Stage-Truth":
                if not attr:
                    last_item = last_item + "_0"
                    attr = True
                else:
                    last_item = last_item + "_1"
            elif model_name[model] == "LTM":
                last_item = last_item + "_50"
            recall, precision, f1_measure = main_compare_truth(1, os.path.join("../", model_name[model], "movie",
                                                                               "truth_result_" + model_file[model] + last_item), tag)
            total_recall_list[count][model_name[model]] = recall
            total_precision_list[count][model_name[model]] = precision
            total_f1_list[count][model_name[model]] = f1_measure
            tag = False

    model_list = list()
    for model in model_name:
        recall_ratio = 0
        precision_ratio = 0
        f1_ratio = 0
        for count in range(10):
            recall_ratio += total_recall_list[count][model]
            precision_ratio += total_precision_list[count][model]
            f1_ratio += total_f1_list[count][model]
        model_list.append(model)
        recall_movie.append(recall_ratio / 10)
        precision_movie.append(precision_ratio / 10)
        f1_measure_movie.append(f1_ratio / 10)

    movie_write = open(file="./Model_movie", mode="w", encoding="utf-8")
    movie_model_write = "MODEL\t"
    for model in model_list:
        movie_model_write = movie_model_write + model + "\t"
    movie_write.write(movie_model_write.strip("\t") + "\n")
    movie_recall_write = "RECALL\tmovie_recall=["
    for recall in recall_movie:
        movie_recall_write = movie_recall_write + str(recall) + ", "
    movie_write.write(movie_recall_write.strip(", ") + "];\n")
    movie_precision_write = "PRECISION\tmovie_precision=["
    for precision in precision_movie:
        movie_precision_write = movie_precision_write + str(precision) + ","
    movie_write.write(movie_precision_write.strip(", ") + "];\n")
    movie_f1_write = "F1-MEASURE\tmovie_f1=["
    for f1_measure in f1_measure_movie:
        movie_f1_write = movie_f1_write + str(f1_measure) + ", "
    movie_write.write(movie_f1_write.strip(", ") + "];\n")
    movie_write.close()

def check_for_model_book():
    model_name = ["DART", "LTM", "MajorityVote", "SourceReliabilityVote", "Two-Stage-Truth"]
    model_file = ["DART", "LTM", "MV", "SRV", "TST"]

    recall_book = list()
    precision_book = list()
    f1_measure_book = list()

    total_recall_list = list()
    total_precision_list = list()
    total_f1_list = list()
    for count in range(10):
        tag = True
        total_recall_list.append(dict())
        total_precision_list.append(dict())
        total_f1_list.append(dict())
        for model in range(len(model_name)):
            last_item = "_book"
            if model_name[model] == "Two-Stage-Truth":
                last_item = last_item + "_0"
            elif model_name[model] == "LTM":
                last_item = last_item + "_50"
            print(model_name[model])
            recall, precision, f1_measure = main_compare_truth(0, os.path.join("../", model_name[model], "book",
                                                                               "truth_result_" + model_file[model] + last_item), tag)
            total_recall_list[count][model_name[model]] = recall
            total_precision_list[count][model_name[model]] = precision
            total_f1_list[count][model_name[model]] = f1_measure
            tag = False

    model_list = list()
    for model in model_name:
        recall_ratio = 0
        precision_ratio = 0
        f1_ratio = 0
        for count in range(10):
            recall_ratio += total_recall_list[count][model]
            precision_ratio += total_precision_list[count][model]
            f1_ratio += total_f1_list[count][model]
        model_list.append(model)
        recall_book.append(recall_ratio / 10)
        precision_book.append(precision_ratio / 10)
        f1_measure_book.append(f1_ratio / 10)

    book_write = open(file="./Model_book", mode="w", encoding="utf-8")
    book_model_write = "MODEL\t"
    for model in model_list:
        book_model_write = book_model_write + model + "\t"
    book_write.write(book_model_write.strip("\t") + "\n")
    book_recall_write = "RECALL\tbook_recall=["
    for recall in recall_book:
        book_recall_write = book_recall_write + str(recall) + ", "
    book_write.write(book_recall_write.strip(", ") + "];\n")
    book_precision_write = "PRECISION\tbook_precision=["
    for precision in precision_book:
        book_precision_write = book_precision_write + str(precision) + ","
    book_write.write(book_precision_write.strip(", ") + "];\n")
    book_f1_write = "F1-MEASURE\tbook_f1=["
    for f1_measure in f1_measure_book:
        book_f1_write = book_f1_write + str(f1_measure) + ", "
    book_write.write(book_f1_write.strip(", ") + "];\n")
    book_write.close()

def check_for_ratio_vary():
    ratioVary_directory = os.path.join("../Two-Stage-Truth", "ratioVary")
    ratios = os.listdir(ratioVary_directory)

    ratio_movie_write = open(file="./ratioVary_movie", mode="w", encoding="utf-8")
    recall_movie = list()
    precision_movie = list()
    f1_measure_movie = list()

    total_recall_list = list()
    total_precision_list = list()
    total_f1_list = list()
    for count in range(10):
        tag = True
        total_recall_list.append(list())
        total_precision_list.append(list())
        total_f1_list.append(list())
        for ratio in range(len(ratios)):
            recall, precision, f1_measure = main_compare_truth(1, os.path.join(ratioVary_directory, ratios[ratio], "movie",
                                                                               "truth_result_TST_movie_0"), tag)
            total_recall_list[count].append(recall)
            total_precision_list[count].append(precision)
            total_f1_list[count].append(f1_measure)
            tag = False
    for ratio in range(len(ratios)):
        recall_ratio = 0
        precision_ratio = 0
        f1_ratio = 0
        for count in range(10):
            recall_ratio += total_recall_list[count][ratio]
            precision_ratio += total_precision_list[count][ratio]
            f1_ratio += total_f1_list[count][ratio]
        recall_movie.append(recall_ratio/10)
        precision_movie.append(precision_ratio/10)
        f1_measure_movie.append(f1_ratio/10)

    movie_recall_write = "RECALL\tmovie_recall=["
    for recall in recall_movie:
        movie_recall_write = movie_recall_write + str(recall) + ", "
    ratio_movie_write.write(movie_recall_write.strip(", ") + "];\n")
    movie_precision_write = "PRECISION\tmovie_precision=["
    for precision in precision_movie:
        movie_precision_write = movie_precision_write + str(precision) + ","
    ratio_movie_write.write(movie_precision_write.strip(", ") + "];\n")
    movie_f1_write = "F1-MEASURE\tmovie_f1=["
    for f1_measure in f1_measure_movie:
        movie_f1_write = movie_f1_write + str(f1_measure) + ", "
    ratio_movie_write.write(movie_f1_write.strip(", ") + "];\n")
    ratio_movie_write.close()

    ratio_book_write = open(file="./ratioVary_book", mode="w", encoding="utf-8")
    recall_book = list()
    precision_book = list()
    f1_measure_book = list()


    total_recall_list = list()
    total_precision_list = list()
    total_f1_list = list()
    for count in range(10):
        tag = True
        total_recall_list.append(list())
        total_precision_list.append(list())
        total_f1_list.append(list())
        for ratio in range(len(ratios)):
            recall, precision, f1_measure = main_compare_truth(0, os.path.join(ratioVary_directory, ratios[ratio], "book",
                                                                               "truth_result_TST_book_0"), tag)
            total_recall_list[count].append(recall)
            total_precision_list[count].append(precision)
            total_f1_list[count].append(f1_measure)
            tag = False

    for ratio in range(len(ratios)):
        recall_ratio = 0
        precision_ratio = 0
        f1_ratio = 0
        for count in range(10):
            recall_ratio += total_recall_list[count][ratio]
            precision_ratio += total_precision_list[count][ratio]
            f1_ratio += total_f1_list[count][ratio]
        recall_book.append(recall_ratio/10)
        precision_book.append(precision_ratio/10)
        f1_measure_book.append(f1_ratio/10)

    book_recall_write = "RECALL\tbook_recall=["
    for recall in recall_book:
        book_recall_write = book_recall_write + str(recall) + ", "
    ratio_book_write.write(book_recall_write.strip(", ") + "];\n")
    book_precision_write = "PRECISION\tbook_precision=["
    for precision in precision_book:
        book_precision_write = book_precision_write + str(precision) + ", "
    ratio_book_write.write(book_precision_write.strip(", ") + "];\n")
    book_f1_write = "F1-MEASURE\tbook_f1=["
    for f1_measure in f1_measure_book:
        book_f1_write = book_f1_write + str(f1_measure) + ", "
    ratio_book_write.write(book_f1_write.strip(", ") + "];\n")
    ratio_book_write.close()

def check_for_iteration():
    dataset = 1
    iteration_directory = "../Two-Stage-Truth/iteration"
    count_holder = os.listdir(iteration_directory)
    iteration_file = open(file="./iteration_movie", mode="w", encoding="utf-8")
    for count in count_holder:
        tag = True
        iteration_holder_directory = os.path.join(iteration_directory, count)
        iteration_holder = os.listdir(iteration_holder_directory)
        #recall_write = "recall_count" + str(count) + "=["
        #precision_write = "precision_count" + str(count) + "=["
        f1_measure_write = "f1_count" + str(count) + "=["
        for iteration in iteration_holder:
            recall, precision, f1_measure = main_compare_truth(dataset, os.path.join(iteration_holder_directory, iteration, "movie", "truth_result_TST_movie_0"), tag)
            #recall_write = recall_write + str(recall) + ", "
            #precision_write = precision_write + str(precision) + ", "
            f1_measure_write = f1_measure_write + str(f1_measure) + ", "
            tag = False
        iteration_file.write(f1_measure_write.strip(", ") + "];\n")
    iteration_file.close()


#check_for_ratio_vary()
#check_for_iteration()
#check_for_model_movie()
#check_for_model_book()