from pylsl import StreamInlet, resolve_byprop
from muselsl.constants import LSL_SCAN_TIMEOUT, LSL_EEG_CHUNK
from time import time


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
            data, timestamps = inlet.pull_chunk(timeout=1.0,
                                                max_samples=eeg_chunck)

            if timestamps:
                callback(timestamps, data)
        except KeyboardInterrupt:
            break

    print('Acquisition is done')
