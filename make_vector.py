

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
      "title": "基本プランの説明",
      "content": "基本プランは３つあります。スタンダードプランには、ヒント無料、管理者問い合わせの軟化、締め切り許容増加３日のオプションが付き、特典はなく価格は15万円です。アドバンスプランには、ヒント無料、管理者問い合わせの軟化、締め切り許容増加７日、APIキーの制限解除、講師の1対1対応のオプションが付き、特典としてcommmune内ポイント5000の付与、価格が25万円です。安心受講プランは、ヒント無料、管理者問い合わせの軟化、締め切り許容増加３０日、APIキーの制限解除、講師の１対１対応、いつでも24時間電話問い合わせのオプションが付き、特典としてcommmune内ポイント5000付与、バッジ作成権、模範解答横流し、弊社インターン確約があり、価格が40万円です。"
    },
    {
      "@search.action": "upload",
      "id": "2",
      "page": "6",
      "title": "各オプションの補償内容：ヒント無料",
      "content": "ヒントの使用にかかるデメリットを無くします。通常、ヒントを使用することで、講義内での評価が下がる仕組みとなっていますが、こちらのデメリットがなくなります。これにより、ご安心してヒントをご使用できます。"
    },
    {
      "@search.action": "upload",
      "id": "3",
      "page": "7",
      "title": "各オプションの補償内容：管理者問い合わせの軟化",
      "content": "管理者とのDMでの対応がより優しくなります。また、対応が全体的に寛大になります。これにより何か不具合があった時や、困った時に管理者へのお問い合わせの心理的ハードルを下げることができます。"
    },
    {
      "@search.action": "upload",
      "id": "4",
      "page": "8",
      "title": "各オプションの補償内容：締め切り許容増加",
      "content": "課題の提出期限を超過した場合でも、各プランでの許容日数分まで不問にしてもらえます。この締め切り許容は各課題で共有となっており、スタンダードプランであれば本講義を通して、合計３日までの期限超過が許容されます。プランの許容上限を超えて提出期限を超えた際には、通常通りのペナルティが発生します。"
    },
    {
      "@search.action": "upload",
      "id": "5",
      "page": "9",
      "title": "各オプションの補償内容：APIキー制限解除",
      "content": "APIキーの使用制限が解除されます。これにより、使用料を気にせずにAPIキーを使用することができます。ただし、意図的に使用料を著しく増加させるなどの悪質なご利用が確認された場合には、契約プランの解約、今後の受講のご案内を停止させていただく可能性がございます。"
    },
    {
    "@search.action": "upload",
    "id": "6",
    "page": "10",
    "title": "各プランの補償内容：講師の１対１対応",
    "content": "講師と１対１のオンラインMTGを設けることができます。週に2時間までご利用が可能であり、生成AI開発講義での疑問点の解消や、作業の場としてご活用していただくことができます。オフラインでのご要望や、講義に関連しない要件でのMTGは対応しかねます。"
    },
    {
    "@search.action": "upload",  
    "id": "7",
    "page": "11",
    "title": "各プランの補償内容：いつでも24時間電話問い合わせ",
    "content": "24時間年中無休でのご対応をいたします。講義でお困りの際に、いつでもタイムラグなしでご対応いたします。これにより、どの時間帯・タイムゾーンでも安心して受講が可能になります。"
    },
    { 
    "@search.action": "upload",
    "id": "8",
    "page": "13",
    "title": "特典内容：割引特典",
    "content": "本保険プランは、加入時に割引特典を用意しています。友達割・・・第一回「生成AI開発講義」受講生のご友人と同時に加入されることで、一人につき1万円の割引が行われます。こちらの適用は最大３人までとなります。紹介割・・・現在ExSeedに参加されていないご友人に紹介を行い、コミュニティへの参加が確認された場合、一人につき2万円の割引が行われます。こちらの適用は最大１人までとなります。これらの割引特典を利用することで、最大5万円の割引となります。"
    },
    { 
    "@search.action": "upload",
    "id": "9",
    "page": "14",
    "title": "特典内容：その他の特典内容",
    "content": "弊社が提供する保険プランでは、プランに応じた特典もございます。Commmune内ポイント付与：commmune内でポイントが付与され、バッジなどの獲得が促進されます。バッジ作成権：お好きな画像・条件を設定して、バッジを作成することができます。模範解答横流し：講義での模範解答を入手することができます。弊社インターン確約：講義終了後の、弊社インターンへの採用が確約されます。"
    },
    {
    "@search.action": "upload",
    "id": "10",
    "page": "16",
    "title": "よくあるご質問：よくあるご質問のQ＆A",
    "content": "Q、この保険プランは、次回の「生成AI開発講義」でも有効ですか？ A、いいえ、こちらの保険プランは現在受講されている第一回「生成AI開発講義」に適用されます。Q、講義開始後に、保険プランに加入した際の保険内容の調節などはありますか？ A、保険加入時の超過日数に応じて、キャッシュバックを行います。講義の残り日数分の費用に調節します。Q、オプションの個別の追加などは可能ですか？ A、現在、オプションの別売りなどは行っておりません。今後の開講予定の「生成AI開発講義」では、保険のオプションをより細分化し、個別での販売を行う予定です。"
    },
    {
    "@search.action": "upload",
    "id": "11",
    "page": "18",
    "title": "契約・資料請求をお求めの方",
    "content": "ご契約に進まれる方は、以下の日程調整フォームより、来社日時のご予約をお願いします。契約書類の記入は対面でのご案内のみとしているため、印鑑や身分証明書をご持参の上、オフィスまでお越しいただけますと幸いです。▼日程調整フォーム https://nittei-chosei/exseed/ ▼弊社連絡先 〒024-0306 東京都港区仮町20-2-4 超種ビル３階 TEL：不明 その他ご質問などある方は、以下の問い合わせフォームより記入をお願いします。▼お問い合わせフォーム https://toiawase/exseed/"
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

