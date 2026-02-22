import base64
import random
import requests
from app.openai_client import client
from app.config import FACEBOOK_PAGE_ID, PAGE_ACCESS_TOKEN, GRAPH_VERSION

# --- Scene Settings by Health Domain ---
DOMAIN_SCENES = {
    "হিজামা ও কাপিং থেরাপি": [
        "clean modern hijama clinic interior with treatment bed",
        "calm river bank with hijama cupping jars on a wooden surface",
        "sea beach at golden hour with cupping sets on a stone",
        "lush green garden with hijama tools on a woven mat",
        "misty forest path with cupping jars on a rustic tray",
        "rooftop garden at sunset with hijama equipment neatly placed",
    ],
    "মানসিক স্বাস্থ্য ও স্ট্রেস ম্যানেজমেন্ট": [
        "peaceful zen garden with smooth stones and flowing water",
        "cozy indoor space with candles and soft warm lighting",
        "open countryside meadow with wildflowers at sunrise",
        "misty lakeside with morning calm and soft reflections",
        "serene rooftop with city lights and a starry sky",
    ],
    "ব্যথা ব্যবস্থাপনা — ঘাড়, কোমর, হাঁটু": [
        "minimalist wellness clinic with treatment tools on a tray",
        "calm natural landscape with therapeutic herbs on a wooden table",
        "clean white medical room with soft warm lighting",
        "traditional Bangladeshi courtyard with herbal remedies",
    ],
    "রোগ প্রতিরোধ ক্ষমতা বৃদ্ধি": [
        "vibrant vegetable and herb garden in morning light",
        "tropical rainforest with sunlight breaking through trees",
        "open meadow with wildflowers and clear blue sky",
        "fresh farmer's market with natural produce and herbs",
    ],
    "ডায়াবেটিস সচেতনতা ও প্রতিরোধ": [
        "clean modern clinic interior with wellness tools",
        "a peaceful garden with fresh vegetables and herbs",
        "minimalist white surface with natural health objects",
        "serene countryside with morning mist and green fields",
    ],
    "উচ্চ রক্তচাপ ও হৃদরোগ সচেতনতা": [
        "calm sea at sunrise with gentle waves",
        "peaceful green park with trees and open sky",
        "serene mountain valley with soft morning light",
        "quiet indoor space with plants and natural light",
    ],
    "হজম ও গ্যাস্ট্রিক সমস্যা": [
        "rustic kitchen with natural herbs and spices on a wooden table",
        "traditional village setting with clay pots and medicinal plants",
        "outdoor market with fresh fruits and herbal ingredients",
        "garden setting with digestive herbs and natural elements",
    ],
    "ঘুমের সমস্যা ও ইনসোমনিয়া": [
        "cozy bedroom corner with moonlight through the window",
        "calm lakeside with stars and night sky reflection",
        "peaceful indoor space with dim candlelight and soft textures",
        "misty forest at twilight with soft blue tones",
    ],
    "থাইরয়েড ও হরমোনজনিত সমস্যা": [
        "clean modern clinic with soft lighting and medical tools",
        "natural wellness space with herbs and organic elements",
        "serene garden with calming greenery and morning light",
    ],
    "মাইগ্রেন ও দীর্ঘস্থায়ী মাথাব্যথা": [
        "quiet dark room with a single soft light and lavender sprigs",
        "peaceful garden at dusk with cool blue and purple tones",
        "misty mountain top with cool calm atmosphere",
        "indoor wellness corner with essential oils and calming objects",
    ],
    "নারী স্বাস্থ্য — মাসিক সমস্যা, পিসিওএস": [
        "soft floral garden with pastel tones and morning dew",
        "cozy wellness space with flowers, candles and warm light",
        "peaceful indoor setting with natural feminine elements",
        "lush garden with medicinal herbs and soft sunlight",
    ],
    "চর্মরোগ ও ত্বকের যত্ন": [
        "flat lay of natural skincare herbs and oils on marble",
        "garden with aloe vera, neem, and medicinal plants",
        "clean white surface with natural skin wellness ingredients",
        "outdoor setting with fresh flowers and herbal elements",
    ],
    "কিডনি ও লিভার স্বাস্থ্য সচেতনতা": [
        "clear mountain stream with clean fresh water and stones",
        "minimalist medical wellness space with clean tones",
        "natural spring water setting with herbs nearby",
        "serene river bank with purifying plant elements",
    ],
    "শিশু স্বাস্থ্য ও পুষ্টি": [
        "colorful vegetable garden with fresh produce in sunlight",
        "bright outdoor park with natural greenery",
        "cheerful natural setting with fruits and fresh herbs",
        "cozy indoor space with nutritious food elements",
    ],
    "বয়স্কদের স্বাস্থ্য ও আর্থ্রাইটিস": [
        "peaceful garden bench surrounded by mature trees",
        "calm countryside path with autumn leaves and soft light",
        "traditional courtyard with terracotta pots and herbs",
        "serene lakeside at golden hour with warm tones",
    ],
    "ডিটক্সিফিকেশন ও শরীর পরিশোধন": [
        "clear river with stones and fresh flowing water",
        "flat lay of detox herbs, lemon, and natural ingredients",
        "lush green forest with sunlight filtering through",
        "clean minimalist spa-like setting with organic elements",
    ],
    "পুষ্টি ও সুষম খাদ্যাভ্যাস": [
        "vibrant farmer's market with colorful fresh produce",
        "rustic wooden table with assorted natural foods and herbs",
        "lush vegetable garden with morning dew",
        "clean kitchen counter with whole natural ingredients",
    ],
    "শারীরিক কার্যকলাপ ও সক্রিয় জীবনযাপন": [
        "open park with green fields and morning sunlight",
        "mountain trail with clear sky and fresh air",
        "riverside path surrounded by trees",
        "open rooftop with city skyline and blue sky",
    ],
    "প্রাকৃতিক ও বিকল্প চিকিৎসা পদ্ধতি": [
        "traditional healing space with herbal jars and natural tools",
        "rustic wooden shelf with medicinal herbs and cupping jars",
        "outdoor herbal garden with traditional medicine elements",
        "natural wellness setup with cupping tools and organic materials",
    ],
    "সাধারণ স্বাস্থ্য সচেতনতা": [
        "open green landscape with clear sky and fresh air",
        "peaceful nature setting with sunlight and greenery",
        "clean modern wellness space with plants and soft lighting",
        "traditional Bangladeshi village with paddy fields and morning mist",
    ],
}


POST_TYPE_PROPS = {
    "সমস্যা সচেতনতা (Problem Awareness)": [
        "wilted plant beside a healthy one with hijama cupping jars nearby",
        "dark stormy clouds transitioning to sunlight with cupping sets on a stone surface",
        "dried cracked earth beside a green patch with glass cupping jars placed nearby",
        "neglected medicinal herbs beside fresh ones with a hijama kit in the background",
    ],
    "সমাধান শিক্ষামূলক পোস্ট (Solution Education)": [
        "hijama cupping jars with medicinal herbs and essential oils neatly arranged",
        "cupping therapy tools with natural ingredients and dried herbs on a wooden surface",
        "herbal remedies and hijama cupping set displayed on a clean tray with flowers",
        "glass cupping jars beside medicinal plants and a bowl of natural herbs",
        "hijama kit with labeled herbal jars and wellness tools on a marble surface",
    ],
    "বিশ্বাস তৈরির পোস্ট (Trust Building)": [
        "clean organized hijama clinic tools with sterilized cupping sets on a professional tray",
        "neatly arranged cupping therapy jars and medical-grade tools on a clinical surface",
        "professional hijama equipment with sealed sterile packs and herbal oils",
        "glass cupping jars with antiseptic tools and fresh herbs in a clean clinical setup",
    ],
    "রোগীর সাফল্যের গল্প (Success Story)": [
        "bright sunlight breaking through clouds with blooming flowers and hijama cupping jars",
        "fresh green plants thriving with a hijama kit placed beside them in natural light",
        "blooming flower garden with cupping therapy tools on a wooden surface nearby",
        "sunrise landscape with hijama tools and medicinal herbs glowing in warm light",
    ],
    "মিথ ভাঙা (Myth Busting)": [
        "traditional glass cupping jars beside modern medical tools on a split surface",
        "ancient hijama cupping set alongside contemporary wellness equipment",
        "traditional herbal remedies and cupping jars beside scientific medical instruments",
        "old and new healing tools — hijama jars and modern therapy devices side by side",
    ],
    "সীমিত অফার / আর্জেন্সি পোস্ট (Urgency & Offer)": [
        "calendar with hijama cupping tools and seasonal flowers on a clean surface",
        "hijama kit with seasonal herbs and a soft warm glow suggesting limited time",
        "cupping jars with a countdown-themed arrangement of flowers and wellness objects",
        "neatly packed hijama set with fresh herbs suggesting a special occasion",
    ],
    "মৌসুমী স্বাস্থ্য সতর্কতা (Seasonal Health Alert)": [
        "seasonal landscape with hijama cupping jars and medicinal herbs on a stone",
        "weather-themed natural setting with cupping tools and seasonal fruits nearby",
        "seasonal flowers and herbs with a hijama kit on a rustic wooden surface",
        "rain-soaked or sun-drenched scene with glass cupping jars and herbal remedies",
    ],
    "আত্মিক ও শান্তিপূর্ণ": [
        "prayer beads and hijama cupping jars on a soft linen cloth in warm light",
        "open Quran beside traditional hijama tools and rose petals in soft candlelight",
        "incense, herbal oils and hijama cupping set in a peaceful corner with soft glow",
        "tasbeeh and glass cupping jars on a prayer mat with natural morning light",
    ],
    "FAQ স্টাইল পোস্ট": [
        "hijama cupping jars with small herb labels and organized tools on a clean surface",
        "neatly arranged cupping set with question-themed visual — open book and herbs",
        "hijama toolkit displayed like an educational flat lay with medicinal ingredients",
    ],
    "সামাজিক প্রমাণ পোস্ট (Social Proof)": [
        "multiple cupping jars neatly lined up suggesting many sessions and trust",
        "hijama tools with a warm welcoming clinic background and fresh flowers",
        "organized hijama workspace with professional tools and calming herbal elements",
    ],
    "লাইফস্টাইল ও প্রতিরোধমূলক স্বাস্থ্য পোস্ট": [
        "hijama cupping set beside fresh vegetables, herbs and natural wellness items",
        "cupping jars with morning tea, medicinal herbs and a calm natural background",
        "hijama tools alongside yoga mat, herbs and natural lifestyle objects",
    ],
    "স্বাস্থ্য টিপস — দ্রুত ও কার্যকর (Quick Health Tip)": [
        "hijama cupping jars with a few key herbs and minimalist clean background",
        "compact hijama kit with one or two medicinal herbs in sharp focused lighting",
        "single glass cupping jar with fresh herb sprigs on a marble surface",
    ],
    "ভুল ধারণা সংশোধন (Common Misconception Fix)": [
        "hijama cupping jars with a clear clean professional setup dispelling doubt",
        "traditional cupping tools beside a calm reassuring natural background",
        "glass cupping jars with medicinal herbs showing safety and cleanliness",
    ],
    "রোগের প্রাথমিক লক্ষণ চেনা (Early Warning Signs)": [
        "hijama tools beside a fading plant transitioning to healthy greenery",
        "cupping jars with seasonal herbs suggesting early care and prevention",
        "glass cupping set with warning-colored flowers like red and yellow in nature",
    ],
    "বিজ্ঞান ও ঐতিহ্যবাহী চিকিৎসার মিল (Science + Tradition)": [
        "traditional hijama glass jars beside modern medical reference books and herbs",
        "ancient cupping tools and contemporary wellness equipment on a split wooden surface",
        "hijama cupping set with botanical herb charts and natural science elements",
    ],
    "সার্ভিস পরিচিতি — নরম প্রমোশন (Soft CTA)": [
        "inviting hijama clinic setup with cupping tools, fresh flowers and soft lighting",
        "welcoming wellness space with hijama kit and calming herbal arrangement",
        "neatly laid out hijama tools on a treatment table with warm ambient light",
    ],
    "তুলনামূলক পোস্ট — প্রাকৃতিক vs ওষুধনির্ভর চিকিৎসা": [
        "hijama cupping jars on one side and pharmaceutical pills on the other in nature",
        "natural herbs and cupping tools contrasted with synthetic medicine on a split surface",
        "glass cupping set beside medicinal plants contrasting with clinical white pills",
    ],
    "আগে-পরের অভিজ্ঞতা (Before & After Story)": [
        "wilted plant transforming to blooming flower with hijama cupping jars beside it",
        "dark moody background transitioning to bright sunlight with cupping tools in frame",
        "dried herbs on one side and fresh blooming ones on the other with a hijama kit",
    ],
    "জরুরি স্বাস্থ্য সতর্কতা (Health Warning)": [
        "stormy sky with hijama cupping tools and warning-colored herbs on a stone",
        "dark dramatic lighting with cupping jars and red medicinal flowers nearby",
        "urgent natural scene with hijama kit and seasonal warning elements",
    ],
    "কৌতূহল জাগানো প্রশ্ন পোস্ট (Curiosity Hook)": [
        "mysterious close-up of hijama cupping jars with soft bokeh background",
        "partially revealed hijama tools with dramatic lighting creating curiosity",
        "single glass cupping jar with an intriguing arrangement of herbs and shadows",
    ],
}

SURFACE_DETAILS = [
    "on a wooden table",
    "on a marble surface",
    "on a clay surface",
    "on a stone slab",
    "on a woven mat",
    "on a white linen cloth",
    "on a rustic tray",
    "on a bamboo surface",
]

IMAGE_MOODS = [
    "warm and healing",
    "calm and professional",
    "natural and organic",
    "modern and clinical",
    "spiritual and peaceful",
    "fresh and energetic",
    "soft and comforting",
    "earthy and grounded",
]

SEASON_LIGHTING = {
    "শীতকাল": "soft winter morning fog and golden light",
    "গ্রীষ্মকাল": "bright sunny summer daylight with warm tones",
    "বর্ষাকাল": "rainy day with lush green background and cool tones",
    "শরৎকাল": "clear autumn sky with soft diffused golden light",
}


def build_image_prompt(health_domain: str = "", post_type: str = "", season: str = "", emotion: str = "") -> str:
    # Pick scene based on health domain
    scenes = DOMAIN_SCENES.get(health_domain, DOMAIN_SCENES["সাধারণ স্বাস্থ্য সচেতনতা"])
    scene = random.choice(scenes)

    # Pick props based on post type, fallback to generic
    props_list = POST_TYPE_PROPS.get(post_type, POST_TYPE_PROPS["সমাধান শিক্ষামূলক পোস্ট (Solution Education)"])
    props = random.choice(props_list)

    surface = random.choice(SURFACE_DETAILS)
    mood = random.choice(IMAGE_MOODS)
    lighting = SEASON_LIGHTING.get(season, "natural soft lighting")

    prompt = (
        f"{scene}, with {props} {surface}. "
        f"Mood: {mood}. "
        f"Lighting: {lighting}. "
        f"No humans, no animals, no text, no watermarks. "
        f"High quality, 4k, professional health and wellness photography."
    )

    return prompt


def generate_image(health_domain: str = "", post_type: str = "", season: str = "", emotion: str = "") -> bytes:
    """Returns raw image bytes"""
    prompt = build_image_prompt(health_domain, post_type, season, emotion)

    response = client.images.generate(
        model="gpt-image-1-mini",
        prompt=prompt,
        size="1024x1024",
        quality='high',
        n=1
    )

    image_bytes = base64.b64decode(response.data[0].b64_json)
    return image_bytes


def upload_image_to_facebook(image_bytes: bytes, page_id: str, access_token: str) -> str:
    """Upload raw image bytes to Facebook and return photo ID"""
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{page_id}/photos"

    response = requests.post(
        url,
        data={"published": "false", "access_token": access_token},
        files={"source": ("image.png", image_bytes, "image/png")}
    )

    if response.status_code != 200:
        raise Exception(f"Facebook Image Upload Error: {response.text}")

    return response.json().get("id")