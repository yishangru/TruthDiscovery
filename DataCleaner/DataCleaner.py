import os
import pandas
"""
This a rewrite version of the data clean method for the original dataset provided by XueLing, with following links:
Book: https://drive.google.com/open?id=1Q11D7V4vuhgpugCC_Db_GbP4149XnMpY
Movie: https://drive.google.com/open?id=1hTAQcGeHSUuu0fZq655q0wWkRZVdQEnr
Refractor code according pandas dict to read and load data
"""

class DataCleaner(object):
    def __init__(self, dataPath):
        self.dataPath = dataPath

    def loadData(self):
        self.dataDict = dict()

    def checkNamingConvention():

class