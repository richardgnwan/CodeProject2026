# Semantic Sentence API - Coding Challenge

## Time Limit
**90 minutes recommended** (honor system)

Please record your actual time spent. We value honesty about time investment.

## Overview
Build a Python REST API with two endpoints using MLC LLM (a local LLM framework).

### Endpoint 1: Semantic Grouping
**POST /group-sentences**

Takes a list of sentences and returns them grouped by semantic similarity.

Example Input:
```json
{
  "sentences": [
    "The cat sat on the mat",
    "Dogs love to play fetch",
    "My feline friend enjoys napping",
    "The puppy ran across the yard",
    "Machine learning is fascinating",
    "AI models can process text"
  ]
}
```

Example Output:
```json
{
  "groups": [
    ["The cat sat on the mat", "My feline friend enjoys napping"],
    ["Dogs love to play fetch", "The puppy ran across the yard"],
    ["Machine learning is fascinating", "AI models can process text"]
  ]
}
```

### Endpoint 2: Paragraph Synthesis
**POST /synthesize**

Takes multiple sentences and returns a single coherent paragraph.

Example Input:
```json
{
  "sentences": [
    "The weather is sunny today",
    "I plan to go to the beach",
    "Swimming is my favorite activity"
  ]
}
```

Example Output:
```json
{
  "paragraph": "It's a beautiful sunny day, perfect for heading to the beach. Swimming has always been my favorite activity, and today's weather makes it an ideal opportunity to enjoy the water."
}
```

---

## Requirements

### Must Use
- **MLC LLM** for language model inference (https://llm.mlc.ai/)
- **Python 3.10+**

### Your Choice
- Web framework (Flask, FastAPI, etc.)
- Additional libraries for embeddings/similarity (if needed)
- Model selection from MLC-compatible models

### Hardware & Installation

**Recommended small models** (work on both CPU and GPU):
- `HF://mlc-ai/Qwen3-0.6B-q4f16_1-MLC` (~600M params)
- `HF://mlc-ai/TinyLlama-1.1B-Chat-v0.4-q4f16_1-MLC`
- `HF://mlc-ai/phi-1_5-q4f16_1-MLC`

**GPU Installation** (NVIDIA CUDA):
```bash
pip install --pre -U -f https://mlc.ai/wheels mlc-llm-nightly mlc-ai-nightly
```

**CPU Installation** (no GPU required):
```bash
pip install --pre -U -f https://mlc.ai/wheels mlc-llm-nightly-cpu mlc-ai-nightly-cpu
```

**macOS with Apple Silicon** (M1/M2/M3):
```bash
pip install --pre -U -f https://mlc.ai/wheels mlc-llm-nightly mlc-ai-nightly
```

---

## Setup

```bash
# 1. Create virtual environment (conda recommended)
conda create -n semantic-api python=3.11
conda activate semantic-api

# 2. Install MLC LLM (see "Hardware & Installation" above for the right command)

# 3. Install git-lfs (required for model downloads)
# macOS: brew install git-lfs
# Ubuntu: sudo apt install git-lfs
git lfs install

# 4. Install your additional dependencies
pip install -r requirements.txt
```

Or run the provided setup script for guidance:
```bash
./setup.sh
```

---

## Submission

### How to Submit

1. **Fork this repository** to your own GitHub account
2. Complete the challenge in your forked repo
3. **Submit the URL** of your forked GitHub repository

### Your repo must include:

1. **All source code** for your solution
2. **requirements.txt** with your dependencies
3. **Updated README** (the "Your Solution" section below) explaining:
   - How to run your solution
   - Your approach and design decisions
   - Any tradeoffs or limitations
   - Actual time spent (be honest!)
   - Whether you used AI coding assistants (allowed, just disclose it)

**Important:** Make sure your repository is **public** or that you've granted us access before submitting.

---

## Evaluation Criteria

- **Functionality**: Do both endpoints work correctly?
- **Code Quality**: Clean, readable, maintainable code
- **Technical Decisions**: Did you make sensible library/approach choices?
- **API Design**: Proper REST conventions, error handling
- **Documentation**: Clear instructions and explanations

---

## Hints

- MLC LLM provides an OpenAI-compatible chat API
- Semantic similarity might require creative problem-solving
- Start simple, then iterate if time permits
- Working code beats perfect code
- See `example_usage.py` for basic MLC LLM patterns

---

## Helpful Resources

- MLC LLM Documentation: https://llm.mlc.ai/docs/
- MLC LLM Models on HuggingFace: https://huggingface.co/mlc-ai

---

## Your Solution

**Please fill out this section before submitting:**

### How to Run
<!-- Your instructions for running the solution -->


### Approach
<!-- Your design decisions and how you solved the semantic grouping problem -->


### Tradeoffs/Limitations
<!-- What you'd improve with more time -->


### Time Spent
<!-- Be honest! We value integrity over speed -->


### AI Assistant Usage
<!-- Did you use Claude, Copilot, ChatGPT, etc.? It's allowed, just disclose it -->
