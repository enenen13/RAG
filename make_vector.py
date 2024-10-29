

import os
from azure.search.documents import _search_client
from azure.core.credentials import AzureKeyCredential
from typing import Optional,Any, List ,Tuple
from openai import OpenAI
from azure.search.documents import SearchClient
from dotenv import load_dotenv
dotenv_path = '/root/app/RAGchatbot_App/.env.dev'
load_dotenv(dotenv_path=dotenv_path)
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

#indexの名前
index_name =  "endo001"


# Azure Search サービスの設定
endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
admin_api_key = os.getenv("AZURE_AI_SEARCH_API_KEY")


def init_openai():
    """
    openaiの機能を使うためのクライアントを作成するよ
    Returns:
        openai_client (OpenAI): openaiのクライアント
    """
    assert (
        "OPENAI_EMBEDDING_MODEL" in os.environ
    ), "OPENAI_EMBEDDING_MODEL environment variable is not set"
    assert (
        "OPENAI_CHAT_COMPLETION_MODEL" in os.environ
    ), "OPENAI_CHAT_COMPLETION_MODEL environment variable is not set"
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return openai_client


def create_embedding(text: str) -> Optional[List[float]]:
    """
    貰った質問文に対して、openai機能を使って、ベクトル化したものを返すよ
    Args:
        text (str): ユーザーからの質問文
    Returns:
        embedding (List[float]): ベクトル化された質問文
    """
    openai_client = init_openai()
    try:
        response = (
            openai_client.embeddings.create(
                input=[text],
                model=os.getenv("OPENAI_EMBEDDING_MODEL", None),
            )
            .data[0]
            .embedding
        )
        return response
    except Exception:
        logger.error("embeddingの作成中にエラーが発生しました in create_embedding", exc_info=True)
        return None

# データのアップロード
search_client = SearchClient(endpoint, index_name, AzureKeyCredential(admin_api_key))

"""
ここにインデックスデータをアップロード（chatGPTなど）
"""

search_index_data = [
    {
      "@search.action": "upload",
      "id": "1",
      "page": "4",
      "title": "基本プラン",
      "content": "具体的な内容を異常のようなkey:valueで追加"
    }
]



# 検索インデックスのデータをfor文で処理し、各contentをベクトル化して更新する例
import time

for i in range(len(search_index_data)):
    item = search_index_data[i]
    content_text = item["content"]
    vector_content = create_embedding(content_text)
    if vector_content is not None:
        item["vector_content"] = vector_content
    else:
        item["vector_content"] = []  # ベクトル化に失敗した場合は空のリストを割り当てる

    # 更新された検索インデックスデータを確認
    print(item)

    # Wait for 2 seconds
    time.sleep(1)

    

# データのアップロード

# ベクトルデータをカンマ区切りの文字列に変換する関数
def vector_to_string(vector):
    return ','.join(map(str, vector))

for i in range(len(search_index_data)):
    item = search_index_data[i]
    if 'vector_content' in item:
        item['vector_content'] = vector_to_string(item['vector_content'])
    else:
        item["vector_content"] = [] 
    time.sleep(1)


print(search_index_data)

