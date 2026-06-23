from openai import OpenAI


def chat(
    model_name,
    base_url,
    api_key,
    messages,
    temperature
):

    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=temperature
    )

    return response.choices[0].message.content