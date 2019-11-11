# download wav files
RAW_WAV_DIR="$1/chickendata"
for yt_id in rzsq6ab6wpQ K3CenN7d30Y; do
    python3 dl_single.py "https://www.youtube.com/watch?v=${yt_id}" --out_dir $RAW_WAV_DIR
done

# remove silence
for fpath in ${RAW_WAV_DIR}/*.wav; do
    python3 remove_silences.py ${fpath} --overwrite
done

# preprocess
PROCESSED_WAV_DIR="$1/chickendata_out"
./preprocess_data.sh $RAW_WAV_DIR $PROCESSED_WAV_DIR
