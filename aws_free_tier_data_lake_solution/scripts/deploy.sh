#!/usr/bin/env bash
set -euo pipefail

PROJECT_NAME="${1:-yu-free-datalake}"
REGION="${2:-us-west-2}"
STACK_NAME="${PROJECT_NAME}-stack"

echo "Deploying stack: $STACK_NAME in $REGION"

aws cloudformation deploy \
  --template-file cloudformation/free-tier-data-lake.yml \
  --stack-name "$STACK_NAME" \
  --region "$REGION" \
  --parameter-overrides ProjectName="$PROJECT_NAME"

RAW_BUCKET=$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --region "$REGION" \
  --query "Stacks[0].Outputs[?OutputKey=='RawBucketName'].OutputValue" \
  --output text)

echo "Uploading sample data to s3://$RAW_BUCKET/sales/"
aws s3 cp data/sales_events.csv "s3://$RAW_BUCKET/sales/sales_events.csv" --region "$REGION"

echo "Done."
echo "Raw bucket: $RAW_BUCKET"
echo "Open Athena, choose the workgroup '${PROJECT_NAME}-workgroup', database '${PROJECT_NAME}_db', and query table sales_csv."
