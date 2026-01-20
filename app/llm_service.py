"""
LLM Service module for MLC LLM integration.

This module provides a singleton service for interacting with MLC LLM,
including methods for semantic sentence grouping and paragraph synthesis.

Author:
    Richard Gunawan (richardgunawan26@gmail.com)
"""

import json
import logging
import re

from mlc_llm import MLCEngine

from app.prompts import (
    GROUPING_PROMPT_TEMPLATE,
    GROUPING_SYSTEM_MESSAGE,
    SYNTHESIS_PROMPT_TEMPLATE,
    SYNTHESIS_SYSTEM_MESSAGE,
)

logger = logging.getLogger(__name__)

# Default model to use
DEFAULT_MODEL = "HF://mlc-ai/Qwen3-0.6B-q4f16_1-MLC"


class LLMService:
    """
    Service class for MLC LLM operations.

    Uses a singleton pattern to ensure only one MLCEngine instance is created,
    as engine initialization is expensive.
    """

    _instance: "LLMService | None" = None
    _engine: MLCEngine | None = None
    _model: str = DEFAULT_MODEL

    def __new__(cls) -> "LLMService":
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self, model: str | None = None) -> None:
        """
        Initialize the MLC LLM engine.

        Args:
            model: The model identifier to use. Defaults to Qwen3-0.6B.
        """
        if self._engine is not None:
            logger.warning("Engine already initialized, skipping re-initialization")
            return

        self._model = model or DEFAULT_MODEL
        logger.info("Initializing MLCEngine with model: %s", self._model)
        try:
            self._engine = MLCEngine(self._model, device="auto")
        except Exception as e:
            logger.error("Error initializing MLCEngine: %s", e)
            self._engine = MLCEngine(self._model, device="cpu")
        logger.info("MLCEngine initialized successfully")

    def terminate(self) -> None:
        """Terminate the MLC LLM engine and release resources."""
        if self._engine is not None:
            logger.info("Terminating MLCEngine...")
            self._engine.terminate()
            self._engine = None
            logger.info("MLCEngine terminated successfully")

    def _get_engine(self) -> MLCEngine:
        """Get the engine instance, raising an error if not initialized."""
        if self._engine is None:
            raise RuntimeError("LLM Engine not initialized. Call initialize() first.")
        return self._engine

    def _extract_json_from_response(self, response_text: str) -> list[list[str]]:
        """
        Extract JSON array from LLM response text.

        Args:
            response_text: The raw response text from the LLM.

        Returns:
            Parsed list of sentence groups.

        Raises:
            ValueError: If JSON cannot be extracted or parsed.
        """
        # Try to find JSON array in the response
        # Look for pattern like [[...], [...], ...]
        json_match = re.search(r"\[\s*\[.*?\]\s*\]", response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        # Try parsing the entire response as JSON
        try:
            result = json.loads(response_text)
            if isinstance(result, list):
                return result
        except json.JSONDecodeError:
            pass

        raise ValueError(f"Could not extract valid JSON from response: {response_text}")

    def group_sentences_by_similarity(self, sentences: list[str]) -> list[list[str]]:
        """
        Group sentences by semantic similarity using the LLM.

        Args:
            sentences: List of sentences to group.

        Returns:
            List of sentence groups, where each group contains semantically similar sentences.
        """
        engine = self._get_engine()

        # Handle edge cases
        if len(sentences) == 0:
            return []
        if len(sentences) == 1:
            return [sentences]

        # Create the prompt with few-shot example for reliable JSON output
        prompt = GROUPING_PROMPT_TEMPLATE.format(sentences_json=json.dumps(sentences))

        logger.debug("Sending grouping request to LLM")
        # TODO: We can add response_format inside the `create` to utilize json mode
        response = engine.chat.completions.create(
            messages=[
                {"role": "system", "content": GROUPING_SYSTEM_MESSAGE},
                {"role": "user", "content": prompt},
            ],
            model=self._model,
            stream=False,
        )

        content = response.choices[0].message.content
        if content is None:
            logger.error("LLM returned None content for grouping request")
            raise ValueError("LLM returned empty response")
        response_text = content
        logger.debug("LLM response: %s", response_text)

        try:
            groups = self._extract_json_from_response(response_text)
            # Validate that all original sentences are in the result
            flat_result = [s for group in groups for s in group]
            missing = set(sentences) - set(flat_result)
            if missing:
                logger.warning("Some sentences missing from groups, adding as separate group: %s", missing)
                groups.append(list(missing))
            return groups
        except ValueError as e:
            logger.error("Failed to parse LLM response: %s", e)
            # Fallback: return all sentences as one group
            return [sentences]

    def synthesize_paragraph(self, sentences: list[str]) -> str:
        """
        Synthesize a coherent paragraph from multiple sentences.

        Args:
            sentences: List of sentences to synthesize.

        Returns:
            A coherent paragraph combining the input sentences.
        """
        engine = self._get_engine()

        # Handle edge cases
        if len(sentences) == 0:
            return ""
        if len(sentences) == 1:
            return sentences[0]

        sentences_text = "\n".join(f"- {s}" for s in sentences)
        prompt = SYNTHESIS_PROMPT_TEMPLATE.format(sentences_text=sentences_text)

        logger.debug("Sending synthesis request to LLM")
        response = engine.chat.completions.create(
            messages=[
                {"role": "system", "content": SYNTHESIS_SYSTEM_MESSAGE},
                {"role": "user", "content": prompt},
            ],
            model=self._model,
            stream=False,
        )

        content = response.choices[0].message.content
        if content is None:
            logger.warning("LLM returned None content, returning empty string")
            return ""
        if not isinstance(content, str):
            logger.warning("LLM returned non-string content: %s", type(content))
            return str(content).strip()
        paragraph = content.strip()
        logger.debug("LLM synthesis response: %s", paragraph)
        return paragraph


# Global service instance
llm_service = LLMService()
