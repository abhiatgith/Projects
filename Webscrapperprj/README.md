# Project details:

- Scrap IT Jobs from the "https://www.monsterindia.com" website and store them in an MongoDB database.

a) naukriscrapper.py does the following:

1) Execution starts at line 96 - websiteUrl = "https://www.monsterindia.com"
2) Initialize 'nextpageUrl' variable to "https://www.monsterindia.com/search/it-computers-software-jobs?searchId=5252de8a-b778-4c92-b8f2-672b31de3db6". This URL lists all the IT Computer software jobs on the monster portal.
3) Call the 'get_jobs' function and pass the 'nextpageUrl' to scrap all below information for each job listing on the above URL. Assign these values for each job listing to an object(job_obj) of the class Job(Class Job is created as a seperate python file - 'Job.py'). Use the object(job_obj) to append each job to a list(lstJobs) as an object. Print the details for each job listing to the output.

'Job Title'
'Job Company'
'Job Location'
'Job Experience Required'
'Job Package' 
'Job Description'
'Job Skills Required'

4) Now, find the tag with the class on the above URL which has the link for the 'next' page and again call the'get_jobs' function and pass the 'next' page URL/link that you got now to scrap all the jobs from this page. Continue this process for the first 10 pages and then break the loop.

5) For each item in 'lstJobs' list, create a JSON format object by calling the 'json_default_format' fucntion and store the result in a dictionary.

6) insertDataInDB(json_default_format(r), 'JobScraperDB', 'scraperCollection')

For each item in the lstJobs list, create an entry in the 'scraperCollection' collection of the 'JobScraperDB' Mongo DB by calling the 'insertDataInDB' function and passing the DB, collection name and the JSON format of each entry in the lstJobs list.

The  'insertDataInDB' function first creates a connection object to the Mongodb, then checks if the database and collection are already existing and creates them if required after which the data is inserted as a JSON object into the collection.



6) Also pass the dictionary to json.dumps function to print the JSON file as output.
