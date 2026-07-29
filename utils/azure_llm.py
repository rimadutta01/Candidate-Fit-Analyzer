"""
Wraps the Azure OpenAI chat completion call and parses the JSON response
into a Python dict the Streamlit app can render directly.
"""

import json
from openai import AzureOpenAI

import config
from prompts.analysis_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


def _get_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_key=config.AZURE_OPENAI_API_KEY,
        azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
        api_version=config.AZURE_OPENAI_API_VERSION,
    )


def analyze_fit(cv_text: str, jd_text: str, job_role: str) -> dict:
    """
    Sends CV + JD + role to Azure OpenAI, returns a parsed dict matching
    the schema in prompts/analysis_prompt.py.
    Raises ValueError if the model doesn't return valid JSON.
    """
    client = _get_client()

    user_prompt = USER_PROMPT_TEMPLATE.format(
        job_role=job_role,
        jd_text=jd_text,
        cv_text=cv_text,
    )

    response = client.chat.completions.create(
        model=config.AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        response_format={"type": "json_object"},  # forces valid JSON output
    )

    raw_content = response.choices[0].message.content

    try:
        return json.loads(raw_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model did not return valid JSON: {e}\nRaw output: {raw_content}")