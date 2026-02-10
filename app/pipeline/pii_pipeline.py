"""
PII Masking Pipeline
-------------------
Combines PII detection and masking into a single pipeline.
"""

from typing import Dict

from app.pipeline.pii_detection import detect_pii
from app.pipeline.pii_masking import mask_pii


def run_pii_masking_pipeline(text: str) -> Dict[str, str]:
    """
    Runs the full PII masking pipeline.

    Steps:
    1. Detect PII entities from text
    2. Mask detected PII in the text

    Args:
        text: Raw input text

    Returns:
        Dictionary containing:
        - original_text
        - masked_text
        - detected_pii
    """

    # Step 1: Detect PII
    detection_result = detect_pii(text)
    pii_entities = detection_result.get("pii_entities", [])

    # Step 2: Mask PII
    masked_text = mask_pii(text, pii_entities)

    return {
        "original_text": text,
        "masked_text": masked_text,
        "detected_pii": pii_entities
    }


if __name__ == "__main__":
    sample_text = (
        "Hello, my name is Nandini and my email is nandi@gmail.com "
        "or call 9876543210"
    )

    result = run_pii_masking_pipeline(sample_text)

    print("Original Text:")
    print(result["original_text"])
    print("\nMasked Text:")
    print(result["masked_text"])
    print("\nDetected PII:")
    print(result["detected_pii"])
