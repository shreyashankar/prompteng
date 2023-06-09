from motion import Component

from components.params import LLMRequest

import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_version = "2023-05-15"

TravelAgent = Component("TravelAgent")
PRICE_PER_TOKEN = float(0.002 / 1000.0)


@TravelAgent.init_state
def init_state(prompt_template: str):
    assert (
        "{example}" in prompt_template
    ), "Prompt template must contain {example}"

    return {
        "prompt_template": prompt_template,
        "system_message": "You are a professional travel agent.",
        "cost": 0.0,
    }


@TravelAgent.infer("example")
async def run_llm(state, value: LLMRequest):
    response = await openai.ChatCompletion.acreate(
        engine="gpt-35-turbo",
        messages=[
            {
                "role": "system",
                "content": state["system_message"],
            },
            {
                "role": "user",
                "content": state["prompt_template"].format(
                    example=value.place
                ),
            },
        ],
    )
    reply = response["choices"][0]["message"]["content"]
    cost = float(response["usage"]["total_tokens"]) * PRICE_PER_TOKEN
    return {
        "example": value.place,
        "template": state["prompt_template"],
        "reply": reply,
        "cost": cost,
    }
