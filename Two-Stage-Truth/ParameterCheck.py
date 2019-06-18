# only on server
import os
import TSTM
# both use movie dataset to perform parameter check
def check_for_Ratio_Varying():
    dataset = 1
    alpha = 1.5
    iteration_SATM = 10
    whether_estimate = False
    datasetPath = "../DataToUse"
    ratio_holder = [[1,1,1,99], [10,10,1,99], [20,20,1,99], [30,30,1,99], [40,40,1,99], [50,50,1,99]]
    for ratio in range(len(ratio_holder)):
        outputWrite = os.path.join("./ratioVary/", "ratio" + str(ratio))
        if not os.path.exists(outputWrite):
            os.mkdir(outputWrite)
        if not os.path.exists(os.path.join(outputWrite, "movie")):
            os.mkdir(os.path.join(outputWrite, "movie"))
        TSTM.main_for_TSTM(dataset, ratio_holder[ratio], alpha, iteration_SATM, whether_estimate, datasetPath, outputWrite)

    dataset = 0
    alpha = 2
    iteration_SATM = 10
    whether_estimate = False
    datasetPath = "../DataToUse"
    ratio_holder = [[1,1,1,99], [10,10,1,99], [20,20,1,99], [30,30,1,99], [40,40,1,99], [50,50,1,99]]
    for ratio in range(len(ratio_holder)):
        outputWrite = os.path.join("./ratioVary/", "ratio" + str(ratio))
        if not os.path.exists(outputWrite):
            os.mkdir(outputWrite)
        if not os.path.exists(os.path.join(outputWrite, "book")):
            os.mkdir(os.path.join(outputWrite, "book"))
        TSTM.main_for_TSTM(dataset, ratio_holder[ratio], alpha, iteration_SATM, whether_estimate, datasetPath, outputWrite)

def check_for_iteration_Number():
    iteration_holder = [1, 2, 3, 5, 10, 15, 20, 50, 100, 200, 300]
    dataset = 1
    alpha = 1.5
    ratio_matrix = [1, 1, 1, 99]
    whether_estimate = False
    datasetPath = "../DataToUse"
    outputWrite = "./iteration"
    for count in range(10):
        count_directory = os.path.join(outputWrite, str(count))
        if not os.path.exists(count_directory):
            os.mkdir(count_directory)
        for iteration in iteration_holder:
            if iteration < 50:
                continue
            iteration_directory = os.path.join(count_directory, str(iteration))
            if not os.path.exists(iteration_directory):
                os.mkdir(iteration_directory)
            if not os.path.exists(os.path.join(iteration_directory, "movie")):
                os.mkdir(os.path.join(iteration_directory, "movie"))
            TSTM.main_for_TSTM(dataset, ratio_matrix, alpha, iteration, whether_estimate, datasetPath,
                               iteration_directory)
#check_for_Ratio_Varying()
#check_for_iteration_Number()

#check_for_Ratio_Varying()
#check_for_iteration_Number()