import sys
import os
from dotenv import load_dotenv
from utils.telegram_notification import telegram_notification


load_dotenv()

aisy_path = os.getenv("AISY_PATH")
sys.path.append(os.path.abspath(aisy_path))

import aisy_sca
from app import *
from custom.custom_models.neural_networks import *
import json


datasets_root_folder = os.getenv("DATASETS_ROOT_FOLDER")
resources_root_folder = os.getenv("RESOURCES_ROOT_FOLDER")
databases_root_folder = os.getenv("DATABASES_ROOT_FOLDER")

config_file_folder = os.getenv("CONFIG_FILE_FOLDER")

data_type = os.getenv("data_type")


max_dataset_num = 5

telegram_notification(f"The program has started")
for i in range(0, max_dataset_num):
    # Leer el contenido del archivo txt
    with open(config_file_folder+'/config_dataset_file_'+str(i)+'_FPGA.txt', 'r') as file:
        data = file.read()

    # Convertir el contenido leído de string a diccionario
    dataset_configuration = json.loads(data)

    # Verificar el contenido de la variable
    print(dataset_configuration)

    # AISY SCA configuration
    telegram_notification(f"The program is in dataset number {i}")
    for byte in range(0,16):#range of bits 0-16:
        telegram_notification(f"The program is in byte number {byte}")
        try:
            aisy = aisy_sca.Aisy()
            aisy.set_resources_root_folder(resources_root_folder)
            aisy.set_database_root_folder(databases_root_folder)
            aisy.set_datasets_root_folder(datasets_root_folder)
            aisy.set_database_name(f"database_{data_type}_hyper_selec_random_search_mlp.sqlite")
            aisy.set_dataset(dataset_configuration)
            aisy.set_aes_leakage_model(leakage_model='ID', byte=byte)
            
            random_search = {
                "neural_network": "mlp",
                "hyper_parameters_search": {
                    'layers': {"min": 2, "max": 5, "step": 1},
                    'neurons_per_layer': {"min": 64, "max": 256, "step": 64},
                    'learning_rate': [0.005, 0.001, 0.0005, 0.0001],
                    'activation': ["relu", "tanh", "sigmoid"],
                    'epochs': {"min": 10, "max": 50, "step": 10},
                    'batch_size': {"min": 100, "max": 300, "step": 50},
                    'optimizer': ["Adam", "RMSprop", "SGD"]
                },
                "structure": {
                    "use_pooling_after_convolution": False,  # only for CNNs
                    "use_pooling_before_first_convolution": False, # only for CNNs
                    "use_pooling_before_first_dense": False, 
                    "use_batch_norm_after_pooling": False,
                    "use_batch_norm_before_pooling": False,
                    "use_batch_norm_after_convolution": False, # only for CNNs
                    "use_dropout_after_dense_layer": False,
                    "use_dropout_before_dense_layer": False,
                },
                "metric": "accuracy",
                "stop_condition": False,
                "stop_value": 1.0,
                "max_trials": 10,
                "train_after_search": True
            }

            aisy.run(random_search=random_search)

        except Exception as e:
            telegram_notification(f"Error in byte: {byte}")
            print("------> ERROR: ", str(e))


telegram_notification(f"The program has finished")
