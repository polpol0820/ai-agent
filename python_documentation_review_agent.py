import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# .envファイルを読み込む
load_dotenv()

# 環境変数からAPIキーを取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class DocumentationReviewAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.0, openai_api_key=OPENAI_API_KEY)

    def review_documentation(self, documentation):
        reviews = {
            "classes": [],
            "functions": []
        }

        # クラスごとの評価
        for cls in documentation.get("classes", []):
            review = self._evaluate_class_doc(cls)
            reviews["classes"].append(review)

        # 関数ごとの評価
        for func in documentation.get("functions", []):
            review = self._evaluate_function_doc(func)
            reviews["functions"].append(review)

        return reviews

    def _evaluate_class_doc(self, cls_doc):
        prompt = f"""
        以下のPythonクラスのドキュメントを評価してください。
        
        ドキュメント:
        {cls_doc['documentation']}
        
        以下の基準で評価してください:
        1. 完全性: クラスやメソッドの説明が適切か。
        2. 正確性: クラスの機能が正しく説明されているか。
        3. 可読性: 日本語としてわかりやすいか。
        
        スコアを10点満点で評価し、改善点を具体的に提案してください。
        """
        response = self._query_llm(prompt)
        return {"class_name": cls_doc["class_name"], "review": response}

    def _evaluate_function_doc(self, func_doc):
        prompt = f"""
        以下のPython関数のドキュメントを評価してください。
        
        ドキュメント:
        {func_doc['documentation']}
        
        以下の基準で評価してください:
        1. 完全性: 関数の目的や使用例が適切に記載されているか。
        2. 正確性: 関数の動作が正しく説明されているか。
        3. 可読性: 日本語としてわかりやすいか。
        
        スコアを10点満点で評価し、改善点を具体的に提案してください。
        """
        response = self._query_llm(prompt)
        return {"function_name": func_doc["function_name"], "review": response}

    def _query_llm(self, prompt):
        response = self.llm.predict(prompt)
        return response.strip()

# 実行例
if __name__ == "__main__":
    # ドキュメントを読み込む
    with open("documentation.json", "r", encoding="utf-8") as file:
        documentation = json.load(file)

    # DocumentationReviewAgentを初期化して実行
    review_agent = DocumentationReviewAgent()
    reviews = review_agent.review_documentation(documentation)

    # レビュー結果を保存
    with open("reviews.json", "w", encoding="utf-8") as file:
        json.dump(reviews, file, indent=4, ensure_ascii=False)

    print("ドキュメントの評価結果が reviews.json に保存されました。")
