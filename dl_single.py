import os
import re
import argparse
import youtube_dl
import subprocess

def dl_single(video_url, out_dir, seg_len, min_seg_len, video_cutoff_len):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    ydl_options = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(out_dir, 'temp.wav'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'forceduration': True,
    }
    ffmpeg_cmd_tmpl = 'ffmpeg -i %s -ss %d -to %d %s'  # (in, start_sec, end_sec, out)

    # download wav
    with youtube_dl.YoutubeDL(ydl_options) as ydl:
        meta = ydl.extract_info(video_url, download=True)
    # determine number of existing segments
    segs_written = 0
    for fname in os.listdir(out_dir):
        m = re.match(r'(\d+).wav', fname)
        if m:
            segs_written = max(int(m.group(1)) + 1, segs_written)
    # split into segments
    duration = min(meta['duration'], video_cutoff_len)
    t0 = 0
    while t0 + min_seg_len < duration:
        out_path = os.path.join(out_dir, str(segs_written).zfill(5) + '.wav')
        t1 = min(t0 + seg_len, duration)
        ffmpeg_cmd = ffmpeg_cmd_tmpl % (ydl_options['outtmpl'], t0, t1, out_path)
        subprocess.check_output(ffmpeg_cmd.split())
        segs_written += 1
        t0 = t1
    # remove full wav
    subprocess.check_output(['rm', ydl_options['outtmpl']])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('video_url', type=str)
    parser.add_argument('--out_dir', type=str, default='data/chickens')
    parser.add_argument('--seg_len', type=int, default=120, help='segment length in seconds')
    parser.add_argument('--min_seg_len', type=int, default=30, help='minimum segment length')
    parser.add_argument('--video_cutoff_len', type=float, default=float('inf'), help='in seconds')
    args = parser.parse_args()
    dl_single(args.video_url, args.out_dir, args.seg_len, args.min_seg_len, args.video_cutoff_len)
