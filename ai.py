import requests
from decouple import config
import json

api_key = config("OPENAI_API_KEY")

def get_details(base64_image, question):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "low"
                            }
                        }
                    ]
                }
            ],
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        # print("Response status code:", response.status_code)
        # print("Response content:", response.content)

        result = response.json()
        if "choices" in result:
            details = result["choices"][0]["message"]["content"]
            details = details.replace("```json\n", "").replace("\n```", "")
            return json.loads(details)
            # return details
        else:
            return "Failed to get details"
    
    except Exception as e:
        print("An error occurred:", e)
        return "Failed to get details due to an error"
