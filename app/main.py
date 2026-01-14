"""
FastAPI application for Semantic Sentence API.

This module provides the main FastAPI application with endpoints for
semantic sentence grouping and paragraph synthesis.

Author:
    Richard Gunawan (richardgunawan26@gmail.com)
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.llm_service import llm_service
from app.models import (
    GroupSentencesRequest,
    GroupSentencesResponse,
    SynthesizeRequest,
    SynthesizeResponse,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage the application lifespan.

    Initializes the LLM engine on startup and terminates it on shutdown.
    """
    logger.info("Starting Semantic Sentence API...")
    try:
        llm_service.initialize()
        logger.info("LLM service initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize LLM service: %s", e)
        raise

    yield

    logger.info("Shutting down Semantic Sentence API...")
    llm_service.terminate()
    logger.info("Shutdown complete")


app = FastAPI(
    title="Semantic Sentence API",
    description="API for semantic sentence grouping and paragraph synthesis using MLC LLM",
    version="0.1.0",
    lifespan=lifespan,
)


@app.post(
    "/group-sentences",
    response_model=GroupSentencesResponse,
    summary="Group sentences by semantic similarity",
    description="Takes a list of sentences and returns them grouped by semantic similarity.",
)
async def group_sentences(request: GroupSentencesRequest) -> GroupSentencesResponse:
    """
    Group sentences by semantic similarity.

    Args:
        request: The request containing sentences to group.

    Returns:
        Response containing grouped sentences.

    Raises:
        HTTPException: If an error occurs during processing.
    """
    logger.info("Received group-sentences request with %d sentences", len(request.sentences))

    try:
        groups = llm_service.group_sentences_by_similarity(request.sentences)
        logger.info("Successfully grouped sentences into %d groups", len(groups))
        return GroupSentencesResponse(groups=groups)
    except RuntimeError as e:
        logger.error("LLM service error: %s", e)
        raise HTTPException(status_code=503, detail="LLM service unavailable") from e
    except Exception as e:
        logger.error("Unexpected error during sentence grouping: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error") from e


@app.post(
    "/synthesize",
    response_model=SynthesizeResponse,
    summary="Synthesize sentences into a paragraph",
    description="Takes multiple sentences and returns a single coherent paragraph.",
)
async def synthesize(request: SynthesizeRequest) -> SynthesizeResponse:
    """
    Synthesize multiple sentences into a coherent paragraph.

    Args:
        request: The request containing sentences to synthesize.

    Returns:
        Response containing the synthesized paragraph.

    Raises:
        HTTPException: If an error occurs during processing.
    """
    logger.info("Received synthesize request with %d sentences", len(request.sentences))

    try:
        paragraph = llm_service.synthesize_paragraph(request.sentences)
        logger.info("Successfully synthesized paragraph")
        return SynthesizeResponse(paragraph=paragraph)
    except RuntimeError as e:
        logger.error("LLM service error: %s", e)
        raise HTTPException(status_code=503, detail="LLM service unavailable") from e
    except Exception as e:
        logger.error("Unexpected error during synthesis: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error") from e


@app.get("/health", summary="Health check endpoint")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        A dictionary indicating the service status.
    """
    return {"status": "healthy"}
