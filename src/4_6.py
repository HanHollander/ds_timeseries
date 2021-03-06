import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import os

from cycler import cycler

CLASSES = {1: 'WALKING',
           2: 'WALKING_UPSTAIRS',
           3: 'WALKING_DOWNSTAIRS',
           4: 'SITTING',
           5: 'STANDING',
           6: 'LAYING'}

wd = os.getcwd()
data_file = wd[:-4].replace(os.sep, "/") + "/data/UCI_HAR_Dataset/train/Inertial_Signals/body_acc_z_train.txt"
label_file = wd[:-4].replace(os.sep, "/") + "/data/UCI_HAR_Dataset/train/y_train.txt"

raw_data_df = pd.read_csv(data_file, sep="\s+", header=None)
label_df = pd.read_csv(label_file, sep="\s+", header=None)

raw_labeled_data = raw_data_df.assign(label=label_df.values)
raw_labeled_data = raw_labeled_data.drop(raw_labeled_data.columns[64:128], axis=1)

original_signal = np.zeros(470528)
for index, row in raw_labeled_data.iterrows():
    eff = index * 64
    original_signal[eff:eff + 64] = row.values[:-1]

sizes = [1226, 1073, 986, 1286, 1373, 1407]
classified_signal = []
for size in sizes:
    classified_signal.append(np.zeros(size))
for i, row in raw_labeled_data.iterrows():
    classified_signal[int(row['label']) - 1] = \
        np.concatenate((classified_signal[int(row['label']) - 1], row.values[:-1]), axis=None)

# PLOT SINE FREQUENCY SPECTRUM

# variables
n = 1000  # number of sample points
dt = 1/200  # sample spacing or 1 / sample rate, for example sample rate is 200 then sample spacing is 1 / 200
max_freq = 60  # filled in manually
nyquist = max_freq < 1 / (2 * dt)  # we need the sample rate to be bigger than two times the maximum frequency

# function
t = np.linspace(0, n * dt, n)
s = np.sin(2 * 2 * np.pi * t) + 0.8 * np.sin(4 * 2 * np.pi * t) + \
    0.5 * np.sin(6 * 2 * np.pi * t) + 0.2 * np.sin(60 * 2 * np.pi * t)

# fast fourier transform
fft = np.fft.fft(s - np.mean(s))  # substract mean to get rid of DC-offset
freq = np.linspace(0, 1 / (2 * dt), n // 2)  # max frequency (by nyquist) is [0, 1 / 2dt] with n / 2 samples

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(freq, 2 / n * np.abs(fft[:n // 2]))
ax.title.set_text('4.6 a) Frequency spectrum of\nsin(4 pi t) + 0,8 sin(8 pi t) + 0,5 sin(12 pit )')
ax.set_xlabel('Frequency')
ax.set_ylabel('Amplitude')
plt.savefig(wd[:-4] + '/img/4_6_sine.png')
print('The frequency spectrum of the sine wave can be found in 4_6_sine.png. This was used to test the implementation.')
print('The variables are: n = 1000, dt = 1/200 (= 1/fs), max_freq = 60 and nyquist = 1/2dt.')
print('The sine is: sin(2 * 2 pi t) + 0.8 sin(4 * 2 pi t) + 0.5 sin(6 * 2 pi t) + 0.2 sin(60 * 2 pi t)')

fig = plt.figure()
fig.suptitle('4.6 a) Frequency spectrum of body_acc_z_train (classified)', size=12)

print('')
print('a)')
print('')
print('\tThe frequency spectra of the signal can be found in 4_6_signal.png, as well as in 4_6_[class].png.')
print('\tThe variables are: n = [length of class data] anddt = 1/50 (= 1/fs).')
for i in range(0, 6):
    signal = classified_signal[i]

    n = len(classified_signal[i])
    dt = 1/50

    fft = np.fft.fft(signal - np.mean(signal))
    freq = np.linspace(0, 1 / (2 * dt), n // 2)

    location = int('32' + str(i + 1))
    ax = fig.add_subplot(location)
    ax.plot(freq, 2 / n * np.abs(fft[:n // 2]))
    ax.title.set_text(CLASSES[i + 1])
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Amplitude')

fig.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(wd[:-4] + '/img/4_6_signal.png')

for i in range(0, 6):
    signal = classified_signal[i]

    n = len(classified_signal[i])
    dt = 1/50

    fft = np.fft.fft(signal - np.mean(signal))
    freq = np.linspace(0, 1 / (2 * dt), n // 2)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(freq, 2 / n * np.abs(fft[:n // 2]))
    ax.title.set_text('4.6 a) Frequency spectrum of ' + CLASSES[i + 1])
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Amplitude')
    plt.savefig(wd[:-4] + '/img/4_6_' + CLASSES[i + 1] + '.png')

print('')
print('b)')
print('')
print('\tAgain, similar to 4.5, we can mostly discriminate between the three walking and the three stationary classes\n'
      '\twhile discriminating between the classes within those categories might be difficult.')
