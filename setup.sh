#!/bin/bash

echo "============================================"
echo "  Semantic Sentence API - Environment Setup"
echo "============================================"
echo ""

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "WARNING: conda not found. We recommend using conda for environment management."
    echo "Install miniconda from: https://docs.conda.io/en/latest/miniconda.html"
    echo ""
    echo "Alternatively, you can use venv:"
    echo "  python -m venv venv"
    echo "  source venv/bin/activate"
    echo ""
else
    echo "Step 1: Creating conda environment..."
    echo "  conda create -n semantic-api python=3.11 -y"
    echo ""
    echo "  Then activate it:"
    echo "  conda activate semantic-api"
    echo ""
fi

echo "Step 2: Install MLC LLM"
echo "  Choose based on your hardware:"
echo ""
echo "  GPU (NVIDIA CUDA):"
echo "    pip install --pre -U -f https://mlc.ai/wheels mlc-llm-nightly mlc-ai-nightly"
echo ""
echo "  macOS Apple Silicon (M1/M2/M3):"
echo "    pip install --pre -U -f https://mlc.ai/wheels mlc-llm-nightly mlc-ai-nightly"
echo ""
echo "  CPU only (no GPU):"
echo "    pip install --pre -U -f https://mlc.ai/wheels mlc-llm-nightly-cpu mlc-ai-nightly-cpu"
echo ""

echo "Step 3: Install git-lfs (required for model downloads)"
echo "  macOS:  brew install git-lfs"
echo "  Ubuntu: sudo apt install git-lfs"
echo "  Then run: git lfs install"
echo ""

echo "Step 4: Install your additional dependencies"
echo "  pip install -r requirements.txt"
echo ""

echo "Step 5: Test MLC LLM installation"
echo "  python example_usage.py"
echo ""

echo "============================================"
echo "  Setup instructions complete!"
echo "  Read README.md for the full challenge."
echo "============================================"
