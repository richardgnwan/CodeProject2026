"""
Prompt templates and system messages for LLM operations.

This module contains all prompt templates and system messages used by the LLM service
to ensure consistency and maintainability.

Author:
    Richard Gunawan (richardgunawan26@gmail.com)
"""

# System messages
GROUPING_SYSTEM_MESSAGE = (
    "You are a helpful assistant that groups sentences by semantic similarity. "
    "Always respond with valid JSON arrays only, no explanations."
)

SYNTHESIS_SYSTEM_MESSAGE = (
    "You are a helpful assistant that combines sentences into coherent paragraphs. "
    "Write naturally flowing text that preserves the meaning of all input sentences."
)

# Prompt templates
GROUPING_PROMPT_TEMPLATE = """Analyze the following sentences and group them by semantic similarity.
Return ONLY a JSON array of arrays, where each inner array contains sentences that are semantically similar.
Do not include any explanation or additional text, just the JSON array.

Example input:
["The cat sleeps", "Dogs bark loudly", "My kitten naps"]

Example output:
[["The cat sleeps", "My kitten naps"], ["Dogs bark loudly"]]

Now group these sentences:
{sentences_json}

Output (JSON array only):"""

SYNTHESIS_PROMPT_TEMPLATE = """Combine the following sentences into a single coherent, flowing paragraph.
Maintain the key information from each sentence while making the text natural and well-connected.

Sentences:
{sentences_text}

Write a coherent paragraph:"""
