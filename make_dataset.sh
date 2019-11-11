# download wav files
RAW_WAV_DIR="$1/chickendata"
for yt_id in rzsq6ab6wpQ K3CenN7d30Y -MEuc2JufyY Y2qWdZzSKkw; do
    python3 dl_single.py "https://www.youtube.com/watch?v=${yt_id}" --out_dir $RAW_WAV_DIR
done

# remove silence
for fpath in ${RAW_WAV_DIR}/*.wav; do
    python3 remove_silences.py ${fpath} --overwrite
done

# giant YouTube videos with continuous chicken cacophonies
for yt_id in hS_J6C6rZiQ Wn8K-jkaKeY; do
    python3 dl_single.py "https://www.youtube.com/watch?v=${yt_id}" --out_dir $RAW_WAV_DIR --seg_len 300 --video_cutoff_len 1800
done

# preprocess
PROCESSED_WAV_DIR="$1/chickendata_out"
./preprocess_data.sh $RAW_WAV_DIR $PROCESSED_WAV_DIR
