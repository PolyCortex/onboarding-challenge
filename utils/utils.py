from pylsl import StreamInlet, resolve_byprop
from muselsl.constants import LSL_SCAN_TIMEOUT, LSL_EEG_CHUNK
from time import time
from collections import OrderedDict
from csv import reader


def read_eeg_file(csv_file_path):
    eeg_data = OrderedDict()

    with open(csv_file_path, newline='') as eeg_file:
        csv_reader = reader(eeg_file, delimiter=',')
        eeg_data = OrderedDict({key:[] for key in next(csv_reader)})  # Use the headers as key of eeg_data dict
        for samples in csv_reader:
            for i, key in enumerate(eeg_data.keys()):
                eeg_data[key].append(float(samples[i])) # Add the sample to its channel list
    
    return eeg_data


def debounce_signal(signal, debouncing_time=0.1, period=1/256):
    rising_edges = []
    falling_edges = []
    last_value = signal[0]

    # Find the edge indexes.
    for i, data in enumerate(signal):
        if data is not last_value:
            if last_value:
                falling_edges.append(i)
            else:
                rising_edges.append(i)
        last_value = data

    for i in falling_edges:
        next_rising_edge = next((index for index in rising_edges if index > i), None)
        if next_rising_edge is None:
            break
        
        # If the next rising edge is within the debouncing period, then set the blink signal to 1.
        falling_to_rising_idx_span = next_rising_edge - i
        if falling_to_rising_idx_span * period < debouncing_time:
            signal[i: next_rising_edge] = [True] * falling_to_rising_idx_span
    return signal


def print_eeg_callback(timestamps, eeg_data):
    for i, data in enumerate(eeg_data):
        print(timestamps[i], data)


def acquire_eeg(duration, callback=print_eeg_callback, eeg_chunck=LSL_EEG_CHUNK):

    DATA_SOURCE = "EEG"

    print("Looking for a %s stream..." % (DATA_SOURCE))
    streams = resolve_byprop('type', DATA_SOURCE, timeout=LSL_SCAN_TIMEOUT)

    if len(streams) == 0:
        print("Can't find %s stream." % (DATA_SOURCE))
        return

    print("Started acquiring data.")
    inlet = StreamInlet(streams[0], max_chunklen=eeg_chunck)

    info = inlet.info()
    description = info.desc()
    Nchan = info.channel_count()

    ch = description.child('channels').first_child()
    ch_names = [ch.child_value('label')]
    for i in range(1, Nchan):
        ch = ch.next_sibling()
        ch_names.append(ch.child_value('label'))

    timestamps = []
    t_init = time()
    time_correction = inlet.time_correction()

    print('Start acquiring at time t=%.3f' % t_init)
    print('Time correction: ', time_correction)

    while (time() - t_init) < duration:
        try:
            chunk, timestamps = inlet.pull_chunk(timeout=1.0,
                                                 max_samples=eeg_chunck)

            if timestamps:
                samples = {key: [sample[i] for sample in chunk] for i, key in enumerate(ch_names)}
                callback(timestamps, samples)
        except KeyboardInterrupt:
            break

    print('Acquisition is done')
