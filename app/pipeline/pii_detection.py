"""
PII Detection Agent
-------------------
Detects basic PII (names, email addresses, phone numbers)
from input text using an LLM via LangChain.

NOTE:
Currently running in MOCK mode to avoid API quota issues.
Set USE_MOCK_LLM = False to enable real OpenAI calls.
"""

import json
from typing import List, Dict, TypedDict

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


# 🔹 Toggle this flag
USE_MOCK_LLM = True


class PIIOutput(TypedDict):
    """
    Defines the structure of the PII detection output.
    """
    pii_entities: List[Dict[str, str]]


def format_pii_output(entities: List[Dict[str, str]]) -> PIIOutput:
    """
    Formats detected PII entities into a standard JSON structure.
    """
    return {
        "pii_entities": entities
    }


PII_DETECTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a PII detection system.
            Your task is to identify personally identifiable information in text.

            Detect ONLY the following PII types:
            - name
            - email
            - phone

            Return the result strictly in valid JSON format.
            Do not include explanations or extra text.

            Output format:
            {{
              "pii_entities": [
                {{"type": "name", "value": "John Doe"}},
                {{"type": "email", "value": "john@example.com"}},
                {{"type": "phone", "value": "+91 9876543210"}}
              ]
            }}

            If no PII is found, return:
            {{
              "pii_entities": []
            }}
            """
        ),
        ("human", "{input_text}")
    ]
)


def detect_pii(text: str) -> PIIOutput:
    """
    Detects PII entities from the given input text.
    """

    # 🔹 MOCK MODE (no API call)
    if USE_MOCK_LLM:
        parsed_output = {
            "pii_entities": [
                {"type": "name", "value": "Nandini"},
                {"type": "email", "value": "nandi@gmail.com"},
                {"type": "phone", "value": "9876543210"}
            ]
        }

    # 🔹 REAL LLM MODE
    else:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

        chain = PII_DETECTION_PROMPT | llm
        response = chain.invoke({"input_text": text})

        try:
            parsed_output = json.loads(response.content)
        except json.JSONDecodeError:
            parsed_output = {"pii_entities": []}

    return format_pii_output(parsed_output.get("pii_entities", []))


if __name__ == "__main__":
    sample_text = (
        "Hello, my name is Nandini and my email is nandi@gmail.com "
        "or call 9876543210"
    )
    print(detect_pii(sample_text))
