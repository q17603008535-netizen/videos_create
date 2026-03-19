from openai import OpenAI
import os
from typing import Dict, List
import json

# Initialize DeepSeek client
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")


def rewrite_content(text: str, analysis: Dict) -> List[Dict]:
    """Generate 3 rewrite versions using DeepSeek"""
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
    
    prompt = f"""请对以下内容进行二创改写，生成 3 个不同表达方式的版本：

原内容：
{text}

内容分析：
{json.dumps(analysis, ensure_ascii=False)}

要求：
1. 每个版本都要换语法、换口吻、换比喻方式
2. 保持核心观点不变
3. 版本 1：轻松幽默风格
4. 版本 2：严肃专业风格
5. 版本 3：故事叙述风格

请以 JSON 数组格式返回：
[
    {{"style": "轻松幽默", "content": "改写内容 1"}},
    {{"style": "严肃专业", "content": "改写内容 2"}},
    {{"style": "故事叙述", "content": "改写内容 3"}}
]
"""
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )
    
    result = response.choices[0].message.content
    return json.loads(result)
