# ./preprocess_data.sh <chicken data dir> <output dir>

MT_DIR="music-translation"
python3 ${MT_DIR}/src/split_dir.py -i $1 -o $2/split/$(basename "$1")
python3 ${MT_DIR}/src/preprocess.py -i $2/split -o $2/preprocessed
