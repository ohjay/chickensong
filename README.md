# Project 2: Generative Audio

Owen Jow, owen@eng.ucsd.edu

## Abstract

I would like to perform a musical "style transfer"
from arbitrary audio to the same audio performed by chickens.
In order to do so, I plan to follow the approach of
[A Universal Music Translation Network](https://arxiv.org/pdf/1805.07848.pdf)
by Mor et al., which trains and uses a single WaveNet encoder
in tandem with multiple WaveNet decoders, with one decoder for each "style" of audio.
The encoder takes raw audio and embeds it in a latent space, and each decoder
takes the latent code and recreates the audio in the style of whatever it was trained on.
The authors provide code [here](https://github.com/facebookresearch/music-translation).

I would train a decoder on chicken noises, which I should be able to obtain from Google's
AudioSet dataset. AudioSet indicates clips from YouTube videos containing sounds of different categories. By chance, one of those categories happens to be
"[chickens](https://research.google.com/audioset/dataset/chicken_rooster.html)/[roosters](https://research.google.com/audioset/ontology/chicken_rooster.html)."
I may use [MusicNet](https://homes.cs.washington.edu/~thickstn/musicnet.html) as an additional source of audio for training.

Ultimately, my goal is to emulate the sounds of chickens and compose them in a way that is somewhat melodic to the human ear.
Since most people probably do not consider "chickensong" melodic, I see this as a challenging and worthy goal.

## Model/Data

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
- `.midi` files
- musical scores
- ... some other form

## Technical Notes

Any implementation details or notes we need to repeat your work. 
- Does this code require other pip packages, software, etc?
- Does it run on some other (non-datahub) platform? (CoLab, etc.)

## References

References to any papers, techniques, repositories you used:
- Papers
- Repositories
- Blog posts
