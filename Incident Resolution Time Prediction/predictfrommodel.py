import pandas as pd
import os
import pickle
from file_operations import file_methods
from Data_Preprocessing.preprocessing import Pre_processor
from Prediction_model_data_import.prediction_data_load import Predict_Data_Import
from application_logging import logger
from Prediction_Raw_Data_Validation.prediction_rawvalidation import Prediction_Raw_Data_Validation
from Data_Preprocessing.preprocessing import Pre_processor


class Prediction:

    def __init__(self, path):
        self.file_object = open("Prediction_Logs/Prediction_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()
        self.pred_preprocessor = Pre_processor(self.file_object, self.log_writer)
        self.datapath = "models"
        self.pred_droplist = ['incident_state', 'active', 'impact', 'urgency', 'priority', 'notify']
        self.pred_conv_int32 = ['opened_at_day', 'opened_at_month', 'opened_at_weekday']
        if path is not None:
            self.pred_data_val = Prediction_Raw_Data_Validation(path)

    def predictionFromModel(self):
        # Method for prediction
        try:
            self.pred_data_val.deletePredictionFile()  # deletes the prediction file from last run!
            self.log_writer.log(self.file_object, 'Start of Prediction')

            # Getting the data into pandas dataframe named 'df_ir' for training
            pred_data_get = Predict_Data_Import(self.file_object, self.log_writer)
            pred_df_ir = pred_data_get.predict_get_data()

            # Data Pre-processing steps
            pred_preprocessor = Pre_processor(self.file_object, self.log_writer)

            # function to Check if all date field has been converted to datetime field, else convert to datetime field
            date_cols = ['opened_at', 'sys_created_at', 'sys_updated_at']
            pred_df_ir = pred_preprocessor.covert_date(pred_df_ir, date_cols)

            # Get all boolean columns and update value in column to one standard Boolean (True/False) value
            bool_list = ['active', 'made_sla', 'knowledge', 'u_priority_confirmation']
            self.log_writer.log(self.file_object,
                                "starting boolean update using update_bool method of the Pre_processor class.")
            for bool_cols in bool_list:
                pred_df_ir[bool_cols] = pred_df_ir[bool_cols].apply(pred_preprocessor.update_bool)

            # check if missing values (including '?' as missing values) are present in the dataset and store the count in a seperate file
            pred_is_null_present = pred_preprocessor.is_null_present(pred_df_ir)

            # Delete the following columns similar to training file processing
            pred_delete_cols = ['cmdb_ci', 'problem_id', 'rfc', 'vendor', 'caused_by', 'sys_created_by',
                                'sys_created_at',
                                'sys_updated_by', 'sys_updated_at']
            pred_df_ir = pred_preprocessor.remove_columns(pred_df_ir, pred_delete_cols)

            # Capture changes to data (in different incident states of the same incident) for relevant
            pred_chg_cols = ['category', 'subcategory', 'u_symptom', 'assignment_group', 'assigned_to']
            pred_df_ir = pred_preprocessor.capture_change(pred_df_ir, pred_chg_cols)

            # Creating a new dataframe with only unique Closed incidents with the highest value in the sys_mod_count
            pred_closed_incidents = pred_df_ir[pred_df_ir['incident_state'] == 'Closed']
            pred_df_clsd_uq = pred_closed_incidents.sort_values('sys_mod_count', ascending=False).drop_duplicates(
                ['number'])

            # Reset Index
            pred_df_clsd_uq = pred_df_clsd_uq.reset_index(drop=True)

            # Prediction data feature engineering
            self.log_writer.log(self.file_object, "Starting Prediction data feature engineering.")
            model_file = os.listdir(self.datapath)  # check ML algorithm using model file
            model_name = model_file[0].split('.')[0]
            if model_name == 'XGBoost':
                # Feature engineering for XGBoost model prediction
                # Replace ? by 'Unknown' so that they are treated by XGBoost as a separate category
                pred_df_clsd_uq = self.pred_preprocessor.xgboost_repq(pred_df_clsd_uq)

                # Extract day, month, day of week from opened date.
                pred_df_clsd_uq = self.pred_preprocessor.info_frm_date(pred_df_clsd_uq)

                # Converting Impact Urgency and Priority to numerical data since they are ordinal values
                pred_df_clsd_uq = self.pred_preprocessor.map_to_num(pred_df_clsd_uq)

                # remove other not required columns
                # We will remove 'Number' and 'Opened_at' columns in the next step and use this DataFrame for final prediction manipulations
                pred_df_clsd_uq = self.pred_preprocessor.remove_columns(pred_df_clsd_uq, self.pred_droplist)

                # importing Leaveonehot encoder from pickle file
                self.infile = open('encoder.pkl', 'rb')
                self.le_enc = pickle.load(self.infile)
                self.infile.close()
                # Transform categorical columns into numerical
                pred_df_clsd_uq_final = self.le_enc.transform(pred_df_clsd_uq)

                # Converting bool,object data type columns, opened_at_day,opened_at_month,opened_at_weekday into numerical using one hot encoding
                self.con_oh = ['made_sla', 'contact_type', 'knowledge', 'u_priority_confirmation', 'category_chngd',
                               'subcategory_chngd', 'u_symptom_chngd', 'assignment_group_chngd', 'assigned_to_chngd',
                               'opened_at_day', 'opened_at_month', 'opened_at_weekday']
                pred_df_clsd_uq = pd.get_dummies(pred_df_clsd_uq, columns=self.con_oh)

            elif model_name == 'LightGBM':
                # Feature engineering for LightGBM model prediction
                # Replace ? by 'Unknown' so that they are treated by XGBoost as a separate category
                pred_df_clsd_uq = self.pred_preprocessor.lightgbm_repq(pred_df_clsd_uq)

                # Extract day, month, day of week from opened date.
                pred_df_clsd_uq = self.pred_preprocessor.info_frm_date(pred_df_clsd_uq)

                # Converting Impact Urgency and Priority to numerical data since they are ordinal values
                pred_df_clsd_uq = self.pred_preprocessor.map_to_num(pred_df_clsd_uq)

                # remove other not required columns
                # We will remove 'Number' and 'Opened_at' columns in the next step and use this DataFrame for final prediction manipulations
                pred_df_clsd_uq = self.pred_preprocessor.remove_columns(pred_df_clsd_uq, self.pred_droplist)

                # Convert categorical columns that were encoded to ‘int64’ data type to ‘int32’ datatype.
                pred_df_clsd_uq = self.pred_preprocessor.convert_to_int32(pred_df_clsd_uq, self.pred_conv_int32)

                # convert to datatype category for lightGBM processing
                to_cat = ['caller_id', 'opened_by', 'contact_type', 'location', 'category', 'subcategory', 'u_symptom',
                          'assignment_group', 'assigned_to', 'closed_code', 'resolved_by', 'opened_at_day',
                          'opened_at_month', 'opened_at_weekday']

                # Convert ‘object’ datatype columns and other categorical columns into datatype category
                for col in to_cat:
                    pred_df_clsd_uq[col] = pred_df_clsd_uq[col].astype('category')

            # Remove 'Number' and 'Opened_at' columns
            pred_df_clsd_uq_final = pred_df_clsd_uq.drop(labels=['number', 'opened_at'], axis=1)

            # Load model
            self.file_loader = file_methods.File_Operations(self.file_object, self.log_writer)
            self.model = self.file_loader.load_model(model_name)
            self.predict = list(self.model.predict(pred_df_clsd_uq_final))
            inc_nums = list(pred_df_clsd_uq['number'])
            opend_at_dt = list(pred_df_clsd_uq['opened_at'])
            result = pd.DataFrame(list(zip(inc_nums, opend_at_dt, self.predict)),
                                  columns=['number', 'opened_at', 'Prediction'])
            result['Resolution_Time'] = result['Prediction'].apply(self.min_to_cat)
            final_res = pd.merge(pred_df_clsd_uq, result, on='number')
            final_result = final_res[['number', 'Resolution_Time', 'caller_id', 'opened_by', 'opened_at_x', 'contact_type', 'location', 'category', 'subcategory',
             'assignment_group', 'assigned_to', 'closed_code', 'resolved_by', 'Prediction']]
            final_result.to_csv("Prediction_Output_File/Prediction.csv", header=True,
                                mode='a+')  # appends result to prediction file
            path_folder = "Prediction_Output_File"
            path_file = "Prediction.csv"
            self.log_writer.log(self.file_object, 'End of Prediction')
            return path_folder, path_file
        except Exception as ex:
            self.log_writer.log(self.file_object, 'Error occured while running prediction!! Error:: %s' % ex)
            raise ex

    # Function for mapping prediction time to categories by hours/days/weeks/months
    def min_to_cat(self, val):
        if val < 360:
            return 'Within 6 hours'
        elif (val >= 360) & (val < 1440):
            return 'Within 24 hours'
        elif (val >= 1440) & (val < 2880):
            return '24 - 48 hours'
        elif (val >= 2880) & (val < 10080):
            return '2 to 7 days'
        elif (val >= 10080) & (val < 20160):
            return '1 - 2 weeks'
        elif (val >= 20160) & (val < 43200):
            return '2 weeks - 1 month'
        elif (val >= 43200) & (val < 86400):
            return '1 - 2 months'
        elif (val >= 86400) & (val <= 144000):
            return '2 - 3 months'

#if __name__ == "__main__":
#    obj1 = Prediction('Prediction_FileFromDB')
#    obj1.predictionFromModel()