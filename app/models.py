"""
Pydantic models for request and response schemas.

This module defines the data models used by the Semantic Sentence API endpoints.

Author:
    Richard Gunawan (richardgunawan26@gmail.com)
"""

from pydantic import BaseModel, Field


class GroupSentencesRequest(BaseModel):
    """Request model for the /group-sentences endpoint."""

    sentences: list[str] = Field(
        ...,
        min_length=1,
        description="List of sentences to group by semantic similarity",
        examples=[
            [
                "The cat sat on the mat",
                "Dogs love to play fetch",
                "My feline friend enjoys napping",
            ]
        ],
    )


class GroupSentencesResponse(BaseModel):
    """Response model for the /group-sentences endpoint."""

    groups: list[list[str]] = Field(
        ...,
        description="Sentences grouped by semantic similarity",
        examples=[
            [
                ["The cat sat on the mat", "My feline friend enjoys napping"],
                ["Dogs love to play fetch"],
            ]
        ],
    )


class SynthesizeRequest(BaseModel):
    """Request model for the /synthesize endpoint."""

    sentences: list[str] = Field(
        ...,
        min_length=1,
        description="List of sentences to synthesize into a coherent paragraph",
        examples=[
            [
                "The weather is sunny today",
                "I plan to go to the beach",
                "Swimming is my favorite activity",
            ]
        ],
    )


class SynthesizeResponse(BaseModel):
    """Response model for the /synthesize endpoint."""

    paragraph: str = Field(
        ...,
        description="A coherent paragraph synthesized from the input sentences",
        examples=[
            "It's a beautiful sunny day, perfect for heading to the beach. "
            "Swimming has always been my favorite activity, and today's weather "
            "makes it an ideal opportunity to enjoy the water."
        ],
    )
