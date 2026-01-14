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

1. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Install MLC LLM** (choose based on your hardware):
   ```bash
   # GPU (NVIDIA CUDA):
   pip install --pre -U -f https://mlc.ai/wheels mlc-llm-nightly mlc-ai-nightly
   
   # CPU only:
   pip install --pre -U -f https://mlc.ai/wheels mlc-llm-nightly-cpu mlc-ai-nightly-cpu
   
   # macOS Apple Silicon:
   pip install --pre -U -f https://mlc.ai/wheels mlc-llm-nightly mlc-ai-nightly
   ```

3. **Install git-lfs** (required for model downloads):
   ```bash
   # Ubuntu
   sudo apt install git-lfs
   git lfs install
   ```

4. **Install dependencies with Poetry**:
   ```bash
   poetry install
   ```

5. **Run the API server**:
   ```bash
   poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

6. **Test the endpoints**:
   ```bash
   # Group sentences
   curl -X POST http://localhost:8000/group-sentences \
     -H "Content-Type: application/json" \
     -d '{"sentences": ["The cat sat on the mat", "Dogs love to play fetch", "My feline friend enjoys napping"]}'
   
   # Synthesize paragraph
   curl -X POST http://localhost:8000/synthesize \
     -H "Content-Type: application/json" \
     -d '{"sentences": ["The weather is sunny today", "I plan to go to the beach", "Swimming is my favorite activity"]}'
   ```

7. **API Documentation**: Visit http://localhost:8000/docs for interactive Swagger UI.

### Approach

**Architecture**: FastAPI application with a singleton LLM service pattern.

**Semantic Grouping (Option A - LLM-Native)**:
- Used prompt engineering to have the LLM analyze and group sentences by semantic similarity
- The prompt includes few-shot examples to ensure reliable JSON output format
- Fallback handling for cases where the LLM response cannot be parsed

**Paragraph Synthesis**:
- Direct prompting asking the LLM to combine sentences into a coherent, flowing paragraph
- System prompt guides the model to preserve meaning while creating natural text

**Key Design Decisions**:
- Singleton pattern for MLCEngine (expensive initialization)
- Lifespan context manager for proper resource cleanup
- Pydantic models for request/response validation
- Comprehensive error handling with appropriate HTTP status codes

### Tradeoffs/Limitations

- **LLM-based grouping**: Less deterministic than embedding-based approaches; results may vary between runs
- **JSON parsing**: The LLM may occasionally produce malformed JSON; fallback returns all sentences in one group
- **Performance**: Each grouping request requires an LLM call; could be slow for large batches
- **No caching**: Repeated identical requests trigger new LLM calls
- **Single model**: Currently hardcoded to Qwen3-0.6B; could be made configurable

**With more time, I would add**:
- Configurable model selection via environment variables
- Request caching for identical inputs
- Batch processing optimization
- More robust JSON extraction with multiple fallback strategies
- Unit tests for the LLM service

### Time Spent
~1.5 hours


### AI Assistant Usage
1. Claude for brainstorming and planning
2. Cursor

### Issues
1. Since my device does not have GPU, the time used for inference is very long.
