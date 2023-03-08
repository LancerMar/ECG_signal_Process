
import numpy as np
import firfilter
import pylab as pl


data=np.loadtxt("ECG_msc_matric_8.dat")
data_time_normolised=np.linspace(0,len(data)/250,len(data))

pl.figure(1)
pl.plot(data_time_normolised,data)
pl.title("original data(time domain)")
pl.xlabel("time(sec)")
pl.figure(2)
pl.plot(np.linspace(0,250,len(data)),np.abs(np.fft.fft(data)))
pl.title("original data(Frequency domain)")
pl.xlabel("frequency(Hz)")


numtaps = 100
learning_rate = 0.03
#learning_rate = 0.3
fs = 250


# Construct FIRfilter(all coefficients equals zero)
zero_firfilter=np.zeros(numtaps)
fir=firfilter.lmsFilter(zero_firfilter)

# filter the data
for i in range(0,len(data)):
    # generate the noise (50Hz sin wave)
    noise = np.sin(2.0*np.pi*50*i/fs)
    data[i]=fir.doFilterAdaptive(data[i],noise,learning_rate)


pl.figure(3)
pl.plot(np.linspace(0,fs,len(data)),np.abs(np.fft.fft(data)))
pl.title("lms filter data(Frequency domain)")
pl.xlabel("frequency(Hz)")
pl.figure(4)
pl.plot(data_time_normolised,data)
pl.title("lms filter data(time domain)")
pl.xlabel("time(sec)")
pl.show()