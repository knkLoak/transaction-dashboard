#!/bin/bash

# This script is not committed to GitHub or Hugging Face
git remote add huggingface https://user:${HF_TOKEN}@huggingface.co/spaces/knkLoak/transaction-dashboard
git push huggingface main --force
