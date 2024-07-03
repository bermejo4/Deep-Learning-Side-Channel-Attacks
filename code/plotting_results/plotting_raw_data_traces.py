import numpy as np
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

def flatting_data(data):
    data_flat = data.ravel()
    return data_flat


data_raw_1 = np.load('../../data/good_ecg/raw_datasets/2024.06.27-15.11.03_0traces.npy')
data_raw_2 = np.load('../../data/regular_ecg/raw_datasets/2024.06.14-09.43.09_0traces.npy')
data_raw_3 = np.load('../../data/bad_ecg/raw_datasets/2024.06.27-15.38.54_0traces.npy')
data_raw_4 = np.load('../../data/random_data_not_ecg/raw_datasets/2024.06.13-07.44.29_0traces.npy')

data_norm_1 = np.load('../../data/good_ecg/datasets_ready/0_traces.npy')
data_norm_2 = np.load('../../data/regular_ecg/datasets_ready/0_traces.npy')
data_norm_3 = np.load('../../data/bad_ecg/datasets_ready/0_traces.npy')
data_norm_4 = np.load('../../data/random_data_not_ecg/datasets_ready/0_traces.npy')

data_lenth = (129*5)
data_raw_1_flat = flatting_data(data_raw_1)[:data_lenth]
data_raw_2_flat = flatting_data(data_raw_2)[:data_lenth]
data_raw_3_flat = flatting_data(data_raw_3)[:data_lenth]
data_raw_4_flat = flatting_data(data_raw_4)[:data_lenth]

data_norm_1_flat = flatting_data(data_norm_1)[:data_lenth]
data_norm_2_flat = flatting_data(data_norm_2)[:data_lenth]
data_norm_3_flat = flatting_data(data_norm_3)[:data_lenth]
data_norm_4_flat = flatting_data(data_norm_4)[:data_lenth]

vertical_lines = [129, (129*2), (129*3), (129*4), (129*5)]  

fig2, axs2 = plt.subplots(4, 1, figsize=(15, 9), sharex=True)

axs2[0].plot(data_raw_1_flat, label='Raw traces')
for xc in vertical_lines:
    axs2[0].axvline(x=xc, color='red', linestyle='-', linewidth=1)
axs2[0].set_ylabel('Value')
axs2[0].set_title('Good ECG Raw Traces')
axs2[0].legend(loc='lower right')

axs2[1].plot(data_norm_1_flat, label='Normalized traces', color='purple')
for xc in vertical_lines:
    axs2[1].axvline(x=xc, color='red', linestyle='-', linewidth=1)
axs2[1].set_ylabel('Value')
axs2[1].set_title('Good ECG Normalized Traces')
axs2[1].legend(loc='lower right')

axs2[2].plot(data_raw_2_flat, label='Raw traces')
for xc in vertical_lines:
    axs2[2].axvline(x=xc, color='red', linestyle='-', linewidth=1)
axs2[2].set_ylabel('Value')
axs2[2].set_title('Regular ECG Raw Traces')
axs2[2].legend(loc='lower right')

axs2[3].plot(data_norm_2_flat, label='Normalized traces', color='purple')
for xc in vertical_lines:
    axs2[3].axvline(x=xc, color='red', linestyle='-', linewidth=1)
axs2[3].set_xlabel('samples')
axs2[3].set_ylabel('Value')
axs2[3].set_title('Regular ECG Normalized Traces')
axs2[3].legend(loc='lower right')

plt.xticks(vertical_lines)
fig2.tight_layout()
plt.show()

fig1, axs1 = plt.subplots(4, 1, figsize=(15, 9), sharex=True)

axs1[0].plot(data_raw_3_flat, label='Raw traces')
for xc in vertical_lines:
    axs1[0].axvline(x=xc, color='red', linestyle='-', linewidth=1)
axs1[0].set_ylabel('Value')
axs1[0].set_title('Bad ECG Raw Traces')
axs1[0].legend(loc='lower right')

axs1[1].plot(data_norm_3_flat, label='Normalized traces', color='purple')
for xc in vertical_lines:
    axs1[1].axvline(x=xc, color='red', linestyle='-', linewidth=1)
axs1[1].set_ylabel('Value')
axs1[1].set_title('Bad ECG Normalized Traces')
axs1[1].legend(loc='lower right')

axs1[2].plot(data_raw_4_flat, label='Raw traces')
for xc in vertical_lines:
    axs1[2].axvline(x=xc, color='red', linestyle='-', linewidth=1)
axs1[2].set_ylabel('Value')
axs1[2].set_title('Random Data Not ECG Raw Traces')
axs1[2].legend(loc='lower right')

axs1[3].plot(data_norm_4_flat, label='Normalized traces', color='purple')
for xc in vertical_lines:
    axs1[3].axvline(x=xc, color='red', linestyle='-', linewidth=1)
axs1[3].set_xlabel('samples')
axs1[3].set_ylabel('Value')
axs1[3].set_title('Random Data Not ECG Normalized Traces')
axs1[3].legend(loc='lower right')

plt.xticks(vertical_lines)
fig1.tight_layout()
plt.show()

