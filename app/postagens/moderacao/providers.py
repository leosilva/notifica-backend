import os
from typing import final

import httpx
from dotenv import load_dotenv

_ = load_dotenv()


@final
class DeepseekClient:
    client = httpx.Client(
        base_url='https://api.deepseek.com',
        headers={
            'Authorization': f'Bearer {os.getenv("DEEPSEEK_API_KEY")}'
        },
        timeout=15
    )

    @classmethod
    def chat(cls, messages: list[dict[str, str]]):
        res = cls.client.post(
            url='/chat/completions',
            json={
                'model': 'deepseek-v4-flash',
                'messages': messages,
                'thinking': {'type': 'disabled'}
            }
        )
        _ = res.raise_for_status()

        return res.json()['choices'][0]['message']['content']
