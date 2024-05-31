import requests
import json
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
# pip install --upgrade spark_ai_python

# 读取配置文件
with open('config.json', 'r') as f:
    config = json.load(f)

def spark_completion(messages):
    print("spark_completion")
    # 读取配置项
    SPARKAI_URL = config["SPARKAI_URL"]
    SPARKAI_APP_ID = config["SPARKAI_APP_ID"]
    SPARKAI_API_SECRET = config["SPARKAI_API_SECRET"]
    SPARKAI_API_KEY = config["SPARKAI_API_KEY"]
    SPARKAI_DOMAIN = config["SPARKAI_DOMAIN"]

    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )

    # Convert messages to the format required by ChatSparkLLM
    formatted_messages = [
        ChatMessage(role=msg["role"], content=msg["content"]) for msg in messages
    ]

    handler = ChunkPrintHandler()

    response = spark.generate([formatted_messages], callbacks=[handler])

    if response:
        print("response: ", response)
        return response
    else:
        return None


# # Example usage:
if __name__ == "__main__":
    messages = [{"role": "user", "content": "你好呀"}]
    result = spark_completion(messages)
    print(result)
