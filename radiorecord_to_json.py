import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import json

uri = "http://www.radiorecord.ru/player/"
prefix = "http://air.radiorecord.ru:805/"
suffix = "_320"
print("Please wait, making Web Scrapping from " + uri)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1500x1500")

chrome_driver = os.path.join(os.getcwd(), "chromedriver.exe")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
driver.set_page_load_timeout(1000)
driver.set_script_timeout(1000)
driver.get(uri)

print(driver.title)
driver.save_screenshot("screenshot.png")
print("saved screenshot.png")

a = driver.find_element(by=By.XPATH, value="//div[@class='lists lists_stations']")
a = a.find_elements(by=By.XPATH, value="//a")
i = 1
ajson = []
for element in a:
    attr = element.get_attribute("onclick")
    if attr is not None:
        if "onStation" in attr:
            station_code = re.split("'", attr)[1]
            station_name = element.find_element_by_id("station").find_element_by_id("station_title").text
            station_uri = prefix + station_code + suffix
            print(station_code + " : " + station_name + " (" + station_uri + ")")
            ajson.append({"station_name": station_name, "station_code": station_code, "station_uri": station_uri})
            i += 1
with open('stations.json', 'w', encoding='utf8') as outfile:
    outfile.write(json.dumps({"stations": ajson}, ensure_ascii=False))
print("Scrapped "+str(i)+" stations! ")
print("Stations saved to stations")
