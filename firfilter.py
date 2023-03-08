
import pylab as pl
import numpy as np


'''
description: generate highpass filter coefficients
param {fs}  sampling rate
param {fc}  cutoff frequencies
param {ntaps}  number of taps
return {h}  FIR filter coefficients
'''
def highpassDesign(fs,fc,ntaps) :
    h_temp = np.ones(ntaps)
    fc_point = int((fc/fs)*ntaps)
    h_temp[0:fc_point+1] = 0
    h_temp[ntaps-fc_point:ntaps+1] = 0

    h_temp = np.fft.ifft(h_temp)
    h_temp = np.real(h_temp)
    h = np.zeros(ntaps)
    # shift
    h[0:int(ntaps/2)] = h_temp[int(ntaps/2):ntaps]
    h[int(ntaps/2):ntaps] = h_temp[0:int(ntaps/2)]
    # pl.figure(1)
    # pl.plot(h)
    # pl.title("coefficients of highpass filter")
    return h
'''
description: generate bandstop filter coefficients
param {fs}  sampling rate
param {fc}  cutoff frequencies
param {ntaps}  number of taps
return {h}  FIR filter coefficients
'''
def bandstopDesign(fs,fc,ntaps):
    h_temp = np.ones(ntaps)
    fc_poit = int((fc/fs)*ntaps)
    h_temp[fc_poit-5:fc_poit+5] = 0
    h_temp[ntaps-(fc_poit+5):ntaps-(fc_poit-5)+1] = 0
    h_temp = np.fft.ifft(h_temp)
    h_temp = np.real(h_temp)
    h = np.zeros(ntaps)
    # shift
    h[0:int(ntaps/2)] = h_temp[int(ntaps/2):ntaps]
    h[int(ntaps/2):ntaps] = h_temp[0:int(ntaps/2)]
    # add window
    h = h*np.blackman(ntaps)
    # pl.figure(2)
    # pl.plot(h)
    # pl.title("coefficients of bandstop filter")
    return h

'''
description: generate highpass and bandstop filter coefficients
param {fs}  sampling rate
param {fc}  cutoff frequencies
param {ntaps}  number of taps
return {h}  FIR filter coefficients
'''
def HighpassBandstopDesign(fs,fhpc,fbsc,ntaps):
    h_temp = np.ones(ntaps)
    # create highpass filter 
    fhpc_point = int((fhpc/fs)*ntaps)
    h_temp[0:fhpc_point+1] = 0
    h_temp[ntaps-fhpc_point:ntaps+1] = 0
    # create bandstop filter
    fbsc_poit = int((fbsc/fs)*ntaps)
    h_temp[fbsc_poit-5:fbsc_poit+5] = 0
    h_temp[ntaps-(fbsc_poit+5):ntaps-(fbsc_poit-5)+1] = 0

    h_temp = np.fft.ifft(h_temp)
    h_temp = np.real(h_temp)
    h = np.zeros(ntaps)
    # shift
    h[0:int(ntaps/2)] = h_temp[int(ntaps/2):ntaps]
    h[int(ntaps/2):ntaps] = h_temp[0:int(ntaps/2)]
    return h


class FIRfilter:
    '''
    description: 
    param {self}
    param {_coefficients} H(n)
    '''
    def __init__(self,_coefficients):
        self._coefficients = _coefficients
        self.buf_value=np.array([])

    '''
    description: stantard realtime filter
    param  self
    param {v} realtime input(scalar)
    return {result} realtime output(scalar)
    '''
    def dofilter(self,v):
        result=0.0
        
        # construct the analyse buffer
        if len(self.buf_value) == len(self._coefficients):
            self.buf_value = self.buf_value[1:len(self.buf_value)]
        self.buf_value=np.append(self.buf_value,v)

        # Y(n) = X(n)*H(n)
        for i in range(0,len(self.buf_value)):
            result=result + self._coefficients[i] * self.buf_value[len(self.buf_value)-1-i]

        return result

    '''
    description: inialise the buffer
    param {*} self
    '''
    def init_buffer(self):
        self.buf_value=np.array([])
        return


class lmsFilter:
    def __init__(self,_coefficients):
        self.ntaps=len(_coefficients)
        self.coefficients = _coefficients
        self.buffer = np.zeros(self.ntaps)

    '''
    description: lms filter
    param {self} 
    param {signal} signal to be filtered (scalar)
    param {noise} Noise signal of specified frequency (scalar)
    param {learning_rate}
    return {output_signal}  realtime output(scalar)
    '''
    def doFilterAdaptive(self,signal,noise,learning_rate):
        output_signal=0.0
        # standard filter the noise
        canceller=self.filter(noise)
        # e(n) = d(n) - y(n)
        output_signal=signal-canceller
        # update the codfficients
        self.lms(output_signal,learning_rate)
        return output_signal

    '''
    description: standard filter
    param {self} 
    param {signal} signal to be filtered (scalar)
    return {output_signal}  realtime output(scalar)
    '''
    def filter(self,signal):
        # create delay array
        for i in range(self.ntaps-1):
            self.buffer[self.ntaps-1] = self.buffer[self.ntaps-i-2]
        self.buffer[0]=signal

        # Y(n) = X(n)*H(n)
        result = 0.0
        for i in range(self.ntaps):
            result= result+self.buffer[i]*self.coefficients[i]
        return result

    '''
    description: update the coeffecient
    param {self} 
    param {error} e(n) error signal
    param {mu} learning rate
    '''
    def lms(self,error,mu):
        for j in range(self.ntaps):
            self.coefficients[j] = self.coefficients[j]+error*mu*self.buffer[j]


# test code(Q1):
# def main():
#     fs = 250
#     fhpc = 5
#     fbsc = 50
#     ntaps = 100

#     # generate hightpass FIR filter coefficients
#     highPass_filter=highpassDesign(fs,fhpc,ntaps)
#     # generate bandstop FIR filter coefficients
#     bandstop_filter=bandstopDesign(fs,fbsc,ntaps)
#     pl.show()

# if __name__ == '__main__':
#     main()
