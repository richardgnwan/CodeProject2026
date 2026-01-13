#!/bin/bash

# Test script for Semantic Sentence API
# Adjust BASE_URL if your server runs on a different port

BASE_URL="${1:-http://localhost:8000}"

echo "============================================"
echo "  Testing Semantic Sentence API"
echo "  Base URL: $BASE_URL"
echo "============================================"
echo ""

# Test 1: Group Sentences
echo "=== Test 1: POST /group-sentences ==="
echo "Sending sentences about cats, dogs, and technology..."
echo ""

curl -s -X POST "$BASE_URL/group-sentences" \
  -H "Content-Type: application/json" \
  -d '{
    "sentences": [
      "The cat sat on the mat",
      "Dogs love to play fetch",
      "My feline friend enjoys napping",
      "The puppy ran across the yard",
      "Machine learning is fascinating",
      "AI models can process text"
    ]
  }' | python -m json.tool 2>/dev/null || echo "(raw output above)"

echo ""
echo ""

# Test 2: Synthesize Paragraph
echo "=== Test 2: POST /synthesize ==="
echo "Sending sentences to combine into a paragraph..."
echo ""

curl -s -X POST "$BASE_URL/synthesize" \
  -H "Content-Type: application/json" \
  -d '{
    "sentences": [
      "The weather is sunny today",
      "I plan to go to the beach",
      "Swimming is my favorite activity"
    ]
  }' | python -m json.tool 2>/dev/null || echo "(raw output above)"

echo ""
echo ""

# Test 3: Edge case - Empty input
echo "=== Test 3: Edge Case - Empty sentences ==="
echo ""

curl -s -X POST "$BASE_URL/group-sentences" \
  -H "Content-Type: application/json" \
  -d '{
    "sentences": []
  }' | python -m json.tool 2>/dev/null || echo "(raw output above)"

echo ""
echo ""

# Test 4: Edge case - Single sentence
echo "=== Test 4: Edge Case - Single sentence ==="
echo ""

curl -s -X POST "$BASE_URL/synthesize" \
  -H "Content-Type: application/json" \
  -d '{
    "sentences": ["Just one sentence here."]
  }' | python -m json.tool 2>/dev/null || echo "(raw output above)"

echo ""
echo "============================================"
echo "  Tests complete!"
echo "============================================"
