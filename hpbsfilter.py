

import numpy as np
import firfilter
import pylab as pl

# firfilter.highpassDesign(250,5,100)

data=np.loadtxt("ECG_msc_matric_8.dat")

fs = 250
fhpc = 5
fbsc = 50
ntaps = 100

data_time_normolised=np.linspace(0,len(data)/fs,len(data))

pl.figure(1)
pl.plot(data_time_normolised,data)
pl.title("original data time domain")
pl.xlabel("time(sec)")
pl.figure(2)
pl.plot(np.linspace(0,fs,len(data)),np.abs(np.fft.fft(data)))
pl.title("original data Frequency domain")
pl.xlabel("Frequency(Hz)")



bandstop_filter=firfilter.bandstopDesign(fs,fbsc,ntaps)
highPass_filter=firfilter.highpassDesign(fs,fhpc,ntaps)

data_clean = np.zeros(len(data))
fir_ecg_bs=firfilter.FIRfilter(bandstop_filter)
for i in range(0,len(data)):
    data_clean[i]=fir_ecg_bs.dofilter(data[i])

fir_ecg_hp=firfilter.FIRfilter(highPass_filter)
for i in range(0,len(data)):
    data_clean[i]=fir_ecg_hp.dofilter(data_clean[i])


pl.figure(3)
pl.plot(data_time_normolised,data_clean)
pl.title("removal 50Hz ,DC and wander line(time domain)")
pl.xlabel("time(sec)")
pl.figure(4)
pl.plot(np.linspace(0,fs,len(data_clean)),np.abs(np.fft.fft(data_clean)))
pl.title("removal 50Hz ,DC and wander line(frequency domain)")
pl.xlabel("Frequency(Hz)")
pl.show()
