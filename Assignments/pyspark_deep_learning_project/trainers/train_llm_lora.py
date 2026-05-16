"""
Lightweight LLM fine-tuning with Hugging Face + PEFT LoRA.

This script is intentionally small and practical. It formats classification examples as instructions
and fine-tunes a compact causal LM with LoRA adapters instead of full-model training.

For a small demo, use:
  --model_name sshleifer/tiny-gpt2

For a stronger base model on a GPU machine, swap to a supported instruction-tuned checkpoint.
"""

import argparse
from pathlib import Path

from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from peft import LoraConfig, TaskType, get_peft_model

from common import read_parquet


def format_row(text: str, label: int) -> str:
    target = "positive" if int(label) == 1 else "negative"
    return (
        "Classify the sentiment of the following review.\n\n"
        f"Review: {text}\n"
        f"Sentiment: {target}"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_parquet", required=True)
    parser.add_argument("--valid_parquet", required=True)
    parser.add_argument("--output_dir", default="artifacts/llm_lora")
    parser.add_argument("--model_name", default="sshleifer/tiny-gpt2")
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--max_length", type=int, default=128)
    args = parser.parse_args()

    train_df = read_parquet(args.train_parquet)
    valid_df = read_parquet(args.valid_parquet)

    train_df = train_df.copy()
    valid_df = valid_df.copy()
    train_df["text_for_lm"] = [format_row(t, y) for t, y in zip(train_df["text"], train_df["label"])]
    valid_df["text_for_lm"] = [format_row(t, y) for t, y in zip(valid_df["text"], valid_df["label"])]

    train_ds = Dataset.from_pandas(train_df[["text_for_lm"]], preserve_index=False)
    valid_ds = Dataset.from_pandas(valid_df[["text_for_lm"]], preserve_index=False)

    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    def tokenize(batch):
        out = tokenizer(
            batch["text_for_lm"],
            truncation=True,
            padding="max_length",
            max_length=args.max_length,
        )
        out["labels"] = out["input_ids"].copy()
        return out

    train_ds = train_ds.map(tokenize, batched=True, remove_columns=["text_for_lm"])
    valid_ds = valid_ds.map(tokenize, batched=True, remove_columns=["text_for_lm"])

    model = AutoModelForCausalLM.from_pretrained(args.model_name)
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        target_modules=["c_attn"] if "gpt2" in args.model_name.lower() else None,
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        eval_strategy="epoch",
        save_strategy="epoch",
        num_train_epochs=args.epochs,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        learning_rate=2e-4,
        logging_steps=10,
        report_to="none",
        fp16=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=valid_ds,
    )

    trainer.train()
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    print(f"Saved LoRA adapter and tokenizer to {args.output_dir}")


if __name__ == "__main__":
    main()
