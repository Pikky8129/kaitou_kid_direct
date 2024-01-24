# kaitou kid direct について

「質問の定型部分」 に 「アブストラクトのテキスト」を結合し、
それをプロンプトとして ChatGPT に質問を投げかけ、回答を得るシステム。

# プログラムの仕組み

下記の 「メイン処理」 を参照。  

`ChatGPT への質問について`  
　「質問の定型部分」 と 「アブストラクトのテキスト」を結合し、プロンプトを作成。  

★プロンプトの内容は、今回のアブストラクトに限らず、  
　必要に応じて、関数[`_create_prompt`] を編集することで汎用的に利用できます。  

`ChatGPT からの回答について`  
　変数[`answer_file_path_1`] に設定したフォルダにテキストファイルが生成され、  
　そのテキストファイルに回答が書き込まれる仕組み。

```
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
```

# セットアップ(VSCode使用)

1. リポジトリをクローンします。
2. python仮想環境を構築します。

```
$ python -m venv venv  
$ venv\Scripts\activate  
$ python -m pip install --upgrade pip  
```

3. 必要なPythonライブラリをインストールします。

```
$ python -m pip install -r requirements.txt
```

4. question_and_answer.py の変数[`question_template_en`] に質問の定型部分を記載

```
###############################################################################################
# 質問
###############################################################################################
question_template_en = """
The abstract of the paper is listed below.
If the abstract of the paper is about the production of a compound by a microorganism, I would like you to extract the following five pieces of information: 1. the raw material, 2. the product, 3. the name of the biosynthetic pathway, 4. the key to increasing production, and 5. the name of the microorganism.
If the content of the abstract is not about the production of compounds by microorganisms, please do not extract any information and just answer 'out of scope'.
Abstract:
"""
```

5. question_and_answer.py の変数[`abstract_file_path_1`] にアブストラクトのテキストファイルパスを設定
6. question_and_answer.py の変数[`answer_file_path_1`] に ChatGPT からの回答を書き込むファイルのファイルパスを設定

```
###############################################################################################
# 設定
###############################################################################################
# アブストラクト　ファイルパス
abstract_file_path_1 = "input/context/abstract_001.txt"
# 回答　ファイルパス
answer_file_path_1 = "output/answer_001.txt"
```

7. OPENAI_API_KEY を設定

```
            # OPENAI_API_KEY
            client = OpenAI(
                api_key="OPENAI_API_KEY"
            )

```
