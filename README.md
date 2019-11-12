# Project 2: Generative Audio

Owen Jow, owen@eng.ucsd.edu

## Abstract

In this project, I perform a musical "style transfer" from arbitrary audio to the same audio performed by chickens. I follow the approach of [A Universal Music Translation Network](https://arxiv.org/pdf/1805.07848.pdf) by Mor et al., which trains and uses a single WaveNet encoder in tandem with multiple WaveNet decoders, with one decoder for each "style" of audio. The encoder takes raw audio and embeds it in a latent space, and each decoder takes the latent embedding and recreates the audio in the timbre of whatever it was trained on. The authors provide code for their project [here](https://github.com/facebookresearch/music-translation), which I have of course hijacked.

I train a decoder on chicken noises, which I obtain from random YouTube videos that I found myself. Originally I planned to use Google's AudioSet dataset, which indicates clips from YouTube videos containing sounds corresponding to different categories. (Conveniently, one of those categories happens to be "[chickens](https://research.google.com/audioset/dataset/chicken_rooster.html)/[roosters](https://research.google.com/audioset/ontology/chicken_rooster.html).") However, I found that these clips were too noisy and full of other, non-chicken utterances. I use Beethoven piano music from [MusicNet](https://homes.cs.washington.edu/~thickstn/musicnet.html) as the other "style" of audio.

In the interest of time, I take the published pre-trained encoder and freeze it along with the domain confusion network. After all, I am not going to be translating _from_ the chicken domain, only _to_ the chicken domain. In other words, I only train the chicken decoder. I have included the code for this in the `music-translation` submodule.

> _emulate the sounds of chickens, composing them in a way that is at least somewhat melodic to the human ear_

## Future/Alternative Directions

- Another way to generate chicken audio would be to use NSynth to produce chicken timbre conditioned on MIDI note sequences. However, I don't have access to chicken audio that is annotated to the same level as the NSynth dataset. To match the NSynth dataset, I would need truncated squawk clips labeled with note, pitch, and velocity. While I could try to create this using a library such as [`aubio`](https://aubio.org), I don't think I have time for an attempt.
- A baseline generation scheme could involve fitting a fixed representation of chicken crowing to MIDI notes (i.e. a less flexible synthesizer). To keep things simpler, the chicken audio would have fixed velocity. At the risk of being less interesting machine-learning-wise, the fitting scheme could be done according to `aubio` or some kind of small autoregressive model. Or even manually. I imagine that the creators of [this song](https://www.youtube.com/watch?v=IpNgah-e6v4) did things manually, for example.
- [This recent paper](https://arxiv.org/pdf/1811.09620.pdf) might produce superior results, but I don't have time to implement it.
- For this project, I could of course experiment with other domain translations. There exists a vast space of music and music genres that might be translated into chickensong.
- Even with the same method, I expect that the results can be improved with more data and more training.

## Model/Data

- You can download the trained model from [Google Drive](TODO). Place it in the `music-translation/checkpoints` directory. (The resulting folder hierarchy will be `music-translation/checkpoints/chickenNet`.)
- To download and preprocess the data, run `./make_dataset.sh <desired data root>`.
- To download the outdated AudioSet data, get the [unbalanced train split](https://research.google.com/audioset/download.html) and run
```
python3 dl_train_segments.py unbalanced_train_segments.csv --out_dir <raw wav dir>
for fpath in <raw wav dir>/*.wav; do python3 remove_silences.py ${fpath} --overwrite; done
./preprocess_data.sh <raw wav dir> <processed wav dir>
```

## Code

To generate audio, follow the [`music-translation`](https://github.com/chickensong/music-translation) setup instructions. Make sure to download the pre-trained models ([direct link](https://dl.fbaipublicfiles.com/music-translation/pretrained_musicnet.zip)) and place them in the `music-translation/checkpoints` directory. (The resulting folder hierarchy will be `music-translation/checkpoints/pretrained_musicnet`.) Then run
```
cd music-translation
./train_decoder.sh <data root>  # OR download pre-trained model
./sample_chickens.sh <wav to translate>
```

## Quickstart

```
git clone --recursive https://github.com/ohjay/chickensong.git
cd chickensong
```
Follow setup instructions for the `music-translation` submodule, including downloading the pre-trained models (see [Code](https://github.com/ohjay/chickensong#code)). Then, depending on whether or not you are using the pre-trained chicken model, you have two options.

### If using the pre-trained chicken model
Download the chicken model (see [Model/Data](https://github.com/ohjay/chickensong#modeldata)). Then run
```
cd music-translation
./sample_chickens.sh <wav to translate>
```

### If training the model yourself
```
./make_dataset.sh .
cd music-translation
./train_decoder.sh ..
./sample_chickens.sh <wav to translate>
```

## Results

- [**`beethoven_ft_chicken.wav`**](TODO): chicken rendition of a Beethoven string quartet.
- [**`cambini_wind_ft_chicken.wav`**](TODO): chicken rendition of a Cambini wind quintet.

## Bonus: Chickenspeak

I already had the [code for it](https://github.com/ohjay/visual-questioner/blob/master/tts.py) (note: as a cleaned-up fragment of [CorentinJ's excellent voice cloning project](https://github.com/CorentinJ/Real-Time-Voice-Cloning)), so I figured I'd try performing voice cloning on a chicken. This was the result: [**`chickenspeak.wav`**](TODO).

## Technical Notes

- The code runs on Ubuntu 18.04 with Python 3.6.8.
- To get the data, you'll need `youtube-dl`. You can install it with pip.
- Other than that, the requirements are PyTorch, librosa, SciPy, tqdm, etc. Nothing too unusual.

## References

- Papers
  - [A Universal Music Translation Network](https://arxiv.org/pdf/1805.07848.pdf)
- Repositories
  - [`music-translation`](https://github.com/facebookresearch/music-translation)
  - [`Real-Time-Voice-Cloning`](https://github.com/CorentinJ/Real-Time-Voice-Cloning)
- Datasets
  - [AudioSet](https://research.google.com/audioset)
