#!/usr/bin/env bash
set -euo pipefail

python spark_etl/prepare_text_data.py   --input data/raw/sample_reviews.csv   --output_dir data/processed/text_reviews

python trainers/train_lstm_tensorflow.py   --train_parquet data/processed/text_reviews/train.parquet   --valid_parquet data/processed/text_reviews/valid.parquet   --output_dir artifacts/lstm

python trainers/train_bert_hf.py   --train_parquet data/processed/text_reviews/train.parquet   --valid_parquet data/processed/text_reviews/valid.parquet   --output_dir artifacts/bert   --epochs 1

python trainers/train_llm_lora.py   --train_parquet data/processed/text_reviews/train.parquet   --valid_parquet data/processed/text_reviews/valid.parquet   --output_dir artifacts/llm_lora   --epochs 1

python trainers/train_cnn_pytorch.py   --output_dir artifacts/cnn   --epochs 2
