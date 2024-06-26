from dataset_raw_class import Dataset_Raw
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
import json


class Dataset_Proc:
    def __init__(self, raw1: Dataset_Raw, raw2: Dataset_Raw, dataset_num):
        self.dataset_num = dataset_num
        self.destination_path = os.getenv("DATASETS_READY_FOLDER")
        self.final_traces_path = self.combine_traces(raw1, raw2, self.destination_path)
        self.final_textin_path = self.combine_textin_files(raw1, raw2, self.destination_path)
        self.final_textout_path = self.combine_textout_files(raw1, raw2, self.destination_path)
        self.final_keys_path = self.combine_keys_files(raw1, raw2, self.destination_path)

        self.key_array = raw1.key_array
        self.key_string = raw1.key_string

        self.traces_cols = 0
        self.traces_rows = 0
        self.textin_cols = 0
        self.textin_rows = 0
        self.textout_cols = 0
        self.textout_rows = 0
        self.keys_cols = 0
        self.keys_rows = 0

        self.check_traces_cols_and_rows()
        self.check_textin_cols_and_rows()
        self.check_textout_cols_and_rows()
        self.check_keys_cols_and_rows()

        self.normalize_and_save_npy()

        self.final_keys_json_path = self.save_keys_to_json()




    def combine_traces(self, raw1: Dataset_Raw, raw2: Dataset_Raw, destination):
        try:
            traces1 = np.load(raw1.traces_file_path)
            traces2 = np.load(raw2.traces_file_path)
            combined_data = np.vstack((traces1, traces2))

            new_name = str(self.dataset_num)+'_traces.npy'
            destination_path = os.path.join(destination, new_name)
            np.save(destination_path, combined_data)
            print(f"Combined file saved as {destination_path}")

            return destination_path
        except Exception as e:
            print(f"Error combining traces: {e}")
            return None

    def combine_textin_files(self, raw1: Dataset_Raw, raw2: Dataset_Raw, destination):
        try:
            textin_1 = np.load(raw1.textin_file_path)
            textin_2 = np.load(raw2.textin_file_path)
            combined_data = np.vstack((textin_1, textin_2))

            new_name = str(self.dataset_num)+'_textin.npy'
            destination_path = os.path.join(destination, new_name)
            np.save(destination_path, combined_data)
            print(f"Combined file saved as {destination_path}")

            return destination_path
        except Exception as e:
            print(f"Error combining textin: {e}")
            return None
    
    def combine_textout_files(self, raw1: Dataset_Raw, raw2: Dataset_Raw, destination):
        try:
            textout_1 = np.load(raw1.textout_file_path)
            textout_2 = np.load(raw2.textout_file_path)
            combined_data = np.vstack((textout_1, textout_2))

            new_name = str(self.dataset_num)+'_textout.npy'
            destination_path = os.path.join(destination, new_name)
            np.save(destination_path, combined_data)
            print(f"Combined file saved as {destination_path}")

            return destination_path
        except Exception as e:
            print(f"Error combining textout: {e}")
            return None
        
    def combine_keys_files(self, raw1: Dataset_Raw, raw2: Dataset_Raw, destination):
        try:
            text_keys_1 = np.load(raw1.keys_file_path)
            text_keys_2 = np.load(raw2.keys_file_path)
            combined_data = np.vstack((text_keys_1, text_keys_2))

            new_name = str(self.dataset_num)+'_keys.npy'
            destination_path = os.path.join(destination, new_name)
            np.save(destination_path, combined_data)
            print(f"Combined file saved as {destination_path}")

            return destination_path
        except Exception as e:
            print(f"Error combining keys: {e}")
            return None

    def display_info(self):
        print(f"Dataset Number: {str(self.dataset_num)}")
        print(f"Combined Traces path: {self.final_traces_path} and dimensions: rows = {self.traces_rows} and cols = {self.traces_cols}")
        print(f"Combined Textin path: {self.final_textin_path} and dimensions: rows = {self.textin_rows} and cols = {self.textin_cols}")
        print(f"Combined Textout path: {self.final_textout_path} and dimensions: rows = {self.textout_rows} and cols = {self.textout_cols}")
        print(f"Combined Keys path: {self.final_keys_path} and dimensions: rows = {self.keys_rows} and cols = {self.keys_cols}")
        print(f"Combined Key Array: {self.key_array}")
        print(f"Combined Key String: {self.key_string}")
        print(f"Combined Key json path: {self.final_keys_json_path}")
        


    
    def get_display_info(self):
        info = []
        info.append(f"Dataset Number: {str(self.dataset_num)}")
        info.append(f"Combined Traces path: {self.final_traces_path} and dimensions: rows = {self.traces_rows} and cols = {self.traces_cols}")
        info.append(f"Combined Textin path: {self.final_textin_path} and dimensions: rows = {self.textin_rows} and cols = {self.textin_cols}")
        info.append(f"Combined Textout path: {self.final_textout_path} and dimensions: rows = {self.textout_rows} and cols = {self.textout_cols}")
        info.append(f"Combined Keys path: {self.final_keys_path} and dimensions: rows = {self.keys_rows} and cols = {self.keys_cols}")
        info.append(f"Combined Key Array: {self.key_array}")
        info.append(f"Combined Key String: {self.key_string}")
        info.append(f"Combined Key path: {self.final_keys_path}")
        return "\n".join(info)

    def check_traces_cols_and_rows(self):
        traces_data = np.load(self.final_traces_path)
        self.traces_rows = traces_data.shape[0]
        self.traces_cols = traces_data.shape[1]
    
    def check_textin_cols_and_rows(self):
        textin_data = np.load(self.final_textin_path)
        self.textin_rows = textin_data.shape[0]
        self.textin_cols = textin_data.shape[1]

    def check_textout_cols_and_rows(self):
        textout_data = np.load(self.final_textout_path)
        self.textout_rows = textout_data.shape[0]
        self.textout_cols = textout_data.shape[1]

    def check_keys_cols_and_rows(self):
        keys_data = np.load(self.final_textout_path)
        self.keys_rows = keys_data.shape[0]
        self.keys_cols = keys_data.shape[1]

    def normalize_and_save_npy(self):
        try:
            # loading the .npy
            data = np.load(self.final_traces_path)
            scaler = MinMaxScaler(feature_range=(-100, 100))
            normalized_data = scaler.fit_transform(data)

            # Saving the normalized data into a file
            np.save(self.final_traces_path, normalized_data)

            print(f"Data normalized and saved in {self.final_traces_path}")
        except Exception as e:
            print(f"Error loading or saving the file after normalization: {e}")

    def save_keys_to_json(self):
        keys_data = {
            "key_string": self.key_string,
            "key_array": self.key_array.tolist()  # Convertir a lista si es un numpy array
        }
        json_path = os.path.join(self.destination_path, f"{self.dataset_num}_keys.json")
        try:
            with open(json_path, 'w') as json_file:
                json.dump(keys_data, json_file, indent=4)
            print(f"Keys saved to {json_path}")
            return json_path
        except Exception as e:
            print(f"Error saving keys to JSON: {e}")