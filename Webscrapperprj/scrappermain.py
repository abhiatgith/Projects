import json
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import usermgmt.UserManagementDBOperations as dbmgmt

from Job import Job


def get_jobs(page_url):
    page_number = '1'
    # Get current page number if page number greater than 1
    if str(page_url).__contains__("https://www.monsterindia.com/search/it-computers-software-jobs-"):
        str1 = page_url.split("https://www.monsterindia.com/search/it-computers-software-jobs-")[1]
        page_number = str1.split("?")[0]

    print('Page ' + str(page_number) + ': ' + page_url)
    # Get all jobs of current page
    req_data = requests.get(page_url)
    job_soup = BeautifulSoup(req_data.content, 'html.parser')
    all_jobs = job_soup.find_all('div', {'class': 'card-apply-content'})
    # for each job of the current page, get the required details
    for job in all_jobs:
        job_place = ''
        job_exp = ''
        job_pac = ''

        try:
            job_title = job.find('div', {'class': 'job-tittle'}).find('h3', {'class': 'medium'}).find('a', {
                'href': True}).text
            job_company = job.find('div', {'class': 'job-tittle'}).find('span', {'class': 'company-name'}).find('a', {
                'href': True}).text
            # get all the sub section 'span' classes to get the place, experience and package details
            job_pep = job.find('div', {'class': 'job-tittle'}).find('div', {'class': 'searctag row'}).find_all('span', {
                'class': 'loc'})
            job_place = job_pep[0].text.strip()
            job_exp = job_pep[1].text.strip()
            job_pac = job_pep[2].text.strip()
            job_desc = job.find('p', {'class': 'job-descrip'}).text.strip()
            job_skills = job.find('p', {'class': 'descrip-skills'}).text.strip().replace('\n', '') \
                .replace(' ', '').replace('Skills:', '')

            #         if job_skills.lower().__contains__('datascience') or job_skills.lower().__contains__('machinelearning'):
            # Create an object of type job
            job_obj = Job(job_title, job_company, job_place, job_exp, job_pac, job_desc, job_skills)
            # append each job to the list as an object of the class job
            lstJobs.append(job_obj)

            print('Job Title :' + job_obj.jobTitle)
            print('Job Company : ' + job_obj.jobCompany)
            print("Job Location: " + job_obj.jobPlace)
            print('Job Experience Required :' + job_obj.jobExp)
            print('Job Package : ' + job_obj.jobPac)
            print('Job Description : ' + job_obj.jobDesc)
            print('Job Skills Required : ' + job_obj.jobSkills)
            print('--------------------------------------------------------------------------------------------------')

        except:
            print('Error on ' + str(page_number) + ': ' + page_url)


def insertDataInDB(data, dbName, collectionName):
    # client = MongoClient()
    # db = client[dbName]
    # collections = db.collectionName
    # result = collections.insert_one(data)
    # return result
    db_ob1 = dbmgmt.DBUserManagement("mongodb://localhost:27017/")
    if db_ob1.checfIfDBExists(dbName) != True:
        db = db_ob1.createDatabse(dbName)
    else:
        db = db_ob1.myclient[dbName]
    if db_ob1.checkIfCollectionExist(db, collectionName) != True:
        collections = db_ob1.createCollection(db, collectionName)
    else:
        collections = db[collectionName]
    result = collections.insert_one(data)
    return result


# def getDataByuserId( dbName, collectionName):
#    client = MongoClient()
#    db = client[dbName]
#    result = db[collectionName].find_one({'user': 'Moumita Dey'})
#    return result

# Create an object into JSON
def json_default_format(jobsObj):
    if isinstance(jobsObj, Job):
        return {
            'Job Title': jobsObj.jobTitle,
            'Job Company': jobsObj.jobCompany,
            'Job Location': jobsObj.jobPlace,
            'Job Experience Required': jobsObj.jobExp,
            'Job Package': jobsObj.jobPac,
            'Job Description': jobsObj.jobDesc,
            'Job Skills Required': jobsObj.jobSkills
        }


if __name__ == "__main__":
    websiteUrl = "https://www.monsterindia.com"

    # URL for all IT computer software jobs on monster
    nextpageUrl = "https://www.monsterindia.com/search/it-computers-software-jobs?searchId=5252de8a-b778-4c92-b8f2-672b31de3db6"

    # Initialize list for storing relevant jobs
    lstJobs = []

    # databaseObj = DataAcccess('ReviewDB', 'ScrapperCollection')

    try:
        while nextpageUrl != '':
            try:
                print('Current page  : ' + nextpageUrl)
                # calls the function that finds the jobs in each page and keeps appending the jobs in each URL to the lstJobs list
                get_jobs(nextpageUrl)
                # using the requests package to get the contents of the nextpageUrl into the variable req
                req = requests.get(nextpageUrl)
                # using the beautiful soup package with the html.parser parameter to get the contents of the nextpageUrl into the variable nxt_soup
                nxt_soup = BeautifulSoup(req.content, 'html.parser')
                # finding the URL of the 'next' page
                # find the tag with the class which has the link for the 'next' page
                u = nxt_soup.find_all('button', {'class': 'btn-next-prev'})
                if len(u) == 1:
                    if str.lower(u[0].text.strip()) == 'next':
                        nextpageUrl = u[0].find_parent('a', {'href': True})['href']
                    else:
                        nextpageUrl = ''
                else:
                    nextpageUrl = u[1].find_parent('a', {'href': True})['href']
                # testing for first 10 pages
                str0 = nextpageUrl.split("https://www.monsterindia.com/search/it-computers-software-jobs-")[1]
                page_number0 = str0.split("?")[0]
                if str(page_number0) == '10':
                    break
                print('Next Page : ' + nextpageUrl)
                # print( u)
            except:
                print('Error Occured or last page ')
                break
    except:
        print('Error Occurred')

    dict_list = []

    for r in lstJobs:
        insertDataInDB(json_default_format(r), 'JobScraperDB', 'scraperCollection_1dec2020')
        dict_list.append(json_default_format(r))

    # print('*' * 100)
    # print('Get Review by is')

    jsonObj = json.dumps(dict_list)
    print(jsonObj)
