import h5py
import numpy as np
import json
import os
from dotenv import load_dotenv



profiling_percent = 0.9

load_dotenv()
dataset_path = os.getenv("DATASETS_READY_FOLDER")
print(f"dataset_path = {dataset_path}")
results_splitted_path = os.getenv("DATASETS_PRE_GENERATE")
params_folder_path = os.getenv("PARAMS_FOLDER")
config_folder_path = os.getenv("CONFIG_FILE_FOLDER")
post_generate_folder_path = os.getenv("DATASETS_POST_GENERATE")

#solo para gcp:
# post_generate_folder_path_gcp = "/home/jaimebermejotorres/h5-datasets-to-gcp/datasets"
post_generate_folder_path_gcp = post_generate_folder_path

num_of_datasets = 5

#loading data:
for i in range(0, num_of_datasets):
    traces = np.load(dataset_path+'/'+str(i)+'_traces.npy')
    plaintext = np.load(dataset_path+'/'+str(i)+'_textin.npy')
    ciphertext = np.load(dataset_path+'/'+str(i)+'_textout.npy')
    key = np.load(dataset_path+'/'+str(i)+'_keys.npy')
    with open(str(dataset_path+'/'+str(i)+'_keys.json'), 'r') as json_file:
        keys_data = json.load(json_file)
        key_hexa = keys_data['key_string']

    # 0s mask generation
    masks = np.zeros((plaintext.shape[0], 16), dtype=np.uint8)
    
    dtype = np.dtype([
        ('plaintext', 'u1', (16,)), 
        ('ciphertext', 'u1', (16,)), 
        ('key', 'u1', (16,)), 
        ('masks', 'u1', (16,))
    ])

    # dtype = np.dtype([('plaintext', 'u1', (16,)), ('ciphertext', 'u1', (16,)), ('key', 'u1', (16,))])
    # metadata_combined = np.rec.fromarrays([plaintext, ciphertext, key], dtype=dtype)
    
    metadata_combined = np.rec.fromarrays([plaintext, ciphertext, key, masks], dtype=dtype)


    with h5py.File(str(results_splitted_path+'/'+str(i)+'_FPGA_dataset_pre.h5'), 'w') as h5_file:
        h5_file.create_dataset('metadata', data=metadata_combined, dtype=dtype)
        h5_file.create_dataset('traces', data=traces, dtype=np.int8)

    splitting = int(traces.shape[0]*profiling_percent)
    print("\n--------------------------------------")
    print(f"Generating params file corresponding to dataset number {i}:")
    data = """{{
    "traces_file" : "{3}/{0}_FPGA_dataset_pre.h5",
    "labeled_traces_file" : "{4}/{0}_FPGA_dataset_post.h5",
    "profiling_index" : [n for n in range(0,{1})],
    "attack_index" : [n for n in range({1},{2})],
    "target_points" : [n for n in range(0,129)],
    "profiling_desync" : 0,
    "attack_desync" : 0
    }}""".format(i, splitting, str(traces.shape[0]), results_splitted_path, post_generate_folder_path)
    params_file_name = '/generate_params_'+str(i)+'_FPGA'
    with open(params_folder_path+params_file_name, 'w') as f:
        f.write(data)
    
    print("\n--------------------------------------")
    print(f"Generating config dataset file corresponding to dataset number {i}:")
    dataset = """{{
        "filename": "{5}/{0}_FPGA_dataset_post.h5",
        "key": "{1}",
        "first_sample": 0,
        "number_of_samples": {2},
        "number_of_profiling_traces": {3},
        "number_of_attack_traces": {4}
    }}""".format(i, key_hexa, str(traces.shape[1]), splitting, str(abs(traces.shape[0]-splitting)), post_generate_folder_path_gcp)
    config_file_name = '/config_dataset_file_'+str(i)+'_FPGA.txt'
    with open(config_folder_path+config_file_name, 'w') as f:
        f.write(dataset)
    print(dataset)
    print("--------------------------------------\n")
