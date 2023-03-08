
from matplotlib.pyplot import tight_layout, title
import numpy as np
import pylab as pl
import firfilter

def sin_generator(A,f,t,fs):
    return A * np.sin(np.linspace(0, f * t * 2 * np.pi , fs* t))

def wavelet_generator():
    # generate P wave
    A=0.1
    f=1/8
    t=12
    fs=1
    wave = sin_generator(A,f,t,fs)
    Pwave = wave[0:8]

    # generate T wave
    A=0.4
    f=1/8
    t=12
    fs=1
    wave = sin_generator(A,f,t,fs)
    TWave = wave[4:12]

    # generate R wave
    A=1
    f=1/16
    t=8
    fs=1
    RWave = sin_generator(A,f,t,fs)

    wavelet=np.zeros(300)
    wavelet[141:149]=Pwave
    wavelet[149:157]=RWave
    wavelet[157:165]=TWave
    return wavelet

def memory_heart_beat_detector(threshold,ecg_data):
    mom_hr_array=np.zeros(len(ecg_data))
    current_peak_sample=0
    current_heart_rate=0
    for i in range(len(ecg_data)):
        if ecg_data[i]<threshold :
            mom_hr_array[i]=current_heart_rate
        if ecg_data[i]>=threshold :
            mom_hr_array[i]=current_heart_rate
            if ecg_data[i+1]<threshold:
                current_heart_rate = 60*fs/(i-current_peak_sample)
                # The heart rate range of normal people is 60 ~ 180, so removal the unnormal heart rate which >180
                if current_heart_rate>180:
                    current_heart_rate = 0
                current_peak_sample=i

    return mom_hr_array

'''
 step 1 get the clean ECG 
'''
data=np.loadtxt("ECG_msc_matric_8.dat")

# paramaters
fs = 250
fhpc = 5
fbsc = 50
ntaps = 100

# generate the coefficients
hpbs_filter=firfilter.HighpassBandstopDesign(fs,fhpc,fbsc,ntaps)

# filter the original data
data_clean = np.zeros(len(data))
fir_ecg=firfilter.FIRfilter(hpbs_filter)
for i in range(0,len(data)):
    data_clean[i]=fir_ecg.dofilter(data[i])

data_clean_scaling=data_clean*(2**16)

'''
step 2 generate the template
'''
R_peak_real = data_clean[400:700]

'''
step 3 generate the wavelets
'''
wavelet = wavelet_generator()

'''
step 4 filter the ecg with the wavelet
'''
data_clean_trfir=np.zeros(len(data_clean))
fir_ecg_tr = firfilter.FIRfilter(wavelet)
for i in range(0,len(data_clean)):
    data_clean_trfir[i]=fir_ecg_tr.dofilter(data_clean[i])
    data_clean_trfir[i]=data_clean_trfir[i]
# scaling the ecg data
data_clean_trfir=data_clean_trfir*(2**16)
data_clean_trfir=data_clean_trfir*data_clean_trfir

'''
step 5 momentory heart beat detector
'''
# find the point which greater than 50
mom_hr_array=memory_heart_beat_detector(2500,data_clean_trfir)
# find the point which greater than 12
mom_hr_array_original_data=memory_heart_beat_detector(12,data_clean_scaling)

################### plot code ##################################################

data_time_normolised=np.linspace(0,len(data)/fs,len(data))
pl.figure(1)
pl.subplot(2,1,1)
pl.step(data_time_normolised,mom_hr_array)
pl.title("momentory heart beat detector(filtered by using wavelet)")
pl.xlabel("time(sec)")
pl.ylabel("heart beat rate(times/min)")

pl.subplot(2,1,2)
pl.title("comparasion")
pl.step(data_time_normolised,mom_hr_array_original_data, label='original_data')
pl.xlabel("time(sec)")
pl.ylabel("heart beat rate(times/min)")

pl.step(data_time_normolised,mom_hr_array,where='post',label='match_filter_ata')
pl.xlabel("time(sec)")
pl.ylabel("heart beat rate(times/min)")

pl.grid(axis='x', color='0.95')
pl.legend(title='Parameter where:')

pl.figure(2)
data_time_normolised=np.linspace(0,len(data)/fs,len(data))
pl.subplot(4,1,1)
pl.plot(data_time_normolised,data_clean)
pl.xlabel("time(sec)")
pl.title("removal 50Hz ,DC and wander line(time domain)")

pl.subplot(4,1,2)
pl.step(data_time_normolised,mom_hr_array_original_data)
pl.title("momentory heart beat detector (detect original data(removal 50Hz ,DC and wander line))")
pl.xlabel("time(sec)")
pl.ylabel("heart beat rate(times/min)")
pl.tight_layout()

pl.subplot(4,1,3)
pl.plot(data_time_normolised,data_clean_trfir)
pl.title("ecg filtered by wavelet ")
pl.xlabel("time(sec)")

pl.subplot(4,1,4)
pl.step(data_time_normolised,mom_hr_array)
pl.title("momentory heart beat detector(filtered by using wavelet)")
pl.xlabel("time(sec)")
pl.ylabel("heart beat rate(times/min)")
pl.tight_layout()

pl.figure(3)
time_template_normelized= np.linspace(400/fs,700/fs,300)
pl.subplot(2,1,1)
pl.title("real R peak")
pl.plot(time_template_normelized,R_peak_real)
pl.xlabel("time(sec)")

pl.subplot(2,1,2)
pl.title("wavelet")
pl.plot(time_template_normelized,wavelet)
pl.xlabel("time(sec)")
pl.tight_layout()

pl.show()