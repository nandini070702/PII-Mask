"""
PII Masking Module
------------------
Takes original text and detected PII entities,
and returns masked (redacted) text.
"""

from typing import List, Dict


MASK_TOKENS = {
    "name": "[NAME]",
    "email": "[EMAIL]",
    "phone": "[PHONE]"
}


def mask_pii(text: str, pii_entities: List[Dict[str, str]]) -> str:
    """
    Masks PII entities in the given text.

    Args:
        text: Original input text
        pii_entities: List of detected PII entities

    Returns:
        Masked text with PII replaced
    """

    masked_text = text

    for entity in pii_entities:
        pii_type = entity.get("type")
        pii_value = entity.get("value")

        if not pii_type or not pii_value:
            continue

        mask_token = MASK_TOKENS.get(pii_type)

        if mask_token:
            masked_text = masked_text.replace(pii_value, mask_token)

    return masked_text


if __name__ == "__main__":
    sample_text = (
        "Hello, my name is Nandini and my email is nandi@gmail.com "
        "or call 9876543210"
    )

    sample_pii = [
        {"type": "name", "value": "Nandini"},
        {"type": "email", "value": "nandi@gmail.com"},
        {"type": "phone", "value": "9876543210"}
    ]

    print(mask_pii(sample_text, sample_pii))
