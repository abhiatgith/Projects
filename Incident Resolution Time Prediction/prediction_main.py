from datetime import datetime
from Prediction_Raw_Data_Validation.prediction_rawvalidation import Prediction_Raw_Data_Validation
from Data_Transform_Prediction.data_transform_prediction import Data_Transform_Predict
from DB_Operations_Prediction.dboperations_prediction import DBOperation_Predict
from application_logging import logger

class pred_validation:
    def __init__(self, path):
        self.raw_data = Prediction_Raw_Data_Validation(path)
        self.dataTransform = Data_Transform_Predict()
        self.dBOperation = DBOperation_Predict()
        self.file_object = open("Prediction_Logs/Prediction_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()

    def prediction_validation(self):
        try:
            self.log_writer.log(self.file_object, 'Prediction: Starting Raw Data Validation of Files.')
            # extracting values from Prediction Schema to compare with input files
            noofcolumns, column_names = self.raw_data.valuesFromSchema()

            # getting the regex defined to validate filename
            regex = self.raw_data.regexfilename()

            # validating filename of training files and creating directory structure to store training files
            self.raw_data.validationRawFile(regex)

            # validating no of columns in the inout file
            self.raw_data.validationNumOfCols(noofcolumns)
            self.log_writer.log(self.file_object, "Prediction: Raw Data Validation Complete.")

            self.log_writer.log(self.file_object, "Prediction: Starting Data Transformation Step.")
            # replacing blanks in the csv file with "Null" values to insert into DB table
            self.dataTransform.replaceMissingWithNull()
            self.log_writer.log(self.file_object, "Prediction: Data Transformation Completed.")

            self.log_writer.log(self.file_object,
                                "Prediction: Starting DB Operations: Creating Database,Table and inserting data from CSV.")
            # Create Database with the given name/open connection if DB already present.
            # Create Table with columns as given in training schema file
            self.dBOperation.CreateTableDB('predict_ir_db', column_names)

            self.log_writer.log(self.file_object, "Prediction: Table Creation Completed.")
            self.log_writer.log(self.file_object, "Prediction: Insertion of Data into Table Started.")
            # insert data from csv files into DB table
            self.dBOperation.insertIntoTableGoodData('predict_ir_db')
            self.log_writer.log(self.file_object, "Prediction: Insertion into Table Completed.")

            self.log_writer.log(self.file_object, "Prediction: Deleting Good Data Folder.")
            # Delete the Good Data Folder after loading the file into the DB table
            self.raw_data.deleteExistingGoodDataTrainingFolder()
            self.log_writer.log(self.file_object, "Prediction: Good_Data folder deleted.")
            self.log_writer.log(self.file_object, "Prediction: DB Operations Completed.")

            self.log_writer.log(self.file_object, "Prediction: Extracting CSV file from DB Table.")
            # Export data from DB table into CSV
            self.dBOperation.selectingDatafromtableintocsv('predict_ir_db')
            self.log_writer.log(self.file_object, "Prediction: Extracting CSV file from DB Table completed.")

            # Copy data to archive table
            # Create archive Table with columns as given in training schema file
            self.log_writer.log(self.file_object, "Prediction: Archive Table Creation Started.")
            self.dBOperation.CreateArchiveTableDB('predict_ir_db', column_names)
            self.log_writer.log(self.file_object, "Prediction: Archive Table Creation Completed.")

            # Copy data from Good_Raw_Data table to Archive_Raw_Data Table
            self.log_writer.log(self.file_object, "Prediction: Insertion of Data into Archive Table Started.")
            self.dBOperation.insertIntoArchiveTableGoodData('predict_ir_db')
            self.log_writer.log(self.file_object, "Prediction: Insertion into Archive Table Completed.")

            self.file_object.close()

        except Exception as e:
            raise e

#if __name__ == "__main__":
#    obj1 = pred_validation('Prediction_Batch_Files')
#    obj1.prediction_validation()