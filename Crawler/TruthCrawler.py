# -*- coding:utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# crawl movie truth from https://www.themoviedb.org
def crawl_from_moviedb(movie_name, year):
    global driver
    country_info = ""
    people_list = list()
    movie_address = "https://www.themoviedb.org"
    try:
        search_movie_name = movie_name.replace("&", "") # 神奇改变1
        search_movie_name = search_movie_name.replace("#", "")  # 神奇改变2
        search_movie_name = search_movie_name.replace(r"\\", "")  # 神奇改变2
        driver.get(movie_address)
        search_bar = driver.find_element_by_id("search_v4")
        search_bar.send_keys(search_movie_name + Keys.ENTER)  # title
        time.sleep(2)
        # find Movies and TV Shows
        search_condition = [".//a[@id='movie' and @title='Movies']", "//a[@id='tv' and @title='TV Shows']"]
        #search_condition = ["/movie?", "/tv?"]
        for searching in range(len(search_condition)):
            #print(driver.current_url)
            driver.get(driver.find_element_by_xpath(search_condition[searching]).get_attribute('href'))
            #"https://www.themoviedb.org/search/movie?query=Adam%20&amp;%20Paul&language=en"
            #"https://www.themoviedb.org/search/tv?query=Adam%20&amp;%20Paul&language=en"
            #query_list = driver.current_url.split("?")
            #query_url = movie_address + search_condition[searching]
            #for query_item in range(1, len(query_list)):
            #    query_url = query_url + query_list[query_item]
            #driver.get(query_url)
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
                    movie_release_holder = movie_release.find_elements_by_xpath(".//li")
                    flag = False
                    for movie_release_item in movie_release_holder:
                        if movie_release_item.text.find(year) >= 0:
                            flag = True
                            break
                    if not (movie_release1.find(year) >= 0 or flag):
                        driver.back()
                        continue
                    try:
                        profile_item = driver.find_element_by_css_selector("[class='people no_image']")
                        people_items = profile_item.find_elements_by_xpath("./li[@class='profile']")
                        for people_item in people_items:
                            people_name = people_item.find_element_by_xpath(".//a").text
                            people_role = people_item.find_element_by_xpath(".//p[@class='character']").text
                            if people_role.find("Director")>=0 or people_role.find("Creator")>=0:
                                people_list.append(people_name)
                    except NoSuchElementException:
                        people_list = list()
                    try:
                        country_info = movie_release.find_element_by_xpath(".//img").get_attribute('src').split("/")[7].split("-")[0]
                    except Exception:
                        try:
                            country_info = movie_release.find_element_by_xpath(".//img").get_attribute('data-src').split("/")[7].split("-")[0]
                        except Exception:
                            country_info = ""
                    if not (country_info == "" and len(people_list) == 0):
                        break
            if not(country_info == "" and len(people_list) == 0):
                break
    except NoSuchElementException:
        pass
    return people_list, country_info

def main_for_crawler_movie():
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
    validation_file = open(file="../DataToUse/movie/validation_movie", mode="r", encoding="utf-8")
    truth_file = open(file="./truth_crawled_movie", mode="a+", encoding="utf-8")
    validation_lines = validation_file.readlines()
    for validation_line in range(len(validation_lines)):  #
        dataRead = validation_lines[validation_line].strip("\n")
        if validation_line == 0:
            truth_file.write(dataRead + "\tDirector\tCountry\n")
        else:
            information = dataRead.split("\t")
            information[1] = deal_with_crawling_character2(deal_with_crawling_character1(information[1]))
            director_list, country = crawl_from_moviedb(information[1], information[2])
            dataRead = dataRead + "\t"
            for director in director_list:
                dataRead = dataRead + director + ";"
            truth_file.write(dataRead.strip(";") + "\t" + country + "\n")
            truth_file.flush()
    driver.quit()
    truth_file.close()
    validation_file.close()

# crawl book author truth from https://isbnsearch.org
def crawl_from_isbnsearch(isbn_13):
    global driver
    author_list = list()
    try:
        driver.get("https://isbnsearch.org")
        driver.find_element_by_id("searchQuery").clear()
        driver.find_element_by_id("searchQuery").send_keys(isbn_13)
        driver.find_element_by_id("searchSubmit").click()
        try:
            time.sleep(1)
            info_list = driver.find_element_by_class_name("bookinfo")
            author_list = info_list.text.split("\n")[3].strip("\n").split(":")[1].strip(" ").split(";")
        except Exception:
            print("Can't Find")
            author_list = list()
            raise NoSuchElementException
    except NoSuchElementException:
        pass
    return author_list

def main_for_crawler_book():
    global driver
    global driver_path
    driver_path = "./chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    validation_file = open(file="../DataToUse/book/validation_book", mode="r", encoding="utf-8")
    truth_file = open(file="./truth_crawled_book", mode="a+", encoding="utf-8")
    validation_lines = validation_file.readlines()
    for validation_line in range(len(validation_lines)):  #
        dataRead = validation_lines[validation_line].strip("\n")
        if validation_line == 0:
            truth_file.write(dataRead + "\tAuthor\n")
        else:
            information = dataRead.split("\t")
            author_list= crawl_from_isbnsearch(information[1])
            dataRead = dataRead + "\t"
            for author in author_list:
                dataRead = dataRead + author + ";"
            truth_file.write(dataRead.strip(";") + "\n")
            truth_file.flush()
    driver.quit()
    truth_file.close()
    validation_file.close()

#main_for_crawler_wiki()
#main_for_crawler_book()
if __name__ == '__main__':
    main_for_crawler_book()