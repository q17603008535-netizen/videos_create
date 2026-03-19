from openai import OpenAI
import os
from typing import Dict
import json

QWEN_API_KEY = os.getenv("QWEN_API_KEY")
QWEN_BASE_URL = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/api/v1")

def review_content(content: str, platform: str = "douyin") -> Dict:
    """Review content for platform suitability"""
    client = OpenAI(api_key=QWEN_API_KEY, base_url=QWEN_BASE_URL)
    
    prompt = f"""请审核以下内容是否适合发布到{platform}平台：

内容：
{content}

请从以下维度评估（JSON 格式）：
{{
    "originality_score": 85,
    "compliance": "pass",
    "appeal_score": "high",
    "completion_rate_prediction": "high",
    "sensitive_words": [],
    "suggestions": ["修改建议 1"],
    "overall_recommendation": "recommend"
}}
"""
    
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": prompt}],
        extra_body={"enable_search": True}
    )
    
    result = response.choices[0].message.content
    return json.loads(result)
