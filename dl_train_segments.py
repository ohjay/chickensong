import os
import csv
import json
import argparse
import youtube_dl
import subprocess

def dl_train_segments(csv_path, out_dir, ontology_path):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    ydl_options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    ydl_base_tmpl = os.path.join(out_dir, '{title}.wav')

    # load ontology
    ontology_ids = {
        'Chicken, rooster': '/m/09b5t',
        'Cluck': '/m/07st89h',
        'Crowing, cock-a-doodle-doo': '/m/07qn5dc',
    }
    if os.path.exists(ontology_path):
        with open(ontology_path, 'r') as f:
            ontology = json.load(f)
        for info in ontology:
            if info['name'] in ontology_ids:
                ontology_ids[info['name']] = info['id']
    else:
        print('Warning: `%s` does not exist! '
              '(The caller indicates that this is PROBABLY not a failure.) '
              'Set the correct path to `ontology.json` using the `--ontology_path` flag. '
              'You can download the latest version of the file from '
              'https://github.com/audioset/ontology.git.\n' % ontology_path)

    ffmpeg_cmd_tmpl = 'ffmpeg -i %s -ss %d -to %d %s'  # (in, start_sec, end_sec, out)
    mv_cmd_tmpl = 'mv %s %s'  # (from, to)
    with open(csv_path, newline='') as f:
        segs_written = 0
        csv_reader = csv.reader(f, delimiter=' ', quotechar='|')
        for i, row in enumerate(csv_reader):
            try:
                row[:3] = [s.replace(',', '') for s in row[:3]]
                yt_id, start_sec, end_sec, labels = row
                start_sec = int(float(start_sec))
                end_sec = int(float(end_sec))
                labels = labels.replace('"', '').split(',')

                if ontology_ids['Chicken, rooster'] in labels:
                    # download wav
                    ydl_options['outtmpl'] = ydl_base_tmpl.format(title=str(segs_written).zfill(5))
                    with youtube_dl.YoutubeDL(ydl_options) as ydl:
                        ydl.download(['http://www.youtube.com/watch?v=%s' % yt_id])
                    # trim output
                    trimmed = ydl_base_tmpl.format(title=str(segs_written).zfill(5)+'_trimmed')
                    ffmpeg_cmd = ffmpeg_cmd_tmpl % (ydl_options['outtmpl'], start_sec, end_sec, trimmed)
                    subprocess.check_output(ffmpeg_cmd.split())
                    # overwrite full wav file
                    mv_cmd = mv_cmd_tmpl % (trimmed, ydl_options['outtmpl'])
                    subprocess.check_output(mv_cmd.split())
                    segs_written += 1
                    with open('success_list.txt', 'a') as success_file:
                        success_file.write('{yt_id}\n'.format(yt_id=yt_id))
            except ValueError as e:
                if i >= 3:
                    print(e)  # else one of the header rows
            except youtube_dl.utils.DownloadError as e:
                if 'Connection timed out' in str(e):
                    print('Timeout when downloading %s' % yt_id)
                    with open('timeout_list.txt', 'a') as timeout_file:
                        timeout_file.write('{yt_id}\n'.format(yt_id=yt_id))
                else:
                    with open('failure_list.txt', 'a') as failure_file:
                        failure_file.write('{yt_id}\n'.format(yt_id=yt_id))
            i += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_path', type=str, help='path to `unbalanced_train_segments.csv`')
    parser.add_argument('--out_dir', type=str, default='data/chickens')
    parser.add_argument('--ontology_path', type=str, help='path to `ontology.json`', default='ontology/ontology.json')
    args = parser.parse_args()
    dl_train_segments(args.csv_path, args.out_dir, args.ontology_path)
