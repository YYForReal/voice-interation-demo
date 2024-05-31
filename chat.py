import requests
import json
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

# pip install --upgrade spark_ai_python


def spark_completion(messages):
    print("spark_completion")
    # 星火认知大模型Spark3.5 Max的URL值，其他版本大模型URL值请前往文档查看
    SPARKAI_URL = "wss://spark-api.xf-yun.com/v3.5/chat"
    
    # 星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台查看
    SPARKAI_APP_ID = "YOUR_SPARKAI_APP_ID"
    SPARKAI_API_SECRET = "YOUR_SPARKAI_API_SECRET"
    SPARKAI_API_KEY = "YOUR_SPARKAI_API_KEY"

    # 星火认知大模型Spark3.5 Max的domain值，其他版本大模型domain值请前往文档查看
    SPARKAI_DOMAIN = "general"

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
