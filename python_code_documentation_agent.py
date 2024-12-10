import json
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

# 環境変数からAPIキーを取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class CodeDocumentationAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.0, openai_api_key=OPENAI_API_KEY)

    def generate_documentation(self, analysis_result):
        documentation = {
            "classes": [],
            "functions": []
        }

        for cls in analysis_result.get("classes", []):
            doc = self._generate_class_doc(cls)
            documentation["classes"].append(doc)

        for func in analysis_result.get("functions", []):
            doc = self._generate_function_doc(func)
            documentation["functions"].append(doc)

        return documentation

    def _generate_class_doc(self, cls):
        prompt = f"""
        以下のPythonクラスについて、日本語で簡潔でわかりやすい説明と、典型的な使用例を生成してください。

        クラス名: {cls['name']}
        メソッド: {', '.join(cls['methods'])}
        ドックストリング: {cls.get('docstring', 'なし')}
        ファイル: {cls['file']}
        行数: {cls['line_start']} - {cls['line_end']}

        クラスの概要とメソッドの役割、使用例をMarkdown形式で記述してください。
        """
        return {
            "class_name": cls["name"],
            "documentation": self._query_llm(prompt)
        }

    def _generate_function_doc(self, func):
        prompt = f"""
        以下のPython関数について、日本語で簡潔でわかりやすい説明と、典型的な使用例を生成してください。

        関数名: {func['name']}
        パラメータ: {', '.join(func['parameters'])}
        ドックストリング: {func.get('docstring', 'なし')}
        ファイル: {func['file']}
        行数: {func['line_start']} - {func['line_end']}

        関数の目的、使用例、および注意点をMarkdown形式で記述してください。
        """
        return {
            "function_name": func["name"],
            "documentation": self._query_llm(prompt)
        }

    def _query_llm(self, prompt):
        response = self.llm.predict(prompt)
        return response.strip()

# 実行例
if __name__ == "__main__":
    with open("analysis_result.json", "r", encoding="utf-8") as file:
        analysis_result = json.load(file)

    documentation_agent = CodeDocumentationAgent()
    documentation = documentation_agent.generate_documentation(analysis_result)

    with open("documentation.json", "w", encoding="utf-8") as file:
        json.dump(documentation, file, indent=4, ensure_ascii=False)

    print("日本語のドキュメントが documentation.json に保存されました。")
