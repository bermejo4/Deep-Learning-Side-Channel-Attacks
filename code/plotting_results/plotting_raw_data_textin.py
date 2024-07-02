import numpy as np
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

def convert_to_16bit(data):
    data_flat = data.ravel()
    if len(data_flat) % 2 != 0:
        data_flat = data_flat[:-1]
    data_16bit = []
    for i in range(0, len(data_flat), 2):
        bin_str = f'{data_flat[i]:08b}' + f'{data_flat[i+1]:08b}'
        data_16bit.append(int(bin_str, 2))
    return data_16bit


data_1 = np.load('../../data/good_ecg/datasets_ready/0_textin.npy')
data_2 = np.load('../../data/bad_ecg/datasets_ready/0_textin.npy')
data_3 = np.load('../../data/regular_ecg/datasets_ready/0_textin.npy')
data_4 = np.load('../../data/random_data_not_ecg/datasets_ready/0_textin.npy')

data_lenth = 30000
data_16bit_1 = convert_to_16bit(data_1)[:data_lenth]
data_16bit_2 = convert_to_16bit(data_2)[:data_lenth]
data_16bit_3 = convert_to_16bit(data_3)[:data_lenth]
data_16bit_4 = convert_to_16bit(data_4)[:data_lenth]

fig, axs = plt.subplots(4, 1, figsize=(15, 10), sharex=True)

axs[0].plot(data_16bit_1, label='Good ECG Data')
axs[0].set_ylabel('Value 16 bits')
axs[0].set_title('Good ECG Data')
axs[0].legend()

axs[1].plot(data_16bit_2, label='Bad ECG Data')
axs[1].set_ylabel('Value 16 bits')
axs[1].set_title('Bad ECG Data')
axs[1].legend()

axs[2].plot(data_16bit_3, label='Regular ECG Data')
axs[2].set_ylabel('Value 16 bits')
axs[2].set_title('Regular ECG Data')
axs[2].legend()

axs[3].plot(data_16bit_4, label='Random Data Not ECG')
axs[3].set_xlabel('Samples')
axs[3].set_ylabel('Value 16 bits')
axs[3].set_title('Random Data Not ECG')
axs[3].legend()

plt.tight_layout()
plt.show()