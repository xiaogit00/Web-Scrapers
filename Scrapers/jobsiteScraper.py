from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import numpy as np

driver = webdriver.Firefox()
driver.get('https://job.[REDACTED].com/en/position?keywords=&category=6704215882479962371&location=&type=&current=1&limit=200')

print('Launching Driver...')

print('Locating Job Titles...')

#Generating 70 unique xpaths and storing it as a list

xpaths = []
for i in range(1,86):
    xpaths.append('//*[@id="bd"]/section/section/main/div/div/div[2]/div[3]/div[1]/div[2]/a[' + str(i) + ']/div/div[1]')

#Searching for those elements and storing them into jobTitles list
jobTitles = []
for i in range(1, 85):
    Elems = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, xpaths[i]))
        )
    jobTitles.append(Elems.text)
#jobTitles is a list that contains 68 jobs
print('{} Job Titles Successfully Found'.format(len(jobTitles)))

#2. GET DATES & LOCATIONS
#Get Date xpaths, store in list:
xpathsSubtitles = []
print('Locating Subtitles..')
for i in range(1,85):
    xpathsSubtitles.append('//*[@id="bd"]/section/section/main/div/div/div[2]/div[3]/div[1]/div[2]/a[' + str(i) + ']/div/div[2]')

#Loop through each xpath to find element, store in subTitles (dunno why 67 only)
subTitles = []

for i in range(1, 84):
    Elems = driver.find_elements_by_xpath(xpathsSubtitles[i])
    subTitles.append(Elems[0].text)

print('{} Job Subtitles Titles Successfully Found'.format(len(subTitles)))
#print('Creating a Dataframe to save the information...')
# 3. CREATE DATAFRAME AND SAVE SCRAPPED INFO INSIDE
#scrapped = {
#    'JobTitles': jobTitles,
#    'Date_Location': subTitles
#}

#df = pd.DataFrame.from_dict(scrapped, orient='index')

#df = pd.DataFrame.from_dict(my_dict, orient='index')
#df = df.T
#print('Dataframe Successfully created')
print('Getting further job information from individual links...please hang on tight..')
print('Generating Links...')
#4. GET ALL THE LINKS TO JOBS AT
# //*[@id="bd"]/section/section/main/div/div/div[2]/div[3]/div[1]/div[2]/a[1]

linksXpath = []

for i in range(1,83):
    linksXpath.append('//*[@id="bd"]/section/section/main/div/div/div[2]/div[3]/div[1]/div[2]/a[' + str(i) + ']')

links = []

for i in range(1,82):
    linkElems = driver.find_elements_by_xpath(linksXpath[i])
    links.append(linkElems[0].get_attribute('href'))

#ADDING LINKS TO DATAFRAME
#df = df.T
#df
#df1 = pd.DataFrame(links, columns = ['Links'])
#df = pd.concat([df,df1], axis=1)
#print('Links successfully added to Dataframe...Now generating all the job infos..hang on..')
#5. AUTOMATE DRIVER TO CLICK ON EACH LINK and APPEND INFO INTO THE 2 LISTS, jobDescriptions
# and Requirements:

jobDescriptions = []
Requirements = []
for i in links:
    driver.get(i)
    try: #try to locate by this Xpath, if not, go to exception
        jd_elems = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="bd"]/section/section/main/div/div/div[4]'))
        )
        jobDescriptions.append(jd_elems.text)
        print('Successfully located Job Description Text')
    except:
        jd_elems = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/section/section/main/div/div/div[4]'))
        )
        jobDescriptions.append(jd_elems.text)
        print('Successfully located Job Description Text')
    try: #try to locate Job Requirement by this xpath, if not, go to exception
        req_elems = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="bd"]/section/section/main/div/div/div[6]'))
        )
        Requirements.append(req_elems.text)
        print('Successfully located Job Requirement Text')
    except:
        jd_elems = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/section/section/main/div/div/div[6]'))
        )
        Requirements.append(req_elems.text)
        print('Successfully located Job Requirement Text')
    time.sleep(np.random.randint(low=1, high=3, size=1)) #-- added to prevent being banned?
print('Job Description Scrapping COmplete')

#6. APPEND TWO LISTS INTO DATAFRAME
print('Creating Dataframe')
Jobs = {
    'JobTitle': jobTitles,
    'Date_Location': subTitles,
    'JobDescriptions': jobDescriptions,
    'JobRequirements': Requirements,
    'Links': links
}
df = pd.DataFrame.from_dict(Jobs, orient='index')
df2 = df.T
df2.to_csv('./[REDACTED]_Scrapped/Dec2019_[REDACTED]_Marketing_Jobs_Scrapped_Raw.csv')
print('Dataframed saved to CSV')
