from openai import OpenAI
import os
from typing import Dict, List
import json

# Initialize Qwen client
QWEN_API_KEY = os.getenv("QWEN_API_KEY")
QWEN_BASE_URL = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/api/v1")


def analyze_content(text: str) -> Dict:
    """Analyze transcribed content using Qwen"""
    client = OpenAI(api_key=QWEN_API_KEY, base_url=QWEN_BASE_URL)
    
    prompt = f"""请分析以下视频转录内容：

{text}

请以 JSON 格式返回：
{{
    "key_points": ["重点 1", "重点 2", ...],
    "main_topic": "核心主题",
    "summary": "200 字以内的内容摘要",
    "tags": ["标签 1", "标签 2", ...],
    "target_audience": "目标受众"
}}
"""
    
    response = client.chat.completions.create(
        model="qwen-flash",
        messages=[{"role": "user", "content": prompt}],
        extra_body={"enable_search": True}
    )
    
    result = response.choices[0].message.content
    return json.loads(result)
