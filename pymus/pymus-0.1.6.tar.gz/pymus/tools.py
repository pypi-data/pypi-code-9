__author__ = 'Jakob Abesser'

from scipy.io.wavfile import read
import numpy as np
import wave


class Tools:
    """ Class provides several tools for audio analysis
    """

    def __init__(self):
        pass

    @staticmethod
    def setMissingValues(options, **defaultValues):
        """ Add default values & keys to dictionary if values are not set
        Args:
            options (dict): Arbitrary dictionary (e.g. containing processing options)
            defaultValues (dict): Keyword list with default values to be set if corresponding keys are not set in options dict
        Returns:
            options (dict): Arbitrary dictionary with added default values if required
        """
        for param in defaultValues.keys():
            if param not in options:
                options[param] = defaultValues[param]
        return options

    @staticmethod
    def loadWAV(fnWAV, mono=False):
        """ Function loads samples from WAV file. Both implementations (wave / scipy package) fail for some WAV files 
            hence we combine them.
        Args:
            fnWAV (string): WAV file name
            mono (bool): Switch if samples shall be converted to mono
        Returns:
            samples (np array): Audio samples (between [-1,1]
                                 > if stereo: (2D ndarray with DIM numSamples x numChannels),
                                 > if mono: (1D ndarray with DIM numSamples)
            sampleRate (float): Sampling frequency [Hz]
        """
        try:
            samples, sampleRate = Tools.loadWAVWithScipy(fnWAV)
        except:
            try:
                samples, sampleRate = Tools.loadWAVWithWave(fnWAV)
            except:
                raise Exception("WAV file could neither be opened using Scipy nor Wave!")

        # mono conversion
        if mono:
            if samples.ndim == 2 and samples.shape[1] > 1:
                samples = np.mean(samples, axis=1)

        # scaling
        if np.max(np.abs(samples)) > 1:
            samples = samples.astype(float) / 32768.0

        return samples, sampleRate

    @staticmethod
    def loadWAVWithWave(fnWAV):
        """ Load samples & sample rate from WAV file """
        fp = wave.open(fnWAV)
        num_channels = fp.getnchannels()
        num_frames = fp.getnframes()
        frame_string = fp.readframes(num_frames*num_channels)
        data = np.fromstring(frame_string, np.int16)
        samples = np.reshape(data, (-1, num_channels))

        sample_rate = float(fp.getframerate())
        return samples, sample_rate

    @staticmethod
    def loadWAVWithScipy(fnWAV):
        """ Load samples & sample rate from WAV file """
        inputData = read(fnWAV)
        samples = inputData[1]
        sampleRate = inputData[0]
        return samples, sampleRate

    @staticmethod
    def aggregate_framewise_function_over_notes(framewiseFunction, timeSec, onset, duration, **options):
        """ Aggregate a frame-wise function (e.g. loudness) over note durations to obtain note-wise features
        :param framewiseFunction: (ndarray) Frame-wise function values
        :param timeSec: (ndarray) Time frame values in seconds
        :param onset: (ndarray) Note onset times in seconds
        :param duration: (ndarray) Note durations in seconds
        :return: result: (dict of ndarrays) Note-wise aggregation results with keys
                    'max': Maximum over note duration
                    'median': Median over note duration
                    'std': Standard deviation over note duration
                    'tempCentroid': Temporal centroid over note duration [0,1]
                    'relPeakPos': Position of global maximum over note duration relative to note duration [0,1]
        """
        options = Tools.setMissingValues(options,
                                         storeAsList=False)
        dt = timeSec[1]-timeSec[0]
        nNotes = len(onset)

        onsetFrame = np.array([round(onset[_]/dt) for _ in range(nNotes)], dtype=int)
        offsetFrame = np.array([round((onset[_] + duration[_])/dt) for _ in range(nNotes)], dtype=int)

        result = dict()
        result['max'] = np.zeros(nNotes)
        result['median'] = np.zeros(nNotes)
        result['std'] = np.zeros(nNotes)
        result['tempCentroid'] = np.zeros(nNotes)
        result['relPeakPos'] = np.zeros(nNotes)

        for n in range(nNotes):
            noteLoudnessFrames = framewiseFunction[onsetFrame[n]:offsetFrame[n]+1]
            nFramesCurr = len(noteLoudnessFrames)
            result['max'][n] = np.max(noteLoudnessFrames)
            result['median'][n] = np.median(noteLoudnessFrames)
            result['std'][n] = np.std(noteLoudnessFrames, ddof=1) # same result as in Matlab
            result['tempCentroid'][n] = np.sum(np.linspace(0, 1, nFramesCurr)*noteLoudnessFrames)/np.sum(noteLoudnessFrames)
            result['relPeakPos'][n] = float(np.argmax(noteLoudnessFrames))/(nFramesCurr-1)

        if options["storeAsList"]:
            result['max'] = list(result['max'])
            result['median'] = list(result['median'])
            result['std'] = list(result['std'])
            result['tempCentroid'] = list(result['tempCentroid'])
            result['relPeakPos'] = list(result['relPeakPos'])

        return result

    @staticmethod
    def quadratic_interpolation(x):
        """ Peak refinement using quadratic interpolation.
        Args:
            x (ndarray): 3-element numpy array. Central element was identified as local peak before (e.g. using numpy.argmax)
        Returns:
            peak_pos (float): Interpolated peak position (relative to central element)
            peak_val (float): Interpolated peak value
        """
        peak_pos = (x[2] - x[0])/(2*(2*x[1] - x[2] - x[0]))
        peak_val = x[1] - 0.25*(x[0]-x[2])*peak_pos
        return peak_pos, peak_val

    @staticmethod
    def moving_average_filter(x, N=5):
        """ Moving average on a vector
        Args:
            x (ndarray): Input vector
            N (int): Filter length
        Returns
            y (ndarry): Filtered vector
        """
        return np.convolve(x, np.ones((N,))/N, mode='valid')

    @staticmethod
    def acf(x):
        """ Autocorrelation function
        Args:
            x (ndarray): Input function
        Returns:
            acf (ndarray): Autocorrelation
        """
        result = np.correlate(x, x, mode='full')
        return result[result.size/2:]

