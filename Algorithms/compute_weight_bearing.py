import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import time
from scipy.signal import medfilt, butter, filtfilt, lfilter,sosfilt,sosfiltfilt, find_peaks, find_peaks_cwt,resample
import statistics
from pyquaternion import Quaternion


# separate generic functions like build_filter and filter

# vars

def build_filter(frequency, sample_rate, filter_type, filter_order):
    nyq = 0.5 * sample_rate

    if filter_type == "bandpass":
        nyq_cutoff = (frequency[0] / nyq, frequency[1] / nyq)
        b, a = butter(filter_order, (frequency[0], frequency[1]), btype=filter_type, analog=False, output='ba', fs=sample_rate)
    elif filter_type == "low":
        print("low pass", frequency[1], sample_rate)
        nyq_cutoff = frequency[1] / nyq
        b, a = butter(filter_order, frequency[1], btype=filter_type, analog=False, output='ba', fs=sample_rate)
    else:
        nyq_cutoff = frequency / nyq

    return b,a

def filter_signal(b, a, signal, filter):
    if(filter=="lfilter"):
        return lfilter(b, a, signal)
    elif(filter=="filtfilt"):
        return filtfilt(b, a, signal)
    #elif(filter=="sos"):
    #    return sosfiltfilt(sos, signal)



# individual axis filter
def filter_acceleration(packet_count, ap_accel_data, vert_accel_data, ml_accel_data, b,a,):

    #def filter_signal(b, a, sos, signal, filter)
    vert_filtered = filter_signal(b,a, vert_accel_data, "filtfilt")
    ap_filtered = filter_signal(b,a,  ap_accel_data, "filtfilt")
    ml_filtered = filter_signal(b,a, ml_accel_data, "filtfilt")

    return vert_filtered, ap_filtered, ml_filtered


def compute_fft_mag(data):
    fftpoints = int(math.pow(2, math.ceil(math.log2(len(data)))))
    fft = np.fft.fft(data, n=fftpoints)
    mag = np.abs(fft) / (fftpoints/2)
    return mag.tolist()


def compute_loading_intensity_and_reaction_force(fft_magnitudes, sampling_frequency, high_cut_off):
    fftpoints = int(math.pow(2, math.ceil(math.log2(len(fft_magnitudes)))))
    LI = 0
    RF = 0
    fs = sampling_frequency
    fc = high_cut_off
    kc = int((fftpoints/fs)* fc) + 1

    magnitudes = fft_magnitudes

    f = []
    for i in range(0, int(fftpoints/2)+1):
        f.append((fs*i)/fftpoints)

    for k in range(0, kc):
        LI = LI + (magnitudes[k] * f[k])
        RF = RF + (magnitudes[k])

    return LI, RF


def extract_accleration_from_window(samples):
    print(len(samples))
    x = []
    y = []
    z = []
    time_idx = []

    for idx, s in enumerate(samples):
        x.append(s[5] / 9.80665)
        y.append(s[6] / 9.80665) 
        z.append(s[7] / 9.80665) 
        time_idx.append(idx)

    return  time_idx, np.array(x), np.array(y), np.array(z)

def vector_magnitude(vectors):
    n = len(vectors[0])
    assert all(len(v) == n for v in vectors), "Vectors have different lengths"
    vm = np.sqrt(sum(v ** 2 for v in vectors))
    return vm

low_cut_off_frequency = 0.1
high_cut_off_frequency = 6
sampling_rate = 60
filter_order = 5

def compute_weight_bearing_for_window(raw_samples, sample_rate):
    time_idx, x, y, z = extract_accleration_from_window(raw_samples)
    a_mag = vector_magnitude([x,y,z])
    b, a = build_filter((low_cut_off_frequency, high_cut_off_frequency), sampling_rate, 'bandpass', filter_order)
    a_mag_filtered = filter_signal(b,a, a_mag, "filtfilt")
    fft_mag = compute_fft_mag(a_mag_filtered)
    LI, RF = compute_loading_intensity_and_reaction_force(fft_mag, sampling_rate, high_cut_off_frequency)
    print(LI)
    return LI, RF

def process_data_in_window( data, data_rate, result_queue):
    print("process data for loading intensity now")
    LI, RF = compute_weight_bearing_for_window(data, data_rate)
    result_queue.put({"LI":LI, "RF": RF })
   