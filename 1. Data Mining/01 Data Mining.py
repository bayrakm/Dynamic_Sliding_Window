#!/usr/bin/python3

import requests as rq
import pandas as pd 
import sqlite3
import datetime
import json
import time
from bs4 import BeautifulSoup as bs
import lxml.html
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PROGRESS = pd.read_csv("progress") #load progress data from progress file
def save_progress(site, i,j, mk, md):
    #this function's only purpose is to save progress of scraping so if the script crashes it will start from where it stopped
    global PROGRESS
    PROGRESS[site][0] = i
    PROGRESS[site][1] = j
    PROGRESS[site][2] = mk
    PROGRESS[site][3] = md
    PROGRESS.to_csv("progress", index=False)

connection = sqlite3.connect("cars.db")
def save_db(date, source, make, model, price, mileage, year, power, consumption, cylinder, gears, fuel, transmission, body, co2, door, seat ,engine):
    #The function saves rows on sqlite DB below exception will handle if the data does not match types in DB and an error log will be saved to log file
    global connection
    insert_text = "INSERT INTO CARS (DATE,SOURCE,MAKE,MODEL,PRICE,MILEAGE,YEAR,POWER,CONSUMPTION,CYLINDER,GEARS,FUEL,TRANSMISSION,BODY,CO2,DOOR,SEAT,ENGINE) VALUES ('{}','{}','{}','{}',{},{},{},{},{},{},{},'{}','{}','{}',{},{},{},{});".format(date, source, make, model, price, mileage, year, power, consumption, cylinder, gears, fuel, transmission, body, co2, door, seat ,engine)
    #print(insert_text)   #debug
    try:
        connection.execute(insert_text)
    except Exception as e:
        log(source, "Couldn't save row sqlite database.")
        print(f"{str(e)} | {insert_text}")
    connection.commit()


def log(source, error):
    #this function logs not only errors but everything that happens during the process
    dt = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    with open("script_log.log",'w') as f:
        f.write(f"{dt} - {source} : {error}" + "\n")

SPECIFIED_MODELS = pd.DataFrame({"toyota":["aygo","auris", "yaris", "rav4", "avensis"],
                    "vauxhall":["astra","corsa","adam","mokka x","insignia"],
                    "volkswagen":["polo", "golf", "scirocco","tiguan","passat"],
                    "ford":["ka", "fiesta", "focus", "kuga", "mondeo"]})


SOURCES = pd.read_sql_query("SELECT SOURCE FROM CARS;", connection) #load urls as they are unique to each car 
postcodes = pd.read_csv("finalcodes") #load postal codes since some websites need postal code for proper results
options = Options()
options.add_argument("start-maximized")
options.add_argument('--headless')
br2 = webdriver.PhantomJS("./phantomjs")


#------------------   autotrader   ------------------
mk = PROGRESS['autotrader'][2]
while mk<3:
    #break #debug
    md = PROGRESS['autotrader'][3]
    while md<5:
        i=PROGRESS['autotrader'][0]
        while True:
            code = postcodes[' Postcode'][i] #continue from where stopped in the postal codes file
            j=PROGRESS['autotrader'][1] #continue from where stopped in the pages count
            while True:
                autotrader = f"https://www.autotrader.co.uk/results-car-search?sort=datedesc&postcode={code}&make={SPECIFIED_MODELS.columns[mk]}&model={SPECIFIED_MODELS[SPECIFIED_MODELS.columns[mk]][md]}&page={j}"
                pg = rq.get(autotrader, headers={"User-agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"})#load results page
                dtr = json.loads(pg.text)
                print(autotrader)
                ps = bs(dtr['html'], 'html.parser')
                cars = ps.find_all('a', class_="listing-fpa-link")
                for c in cars:
                    lnk = "https://www.autotrader.co.uk" + c['href']
                    SOURCES = pd.read_sql_query("SELECT SOURCE FROM CARS;", connection) #check if the url exists in database, if yes then just go to the next car 
                    if lnk.split("?")[0] in SOURCES.values:
                        print("DUPLICATE PASSED <--------")
                        continue
                    br2.get(lnk)
                    try:
                        WebDriverWait(br2, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div/div[2]/aside/section[2]/h1")))
                    except:
                        log(lnk, "Error loading page")
                        continue
                    date = "0000-00-00"
                    source = lnk.split("?")[0]
                    make = br2.find_element(By.XPATH, '/html/body/div[2]/main/div/div[2]/aside/section[2]/h1').text.split(" ")[0]
                    model = br2.find_element(By.XPATH, '/html/body/div[2]/main/div/div[2]/aside/section[2]/h1').text.partition(" ")[2]
                    price = br2.find_element(By.XPATH, '/html/body/div[2]/main/div/div[2]/aside/section[2]/div[1]/div[1]/h2').text.replace(',','').replace("£","")
                    try:
                        mileage = br2.find_element(By.XPATH, '/html/body/div[2]/main/div/div[2]/article/section[2]/span[1]/span[3]').text.split(' ')[0].replace(',','')
                    except:
                        mileage = "0"
                    try:
                        year = int(br2.title.split(' ')[0])
                    except:
                        try:
                            year = int(br2.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/aside/section[2]/p[1]").text.replace('\n','').split(" ")[0])
                        except:
                            year = "0"
                    br2.execute_script("window.scrollTo(0,0);")
                    br2.execute_script("window.scrollTo(0,900);")
                    try:
                        WebDriverWait(br2, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div/div[2]/article/div[1]/button")))
                    except:
                        try:
                            br2.execute_script("window.scrollTo(0,0);")
                            br2.execute_script("window.scrollTo(0,1200);")
                            WebDriverWait(br2, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div/div[2]/article/div[1]/button")))
                        except:
                            log(source, "Unable to load specifications window.")
                            continue
                    try:
                        br2.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/article/div[1]/button").click()
                        br2.find_element(By.XPATH, "/html/body/div[3]/div/section/div[2]/div/ul/li[1]/span/button").click()
                        perf = br2.find_element(By.XPATH, '/html/body/div[3]/div/section/div[2]/div/ul/li[1]/span/div/ul')
                        lis = perf.find_elements(By.TAG_NAME, 'li')
                        power = lis[4].text.split('\n')[1].split(' ')[0]
                        cylinder = lis[2].text.split('\n')[1]
                    except:
                        power = "0"
                        cylinder = "0"       
                    gears = "0" #revisit
                    webdriver.ActionChains(br2).send_keys(Keys.ESCAPE).perform()
                    try:
                        br2.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/article/div[2]/button/span[1]").click()
                        consumption = br2.find_element(By.XPATH, "/html/body/div[3]/div/section/div[2]/div/div[3]/div/div/dl/dd").text.split(' ')[0]
                        co2 = br2.find_element(By.XPATH, "/html/body/div[3]/div/section/div[2]/div/div[2]/div/div/dl/dd[2]").text.replace("g/km",'')
                        webdriver.ActionChains(br2).send_keys(Keys.ESCAPE).perform()
                    except:
                        consumption = "0"
                        co2 = "0"
                    try:
                        fuel = br2.find_element(By.XPATH, '/html/body/div[2]/main/div/div[2]/article/section[2]/ul/li[4]').text
                    except:
                        fuel = "N/A"
                    try:
                        transmission = br2.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/article/section[2]/ul/li[3]").text
                    except:
                        transmission = "N/A"
                    try:
                        body = br2.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/article/section[2]/ul/li[1]").text
                    except:
                        body = "N/A"

                    spec = br2.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/article/section[2]/ul")
                    sps = spec.find_elements(By.TAG_NAME, 'li')
                    door = "0"
                    seat = "0"
                    for li in sps:
                        if "doors" in li.text:
                            try:
                                door = int(li.text.replace('doors', ''))
                            except:
                                door = '0'
                        if 'seats' in li.text:
                            try:
                                seat = int(li.text.replace('seats', ''))
                            except:
                                seat='0'
                        if "M20.65" in li.find_elements(By.TAG_NAME, "path")[-1].get_attribute('d'):
                            body = li.text
                        if "M6 " in li.find_elements(By.TAG_NAME, "path")[-1].get_attribute('d'):
                            transmission = li.text
                        if "m27.5" in li.find_elements(By.TAG_NAME, "path")[-1].get_attribute('d'):
                            fuel = li.text 
                        if "M5 " in li.find_elements(By.TAG_NAME, "path")[-1].get_attribute('d')[:5]:
                            engine = li.text.replace("L", '')
                    print(f"{make} -{model} -{price} -{mileage} -{year} -{power} -{consumption} -{cylinder} -{fuel} -{transmission} -{body} -{co2} -{door} -{seat} -{engine} -{source}")
                    save_db(date, source, make, model, price, mileage, year, power, consumption, cylinder, gears, fuel, transmission, body, co2, door, seat ,engine)
                #break #debug
                if "Maximum displayed results reached" in dtr['html']:
                    j=0
                    md+=1
                    if md>4:
                        mk+=1
                        md=0
                        save_progress("autotrader", 0,0,mk,0)
                        break
                    else:
                        save_progress("autotrader", 0, j, mk, md)
                        break
                else:
                    j+=1
                    save_progress("autotrader", 0, j, mk, md)
                    print(f"code:{i} - page:{j}")

log("autotrader", "All Done, Loading cargurus...")

#------------------   cargurus   ------------------


'''
    instead of make and model cargurus have an entity id for each car model.
    The below IDs where manually collected to be used for scraping the same model above.
    since cargurus have an opne API it is easy to use requests and collect data from json file
'''
entity = ['d2350','d2348','d2352','d2368','d2406','d2412','d2383','d4204','d2391','d2432','d2431','d2434','d2439','d2430','d3075','d3105','d3082','d3101','d3111']
et = PROGRESS['cargurus'][2]
while True:
    if et>18:
        break
    break #debug
    offset = PROGRESS['cargurus'][0]
    while True:
        mdl = entity[et]
        url = f"https://www.cargurus.co.uk/Cars/searchResults.action?inventorySearchWidgetType=AUTO&searchId=0731c598-040d-4678-a73a-92e0e8f7e5bf&nonShippableBaseline=0&shopByTypes=NEAR_BY&sortDir=ASC&sourceContext=carGurusHomePageModel&distance=50&sortType=AGE_IN_DAYS&entitySelectingHelper.selectedEntity={mdl}&offset={offset}&maxResults=15000&filtersModified=true"
        pg = rq.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"})
        if pg.text == "null":
            offset=0
            et+=1
            save_progress("cargurus",offset,0,et,0)
            break
        else:
            offset+=36
            save_progress("cargurus",offset,0,et,0)
        try:
            data = json.loads(pg.text)
        except:
            print("couldn't load data.")
            log(url, "Couldn't load JSON data.")
            continue
        for d in data:
            link = f"https://www.cargurus.co.uk/Cars/detailListingJson.action?inventoryListing={d['id']}"
            SOURCES = pd.read_sql_query("SELECT SOURCE FROM CARS;", connection)
            if link in SOURCES.values:
                print("DUPLICATE PASSED <--------")
                continue
            car = rq.get(link, headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"})
            try:
                car = json.loads(car.text)
            except:
                print("ERROR <-------------------")
                log(link, "Couldn't load JSON data.")
                continue
            try:
                date = datetime.datetime.strptime(car['listing']['localizedRegistrationDate'], "%d %b %Y").strftime("%Y-%m-%d")
            except:
                date = "0000-00-00" 
            source = link
            try:
                make = car['listing']['makeName']
            except:
                make = "N/A"
            try:
                model = car['listing']['modelName']
            except:
                model = "N/A"
            try:
                price = car['listing']['price']
            except:
                price = "0"
            try:
                mileage = car['listing']['mileage']
            except:
                mileage = '0'
            try:
                year = car['autoEntityInfo']['year']
            except:
                year = '0'
            power = '0' #revisit
            try:
                consumption = car['listing']['localizedFuelEconomy'][2].split(' ')[0]
            except:
                consumption = '0'
            cylinder = '0' #revisit
            gears = '0' #revisit
            try:
                fuel = car['listing']['localizedFuelType']
            except:
                fuel = "N/A"
            try:
                transmission = car['listing']['localizedTransmission']
            except:
                transmission = "N/A"
            try:
                body = car['autoEntityInfo']['bodyStyle']
            except:
                body = "N/A"
            try:
                co2 = car['listing']['localizedCO2Emissions'].split(" ")[0]
            except:
                co2 = '0'
            try:
                door = car['listing']['localizedNumberOfDoors'].split(' ')[0]
            except:
                door = '0'
            try:
                seat = car['listing']['localizedMaxSeating'].split(' ')[0]
            except:
                seat = "0"
            try:
                engine = car['listing']['localizedEngineDisplacementName'].replace('L','')
            except:
                engine = '0'
            print(f"{make} -{model} -{price} -{mileage} -{year} -{power} -{consumption} -{cylinder} -{fuel} -{transmission} -{body} -{co2} -{door} -{seat} -{engine} -{source.partition('?')[0]}")
            save_db(date, source, make, model, price, mileage, year, power, consumption, cylinder, gears, fuel, transmission, body, co2, door, seat ,engine)
        save_progress('cargurus',offset,0, et,0)
        print(f"Entity: {et}- offset: {offset}")
log("cargurus", "All Done, Loading parkers...")




#------------------   parkers   ------------------

'''
    even though parkers doesn't have any kind of API, 
    requests was still the best option to do the task faster and cleaner
'''

i= PROGRESS['parkers'][0]
while True:
    break
    if i>3:
        break
    mak = SPECIFIED_MODELS.columns[i]
    s = PROGRESS['parkers'][2]
    while True:
        model = SPECIFIED_MODELS[SPECIFIED_MODELS.columns[i]][s]
        j = PROGRESS['parkers'][1]
        if j==0:
            j+=1
        while True:
            print(f"{mak} : {j}")
            url = f"https://www.parkers.co.uk/{mak}/{model}/search-results/?page={j}"
            pg = rq.get(url, headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"})
            result = bs(pg.text, 'html.parser')
            content = result.find("ul", class_="results-container")
            items = content.find_all("li", class_="result-item")
            for item in items[1:]:
                if item.find('a') == None:
                    continue
                link = item.find("a", class_="for-sale-result-item__image").get("href")
                SOURCES = pd.read_sql_query("SELECT SOURCE FROM CARS;", connection)
                if "redirect" in link or link in SOURCES.values:
                    continue
                elif "https://www.parkers.co.uk" + link in SOURCES.values:
                    print("DUPLICATE PASSED <--------")
                    continue
                carpage = rq.get("https://www.parkers.co.uk" + link)
                doc = bs(carpage.content, "html.parser")
                date = "0000-00-00"  #revisit
                source = "https://www.parkers.co.uk" + link
                make = doc.find("nav", class_="site-breadcrumbs").find_all("li")[1].text.replace("\n", '')
                model = doc.find("nav", class_="site-breadcrumbs").find_all("li")[2].text.replace("\n", "")
                price = item.find("div", class_="for-sale-result-item__price__value").text.replace(",","").replace("£","").replace("\n", "").replace("\t", "").replace("\r","")
                mileage = doc.find("ul", class_="pricing-table").find_all("li")[-1].text.split(' ')[0].replace(",","")
                year = item.find("ul", class_="for-sale-result-item__specs").find_all("li")[0].text.split("/")[0]
                specs = bs(rq.get("https://www.parkers.co.uk" + doc.findAll("a", href=True, text="Read the full specs")[0]['href']).content, 'html.parser').find_all("table", class_="specs-detail-page__section__content__table")
                power = specs[0].find_all("tr")[0].find("td").text.split(" ")[0]
                try:
                    consumption = float(specs[1].find_all('tr')[0].find("td").text.split(' ')[0].replace("\n", "").replace("\t", "").replace("\r",""))
                except:
                    consumption = 0
                cylinder = specs[4].find_all('tr')[1].find('td').text
                gears = specs[4].find_all('tr')[5].find('td').text.split(' ')[0]
                fuel = specs[4].find_all('tr')[3].find('td').text
                transmission = specs[4].find_all('tr')[4].find('td').text
                body = "N/A" #revisit
                co2 = specs[3].find_all('tr')[4].find('td').text.split(' ')[0]
                door = specs[5].find_all('tr')[0].find('td').text
                seat = specs[5].find_all('tr')[1].find('td').text
                try:
                    engine = round(int(specs[4].find_all('tr')[0].find('td').text.replace('cc',''))/1000,1)
                except:
                    engine = '0'
                print(f"{make} -{model} -{price} -{mileage} -{year} -{power} -{consumption} -{cylinder} -{fuel} -{transmission} -{body} -{co2} -{door} -{seat} -{engine} -{source.partition('?')[0]}")
                save_db(date, source, make, model, price, mileage, year, power, consumption, cylinder, gears, fuel, transmission, body, co2, door, seat ,engine)
            if "No matching results found." in result.text:
                j=0
                s+=1
                if s==5:
                    s=0
                    i+=1
                    save_progress("parkers", i, j, s, 0)
                    break
                else:
                    save_progress("parkers", i, j, s, 0)
                    break
            else:
                j+=1
                save_progress("parkers", i, j , s , 0)
    print(f"make: {i} - page: {j}")
    


log("parkers", "All Done, Loading theaa...")

br = webdriver.PhantomJS("./phantomjs")
#------------------   theaa   ------------------

'''
    Theaa uses POST method API which won't allow any API scraping using requests, 
    they only option was to use selenium Firefox to automate it.
'''

ids = pd.DataFrame({
    "144":['106','103','131','125','104'],
    "146":['102', '107','130','128','127'],
    "147":['116','105','125', '123', '114'],
    "113":['113', '109', '110', '126', '115']
})

makeIndex = PROGRESS['theaa'][1]
while True:
    i=PROGRESS['theaa'][0]
    modelIndex = PROGRESS['theaa'][2]
    while True:
        while True:
            #break #debug
            makeId = ids.columns[makeIndex]
            modelId = ids[makeId][modelIndex]
            link = f"https://www.theaa.com/used-cars/displaycars?sortby=datedesc&mymakeid={makeId}&mymodelid={modelId}&page={i}"
            print(link)
            br.get(link)
            try:
                WebDriverWait(br, 5).until(EC.presence_of_element_located((By.ID, "truste-consent-button")))
                br.find_element(By.ID, "truste-consent-button").click()
            except:
                pass
            if "Too Many Requests" in br.page_source:# or i >= int(float(br.find_element(By.CLASS_NAME, "car-count-update").get_attribute("data-count-total"))/20):
                i=0
                modelIndex+=1
                if modelIndex >4:
                    modelIndex=0
                    makeIndex+=1
                    save_progress("theaa", i, makeIndex, modelIndex, 0)
                    break
                else:
                    save_progress("theaa", i,makeIndex, modelIndex, 0)
                    break
            else:
                save_progress("theaa", i,makeIndex, modelIndex, 0)
                i+=1
            container = br.find_element(By.CLASS_NAME, "vl-list")
            cars = container.find_elements(By.CLASS_NAME, "vl-item")
            for car in cars:
                url = car.find_element(By.CLASS_NAME, "black-link").get_attribute("href")
                SOURCES = pd.read_sql_query("SELECT SOURCE FROM CARS;", connection)
                if url in SOURCES.values:
                    print("DUPLICATE PASSED <--------")
                    continue
                br2.get(url)
                try:
                    br.find_element(By.ID, "truste-consent-button").click()
                except:
                    pass
                date = "0000-00-00"
                source = url 
                make = br2.find_element(By.XPATH, "/html/body/div[2]/div[4]/main/div[3]/div[1]/section[1]/div/div/h1/span[1]").text 
                model = br2.find_element(By.XPATH, "/html/body/div[2]/div[4]/main/div[3]/div[1]/section[1]/div/div/h1/span[2]").text
                price = br2.find_element(By.XPATH, "/html/body/div[2]/div[4]/main/div[3]/div[1]/div[1]/div/div/strong").text.replace(",","").replace("£","")
                panel = br2.find_element(By.XPATH, "/html/body/div[2]/div[4]/main/div[3]/div[1]/section[3]/div")
                lis = panel.find_elements(By.TAG_NAME, "li")
                mileage = 0
                year = '0'
                power = "0"
                consumption = "0"
                cylinder = "0"
                gears = "0"
                fuel = 'N/A'
                transmission = "N/A"
                body = "N/A"
                co2 = "0"
                door = "0"
                seat="0"
                engine = "0"
                
                for li in lis:
                    if "Mileage" in li.text:
                        mileage = li.text.split("\n")[1].replace(",","")
                    if "Year" in li.text:
                        year = li.text.split("\n")[1]
                    if "Fuel type" in li.text:
                        fuel = li.text.split("\n")[1]
                    if "Transmission" in li.text:
                        transmission = li.text.split("\n")[1]
                    if "Body type" in li.text:
                        body = li.text.split("\n")[1]
                    if "Doors" in li.text:
                        door = li.text.split("\n")[1]
                    if "Engine size" in li.text:
                        engine = li.text.split("\n")[1].replace("L","")
                    if "CO2 Emissions" in li.text:
                        co2 = li.text.split("\n")[1].replace("g/km","")
                print(f"{make} -{model} -{price} -{mileage} -{year} -{power} -{consumption} -{cylinder} -{fuel} -{transmission} -{body} -{co2} -{door} -{seat} -{engine} -{source.partition('?')[0]}")
                save_db(date, source, make, model, price, mileage, year, power, consumption, cylinder, gears, fuel, transmission, body, co2, door, seat ,engine)
            print(f"page:{i}")



log("---", "All Done, script closing")

br2.quit()
br.quit()
connection.close()























# #motors.co.uk
# br = webdriver.Firefox()
# i = PROGRESS['motors'][0]
# while True:
#     code = postcodes[' Postcode'][i]
#     br.get("https://www.motors.co.uk/")
#     try:
#         WebDriverWait(br, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
#         br.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
#     except:
#         pass
#     search = br.find_element(By.ID, "searchPostcode")
#     search.clear()
#     search.send_keys(code)
#     try:
#         WebDriverWait(br, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/header/div[2]/div[2]/div/section/button")))
#         #search.send_keys(Keys.ENTER)
#         time.sleep(3)
#         br.find_element(By.XPATH, "/html/body/section/header/div[2]/div[2]/div/section/button").click()
#     except:
#         continue
#     while True:
#         container = br.find_element(By.CLASS_NAME, "result-card___wrap")
#         cars = container.find_elements(By.CLASS_NAME, "result-card")
#         for car in cars:
#             link = car.find_element(By.CLASS_NAME, "result-card__link").get_attribute("href")
#             br2.get(link)
#             date = "0000-00-00"
#             try:
#                 WebDriverWait(br, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
#                 br.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
#             except:
#                 pass
#             source = br2.current_url 
#             make = br2.find_element(By.CLASS_NAME, "title-3").text.split(',')[0]
#             model = br2.find_element(By.CLASS_NAME, "title-3").text.split(',')[1]
#             price = br2.find_elements(By.CLASS_NAME, "title-3")[1].text.replace(",","").replace("£","")
#             summary = br2.find_element(By.CLASS_NAME, "grid-specs").find_elements(By.CLASS_NAME, "card-line")[0]
#             mileage = '0'
#             items = summary.find_elements(By.CLASS_NAME, "grid-item")
#             for it in items:
#                 if "M24" in it.find_element(By.TAG_NAME, "path").get_attribute("d")[:10]:
#                     mileage = it.text.replace(",","").replace("Miles",'')
#                 if "M31" in it.find_element(By.TAG_NAME, "path").get_attribute("d")[:10]:
#                     fuel = it.text
#                 if "M44" in it.find_element(By.TAG_NAME, "path").get_attribute("d")[:10]:
#                     seat = it.text.replace("seats",'')
#                 if "M16" in it.find_element(By.TAG_NAME, "path").get_attribute("d")[:10]:
#                     transmission = it.text
#             items2 = car.find_element(By.CLASS_NAME, "result-card__vehicle-info").find_elements(By.TAG_NAME, "li")
#             engine = items[0].text.replace("L","")
#             body = items[4].text
#             year = br2.title.split("-")[0]
#             power = br2.find_element(By.XPATH, "/html/body/section/section/div[3]/div/div[3]/div[1]/section/div/section[4]/section/ul/li[2]/div/span[1]").text
#             door = br2.find_element(By.XPATH, "/html/body/section/section/div[3]/div/div[3]/div[1]/section/div/section[4]/section/ul/li[3]/div/span[1]").text
#             co2 = br2.find_element(By.XPATH, "/html/body/section/section/div[3]/div/div[3]/div[1]/section/div/section[4]/section/ul/li[1]/div/span[1]").text 
#             consumption = br2.find_element(By.XPATH, "/html/body/section/section/div[3]/div/div[3]/div[1]/div/div[2]/div/div[2]/div/div[1]/div").text
#             br2.find_element(By.XPATH, '//*[@id="techSpecTab"]').click()
#             cylinder = br2.find_element(By.XPATH, "/html/body/section/section/div[3]/div/div[3]/div[1]/section/div/section[4]/section/div/div[2]/ul/li[3]/span[2]").text
#             gears = br2.find_element(By.XPATH, "/html/body/section/section/div[3]/div/div[3]/div[1]/section/div/section[4]/section/div/div[2]/ul/li[6]/span[2]").text.replace("SPEED", "")
#             save_db(date, source, make, model, price, mileage, year, power, consumption, cylinder, gears, fuel, transmission, body, co2, door, seat ,engine)
#             print(f"{make} -{model} -{price} -{mileage} -{year} -{power} -{consumption} -{cylinder} -{fuel} -{transmission} -{body} -{co2} -{door} -{seat} -{engine} -{source.partition('?')[0]}")
#         if br.find_element(By.CLASS_NAME, "pgn__next").get_attribute("disabled") == None:
#             br.find_element(By.CLASS_NAME, "pgn__next").click()
#         else:
#             break
#     i+=1
#     save_progress("motors", i,0)




