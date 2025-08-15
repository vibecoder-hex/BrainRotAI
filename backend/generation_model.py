import aiohttp, asyncio, decouple


class YandexArtAPI:
    def __init__(self, prompt, api_key, image_ratio):
        self.API = api_key
        self.TEXT = prompt
        self.api_url = "https://llm.api.cloud.yandex.net"
        self.width_ratio, self.height_ratio = image_ratio[0], image_ratio[1]
        
    def response_body(self):
        return {
                    "modelUri": "art://b1glcms1jv2gp6q57vlh/yandex-art/latest",
                    "generationOptions": {
                    "aspectRatio": {
                        "widthRatio": self.width_ratio,
                        "heightRatio": self.height_ratio
                    }
                    },
                    "messages": [
                    {
                        "weight": "1",
                        "text": self.TEXT
                    }
                    ]
        }
    
    def headers_body(self):
        return {"Authorization": f"Api-Key {self.API}"}


async def generate(text, image_ratio):
    async with aiohttp.ClientSession() as session:
        yandexart = YandexArtAPI(prompt=text, api_key=decouple.config("SECRET_KEY"), image_ratio=image_ratio)
        genapi_url = f"{yandexart.api_url}/foundationModels/v1/imageGenerationAsync"
        async with session.post(genapi_url, headers=yandexart.headers_body(), json=yandexart.response_body()) as response:
            json_response = await response.json()
            response_id = json_response['id']
            result_url = f"{yandexart.api_url}:443/operations/{response_id}"
            attempt_count = 5
            for _ in range(attempt_count, 0, -1):
                async with session.get(result_url, headers=yandexart.headers_body()) as result_response:
                    result_json = await result_response.json()
                    if result_json['done']:
                        image_code = result_json['response']['image']
                        return image_code
                await asyncio.sleep(10)