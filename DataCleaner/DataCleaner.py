import os

"""
This a rewrite version of the data clean method for the original dataset provided by XueLing, with following links:
Book: https://drive.google.com/open?id=1Q11D7V4vuhgpugCC_Db_GbP4149XnMpY
Movie: https://drive.google.com/open?id=1hTAQcGeHSUuu0fZq655q0wWkRZVdQEnr
Refractor code according pandas dict to read and load data
"""

class DataCleaner(object):
    def __init__(self, dataPath):
        self.dataPath = dataPath

    def load_data(self, indexKeys):
        """
        :param indexKeys: [] as index e.g. [title, year, source], [isbn-13, source]
        :return: None
        """
        self.dataDict = dict()
        self.indexKeys = indexKeys
        read_data_lines = open(file=os.path.abspath(self.dataPath), mode='r', encoding='utf-8').readlines()
        for i, dataLine in enumerate(read_data_lines):
            if i == 0:
                self.dataHeader = dataLine
            else:
                presentDict = self.dataDict
                dataSplit = dataLine.strip("\n").split("\t")
                for j, index in enumerate(self.indexKeys):
                    if dataLine[index] not in presentDict.keys():
                        presentDict[dataSplit[index]] = list() if j == len(self.indexKeys) - 1 else dict()
                    presentDict = presentDict[dataSplit[index]]
                    if j == len(self.indexKeys) - 1:
                        presentDict.append(dataLine)

    def remove_single_source(self):


    def check_naming_convention():
        pass

    def unify_naming_convention(self):
        pass

    def remove_non_conflict(self):
        pass

    def write_data(self, dataWritePath):
        pass

dataCleaner = DataCleaner("../Data/test.txt")
dataCleaner.load_data([0, 3, 2])