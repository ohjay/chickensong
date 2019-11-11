# Project 2: Generative Audio

Owen Jow, owen@eng.ucsd.edu

## Abstract

In this project, I perform a musical "style transfer" from arbitrary audio to the same audio performed by chickens. I follow the approach of [A Universal Music Translation Network](https://arxiv.org/pdf/1805.07848.pdf) by Mor et al., which trains and uses a single WaveNet encoder in tandem with multiple WaveNet decoders, with one decoder for each "style" of audio. The encoder takes raw audio and embeds it in a latent space, and each decoder takes the latent embedding and recreates the audio in the style of whatever it was trained on. The authors provide code for their project [here](https://github.com/facebookresearch/music-translation), which I have of course hijacked.

I train an autoencoder on chicken noises, which I obtain from random YouTube videos that I found myself. Originally I planned to use Google's AudioSet dataset, which indicates clips from YouTube videos containing sounds corresponding to different categories. (Conveniently, one of those categories happens to be "[chickens](https://research.google.com/audioset/dataset/chicken_rooster.html)/[roosters](https://research.google.com/audioset/ontology/chicken_rooster.html).") However, I found that these clips were too noisy and full of other, non-chicken utterances. I use Beethoven piano music from [MusicNet](https://homes.cs.washington.edu/~thickstn/musicnet.html) as the other "style" of audio. I would have liked to experiment with other translations as well, but the model takes eons to train.

> _emulate the sounds of chickens, composing them in a way that is at least somewhat melodic to the human ear_

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
- `.midi` files
- musical scores
- ... some other form

Bonus: chickenspeech (perform voice cloning on a chicken).

## Technical Notes

Any implementation details or notes we need to repeat your work. 
- Does this code require other pip packages, software, etc?
- Does it run on some other (non-datahub) platform? (CoLab, etc.)

## References

References to any papers, techniques, repositories you used:
- Papers
- Repositories
- Blog posts
