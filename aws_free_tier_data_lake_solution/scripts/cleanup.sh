#!/usr/bin/env bash
set -euo pipefail

PROJECT_NAME="${1:-yu-free-datalake}"
REGION="${2:-us-west-2}"
STACK_NAME="${PROJECT_NAME}-stack"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "Emptying S3 buckets before stack deletion..."

for suffix in raw curated athena-results; do
  BUCKET="${PROJECT_NAME}-${ACCOUNT_ID}-${REGION}-${suffix}"
  aws s3 rm "s3://${BUCKET}" --recursive --region "$REGION" || true
done

aws cloudformation delete-stack \
  --stack-name "$STACK_NAME" \
  --region "$REGION"

echo "Delete requested. Check CloudFormation until DELETE_COMPLETE."
