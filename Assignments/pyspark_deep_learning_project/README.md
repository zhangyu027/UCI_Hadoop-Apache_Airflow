# PySpark ETL + Modern Deep Learning Project

This project uses **PySpark only for preprocessing / distributed ETL**, then hands off curated datasets to
modern deep learning stacks:

- **PyTorch CNN** for image classification
- **TensorFlow LSTM** for sequence classification
- **Hugging Face Transformers / BERT** for text classification
- **Hugging Face + PEFT LoRA** for lightweight LLM fine-tuning

## Architecture

1. `spark_etl/prepare_text_data.py`
   - reads raw CSV/JSON/text
   - cleans text with PySpark
   - writes train/validation/test splits to Parquet

2. Model trainers read the ETL output:
   - `trainers/train_cnn_pytorch.py`
   - `trainers/train_lstm_tensorflow.py`
   - `trainers/train_bert_hf.py`
   - `trainers/train_llm_lora.py`

## Recommended workflow

```bash
pip install -r requirements.txt

python spark_etl/prepare_text_data.py   --input data/raw/sample_reviews.csv   --output_dir data/processed/text_reviews

python trainers/train_bert_hf.py   --train_parquet data/processed/text_reviews/train.parquet   --valid_parquet data/processed/text_reviews/valid.parquet   --output_dir artifacts/bert_classifier
```

## Notes

- Spark is strongest for large-scale joins, cleaning, deduplication, filtering, and feature assembly.
- Modern deep learning training is usually better done in PyTorch / TensorFlow / Hugging Face than directly in Spark.
- The LLM script uses **LoRA** so it is much lighter than full fine-tuning.
