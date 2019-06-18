# -*- coding:utf-8 -*-
import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# crawler movie truth from wiki
def crawl_from_wiki(movie_name, year):
    global driver
    country_info = ""
    movie_address = "https://www.themoviedb.org"
    counter = 0
    while(True):
        try:
            search_movie_name = movie_name.replace("&", "") # 神奇改变
            search_movie_name = search_movie_name.replace("#", "")  # 神奇改变
            search_movie_name = search_movie_name.replace(r"\\", "")  # 神奇改变2
            driver.get(movie_address)
            search_bar = driver.find_element_by_id("search_v4")
            search_bar.send_keys(search_movie_name + Keys.ENTER)  # title
            time.sleep(2)
            # find Movies and TV Shows
            search_condition = [".//a[@id='movie' and @title='Movies']", "//a[@id='tv' and @title='TV Shows']"]
            for searching in range(len(search_condition)):
                driver.get(driver.find_element_by_xpath(search_condition[searching]).get_attribute('href'))
                time.sleep(1)
                count = 0
                while(True):
                    movie_item_list = driver.find_element_by_css_selector(
                        "[class='results flex']").find_elements_by_css_selector("[class='item poster card']")
                    if count == len(movie_item_list):
                        break
                    movie_link = movie_item_list[count].find_element_by_css_selector("[class='title result']")
                    movie_release1 = movie_item_list[count].find_element_by_css_selector(
                        "[class='flex']").find_element_by_xpath(".//span").text
                    count += 1
                    if not (movie_release1.find(year) >= 0 or movie_link.text == movie_name):
                        continue
                    else:
                        driver.get(movie_link.get_attribute('href'))
                        movie_release = driver.find_element_by_xpath(".//ul[@class='releases' and @data-role='tooltip']")
                        try:
                            country_info = movie_release.find_element_by_xpath(".//img").get_attribute('src').split("/")[7].split("-")[0]
                        except Exception:
                            try:
                                country_info = movie_release.find_element_by_xpath(".//img").get_attribute('data-src').split("/")[7].split("-")[0]
                            except Exception:
                                country_info = ""
                        if not country_info == "":
                            break
                if not country_info == "":
                    break
            break
        except Exception:
            counter += 1
            if counter == 4:
                driver.quit()
                driver_path = "./chromedriver.exe"
                driver = webdriver.Chrome(executable_path=driver_path)
            elif counter == 5:
                break
    return country_info

def main_for_crawler_wiki1():
    # read moive name from file
    def deal_with_crawling_character1(data):
        mapping = dict()
        mapping["&#2"] = "'"
        mapping["&#39;"] = "'"
        mapping["&#039;"] = "'"
        mapping["&#193;"] = "Á"
        mapping["&#197;"] = "Å"
        mapping["&#199;"] = "Ç"
        mapping["&#201;"] = "É"
        mapping["&#205;"] = "Í"
        mapping["&#211;"] = "Ó"
        mapping["&#212;"] = "Ô"
        mapping["&#214;"] = "Ö"
        mapping["&#216;"] = "Ø"
        mapping["&#220;"] = "Ü"
        mapping["&#222;"] = "Þ"
        mapping["&#223;"] = "ß"
        mapping["&#224;"] = "à"
        mapping["&#225;"] = "á"
        mapping["&#227;"] = "ã"
        mapping["&#228;"] = "ä"
        mapping["&#229;"] = "å"
        mapping["&#230;"] = "æ"
        mapping["&#231;"] = "ç"
        mapping["&#232;"] = "è"
        mapping["&#233;"] = "é"
        mapping["&#235;"] = "ë"
        mapping["&#236;"] = "ì"
        mapping["&#237;"] = "í"
        mapping["&#238;"] = "î"
        mapping["&#239;"] = "ï"
        mapping["&#240;"] = "ð"
        mapping["&#241;"] = "ñ"
        mapping["&#242;"] = "ò"
        mapping["&#243;"] = "ó"
        mapping["&#244;"] = "ô"
        mapping["&#245;"] = "õ"
        mapping["&#246;"] = "ö"
        mapping["&#248;"] = "ø"
        mapping["&#250;"] = "ú"
        mapping["&#251;"] = "û"
        mapping["&#252;"] = "ü"
        mapping["&#253;"] = "ý"
        mapping[r"\t"] = ""
        mapping[r"\n"] = ""
        mapping["Sr."] = ""
        mapping["Jr."] = ""
        mapping[" and "] = ";"
        mapping[" & "] = ";"
        mapping["&rsquo;"] = r"'"
        mapping["&eacute;"] = "é"
        mapping["&aacute;"] = "á"
        mapping["&ocirc;"] = "ô"
        mapping["&oacute;"] = "ó"
        mapping["&uacute;"] = "u"
        mapping["&oslash;"] = "ø"
        mapping["&ouml;"] = "ö"
        mapping["&uuml;"] = "ü"
        mapping["&iacute;"] = "í"
        mapping["&Ocirc;"] = "Ô"
        mapping["&auml;"] = "ä"
        mapping["&Aacute;"] = "Á"
        mapping["&egrave;"] = "è"
        mapping["&quot;"] = r"'"
        mapping["&aring;"] = "å"
        mapping["&Aring;"] = "Å"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    def deal_with_crawling_character2(data):
        mapping = dict()
        mapping["'01;"] = "É"
        mapping["'05;"] = "Í"
        mapping["'11;"] = "Ó"
        mapping["'12;"] = "Ô"
        mapping["'14;"] = "Ö"
        mapping["'16;"] = "Ø"
        mapping["'20;"] = "Ü"
        mapping["'22;"] = "Þ"
        mapping["'23;"] = "ß"
        mapping["'24;"] = "à"
        mapping["'25;"] = "á"
        mapping["'27;"] = "?"
        mapping["'28;"] = "ä"
        mapping["'29;"] = "å"
        mapping["'30;"] = "æ"
        mapping["'31;"] = "ç"
        mapping["'32;"] = "è"
        mapping["'33;"] = "é"
        mapping["'35;"] = "ë"
        mapping["'36;"] = "ì"
        mapping["'37;"] = "í"
        mapping["'38;"] = "î"
        mapping["'39;"] = "ï"
        mapping["'40;"] = "ð"
        mapping["'41;"] = "ñ"
        mapping["'42;"] = "ò"
        mapping["'43;"] = "ó"
        mapping["'44;"] = "ô"
        mapping["'45;"] = "õ"
        mapping["'46;"] = "?"
        mapping["'48;"] = "ø"
        mapping["'50;"] = "ú"
        mapping["'51;"] = "û"
        mapping["'52;"] = "ü"
        mapping["'53;"] = "z"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    global driver
    global driver_path
    driver_path = "./chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    validation_file = open(file="./conflictDB_movie", mode="r", encoding="utf-8")
    truth_file = open(file="./movie_attribute_crawl1", mode="r", encoding="utf-8")
    written_length = len(truth_file.readlines())
    truth_file.close()
    truth_file = open(file="./movie_attribute_crawl1", mode="a+", encoding="utf-8")
    validation_lines = validation_file.readlines()
    for validation_line in range(written_length, int(len(validation_lines)/8)):  #len(validation_lines)
        dataRead = validation_lines[validation_line].strip("\n")
        if validation_line == 0:
            truth_file.write(dataRead + "\tCountry\n")
        else:
            information = dataRead.split("\t")
            information[1] = deal_with_crawling_character2(deal_with_crawling_character1(information[1]))
            country = crawl_from_wiki(information[1], information[2])
            truth_file.write(dataRead + "\t" + country + "\n")
            truth_file.flush()
    driver.quit()
    truth_file.close()
    validation_file.close()

def main_for_crawler_wiki5():
    # read moive name from file
    def deal_with_crawling_character1(data):
        mapping = dict()
        mapping["&#2"] = "'"
        mapping["&#39;"] = "'"
        mapping["&#039;"] = "'"
        mapping["&#193;"] = "Á"
        mapping["&#197;"] = "Å"
        mapping["&#199;"] = "Ç"
        mapping["&#201;"] = "É"
        mapping["&#205;"] = "Í"
        mapping["&#211;"] = "Ó"
        mapping["&#212;"] = "Ô"
        mapping["&#214;"] = "Ö"
        mapping["&#216;"] = "Ø"
        mapping["&#220;"] = "Ü"
        mapping["&#222;"] = "Þ"
        mapping["&#223;"] = "ß"
        mapping["&#224;"] = "à"
        mapping["&#225;"] = "á"
        mapping["&#227;"] = "ã"
        mapping["&#228;"] = "ä"
        mapping["&#229;"] = "å"
        mapping["&#230;"] = "æ"
        mapping["&#231;"] = "ç"
        mapping["&#232;"] = "è"
        mapping["&#233;"] = "é"
        mapping["&#235;"] = "ë"
        mapping["&#236;"] = "ì"
        mapping["&#237;"] = "í"
        mapping["&#238;"] = "î"
        mapping["&#239;"] = "ï"
        mapping["&#240;"] = "ð"
        mapping["&#241;"] = "ñ"
        mapping["&#242;"] = "ò"
        mapping["&#243;"] = "ó"
        mapping["&#244;"] = "ô"
        mapping["&#245;"] = "õ"
        mapping["&#246;"] = "ö"
        mapping["&#248;"] = "ø"
        mapping["&#250;"] = "ú"
        mapping["&#251;"] = "û"
        mapping["&#252;"] = "ü"
        mapping["&#253;"] = "ý"
        mapping[r"\t"] = ""
        mapping[r"\n"] = ""
        mapping["Sr."] = ""
        mapping["Jr."] = ""
        mapping[" and "] = ";"
        mapping[" & "] = ";"
        mapping["&rsquo;"] = r"'"
        mapping["&eacute;"] = "é"
        mapping["&aacute;"] = "á"
        mapping["&ocirc;"] = "ô"
        mapping["&oacute;"] = "ó"
        mapping["&uacute;"] = "u"
        mapping["&oslash;"] = "ø"
        mapping["&ouml;"] = "ö"
        mapping["&uuml;"] = "ü"
        mapping["&iacute;"] = "í"
        mapping["&Ocirc;"] = "Ô"
        mapping["&auml;"] = "ä"
        mapping["&Aacute;"] = "Á"
        mapping["&egrave;"] = "è"
        mapping["&quot;"] = r"'"
        mapping["&aring;"] = "å"
        mapping["&Aring;"] = "Å"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    def deal_with_crawling_character2(data):
        mapping = dict()
        mapping["'01;"] = "É"
        mapping["'05;"] = "Í"
        mapping["'11;"] = "Ó"
        mapping["'12;"] = "Ô"
        mapping["'14;"] = "Ö"
        mapping["'16;"] = "Ø"
        mapping["'20;"] = "Ü"
        mapping["'22;"] = "Þ"
        mapping["'23;"] = "ß"
        mapping["'24;"] = "à"
        mapping["'25;"] = "á"
        mapping["'27;"] = "?"
        mapping["'28;"] = "ä"
        mapping["'29;"] = "å"
        mapping["'30;"] = "æ"
        mapping["'31;"] = "ç"
        mapping["'32;"] = "è"
        mapping["'33;"] = "é"
        mapping["'35;"] = "ë"
        mapping["'36;"] = "ì"
        mapping["'37;"] = "í"
        mapping["'38;"] = "î"
        mapping["'39;"] = "ï"
        mapping["'40;"] = "ð"
        mapping["'41;"] = "ñ"
        mapping["'42;"] = "ò"
        mapping["'43;"] = "ó"
        mapping["'44;"] = "ô"
        mapping["'45;"] = "õ"
        mapping["'46;"] = "?"
        mapping["'48;"] = "ø"
        mapping["'50;"] = "ú"
        mapping["'51;"] = "û"
        mapping["'52;"] = "ü"
        mapping["'53;"] = "z"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    global driver
    global driver_path
    driver_path = "./chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    validation_file = open(file="./conflictDB_movie", mode="r", encoding="utf-8")
    truth_file = open(file="./movie_attribute_crawl5", mode="r", encoding="utf-8")
    written_length = len(truth_file.readlines())
    truth_file.close()
    truth_file = open(file="./movie_attribute_crawl5", mode="a+", encoding="utf-8")
    validation_lines = validation_file.readlines()
    for validation_line in range(int(len(validation_lines)/8)+written_length, int(len(validation_lines)/4)):  #len(validation_lines)
        dataRead = validation_lines[validation_line].strip("\n")
        if validation_line == 0:
            truth_file.write(dataRead + "\tCountry\n")
        else:
            information = dataRead.split("\t")
            information[1] = deal_with_crawling_character2(deal_with_crawling_character1(information[1]))
            country = crawl_from_wiki(information[1], information[2])
            truth_file.write(dataRead + "\t" + country + "\n")
            truth_file.flush()
    driver.quit()
    truth_file.close()
    validation_file.close()

def main_for_crawler_wiki2():
    # read moive name from file
    def deal_with_crawling_character1(data):
        mapping = dict()
        mapping["&#2"] = "'"
        mapping["&#39;"] = "'"
        mapping["&#039;"] = "'"
        mapping["&#193;"] = "Á"
        mapping["&#197;"] = "Å"
        mapping["&#199;"] = "Ç"
        mapping["&#201;"] = "É"
        mapping["&#205;"] = "Í"
        mapping["&#211;"] = "Ó"
        mapping["&#212;"] = "Ô"
        mapping["&#214;"] = "Ö"
        mapping["&#216;"] = "Ø"
        mapping["&#220;"] = "Ü"
        mapping["&#222;"] = "Þ"
        mapping["&#223;"] = "ß"
        mapping["&#224;"] = "à"
        mapping["&#225;"] = "á"
        mapping["&#227;"] = "ã"
        mapping["&#228;"] = "ä"
        mapping["&#229;"] = "å"
        mapping["&#230;"] = "æ"
        mapping["&#231;"] = "ç"
        mapping["&#232;"] = "è"
        mapping["&#233;"] = "é"
        mapping["&#235;"] = "ë"
        mapping["&#236;"] = "ì"
        mapping["&#237;"] = "í"
        mapping["&#238;"] = "î"
        mapping["&#239;"] = "ï"
        mapping["&#240;"] = "ð"
        mapping["&#241;"] = "ñ"
        mapping["&#242;"] = "ò"
        mapping["&#243;"] = "ó"
        mapping["&#244;"] = "ô"
        mapping["&#245;"] = "õ"
        mapping["&#246;"] = "ö"
        mapping["&#248;"] = "ø"
        mapping["&#250;"] = "ú"
        mapping["&#251;"] = "û"
        mapping["&#252;"] = "ü"
        mapping["&#253;"] = "ý"
        mapping[r"\t"] = ""
        mapping[r"\n"] = ""
        mapping["Sr."] = ""
        mapping["Jr."] = ""
        mapping[" and "] = ";"
        mapping[" & "] = ";"
        mapping["&rsquo;"] = r"'"
        mapping["&eacute;"] = "é"
        mapping["&aacute;"] = "á"
        mapping["&ocirc;"] = "ô"
        mapping["&oacute;"] = "ó"
        mapping["&uacute;"] = "u"
        mapping["&oslash;"] = "ø"
        mapping["&ouml;"] = "ö"
        mapping["&uuml;"] = "ü"
        mapping["&iacute;"] = "í"
        mapping["&Ocirc;"] = "Ô"
        mapping["&auml;"] = "ä"
        mapping["&Aacute;"] = "Á"
        mapping["&egrave;"] = "è"
        mapping["&quot;"] = r"'"
        mapping["&aring;"] = "å"
        mapping["&Aring;"] = "Å"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    def deal_with_crawling_character2(data):
        mapping = dict()
        mapping["'01;"] = "É"
        mapping["'05;"] = "Í"
        mapping["'11;"] = "Ó"
        mapping["'12;"] = "Ô"
        mapping["'14;"] = "Ö"
        mapping["'16;"] = "Ø"
        mapping["'20;"] = "Ü"
        mapping["'22;"] = "Þ"
        mapping["'23;"] = "ß"
        mapping["'24;"] = "à"
        mapping["'25;"] = "á"
        mapping["'27;"] = "?"
        mapping["'28;"] = "ä"
        mapping["'29;"] = "å"
        mapping["'30;"] = "æ"
        mapping["'31;"] = "ç"
        mapping["'32;"] = "è"
        mapping["'33;"] = "é"
        mapping["'35;"] = "ë"
        mapping["'36;"] = "ì"
        mapping["'37;"] = "í"
        mapping["'38;"] = "î"
        mapping["'39;"] = "ï"
        mapping["'40;"] = "ð"
        mapping["'41;"] = "ñ"
        mapping["'42;"] = "ò"
        mapping["'43;"] = "ó"
        mapping["'44;"] = "ô"
        mapping["'45;"] = "õ"
        mapping["'46;"] = "?"
        mapping["'48;"] = "ø"
        mapping["'50;"] = "ú"
        mapping["'51;"] = "û"
        mapping["'52;"] = "ü"
        mapping["'53;"] = "z"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    global driver
    global driver_path
    driver_path = "./chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    validation_file = open(file="./conflictDB_movie", mode="r", encoding="utf-8")
    truth_file = open(file="./movie_attribute_crawl2", mode="r", encoding="utf-8")
    written_length = len(truth_file.readlines())
    truth_file.close()
    truth_file = open(file="./movie_attribute_crawl2", mode="a+", encoding="utf-8")
    validation_lines = validation_file.readlines()
    for validation_line in range(int(len(validation_lines)/4)+written_length, int(3*len(validation_lines)/8)):  #len(validation_lines)
        dataRead = validation_lines[validation_line].strip("\n")
        information = dataRead.split("\t")
        information[1] = deal_with_crawling_character2(deal_with_crawling_character1(information[1]))
        country = crawl_from_wiki(information[1], information[2])
        truth_file.write(dataRead + "\t" + country + "\n")
        truth_file.flush()
    driver.quit()
    truth_file.close()
    validation_file.close()

def main_for_crawler_wiki6():
    # read moive name from file
    def deal_with_crawling_character1(data):
        mapping = dict()
        mapping["&#2"] = "'"
        mapping["&#39;"] = "'"
        mapping["&#039;"] = "'"
        mapping["&#193;"] = "Á"
        mapping["&#197;"] = "Å"
        mapping["&#199;"] = "Ç"
        mapping["&#201;"] = "É"
        mapping["&#205;"] = "Í"
        mapping["&#211;"] = "Ó"
        mapping["&#212;"] = "Ô"
        mapping["&#214;"] = "Ö"
        mapping["&#216;"] = "Ø"
        mapping["&#220;"] = "Ü"
        mapping["&#222;"] = "Þ"
        mapping["&#223;"] = "ß"
        mapping["&#224;"] = "à"
        mapping["&#225;"] = "á"
        mapping["&#227;"] = "ã"
        mapping["&#228;"] = "ä"
        mapping["&#229;"] = "å"
        mapping["&#230;"] = "æ"
        mapping["&#231;"] = "ç"
        mapping["&#232;"] = "è"
        mapping["&#233;"] = "é"
        mapping["&#235;"] = "ë"
        mapping["&#236;"] = "ì"
        mapping["&#237;"] = "í"
        mapping["&#238;"] = "î"
        mapping["&#239;"] = "ï"
        mapping["&#240;"] = "ð"
        mapping["&#241;"] = "ñ"
        mapping["&#242;"] = "ò"
        mapping["&#243;"] = "ó"
        mapping["&#244;"] = "ô"
        mapping["&#245;"] = "õ"
        mapping["&#246;"] = "ö"
        mapping["&#248;"] = "ø"
        mapping["&#250;"] = "ú"
        mapping["&#251;"] = "û"
        mapping["&#252;"] = "ü"
        mapping["&#253;"] = "ý"
        mapping[r"\t"] = ""
        mapping[r"\n"] = ""
        mapping["Sr."] = ""
        mapping["Jr."] = ""
        mapping[" and "] = ";"
        mapping[" & "] = ";"
        mapping["&rsquo;"] = r"'"
        mapping["&eacute;"] = "é"
        mapping["&aacute;"] = "á"
        mapping["&ocirc;"] = "ô"
        mapping["&oacute;"] = "ó"
        mapping["&uacute;"] = "u"
        mapping["&oslash;"] = "ø"
        mapping["&ouml;"] = "ö"
        mapping["&uuml;"] = "ü"
        mapping["&iacute;"] = "í"
        mapping["&Ocirc;"] = "Ô"
        mapping["&auml;"] = "ä"
        mapping["&Aacute;"] = "Á"
        mapping["&egrave;"] = "è"
        mapping["&quot;"] = r"'"
        mapping["&aring;"] = "å"
        mapping["&Aring;"] = "Å"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    def deal_with_crawling_character2(data):
        mapping = dict()
        mapping["'01;"] = "É"
        mapping["'05;"] = "Í"
        mapping["'11;"] = "Ó"
        mapping["'12;"] = "Ô"
        mapping["'14;"] = "Ö"
        mapping["'16;"] = "Ø"
        mapping["'20;"] = "Ü"
        mapping["'22;"] = "Þ"
        mapping["'23;"] = "ß"
        mapping["'24;"] = "à"
        mapping["'25;"] = "á"
        mapping["'27;"] = "?"
        mapping["'28;"] = "ä"
        mapping["'29;"] = "å"
        mapping["'30;"] = "æ"
        mapping["'31;"] = "ç"
        mapping["'32;"] = "è"
        mapping["'33;"] = "é"
        mapping["'35;"] = "ë"
        mapping["'36;"] = "ì"
        mapping["'37;"] = "í"
        mapping["'38;"] = "î"
        mapping["'39;"] = "ï"
        mapping["'40;"] = "ð"
        mapping["'41;"] = "ñ"
        mapping["'42;"] = "ò"
        mapping["'43;"] = "ó"
        mapping["'44;"] = "ô"
        mapping["'45;"] = "õ"
        mapping["'46;"] = "?"
        mapping["'48;"] = "ø"
        mapping["'50;"] = "ú"
        mapping["'51;"] = "û"
        mapping["'52;"] = "ü"
        mapping["'53;"] = "z"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    global driver
    global driver_path
    driver_path = "./chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    validation_file = open(file="./conflictDB_movie", mode="r", encoding="utf-8")
    truth_file = open(file="./movie_attribute_crawl6", mode="r", encoding="utf-8")
    written_length = len(truth_file.readlines())
    truth_file.close()
    truth_file = open(file="./movie_attribute_crawl6", mode="a+", encoding="utf-8")
    validation_lines = validation_file.readlines()
    for validation_line in range(int(3*len(validation_lines)/8)+written_length, int(len(validation_lines)/2)):  #len(validation_lines)
        dataRead = validation_lines[validation_line].strip("\n")
        information = dataRead.split("\t")
        information[1] = deal_with_crawling_character2(deal_with_crawling_character1(information[1]))
        country = crawl_from_wiki(information[1], information[2])
        truth_file.write(dataRead + "\t" + country + "\n")
        truth_file.flush()
    driver.quit()
    truth_file.close()
    validation_file.close()

def main_for_crawler_wiki3():
    # read moive name from file
    def deal_with_crawling_character1(data):
        mapping = dict()
        mapping["&#2"] = "'"
        mapping["&#39;"] = "'"
        mapping["&#039;"] = "'"
        mapping["&#193;"] = "Á"
        mapping["&#197;"] = "Å"
        mapping["&#199;"] = "Ç"
        mapping["&#201;"] = "É"
        mapping["&#205;"] = "Í"
        mapping["&#211;"] = "Ó"
        mapping["&#212;"] = "Ô"
        mapping["&#214;"] = "Ö"
        mapping["&#216;"] = "Ø"
        mapping["&#220;"] = "Ü"
        mapping["&#222;"] = "Þ"
        mapping["&#223;"] = "ß"
        mapping["&#224;"] = "à"
        mapping["&#225;"] = "á"
        mapping["&#227;"] = "ã"
        mapping["&#228;"] = "ä"
        mapping["&#229;"] = "å"
        mapping["&#230;"] = "æ"
        mapping["&#231;"] = "ç"
        mapping["&#232;"] = "è"
        mapping["&#233;"] = "é"
        mapping["&#235;"] = "ë"
        mapping["&#236;"] = "ì"
        mapping["&#237;"] = "í"
        mapping["&#238;"] = "î"
        mapping["&#239;"] = "ï"
        mapping["&#240;"] = "ð"
        mapping["&#241;"] = "ñ"
        mapping["&#242;"] = "ò"
        mapping["&#243;"] = "ó"
        mapping["&#244;"] = "ô"
        mapping["&#245;"] = "õ"
        mapping["&#246;"] = "ö"
        mapping["&#248;"] = "ø"
        mapping["&#250;"] = "ú"
        mapping["&#251;"] = "û"
        mapping["&#252;"] = "ü"
        mapping["&#253;"] = "ý"
        mapping[r"\t"] = ""
        mapping[r"\n"] = ""
        mapping["Sr."] = ""
        mapping["Jr."] = ""
        mapping[" and "] = ";"
        mapping[" & "] = ";"
        mapping["&rsquo;"] = r"'"
        mapping["&eacute;"] = "é"
        mapping["&aacute;"] = "á"
        mapping["&ocirc;"] = "ô"
        mapping["&oacute;"] = "ó"
        mapping["&uacute;"] = "u"
        mapping["&oslash;"] = "ø"
        mapping["&ouml;"] = "ö"
        mapping["&uuml;"] = "ü"
        mapping["&iacute;"] = "í"
        mapping["&Ocirc;"] = "Ô"
        mapping["&auml;"] = "ä"
        mapping["&Aacute;"] = "Á"
        mapping["&egrave;"] = "è"
        mapping["&quot;"] = r"'"
        mapping["&aring;"] = "å"
        mapping["&Aring;"] = "Å"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    def deal_with_crawling_character2(data):
        mapping = dict()
        mapping["'01;"] = "É"
        mapping["'05;"] = "Í"
        mapping["'11;"] = "Ó"
        mapping["'12;"] = "Ô"
        mapping["'14;"] = "Ö"
        mapping["'16;"] = "Ø"
        mapping["'20;"] = "Ü"
        mapping["'22;"] = "Þ"
        mapping["'23;"] = "ß"
        mapping["'24;"] = "à"
        mapping["'25;"] = "á"
        mapping["'27;"] = "?"
        mapping["'28;"] = "ä"
        mapping["'29;"] = "å"
        mapping["'30;"] = "æ"
        mapping["'31;"] = "ç"
        mapping["'32;"] = "è"
        mapping["'33;"] = "é"
        mapping["'35;"] = "ë"
        mapping["'36;"] = "ì"
        mapping["'37;"] = "í"
        mapping["'38;"] = "î"
        mapping["'39;"] = "ï"
        mapping["'40;"] = "ð"
        mapping["'41;"] = "ñ"
        mapping["'42;"] = "ò"
        mapping["'43;"] = "ó"
        mapping["'44;"] = "ô"
        mapping["'45;"] = "õ"
        mapping["'46;"] = "?"
        mapping["'48;"] = "ø"
        mapping["'50;"] = "ú"
        mapping["'51;"] = "û"
        mapping["'52;"] = "ü"
        mapping["'53;"] = "z"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    global driver
    global driver_path
    driver_path = "./chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    validation_file = open(file="./conflictDB_movie", mode="r", encoding="utf-8")
    truth_file = open(file="./movie_attribute_crawl3", mode="r", encoding="utf-8")
    written_length = len(truth_file.readlines())
    truth_file.close()
    truth_file = open(file="./movie_attribute_crawl3", mode="a+", encoding="utf-8")
    validation_lines = validation_file.readlines()
    for validation_line in range(int(len(validation_lines)/2)+written_length, int(5*len(validation_lines)/8)):  #len(validation_lines)
        dataRead = validation_lines[validation_line].strip("\n")
        information = dataRead.split("\t")
        information[1] = deal_with_crawling_character2(deal_with_crawling_character1(information[1]))
        country = crawl_from_wiki(information[1], information[2])
        truth_file.write(dataRead + "\t" + country + "\n")
        truth_file.flush()
    driver.quit()
    truth_file.close()
    validation_file.close()

def main_for_crawler_wiki7():
    # read moive name from file
    def deal_with_crawling_character1(data):
        mapping = dict()
        mapping["&#2"] = "'"
        mapping["&#39;"] = "'"
        mapping["&#039;"] = "'"
        mapping["&#193;"] = "Á"
        mapping["&#197;"] = "Å"
        mapping["&#199;"] = "Ç"
        mapping["&#201;"] = "É"
        mapping["&#205;"] = "Í"
        mapping["&#211;"] = "Ó"
        mapping["&#212;"] = "Ô"
        mapping["&#214;"] = "Ö"
        mapping["&#216;"] = "Ø"
        mapping["&#220;"] = "Ü"
        mapping["&#222;"] = "Þ"
        mapping["&#223;"] = "ß"
        mapping["&#224;"] = "à"
        mapping["&#225;"] = "á"
        mapping["&#227;"] = "ã"
        mapping["&#228;"] = "ä"
        mapping["&#229;"] = "å"
        mapping["&#230;"] = "æ"
        mapping["&#231;"] = "ç"
        mapping["&#232;"] = "è"
        mapping["&#233;"] = "é"
        mapping["&#235;"] = "ë"
        mapping["&#236;"] = "ì"
        mapping["&#237;"] = "í"
        mapping["&#238;"] = "î"
        mapping["&#239;"] = "ï"
        mapping["&#240;"] = "ð"
        mapping["&#241;"] = "ñ"
        mapping["&#242;"] = "ò"
        mapping["&#243;"] = "ó"
        mapping["&#244;"] = "ô"
        mapping["&#245;"] = "õ"
        mapping["&#246;"] = "ö"
        mapping["&#248;"] = "ø"
        mapping["&#250;"] = "ú"
        mapping["&#251;"] = "û"
        mapping["&#252;"] = "ü"
        mapping["&#253;"] = "ý"
        mapping[r"\t"] = ""
        mapping[r"\n"] = ""
        mapping["Sr."] = ""
        mapping["Jr."] = ""
        mapping[" and "] = ";"
        mapping[" & "] = ";"
        mapping["&rsquo;"] = r"'"
        mapping["&eacute;"] = "é"
        mapping["&aacute;"] = "á"
        mapping["&ocirc;"] = "ô"
        mapping["&oacute;"] = "ó"
        mapping["&uacute;"] = "u"
        mapping["&oslash;"] = "ø"
        mapping["&ouml;"] = "ö"
        mapping["&uuml;"] = "ü"
        mapping["&iacute;"] = "í"
        mapping["&Ocirc;"] = "Ô"
        mapping["&auml;"] = "ä"
        mapping["&Aacute;"] = "Á"
        mapping["&egrave;"] = "è"
        mapping["&quot;"] = r"'"
        mapping["&aring;"] = "å"
        mapping["&Aring;"] = "Å"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    def deal_with_crawling_character2(data):
        mapping = dict()
        mapping["'01;"] = "É"
        mapping["'05;"] = "Í"
        mapping["'11;"] = "Ó"
        mapping["'12;"] = "Ô"
        mapping["'14;"] = "Ö"
        mapping["'16;"] = "Ø"
        mapping["'20;"] = "Ü"
        mapping["'22;"] = "Þ"
        mapping["'23;"] = "ß"
        mapping["'24;"] = "à"
        mapping["'25;"] = "á"
        mapping["'27;"] = "?"
        mapping["'28;"] = "ä"
        mapping["'29;"] = "å"
        mapping["'30;"] = "æ"
        mapping["'31;"] = "ç"
        mapping["'32;"] = "è"
        mapping["'33;"] = "é"
        mapping["'35;"] = "ë"
        mapping["'36;"] = "ì"
        mapping["'37;"] = "í"
        mapping["'38;"] = "î"
        mapping["'39;"] = "ï"
        mapping["'40;"] = "ð"
        mapping["'41;"] = "ñ"
        mapping["'42;"] = "ò"
        mapping["'43;"] = "ó"
        mapping["'44;"] = "ô"
        mapping["'45;"] = "õ"
        mapping["'46;"] = "?"
        mapping["'48;"] = "ø"
        mapping["'50;"] = "ú"
        mapping["'51;"] = "û"
        mapping["'52;"] = "ü"
        mapping["'53;"] = "z"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    global driver
    global driver_path
    driver_path = "./chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    validation_file = open(file="./conflictDB_movie", mode="r", encoding="utf-8")
    truth_file = open(file="./movie_attribute_crawl7", mode="r", encoding="utf-8")
    written_length = len(truth_file.readlines())
    truth_file.close()
    truth_file = open(file="./movie_attribute_crawl7", mode="a+", encoding="utf-8")
    validation_lines = validation_file.readlines()
    for validation_line in range(int(5*len(validation_lines)/8)+written_length, int(3*len(validation_lines)/4)):  #len(validation_lines)
        dataRead = validation_lines[validation_line].strip("\n")
        information = dataRead.split("\t")
        information[1] = deal_with_crawling_character2(deal_with_crawling_character1(information[1]))
        country = crawl_from_wiki(information[1], information[2])
        truth_file.write(dataRead + "\t" + country + "\n")
        truth_file.flush()
    driver.quit()
    truth_file.close()
    validation_file.close()

def main_for_crawler_wiki4():
    # read moive name from file
    def deal_with_crawling_character1(data):
        mapping = dict()
        mapping["&#2"] = "'"
        mapping["&#39;"] = "'"
        mapping["&#039;"] = "'"
        mapping["&#193;"] = "Á"
        mapping["&#197;"] = "Å"
        mapping["&#199;"] = "Ç"
        mapping["&#201;"] = "É"
        mapping["&#205;"] = "Í"
        mapping["&#211;"] = "Ó"
        mapping["&#212;"] = "Ô"
        mapping["&#214;"] = "Ö"
        mapping["&#216;"] = "Ø"
        mapping["&#220;"] = "Ü"
        mapping["&#222;"] = "Þ"
        mapping["&#223;"] = "ß"
        mapping["&#224;"] = "à"
        mapping["&#225;"] = "á"
        mapping["&#227;"] = "ã"
        mapping["&#228;"] = "ä"
        mapping["&#229;"] = "å"
        mapping["&#230;"] = "æ"
        mapping["&#231;"] = "ç"
        mapping["&#232;"] = "è"
        mapping["&#233;"] = "é"
        mapping["&#235;"] = "ë"
        mapping["&#236;"] = "ì"
        mapping["&#237;"] = "í"
        mapping["&#238;"] = "î"
        mapping["&#239;"] = "ï"
        mapping["&#240;"] = "ð"
        mapping["&#241;"] = "ñ"
        mapping["&#242;"] = "ò"
        mapping["&#243;"] = "ó"
        mapping["&#244;"] = "ô"
        mapping["&#245;"] = "õ"
        mapping["&#246;"] = "ö"
        mapping["&#248;"] = "ø"
        mapping["&#250;"] = "ú"
        mapping["&#251;"] = "û"
        mapping["&#252;"] = "ü"
        mapping["&#253;"] = "ý"
        mapping[r"\t"] = ""
        mapping[r"\n"] = ""
        mapping["Sr."] = ""
        mapping["Jr."] = ""
        mapping[" and "] = ";"
        mapping[" & "] = ";"
        mapping["&rsquo;"] = r"'"
        mapping["&eacute;"] = "é"
        mapping["&aacute;"] = "á"
        mapping["&ocirc;"] = "ô"
        mapping["&oacute;"] = "ó"
        mapping["&uacute;"] = "u"
        mapping["&oslash;"] = "ø"
        mapping["&ouml;"] = "ö"
        mapping["&uuml;"] = "ü"
        mapping["&iacute;"] = "í"
        mapping["&Ocirc;"] = "Ô"
        mapping["&auml;"] = "ä"
        mapping["&Aacute;"] = "Á"
        mapping["&egrave;"] = "è"
        mapping["&quot;"] = r"'"
        mapping["&aring;"] = "å"
        mapping["&Aring;"] = "Å"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    def deal_with_crawling_character2(data):
        mapping = dict()
        mapping["'01;"] = "É"
        mapping["'05;"] = "Í"
        mapping["'11;"] = "Ó"
        mapping["'12;"] = "Ô"
        mapping["'14;"] = "Ö"
        mapping["'16;"] = "Ø"
        mapping["'20;"] = "Ü"
        mapping["'22;"] = "Þ"
        mapping["'23;"] = "ß"
        mapping["'24;"] = "à"
        mapping["'25;"] = "á"
        mapping["'27;"] = "?"
        mapping["'28;"] = "ä"
        mapping["'29;"] = "å"
        mapping["'30;"] = "æ"
        mapping["'31;"] = "ç"
        mapping["'32;"] = "è"
        mapping["'33;"] = "é"
        mapping["'35;"] = "ë"
        mapping["'36;"] = "ì"
        mapping["'37;"] = "í"
        mapping["'38;"] = "î"
        mapping["'39;"] = "ï"
        mapping["'40;"] = "ð"
        mapping["'41;"] = "ñ"
        mapping["'42;"] = "ò"
        mapping["'43;"] = "ó"
        mapping["'44;"] = "ô"
        mapping["'45;"] = "õ"
        mapping["'46;"] = "?"
        mapping["'48;"] = "ø"
        mapping["'50;"] = "ú"
        mapping["'51;"] = "û"
        mapping["'52;"] = "ü"
        mapping["'53;"] = "z"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    global driver
    global driver_path
    driver_path = "./chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    validation_file = open(file="./conflictDB_movie", mode="r", encoding="utf-8")
    truth_file = open(file="./movie_attribute_crawl4", mode="r", encoding="utf-8")
    written_length = len(truth_file.readlines())
    truth_file.close()
    truth_file = open(file="./movie_attribute_crawl4", mode="a+", encoding="utf-8")
    validation_lines = validation_file.readlines()
    for validation_line in range(int(3*len(validation_lines)/4)+written_length, int(7*len(validation_lines)/8)):  #len(validation_lines)
        dataRead = validation_lines[validation_line].strip("\n")
        information = dataRead.split("\t")
        information[1] = deal_with_crawling_character2(deal_with_crawling_character1(information[1]))
        country = crawl_from_wiki(information[1], information[2])
        truth_file.write(dataRead + "\t" + country + "\n")
        truth_file.flush()
    driver.quit()
    truth_file.close()
    validation_file.close()

def main_for_crawler_wiki8():
    # read moive name from file
    def deal_with_crawling_character1(data):
        mapping = dict()
        mapping["&#2"] = "'"
        mapping["&#39;"] = "'"
        mapping["&#039;"] = "'"
        mapping["&#193;"] = "Á"
        mapping["&#197;"] = "Å"
        mapping["&#199;"] = "Ç"
        mapping["&#201;"] = "É"
        mapping["&#205;"] = "Í"
        mapping["&#211;"] = "Ó"
        mapping["&#212;"] = "Ô"
        mapping["&#214;"] = "Ö"
        mapping["&#216;"] = "Ø"
        mapping["&#220;"] = "Ü"
        mapping["&#222;"] = "Þ"
        mapping["&#223;"] = "ß"
        mapping["&#224;"] = "à"
        mapping["&#225;"] = "á"
        mapping["&#227;"] = "ã"
        mapping["&#228;"] = "ä"
        mapping["&#229;"] = "å"
        mapping["&#230;"] = "æ"
        mapping["&#231;"] = "ç"
        mapping["&#232;"] = "è"
        mapping["&#233;"] = "é"
        mapping["&#235;"] = "ë"
        mapping["&#236;"] = "ì"
        mapping["&#237;"] = "í"
        mapping["&#238;"] = "î"
        mapping["&#239;"] = "ï"
        mapping["&#240;"] = "ð"
        mapping["&#241;"] = "ñ"
        mapping["&#242;"] = "ò"
        mapping["&#243;"] = "ó"
        mapping["&#244;"] = "ô"
        mapping["&#245;"] = "õ"
        mapping["&#246;"] = "ö"
        mapping["&#248;"] = "ø"
        mapping["&#250;"] = "ú"
        mapping["&#251;"] = "û"
        mapping["&#252;"] = "ü"
        mapping["&#253;"] = "ý"
        mapping[r"\t"] = ""
        mapping[r"\n"] = ""
        mapping["Sr."] = ""
        mapping["Jr."] = ""
        mapping[" and "] = ";"
        mapping[" & "] = ";"
        mapping["&rsquo;"] = r"'"
        mapping["&eacute;"] = "é"
        mapping["&aacute;"] = "á"
        mapping["&ocirc;"] = "ô"
        mapping["&oacute;"] = "ó"
        mapping["&uacute;"] = "u"
        mapping["&oslash;"] = "ø"
        mapping["&ouml;"] = "ö"
        mapping["&uuml;"] = "ü"
        mapping["&iacute;"] = "í"
        mapping["&Ocirc;"] = "Ô"
        mapping["&auml;"] = "ä"
        mapping["&Aacute;"] = "Á"
        mapping["&egrave;"] = "è"
        mapping["&quot;"] = r"'"
        mapping["&aring;"] = "å"
        mapping["&Aring;"] = "Å"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    def deal_with_crawling_character2(data):
        mapping = dict()
        mapping["'01;"] = "É"
        mapping["'05;"] = "Í"
        mapping["'11;"] = "Ó"
        mapping["'12;"] = "Ô"
        mapping["'14;"] = "Ö"
        mapping["'16;"] = "Ø"
        mapping["'20;"] = "Ü"
        mapping["'22;"] = "Þ"
        mapping["'23;"] = "ß"
        mapping["'24;"] = "à"
        mapping["'25;"] = "á"
        mapping["'27;"] = "?"
        mapping["'28;"] = "ä"
        mapping["'29;"] = "å"
        mapping["'30;"] = "æ"
        mapping["'31;"] = "ç"
        mapping["'32;"] = "è"
        mapping["'33;"] = "é"
        mapping["'35;"] = "ë"
        mapping["'36;"] = "ì"
        mapping["'37;"] = "í"
        mapping["'38;"] = "î"
        mapping["'39;"] = "ï"
        mapping["'40;"] = "ð"
        mapping["'41;"] = "ñ"
        mapping["'42;"] = "ò"
        mapping["'43;"] = "ó"
        mapping["'44;"] = "ô"
        mapping["'45;"] = "õ"
        mapping["'46;"] = "?"
        mapping["'48;"] = "ø"
        mapping["'50;"] = "ú"
        mapping["'51;"] = "û"
        mapping["'52;"] = "ü"
        mapping["'53;"] = "z"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    global driver
    global driver_path
    driver_path = "./chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    validation_file = open(file="./conflictDB_movie", mode="r", encoding="utf-8")
    truth_file = open(file="./movie_attribute_crawl8", mode="r", encoding="utf-8")
    written_length = len(truth_file.readlines())
    truth_file.close()
    truth_file = open(file="./movie_attribute_crawl8", mode="a+", encoding="utf-8")
    validation_lines = validation_file.readlines()
    for validation_line in range(int(7*len(validation_lines)/8)+written_length, len(validation_lines)):  #len(validation_lines)
        dataRead = validation_lines[validation_line].strip("\n")
        information = dataRead.split("\t")
        information[1] = deal_with_crawling_character2(deal_with_crawling_character1(information[1]))
        country = crawl_from_wiki(information[1], information[2])
        truth_file.write(dataRead + "\t" + country + "\n")
        truth_file.flush()
    driver.quit()
    truth_file.close()
    validation_file.close()

def main_for_crawler_wiki_add1():
    # read moive name from file
    def deal_with_crawling_character1(data):
        mapping = dict()
        mapping["&#2"] = "'"
        mapping["&#39;"] = "'"
        mapping["&#039;"] = "'"
        mapping["&#193;"] = "Á"
        mapping["&#197;"] = "Å"
        mapping["&#199;"] = "Ç"
        mapping["&#201;"] = "É"
        mapping["&#205;"] = "Í"
        mapping["&#211;"] = "Ó"
        mapping["&#212;"] = "Ô"
        mapping["&#214;"] = "Ö"
        mapping["&#216;"] = "Ø"
        mapping["&#220;"] = "Ü"
        mapping["&#222;"] = "Þ"
        mapping["&#223;"] = "ß"
        mapping["&#224;"] = "à"
        mapping["&#225;"] = "á"
        mapping["&#227;"] = "ã"
        mapping["&#228;"] = "ä"
        mapping["&#229;"] = "å"
        mapping["&#230;"] = "æ"
        mapping["&#231;"] = "ç"
        mapping["&#232;"] = "è"
        mapping["&#233;"] = "é"
        mapping["&#235;"] = "ë"
        mapping["&#236;"] = "ì"
        mapping["&#237;"] = "í"
        mapping["&#238;"] = "î"
        mapping["&#239;"] = "ï"
        mapping["&#240;"] = "ð"
        mapping["&#241;"] = "ñ"
        mapping["&#242;"] = "ò"
        mapping["&#243;"] = "ó"
        mapping["&#244;"] = "ô"
        mapping["&#245;"] = "õ"
        mapping["&#246;"] = "ö"
        mapping["&#248;"] = "ø"
        mapping["&#250;"] = "ú"
        mapping["&#251;"] = "û"
        mapping["&#252;"] = "ü"
        mapping["&#253;"] = "ý"
        mapping[r"\t"] = ""
        mapping[r"\n"] = ""
        mapping["Sr."] = ""
        mapping["Jr."] = ""
        mapping[" and "] = ";"
        mapping[" & "] = ";"
        mapping["&rsquo;"] = r"'"
        mapping["&eacute;"] = "é"
        mapping["&aacute;"] = "á"
        mapping["&ocirc;"] = "ô"
        mapping["&oacute;"] = "ó"
        mapping["&uacute;"] = "u"
        mapping["&oslash;"] = "ø"
        mapping["&ouml;"] = "ö"
        mapping["&uuml;"] = "ü"
        mapping["&iacute;"] = "í"
        mapping["&Ocirc;"] = "Ô"
        mapping["&auml;"] = "ä"
        mapping["&Aacute;"] = "Á"
        mapping["&egrave;"] = "è"
        mapping["&quot;"] = r"'"
        mapping["&aring;"] = "å"
        mapping["&Aring;"] = "Å"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    def deal_with_crawling_character2(data):
        mapping = dict()
        mapping["'01;"] = "É"
        mapping["'05;"] = "Í"
        mapping["'11;"] = "Ó"
        mapping["'12;"] = "Ô"
        mapping["'14;"] = "Ö"
        mapping["'16;"] = "Ø"
        mapping["'20;"] = "Ü"
        mapping["'22;"] = "Þ"
        mapping["'23;"] = "ß"
        mapping["'24;"] = "à"
        mapping["'25;"] = "á"
        mapping["'27;"] = "?"
        mapping["'28;"] = "ä"
        mapping["'29;"] = "å"
        mapping["'30;"] = "æ"
        mapping["'31;"] = "ç"
        mapping["'32;"] = "è"
        mapping["'33;"] = "é"
        mapping["'35;"] = "ë"
        mapping["'36;"] = "ì"
        mapping["'37;"] = "í"
        mapping["'38;"] = "î"
        mapping["'39;"] = "ï"
        mapping["'40;"] = "ð"
        mapping["'41;"] = "ñ"
        mapping["'42;"] = "ò"
        mapping["'43;"] = "ó"
        mapping["'44;"] = "ô"
        mapping["'45;"] = "õ"
        mapping["'46;"] = "?"
        mapping["'48;"] = "ø"
        mapping["'50;"] = "ú"
        mapping["'51;"] = "û"
        mapping["'52;"] = "ü"
        mapping["'53;"] = "z"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    global driver
    global driver_path
    driver_path = "./chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    validation_file = open(file="./movie_to_add", mode="r", encoding="utf-8")
    truth_file = open(file="./movie_attribute_crawl_add1", mode="r", encoding="utf-8")
    written_length = len(truth_file.readlines())
    truth_file.close()
    truth_file = open(file="./movie_attribute_crawl_add1", mode="a+", encoding="utf-8")
    validation_lines = validation_file.readlines()
    for validation_line in range(1 + written_length, int(len(validation_lines)/4)):  #len(validation_lines)
        dataRead = validation_lines[validation_line].strip("\n")
        information = dataRead.split("\t")
        information[1] = deal_with_crawling_character2(deal_with_crawling_character1(information[1]))
        country = crawl_from_wiki(information[1], information[2])
        truth_file.write(dataRead + "\t" + country + "\n")
        truth_file.flush()
    driver.quit()
    truth_file.close()
    validation_file.close()

def main_for_crawler_wiki_add2():
    # read moive name from file
    def deal_with_crawling_character1(data):
        mapping = dict()
        mapping["&#2"] = "'"
        mapping["&#39;"] = "'"
        mapping["&#039;"] = "'"
        mapping["&#193;"] = "Á"
        mapping["&#197;"] = "Å"
        mapping["&#199;"] = "Ç"
        mapping["&#201;"] = "É"
        mapping["&#205;"] = "Í"
        mapping["&#211;"] = "Ó"
        mapping["&#212;"] = "Ô"
        mapping["&#214;"] = "Ö"
        mapping["&#216;"] = "Ø"
        mapping["&#220;"] = "Ü"
        mapping["&#222;"] = "Þ"
        mapping["&#223;"] = "ß"
        mapping["&#224;"] = "à"
        mapping["&#225;"] = "á"
        mapping["&#227;"] = "ã"
        mapping["&#228;"] = "ä"
        mapping["&#229;"] = "å"
        mapping["&#230;"] = "æ"
        mapping["&#231;"] = "ç"
        mapping["&#232;"] = "è"
        mapping["&#233;"] = "é"
        mapping["&#235;"] = "ë"
        mapping["&#236;"] = "ì"
        mapping["&#237;"] = "í"
        mapping["&#238;"] = "î"
        mapping["&#239;"] = "ï"
        mapping["&#240;"] = "ð"
        mapping["&#241;"] = "ñ"
        mapping["&#242;"] = "ò"
        mapping["&#243;"] = "ó"
        mapping["&#244;"] = "ô"
        mapping["&#245;"] = "õ"
        mapping["&#246;"] = "ö"
        mapping["&#248;"] = "ø"
        mapping["&#250;"] = "ú"
        mapping["&#251;"] = "û"
        mapping["&#252;"] = "ü"
        mapping["&#253;"] = "ý"
        mapping[r"\t"] = ""
        mapping[r"\n"] = ""
        mapping["Sr."] = ""
        mapping["Jr."] = ""
        mapping[" and "] = ";"
        mapping[" & "] = ";"
        mapping["&rsquo;"] = r"'"
        mapping["&eacute;"] = "é"
        mapping["&aacute;"] = "á"
        mapping["&ocirc;"] = "ô"
        mapping["&oacute;"] = "ó"
        mapping["&uacute;"] = "u"
        mapping["&oslash;"] = "ø"
        mapping["&ouml;"] = "ö"
        mapping["&uuml;"] = "ü"
        mapping["&iacute;"] = "í"
        mapping["&Ocirc;"] = "Ô"
        mapping["&auml;"] = "ä"
        mapping["&Aacute;"] = "Á"
        mapping["&egrave;"] = "è"
        mapping["&quot;"] = r"'"
        mapping["&aring;"] = "å"
        mapping["&Aring;"] = "Å"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    def deal_with_crawling_character2(data):
        mapping = dict()
        mapping["'01;"] = "É"
        mapping["'05;"] = "Í"
        mapping["'11;"] = "Ó"
        mapping["'12;"] = "Ô"
        mapping["'14;"] = "Ö"
        mapping["'16;"] = "Ø"
        mapping["'20;"] = "Ü"
        mapping["'22;"] = "Þ"
        mapping["'23;"] = "ß"
        mapping["'24;"] = "à"
        mapping["'25;"] = "á"
        mapping["'27;"] = "?"
        mapping["'28;"] = "ä"
        mapping["'29;"] = "å"
        mapping["'30;"] = "æ"
        mapping["'31;"] = "ç"
        mapping["'32;"] = "è"
        mapping["'33;"] = "é"
        mapping["'35;"] = "ë"
        mapping["'36;"] = "ì"
        mapping["'37;"] = "í"
        mapping["'38;"] = "î"
        mapping["'39;"] = "ï"
        mapping["'40;"] = "ð"
        mapping["'41;"] = "ñ"
        mapping["'42;"] = "ò"
        mapping["'43;"] = "ó"
        mapping["'44;"] = "ô"
        mapping["'45;"] = "õ"
        mapping["'46;"] = "?"
        mapping["'48;"] = "ø"
        mapping["'50;"] = "ú"
        mapping["'51;"] = "û"
        mapping["'52;"] = "ü"
        mapping["'53;"] = "z"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    global driver
    global driver_path
    driver_path = "./chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    validation_file = open(file="./movie_to_add", mode="r", encoding="utf-8")
    truth_file = open(file="./movie_attribute_crawl_add2", mode="r", encoding="utf-8")
    written_length = len(truth_file.readlines())
    truth_file.close()
    truth_file = open(file="./movie_attribute_crawl_add2", mode="a+", encoding="utf-8")
    validation_lines = validation_file.readlines()
    for validation_line in range(written_length + int(len(validation_lines)/4), int(len(validation_lines)/2)):  #len(validation_lines)
        dataRead = validation_lines[validation_line].strip("\n")
        information = dataRead.split("\t")
        information[1] = deal_with_crawling_character2(deal_with_crawling_character1(information[1]))
        country = crawl_from_wiki(information[1], information[2])
        truth_file.write(dataRead + "\t" + country + "\n")
        truth_file.flush()
    driver.quit()
    truth_file.close()
    validation_file.close()

def main_for_crawler_wiki_add3():
    # read moive name from file
    def deal_with_crawling_character1(data):
        mapping = dict()
        mapping["&#2"] = "'"
        mapping["&#39;"] = "'"
        mapping["&#039;"] = "'"
        mapping["&#193;"] = "Á"
        mapping["&#197;"] = "Å"
        mapping["&#199;"] = "Ç"
        mapping["&#201;"] = "É"
        mapping["&#205;"] = "Í"
        mapping["&#211;"] = "Ó"
        mapping["&#212;"] = "Ô"
        mapping["&#214;"] = "Ö"
        mapping["&#216;"] = "Ø"
        mapping["&#220;"] = "Ü"
        mapping["&#222;"] = "Þ"
        mapping["&#223;"] = "ß"
        mapping["&#224;"] = "à"
        mapping["&#225;"] = "á"
        mapping["&#227;"] = "ã"
        mapping["&#228;"] = "ä"
        mapping["&#229;"] = "å"
        mapping["&#230;"] = "æ"
        mapping["&#231;"] = "ç"
        mapping["&#232;"] = "è"
        mapping["&#233;"] = "é"
        mapping["&#235;"] = "ë"
        mapping["&#236;"] = "ì"
        mapping["&#237;"] = "í"
        mapping["&#238;"] = "î"
        mapping["&#239;"] = "ï"
        mapping["&#240;"] = "ð"
        mapping["&#241;"] = "ñ"
        mapping["&#242;"] = "ò"
        mapping["&#243;"] = "ó"
        mapping["&#244;"] = "ô"
        mapping["&#245;"] = "õ"
        mapping["&#246;"] = "ö"
        mapping["&#248;"] = "ø"
        mapping["&#250;"] = "ú"
        mapping["&#251;"] = "û"
        mapping["&#252;"] = "ü"
        mapping["&#253;"] = "ý"
        mapping[r"\t"] = ""
        mapping[r"\n"] = ""
        mapping["Sr."] = ""
        mapping["Jr."] = ""
        mapping[" and "] = ";"
        mapping[" & "] = ";"
        mapping["&rsquo;"] = r"'"
        mapping["&eacute;"] = "é"
        mapping["&aacute;"] = "á"
        mapping["&ocirc;"] = "ô"
        mapping["&oacute;"] = "ó"
        mapping["&uacute;"] = "u"
        mapping["&oslash;"] = "ø"
        mapping["&ouml;"] = "ö"
        mapping["&uuml;"] = "ü"
        mapping["&iacute;"] = "í"
        mapping["&Ocirc;"] = "Ô"
        mapping["&auml;"] = "ä"
        mapping["&Aacute;"] = "Á"
        mapping["&egrave;"] = "è"
        mapping["&quot;"] = r"'"
        mapping["&aring;"] = "å"
        mapping["&Aring;"] = "Å"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    def deal_with_crawling_character2(data):
        mapping = dict()
        mapping["'01;"] = "É"
        mapping["'05;"] = "Í"
        mapping["'11;"] = "Ó"
        mapping["'12;"] = "Ô"
        mapping["'14;"] = "Ö"
        mapping["'16;"] = "Ø"
        mapping["'20;"] = "Ü"
        mapping["'22;"] = "Þ"
        mapping["'23;"] = "ß"
        mapping["'24;"] = "à"
        mapping["'25;"] = "á"
        mapping["'27;"] = "?"
        mapping["'28;"] = "ä"
        mapping["'29;"] = "å"
        mapping["'30;"] = "æ"
        mapping["'31;"] = "ç"
        mapping["'32;"] = "è"
        mapping["'33;"] = "é"
        mapping["'35;"] = "ë"
        mapping["'36;"] = "ì"
        mapping["'37;"] = "í"
        mapping["'38;"] = "î"
        mapping["'39;"] = "ï"
        mapping["'40;"] = "ð"
        mapping["'41;"] = "ñ"
        mapping["'42;"] = "ò"
        mapping["'43;"] = "ó"
        mapping["'44;"] = "ô"
        mapping["'45;"] = "õ"
        mapping["'46;"] = "?"
        mapping["'48;"] = "ø"
        mapping["'50;"] = "ú"
        mapping["'51;"] = "û"
        mapping["'52;"] = "ü"
        mapping["'53;"] = "z"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    global driver
    global driver_path
    driver_path = "./chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    validation_file = open(file="./movie_to_add", mode="r", encoding="utf-8")
    truth_file = open(file="./movie_attribute_crawl_add3", mode="r", encoding="utf-8")
    written_length = len(truth_file.readlines())
    truth_file.close()
    truth_file = open(file="./movie_attribute_crawl_add3", mode="a+", encoding="utf-8")
    validation_lines = validation_file.readlines()
    for validation_line in range(int(len(validation_lines)/2) + written_length, int(3*len(validation_lines)/4)):  #len(validation_lines)
        dataRead = validation_lines[validation_line].strip("\n")
        information = dataRead.split("\t")
        information[1] = deal_with_crawling_character2(deal_with_crawling_character1(information[1]))
        country = crawl_from_wiki(information[1], information[2])
        truth_file.write(dataRead + "\t" + country + "\n")
        truth_file.flush()
    driver.quit()
    truth_file.close()
    validation_file.close()

def main_for_crawler_wiki_add4():
    # read moive name from file
    def deal_with_crawling_character1(data):
        mapping = dict()
        mapping["&#2"] = "'"
        mapping["&#39;"] = "'"
        mapping["&#039;"] = "'"
        mapping["&#193;"] = "Á"
        mapping["&#197;"] = "Å"
        mapping["&#199;"] = "Ç"
        mapping["&#201;"] = "É"
        mapping["&#205;"] = "Í"
        mapping["&#211;"] = "Ó"
        mapping["&#212;"] = "Ô"
        mapping["&#214;"] = "Ö"
        mapping["&#216;"] = "Ø"
        mapping["&#220;"] = "Ü"
        mapping["&#222;"] = "Þ"
        mapping["&#223;"] = "ß"
        mapping["&#224;"] = "à"
        mapping["&#225;"] = "á"
        mapping["&#227;"] = "ã"
        mapping["&#228;"] = "ä"
        mapping["&#229;"] = "å"
        mapping["&#230;"] = "æ"
        mapping["&#231;"] = "ç"
        mapping["&#232;"] = "è"
        mapping["&#233;"] = "é"
        mapping["&#235;"] = "ë"
        mapping["&#236;"] = "ì"
        mapping["&#237;"] = "í"
        mapping["&#238;"] = "î"
        mapping["&#239;"] = "ï"
        mapping["&#240;"] = "ð"
        mapping["&#241;"] = "ñ"
        mapping["&#242;"] = "ò"
        mapping["&#243;"] = "ó"
        mapping["&#244;"] = "ô"
        mapping["&#245;"] = "õ"
        mapping["&#246;"] = "ö"
        mapping["&#248;"] = "ø"
        mapping["&#250;"] = "ú"
        mapping["&#251;"] = "û"
        mapping["&#252;"] = "ü"
        mapping["&#253;"] = "ý"
        mapping[r"\t"] = ""
        mapping[r"\n"] = ""
        mapping["Sr."] = ""
        mapping["Jr."] = ""
        mapping[" and "] = ";"
        mapping[" & "] = ";"
        mapping["&rsquo;"] = r"'"
        mapping["&eacute;"] = "é"
        mapping["&aacute;"] = "á"
        mapping["&ocirc;"] = "ô"
        mapping["&oacute;"] = "ó"
        mapping["&uacute;"] = "u"
        mapping["&oslash;"] = "ø"
        mapping["&ouml;"] = "ö"
        mapping["&uuml;"] = "ü"
        mapping["&iacute;"] = "í"
        mapping["&Ocirc;"] = "Ô"
        mapping["&auml;"] = "ä"
        mapping["&Aacute;"] = "Á"
        mapping["&egrave;"] = "è"
        mapping["&quot;"] = r"'"
        mapping["&aring;"] = "å"
        mapping["&Aring;"] = "Å"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    def deal_with_crawling_character2(data):
        mapping = dict()
        mapping["'01;"] = "É"
        mapping["'05;"] = "Í"
        mapping["'11;"] = "Ó"
        mapping["'12;"] = "Ô"
        mapping["'14;"] = "Ö"
        mapping["'16;"] = "Ø"
        mapping["'20;"] = "Ü"
        mapping["'22;"] = "Þ"
        mapping["'23;"] = "ß"
        mapping["'24;"] = "à"
        mapping["'25;"] = "á"
        mapping["'27;"] = "?"
        mapping["'28;"] = "ä"
        mapping["'29;"] = "å"
        mapping["'30;"] = "æ"
        mapping["'31;"] = "ç"
        mapping["'32;"] = "è"
        mapping["'33;"] = "é"
        mapping["'35;"] = "ë"
        mapping["'36;"] = "ì"
        mapping["'37;"] = "í"
        mapping["'38;"] = "î"
        mapping["'39;"] = "ï"
        mapping["'40;"] = "ð"
        mapping["'41;"] = "ñ"
        mapping["'42;"] = "ò"
        mapping["'43;"] = "ó"
        mapping["'44;"] = "ô"
        mapping["'45;"] = "õ"
        mapping["'46;"] = "?"
        mapping["'48;"] = "ø"
        mapping["'50;"] = "ú"
        mapping["'51;"] = "û"
        mapping["'52;"] = "ü"
        mapping["'53;"] = "z"

        for target in mapping.keys():
            while (data.find(target) >= 0):
                index = data.find(target)
                if index >= 0:
                    data = data[0:index] if (index + len(target) == len(data)) else \
                        data[0:index] + mapping[target] + data[index + len(target):len(data)]
        return data

    global driver
    global driver_path
    driver_path = "./chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    validation_file = open(file="./movie_to_add", mode="r", encoding="utf-8")
    truth_file = open(file="./movie_attribute_crawl_add4", mode="r", encoding="utf-8")
    written_length = len(truth_file.readlines())
    truth_file.close()
    truth_file = open(file="./movie_attribute_crawl_add4", mode="a+", encoding="utf-8")
    validation_lines = validation_file.readlines()
    for validation_line in range(int(3*len(validation_lines)/4) + written_length, len(validation_lines)):  #len(validation_lines)
        dataRead = validation_lines[validation_line].strip("\n")
        information = dataRead.split("\t")
        information[1] = deal_with_crawling_character2(deal_with_crawling_character1(information[1]))
        country = crawl_from_wiki(information[1], information[2])
        truth_file.write(dataRead + "\t" + country + "\n")
        truth_file.flush()
    driver.quit()
    truth_file.close()
    validation_file.close()

if __name__ == '__main__':
    # change to command reading  Comp: -data -table_sequence Elective: -general_interval -problem_interval

    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--select', type=str, default=None)
    args = parser.parse_args()
    path = args.select
    if path == "1":
        main_for_crawler_wiki1()
    elif path == "2":
        main_for_crawler_wiki2()
    elif path == "3":
        main_for_crawler_wiki3()
    elif path == "4":
        main_for_crawler_wiki4()
    elif path == "5":
        main_for_crawler_wiki5()
    elif path == "6":
        main_for_crawler_wiki6()
    elif path == "7":
        main_for_crawler_wiki7()
    elif path == "8":
        main_for_crawler_wiki8()
    elif path == "9":
        main_for_crawler_wiki_add1()
    elif path == "10":
        main_for_crawler_wiki_add2()
    elif path == "11":
        main_for_crawler_wiki_add3()
    elif path == "12":
        main_for_crawler_wiki_add4()