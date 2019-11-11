# download wav files
RAW_WAV_DIR="/media/owen/ba9d40b5-89de-4832-bad4-156b118e4a66/chickendata"
for yt_id in rzsq6ab6wpQ K3CenN7d30Y; do
    python3 dl_single.py "https://www.youtube.com/watch?v=${yt_id}" --out_dir $RAW_WAV_DIR
done

# preprocess
PROCESSED_WAV_DIR="/media/owen/ba9d40b5-89de-4832-bad4-156b118e4a66/chickendata_out"
./preprocess_data.sh $RAW_WAV_DIR $PROCESSED_WAV_DIR
