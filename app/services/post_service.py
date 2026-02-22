from app.openai_client import client
from app.config import FACEBOOK_PAGE_ID, OPENAI_MODEL, PAGE_ACCESS_TOKEN
from app.prompt_engine import SYSTEM_PROMPT, build_user_prompt
from app.schemas import GenerateAndPostRequest
from app.services.image_service import generate_image, upload_image_to_facebook
from app.utils.variation import random_variation
from app.services.facebook_service import post_to_facebook

# def generate_and_post(data):
#     variation = random_variation()

#     data.post_type = data.post_type or variation["post_type"]
#     data.emotion = data.emotion or variation["emotion"]
#     data.audience = data.audience or variation["audience"]
#     data.angle = data.angle or variation["angle"]

    
#     response = client.chat.completions.create(
#         model='gpt-4.1',
#         messages=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user", "content": build_user_prompt(data)}
#         ],
#         temperature=0.9,
#         top_p=0.9,
#         presence_penalty=0.6,
#         frequency_penalty=0.5
#     )

#     content = response.choices[0].message.content
#     fb_result = post_to_facebook(content)


#     return {
#         "content": content,
#         "facebook_post_id": fb_result.get("id")
#     }


def generate_and_post(data):
    # --- 1. Normalize input ---
    if isinstance(data, dict):
        data = GenerateAndPostRequest(**data)

    # --- 2. Fill missing fields from random variation ---
    variation = random_variation()
    data.health_domain  = data.health_domain  or variation["health_domain"]
    data.post_type      = data.post_type      or variation["post_type"]
    data.emotion        = data.emotion        or variation["emotion"]
    data.audience       = data.audience       or variation["audience"]
    data.content_format = data.content_format or variation["content_format"]
    data.cta_style      = data.cta_style      or variation["cta_style"]
    data.trust_signal   = data.trust_signal   or variation["trust_signal"]
    data.content_goal   = data.content_goal   or variation["content_goal"]

    # --- 3. Generate post text and image in parallel ---
    import concurrent.futures

    def generate_text():
        response = client.chat.completions.create(
            model='gpt-4.1',
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(data, variation)}
            ],
            temperature=0.9,
            top_p=0.9,
            presence_penalty=0.6,
            frequency_penalty=0.5
        )
        return response.choices[0].message.content

    def generate_img():
        return generate_image(
            health_domain=data.health_domain,
            post_type=data.post_type,
            season=variation["season"],
            emotion=data.emotion
        )

    with concurrent.futures.ThreadPoolExecutor() as executor:
        text_future  = executor.submit(generate_text)
        image_future = executor.submit(generate_img)

        content      = text_future.result()
        image_bytes  = image_future.result()   # bytes, not URL

    photo_id = upload_image_to_facebook(image_bytes, FACEBOOK_PAGE_ID, PAGE_ACCESS_TOKEN)
    fb_result = post_to_facebook(content, photo_id=photo_id)

    return {
        "content": content,
        "facebook_post_id": fb_result.get("id")
    }