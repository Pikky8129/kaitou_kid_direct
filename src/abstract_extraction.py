import json
import logging
import time
import os
from datetime import datetime

from openai import OpenAI


###############################################################################################
# 設定
###############################################################################################
# コンテキスト　ファイルパス
context_file_path_1 = "input/context/Header_and_Abst_and_Footer_03.txt"

# 回答　ファイルパス
answer_file_path_1 = "output/Abstract_only_03.txt"

# インプットフォルダを確認
if not os.path.exists("./input"):
    os.makedirs("./input")

if not os.path.exists("./input/context"):
    os.makedirs("./input/context")

# アウトプットフォルダを確認
if not os.path.exists("./output"):
    os.makedirs("./output")

# 現在の日時を取得
now = datetime.now()
now_string = f"{now.year}{now.month:02d}{now.day:02d}{now.hour:02d}{now.minute:02d}"


class AbstractExtractionUseCase:
    """
    コンテキストからアブストラクトを抽出するクラス
    """

    # def __init__(self) -> None:
    # self._logger = logging.getLogger(__name__)

    def execute(self, context: str) -> str:
        """
        コンテキストからアブストラクトを抽出する

        Parameters
        ----------
        context : str
            コンテキスト

        Returns
        -------
        str
            アブストラクト
        """

        # self._logger.info("Abstract extraction started.")
        print("Abstract extraction started.")

        # コンテキストからアブストラクトを抽出する
        abstract = self._extract_abstract_from_text(context)

        # self._logger.info("Abstract extraction finished.")
        print("Abstract extraction finished.")

        return abstract

    def _extract_abstract_from_text(self, context: str) -> str:
        """
        コンテキストからアブストラクトを抽出する

        Parameters
        ----------
        context : str
            コンテキスト

        Returns
        -------
        str
            アブストラクト
        """

        # メッセージリストを定義
        messages = [{"role": "user", "content": context}]

        # ファンクションを定義
        functions = [
            {
                "name": "abstract_of_paper_extraction",
                "description": """This is a process for removing header and footer information and extracting only the abstract part of a paper from text information retrieved from the PubMed paper search site.

                Header and Footer Information:
                - Publication details: journal name, publication date, volume, page numbers
                - Title of the paper
                - Names and affiliations of the authors
                - Author information
                - DOI, PMCID, PMID
                - Conflict of interest statement
                - Copyright notices
                """,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "paper_information": {
                            "type": "string",
                            "description": "abstract of paper",
                        }
                    },
                    "required": ["paper_information"],
                },
            }
        ]

        # ChatGPTを実行する
        try:
            start_time = time.time()
            # OPENAI_API_KEY
            client = OpenAI(
                api_key="OPENAI_API_KEY"
            )
            chatcompletions = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                temperature=0.0,
                messages=messages,
                functions=functions,
                max_tokens=4096,
                function_call={"name": "abstract_of_paper_extraction"},
            )
            end_time = time.time()

            # レスポンスからアブストラクトを取得する
            extracted_data = json.loads(
                chatcompletions.choices[0].message.function_call.arguments
            )

            extracted_abstract = extracted_data["paper_information"]
        except Exception as e:
            # self._logger.error(f"OpenAI ChatGPT API - Error: {e}")
            raise e

        # self._logger.info(f"Extracted abstract: {extracted_abstract}")
        # self._logger.info(
            # f"OpenAI ChatGPT API - Computation time: {end_time - start_time} sec"
        # )
        print(f"Extracted abstract: {extracted_abstract}")
        print(f"OpenAI ChatGPT API - Computation time: {end_time - start_time} sec")
        return extracted_abstract


###############################################################################################
# メイン処理
###############################################################################################
# コンテキストを読み込む
with open(context_file_path_1, "r", encoding="utf-8") as f:
    # コンテキストを変数に格納
    context = f.read()

# コンテキストに対して質問を投げかけ、回答を得る
answer = AbstractExtractionUseCase().execute(context)

# 回答をファイルへ書き込む
with open(answer_file_path_1, "w", encoding="utf-8") as f:
    f.write(answer)
