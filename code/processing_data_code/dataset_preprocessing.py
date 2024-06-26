import os
import numpy as np
from dataset_proc_class import Dataset_Proc
from dataset_raw_class import Dataset_Raw
import time
from dotenv import load_dotenv


#Start time:
start_time = time.time()

# source and destination directories
load_dotenv()
source_directory = os.getenv("RAW_DATASETS_FOLDER")
reports_folder = os.getenv("REPORTS_FOLDER")
#destination_directory = os.getenv("DATASETS_READY_FOLDER")


#Global Varaiables
max_num_raw_file = 10
max_num_proc_file = 5
raw_datasets_dict = {}
proc_datasets_dict = {}
pair_key_dict = {}


# Initialicing the dictionary raw
for i in range(0, max_num_raw_file):
    dataset = Dataset_Raw('', '', '', '', dataset_num=i)
    raw_datasets_dict[i] = dataset


# Loading the dataset information
for i in range(0, max_num_raw_file):
    for file in os.listdir(source_directory):
        if file.startswith("._"):
            continue
        if file.endswith(f'_{i}traces.npy'):
            # traces_path = os.path.basename(file)
            # raw_datasets_dict[i].traces_file_path = traces_path
            traces_path = os.path.join(source_directory, file)
            raw_datasets_dict[i].traces_file_path = traces_path
            raw_datasets_dict[i].is_last_row_all_zeros()

        if file.endswith(f'_{i}textin.npy'):
            textin_path = os.path.join(source_directory, file)
            raw_datasets_dict[i].textin_file_path = textin_path

        if file.endswith(f'_{i}textout.npy'):
            textout_path = os.path.join(source_directory, file)
            raw_datasets_dict[i].textout_file_path = textout_path

        if file.endswith(f'_{i}keylist.npy'):
            keylist_path = os.path.join(source_directory, file)
            raw_datasets_dict[i].keys_file_path = keylist_path

        if file.endswith(f'_{i}keylist.npy'):
            file_key_path = os.path.join(source_directory, file)
            data = np.load(file_key_path, allow_pickle=True)
            key_array = data[0]
            print(f"key_array = {key_array}")
            raw_datasets_dict[i].key_array = key_array
            raw_datasets_dict[i].binary_array_to_hex_string()


# Showing the dataset information recopiled
for i in range(0, max_num_raw_file):
    print("----------------------------")
    raw_datasets_dict[i].display_info()
    print("----------------------------")
    print("----------------------------")

#process raw data: remove 0s from traces
for i in range(0, max_num_raw_file):
    #raw_datasets_dict[i].is_last_row_all_zeros()
    tmp_key_to_compare = raw_datasets_dict[i].key_string
    for j in range(0, max_num_raw_file):
        if raw_datasets_dict[i].key_string == raw_datasets_dict[j].key_string and i != j:
            pair_key_dict[i] = j

print(f"pair_dict_key = {pair_key_dict}")


# Create a list keys to remove
keys_to_remove = []

# if the key is bigger than the value must be removed becaused it has been saved previously:
for key, value in pair_key_dict.items():
    if key > value:
        keys_to_remove.append(key)

#removing the keys from the list
for key in keys_to_remove:
    pair_key_dict.pop(key)

print(f"pair_dict_key = {pair_key_dict}")

# Initialicing the dictionary proc
counter = 0
for key, value in pair_key_dict.items():
    dataset = Dataset_Proc(raw_datasets_dict[key], raw_datasets_dict[value], counter)
    proc_datasets_dict[counter] = dataset
    counter = counter + 1

for i in range(0, max_num_proc_file):
    print("----------------------------")
    proc_datasets_dict[i].display_info()
    print("----------------------------")
    print("----------------------------")


## Generating a report about the combination:
filename = reports_folder+"/dataset_preprocessing_report.txt"
with open(filename, 'w') as f:
        f.write("DATASET PREPROCESSING REPORT:\n")
        for i in range(0, max_num_proc_file):
            f.write("----------------------------\n")
            info = proc_datasets_dict[i].get_display_info()
            f.write(info + "\n")
            f.write("----------------------------\n")
            f.write("----------------------------\n")

#Finish Time:
end_time = time.time()

# Computing the interval time
execution_time = end_time - start_time

print(f"Execution time: {execution_time} seconds")