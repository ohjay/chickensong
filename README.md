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

Using the following command, you can download "clucking" and "crowing" noises according to the AudioSet unbalanced train split ([download](https://research.google.com/audioset/download.html)):
```
python3 dl_train_segments.py unbalanced_train_segments.csv --out_dir /media/owen/ba9d40b5-89de-4832-bad4-156b118e4a66/chickens
```

Briefly describe the files that are included with your repository:
- trained models
- training data (or link to training data)

## Code

Your code for generating your project:
- Python: generative_code.py
- Jupyter notebooks: generative_code.ipynb

## Results

Documentation of your results in an appropriate format, both links to files and a brief description of their contents:
- `.wav` files or `.mp4`

Bonus: chickenspeech (perform voice cloning on a chicken).

## Technical Notes

- The code runs on Ubuntu 18.04 with Python 3.6.8.
- It requires PyTorch, librosa, SciPy, tqdm, etc. Nothing too unusual.

## References

- Papers
  - [A Universal Music Translation Network](https://arxiv.org/pdf/1805.07848.pdf)
- Repositories
  - [`music-translation`](https://github.com/facebookresearch/music-translation)
- Datasets
  - [AudioSet](https://research.google.com/audioset)
