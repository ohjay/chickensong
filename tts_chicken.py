"""
This code is an updated version of
https://github.com/ohjay/visual-questioner/blob/master/tts.py,
which is essentially a condensed version of
https://github.com/CorentinJ/Real-Time-Voice-Cloning/blob/master/demo_cli.py.
"""

import os
import joblib
import vocoder
import librosa
import argparse
import synthesizer
import numpy as np
from pathlib import Path

vocoder_path = os.path.dirname(list(vocoder.__path__)[0])
synthesizer_path = os.path.dirname(list(synthesizer.__path__)[0])

SYN_MODEL_DIR   = os.path.join(synthesizer_path, 'saved_models', 'logs-pretrained')
VOC_MODEL_FPATH = os.path.join(vocoder_path, 'saved_models', 'pretrained', 'pretrained.pt')

def ttwav(text, embed_fpath):
    """Text-to-WAV."""
    synth = synthesizer.inference.Synthesizer(
        Path(SYN_MODEL_DIR).joinpath('taco_pretrained'), low_mem=False)
    vocoder.inference.load_model(Path(VOC_MODEL_FPATH))
    embed = [joblib.load(embed_fpath)]
    synth.synthesize_spectrograms(['test 1'], embed)

    spec = synth.synthesize_spectrograms([text], embed)[0]
    generated_wav = vocoder.inference.infer_waveform(spec)
    generated_wav = np.pad(
        generated_wav, (0, synth.sample_rate), mode='constant')

    librosa.output.write_wav('generated.wav',
                             generated_wav.astype(np.float32),
                             synth.sample_rate)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('text', type=str)
    parser.add_argument('--embed_fpath', type=str, default='embeddings/chicken.joblib')
    args = parser.parse_args()
    ttwav(args.text, args.embed_fpath)
