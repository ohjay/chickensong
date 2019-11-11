import os
import numpy as np
import argparse
import subprocess
from tqdm import tqdm
from scipy.io import wavfile

"""
A slight variation on
https://gist.github.com/rudolfbyker/8fc0d99ecadad0204813d97fee2c6c06.

Removes silences from a WAV file (instead of just splitting the WAV file).
"""

# Utility functions

def windows(signal, step_size):
    if type(step_size) is not int:
        raise AttributeError('Step size must be an integer.')
    for i_start in range(0, len(signal), step_size):
        i_end = min(i_start + step_size, len(signal))
        yield signal[i_start:i_end]

def energy(samples):
    return np.sum(np.power(samples, 2.0)) / float(len(samples))

# Main function

def remove_silences(input_filepath, overwrite, out_dir, step_duration, silence_threshold):
    sample_rate, samples = wavfile.read(filename=input_filepath, mmap=True)

    max_amplitude = np.iinfo(samples.dtype).max
    max_energy = energy([max_amplitude])

    step_size = int(step_duration * sample_rate)

    signal_windows = windows(
        signal=samples,
        step_size=step_size
    )

    window_energy = (energy(w) / max_energy for w in tqdm(
        signal_windows,
        total=int(len(samples) / float(step_size))
    ))

    window_silence = (e > silence_threshold for e in window_energy)

    processed_samples = []
    for index, keep in enumerate(window_silence):
        if keep:
            start = int(index * step_duration * sample_rate)
            stop = int((index + 1) * step_duration * sample_rate)
            processed_samples.append(samples[start:stop])

    if len(processed_samples) > 0:
        processed_samples = np.concatenate(processed_samples)

        if overwrite:
            output_filepath = input_filepath
        else:
            output_basename = os.path.basename(input_filepath)[:-4] + '_wo_silence.wav'
            output_filepath = os.path.join(os.path.dirname(input_filepath), output_basename)

        if out_dir:
            output_filepath = os.path.join(out_dir, os.path.basename(output_filepath))
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)

        print('Writing file {}'.format(output_filepath))
        wavfile.write(
            filename=output_filepath,
            rate=sample_rate,
            data=processed_samples
        )
    elif overwrite:
        # remove original, since it's 100% "silent"
        subprocess.check_output(['rm', input_filepath])

# Process command line arguments

if __name__ == '__main__':
    t_help = 'The energy level (between 0.0 and 1.0) below which ' + \
             'the signal is regarded as silent. Defaults to 0.5%.'
    s_help = 'The amount of time to step forward in the input file after calculating ' + \
             'energy. Smaller value = slower, but more fine-grained silence detection.'

    parser = argparse.ArgumentParser(description='Remove silences from a WAV file.')
    parser.add_argument('input_file', type=str, help='The WAV file to process.')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite the input file.')
    parser.add_argument('--out_dir', type=str, help='(Optional) Output directory.')
    parser.add_argument('--silence_threshold', '-t', type=float, default=0.002, help=t_help)
    parser.add_argument('--step_duration',     '-s', type=float, default=0.1,   help=s_help)
    args = parser.parse_args()

    input_filepath = args.input_file
    overwrite = args.overwrite
    out_dir = args.out_dir
    step_duration = args.step_duration
    silence_threshold = args.silence_threshold

    print('Removing {}-second chunks with energy below {}%.'.format(
        step_duration,
        silence_threshold * 100.0
    ))

    remove_silences(input_filepath, overwrite, out_dir, step_duration, silence_threshold)
