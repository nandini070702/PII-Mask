from app.pipeline.pii_detection import detect_pii


def test_detect_pii_output_structure():
    """
    Test that detect_pii returns a dictionary
    with key 'pii_entities' as a list.
    """

    text = "My name is Nandini and email is nandi@gmail.com"
    result = detect_pii(text)

    assert isinstance(result, dict)
    assert "pii_entities" in result
    assert isinstance(result["pii_entities"], list)


from app.pipeline.pii_masking import mask_pii


def test_mask_pii_replaces_sensitive_values():
    """
    Test that mask_pii correctly replaces
    PII values with mask tokens.
    """

    text = (
        "Hello, my name is Nandini and my email is nandi@gmail.com "
        "or call 9876543210"
    )

    pii_entities = [
        {"type": "name", "value": "Nandini"},
        {"type": "email", "value": "nandi@gmail.com"},
        {"type": "phone", "value": "9876543210"}
    ]

    masked_text = mask_pii(text, pii_entities)

    assert "[NAME]" in masked_text
    assert "[EMAIL]" in masked_text
    assert "[PHONE]" in masked_text


from app.pipeline.pii_pipeline import run_pii_masking_pipeline


def test_pii_pipeline_returns_expected_keys():
    """
    Test that the full PII pipeline returns
    original text, masked text, and detected PII.
    """

    text = (
        "Hello, my name is Nandini and my email is nandi@gmail.com "
        "or call 9876543210"
    )

    result = run_pii_masking_pipeline(text)

    assert "original_text" in result
    assert "masked_text" in result
    assert "detected_pii" in result

    assert result["original_text"] == text
    assert isinstance(result["detected_pii"], list)
