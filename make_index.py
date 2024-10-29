
#検索インデックスの提出

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes.models import (
    ComplexField,
    SearchIndex,
    SimpleField,
    SearchField,
    SearchableField,
    SearchFieldDataType,
)
import os
from azure.search.documents import _search_client
from dotenv import load_dotenv
dotenv_path = '/root/app/RAGchatbot_App/.env.dev'
load_dotenv(dotenv_path=dotenv_path)
"""
インデックスを作成
"""

#　インデックスの名前
index_name =  "endo001"

# Azure Search サービスの設定
endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
admin_api_key = os.getenv("AZURE_AI_SEARCH_API_KEY")

# インデックスクライアントの作成
index_client = SearchIndexClient(endpoint, AzureKeyCredential(admin_api_key))

# インデックスの定義
from azure.search.documents.indexes.models import SimpleField, SearchableField, SearchFieldDataType

index = SearchIndex(
    name=index_name,
    fields=[
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="page", type=SearchFieldDataType.String, filterable=True, sortable=True),
        SearchableField(name="title", type=SearchFieldDataType.String, sortable=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SearchField(name="contentVector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True, dimensions=1536, vector_search_configuration={"profile_name": "myHnswProfile"}),
])

vector_search = VectorSearch(
    algorithms=[
        HnswAlgorithmConfiguration(
            name="myHnsw"
        )
    ],
    profiles=[
        VectorSearchProfile(
            name="myHnswProfile",
            algorithm_configuration_name="myHnsw",
        )
    ]
)

semantic_config = SemanticConfiguration(
    name="my-semantic-config",
    prioritized_fields=SemanticPrioritizedFields(
        title_field=SemanticField(field_name="title"),
        keywords_fields=[SemanticField(field_name="category")],
        content_fields=[SemanticField(field_name="content")]
    )
)



# インデックスの作成
index_client.create_index(index)

#作成したインデックスの確認
result = index_client.get_index(index_name)
print(result)