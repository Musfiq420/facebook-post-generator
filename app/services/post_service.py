from app.openai_client import client
from app.config import OPENAI_MODEL
from app.prompt_engine import SYSTEM_PROMPT, build_user_prompt
from app.utils.variation import random_variation
from app.services.facebook_service import post_to_facebook

def generate_and_post(data):
    variation = random_variation()

    data.post_type = data.post_type or variation["post_type"]
    data.emotion = data.emotion or variation["emotion"]
    data.audience = data.audience or variation["audience"]
    data.angle = data.angle or variation["angle"]

    
    response = client.chat.completions.create(
        model='gpt-4.1',
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(data)}
        ],
        temperature=0.9,
        top_p=0.9,
        presence_penalty=0.6,
        frequency_penalty=0.5
    )

    content = response.choices[0].message.content
    fb_result = post_to_facebook(content)


    return {
        "content": content,
        "facebook_post_id": fb_result.get("id")
    }