#検索インデックスの提出

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes.models import (
    ComplexField,
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchFieldDataType,
    
)
import os
from azure.search.documents import _search_client
from dotenv import load_dotenv
dotenv_path = '/root/app/RAGchatbot_App/.env.dev'
load_dotenv('.env.dev') 

endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
admin_api_key = os.getenv("AZURE_AI_SEARCH_API_KEY")


"""
インデックスを削除したい
"""

index_name =  "endo001"

# インデックスクライアントの作成
index_client = SearchIndexClient(endpoint, AzureKeyCredential(admin_api_key))

try:
    index_client.delete_index(index_name)
    print("インデックスの削除に成功しました。")
except Exception as e:
    print("インデックスの削除に失敗しました。")
    print("エラー詳細：", str(e))

