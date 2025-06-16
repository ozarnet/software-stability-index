#!/bin/bash

echo 'Creating SSI project structure...'

mkdir -p ssi/docs
mkdir -p ssi/examples
mkdir -p ssi/scoring
mkdir -p ssi/automation
mkdir -p ssi/.github/workflows
touch ssi/README.md
touch ssi/CONTEXT.md
touch ssi/LICENSE
touch ssi/docs/learnability.md
touch ssi/docs/applicability.md
touch ssi/docs/sustainability.md
touch ssi/scoring/compute_ssi.py
touch ssi/examples/sample_scores.json
echo "SSI project scaffold created successfully."