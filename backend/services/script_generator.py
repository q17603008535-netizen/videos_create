from openai import OpenAI
import os
from typing import Dict
import json

QWEN_API_KEY = os.getenv("QWEN_API_KEY")
QWEN_BASE_URL = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/api/v1")


def generate_script(content: str) -> Dict:
    """Generate final script with directions in Markdown"""
    client = OpenAI(api_key=QWEN_API_KEY, base_url=QWEN_BASE_URL)
    
    prompt = f"""请将以下内容转化为详细的逐字稿：

内容：
{content}

请以 JSON 格式返回：
{{
    "markdown": "完整的 Markdown 格式逐字稿，包含：
# 标题

## 【开场 - 语气：轻松好奇】
台词内容...
（重点：停顿 2 秒，眼神直视镜头）

## 【观点 1 - 语气：严肃】
台词内容...
（原因：制造反差）
",
    "titles": ["标题 1", "标题 2", ...],
    "tags": ["标签 1", "标签 2", ...],
    "publish_time_suggestion": "晚 19-21 点",
    "cover_text": "封面文案"
}}
"""
    
    response = client.chat.completions.create(
        model="qwen-flash",
        messages=[{"role": "user", "content": prompt}]
    )
    
    result = response.choices[0].message.content
    return json.loads(result)
