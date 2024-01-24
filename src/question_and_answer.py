import logging
import time
import os
from datetime import datetime

from openai import OpenAI


###############################################################################################
# 質問
###############################################################################################
question_template_en = """
The abstract of the paper is listed below.
If the abstract of the paper is about the production of a compound by a microorganism, I would like you to extract the following five pieces of information: 1. the raw material, 2. the product, 3. the name of the biosynthetic pathway, 4. the key to increasing production, and 5. the name of the microorganism.
If the content of the abstract is not about the production of compounds by microorganisms, please do not extract any information and just answer 'out of scope'.
Abstract:
"""


###############################################################################################
# 設定
###############################################################################################
# アブストラクト　ファイルパス
abstract_file_path_1 = "input/context/abstract_001.txt"

# 回答　ファイルパス
answer_file_path_1 = "output/answer_001.txt"

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


class QuestionAndAnswerUseCase:
    """
    質問を投げかけ、回答を得るクラス
    """

    #    def __init__(self) -> None:
    #        self._logger = logging.getLogger(__name__)

    def execute(self, abstract: str) -> str:
        """
        質問を投げかけ、回答を得る

        Parameters
        ----------
        abstract : str
            アブストラクト

        Returns
        -------
        str
            回答
        """

        # self._logger.info("Question and answer started.")
        print("Question and answer started.")

        # 質問を投げかけ、回答を得る
        answer = self._get_answer_to_question(abstract)

        # self._logger.info("Question and answer finished.")
        print("Question and answer finished.")

        return answer

    def _get_answer_to_question(self, abstract: str) -> str:
        """
        質問を投げかけ、回答を得る

        Parameters
        ----------
        abstract : str
            アブストラクト

        Returns
        -------
        str
            回答
        """

        # プロンプトを作成する
        prompt = self._create_prompt(abstract)

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
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            end_time = time.time()

            # レスポンスから回答を取得する
            content = chatcompletions.choices[0].message.content
        except Exception as e:
            # self._logger.error(f"OpenAI ChatGPT API - Error: {e}")
            raise e

        # self._logger.info(f"Prompt: {prompt}")
        # self._logger.info(f"Answer: {content}")
        # self._logger.info(
        #    f"OpenAI ChatGPT API - Computation time: {end_time - start_time} sec"
        # )

        print(f"Prompt: {prompt}")
        print(f"Answer: {content}")
        print(f"OpenAI ChatGPT API - Computation time: {end_time - start_time} sec")

        return content

    def _create_prompt(self, abstract: str) -> str:
        """
        プロンプトを作成する

        Parameters
        ----------
        abstract : str
            アブストラクト

        Returns
        -------
        str
            プロンプト
        """
        prompt = question_template_en + abstract
        return prompt


###############################################################################################
# メイン処理
###############################################################################################
# アブストラクトを読み込む
with open(abstract_file_path_1, "r", encoding="utf-8") as f:
    # アブストラクトを変数に格納
    abstract = f.read()

# 質問を投げかけ、回答を得る
answer = QuestionAndAnswerUseCase().execute(abstract)

# 回答をファイルへ書き込む
with open(answer_file_path_1, "w", encoding="utf-8") as f:
    f.write(answer)
