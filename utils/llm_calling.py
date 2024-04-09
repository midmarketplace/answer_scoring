from typing import Literal, Optional


def llm_calling(
        user_prompt: str,
        system_prompt: Optional[str] = "You are a Large Language Model. You answer questions",
        llm_model="gpt-4-turbo-preview" | Optional[Literal['gpt-4-turbo-preview', 'gpt-4']],
        temperature: Optional[float] = 1,  # 0 to 2
        max_tokens: Optional[int] = 4095,  # 1 to 4095
        top_p: Optional[float] = 1,  # 0 to 1
        frequency_penalty: Optional[float] = 0,  # 0 to 2
        presence_penalty: Optional[float] = 0  # 0 to 2
) -> str:
    if not (1 <= max_tokens <= 4095):
        raise ValueError("`max_tokens` must be between 1 and 4095, inclusive.")

    from openai import OpenAI
    client = OpenAI()

    response = client.chat.completions.create(
        model=llm_model,
        messages=[
            {
                "role": "system",
                "content": f"{system_prompt}"
            },
            {
                "role": "user",
                "content": f"{user_prompt}"
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    return response.choices[0].message.content
