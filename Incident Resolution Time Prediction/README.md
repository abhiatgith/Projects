# Incident/Ticket Resolution time Prediction 

## Problem Statement

Create a Machine learning application which predicts the estimated time and date for the final closure of an opened ticket based on the given attributes 

Project hosted at Heroku: https://incidentresponsedemo.herokuapp.com/

## Steps for Demo:

1) Download the file named 'incident_event_log_predict.csv' which will be used for the prediction for this demo.
Note: Because of the specific format that the dataset has been provided in, the prediction dataset also needs to be in the same format. I have split 20% of the original dataset to be used for the prediction demo here(Which was not used for training the model).
2) Go to https://incidentresponsedemo.herokuapp.com/
3) Click on 'Browse' and navigate to the folder location where you downloaded the file 'incident_event_log_predict.csv' to and select the file.
4) Click on 'predict'.
5) After a few seconds, you will be prompted to download the file named 'prediction' which you can save to your system.
6) If you open the downloaded file, you can see the prediction for the time to resolve the incident under the 'Resolution_Time' column. The prediction categories are as follows:

* Within 6 hours
* Within 24 hours
* 24 - 48 hours
* 2 to 7 days
* 1 - 2 weeks
* 2 weeks - 1 month
* 1 - 2 months
* 2 - 3 months

## Notes:

- A sample of how the prediction file will look is provided in the project folder named 'Prediction.csv'.

- A detailed documentation of how I approached the project is provided in the file named 'Project Documentation.docx'. 

- The main intention is to demo the project that I worked on and hence I have not uploaded all the project files into GITHUB.

- The file 'Incident_Response_Reports.ipynb' is a jupyter notebook which contains many of the steps performed as part of the project.

- The dataset used for training the model is 'incident_event_log_train.csv' which is present in the project directory. For further details on the problem statement and dataset, please refer to the document - 'Incident_response_problem_statement.txt'.

## Dataset Citation:
Amaral, C. A. L., Fantinato, M., Reijers, H. A., Peres, S. M., Enhancing Completion Time Prediction Through Attribute Selection. Proceedings of the 15th International Conference on Advanced Information Technologies for Management (AITM 2018) and 13th International Conference on Information Systems Management (ISM 2018),

## Source:
Claudio Aparecido Lira do Amaral, claudio.amaral '@' usp.br, University of SÃ£o Paulo, Brazil
Marcelo Fantinato, m.fantinato '@' usp.br, University of SÃ£o Paulo, Brazil
Sarajane Marques Peres, sarajane '@' usp.br, University of SÃ£o Paulo, Brazil