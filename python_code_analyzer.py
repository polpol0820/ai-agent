import ast
import os
import json

class CodeAnalyzer:
    def __init__(self, project_path):
        self.project_path = project_path
        self.analysis_result = {
            "modules": [],
            "classes": [],
            "functions": []
        }

    def analyze_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                tree = ast.parse(file.read(), filename=file_path)
                self._analyze_ast(tree, file_path)
            except SyntaxError as e:
                print(f"Syntax error in {file_path}: {e}")

    def _analyze_ast(self, tree, file_path):
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self.analysis_result["classes"].append({
                    "name": node.name,
                    "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                    "docstring": ast.get_docstring(node),
                    "file": file_path,
                    "line_start": node.lineno,
                    "line_end": getattr(node, 'end_lineno', None)
                })
            elif isinstance(node, ast.FunctionDef):
                self.analysis_result["functions"].append({
                    "name": node.name,
                    "parameters": [arg.arg for arg in node.args.args],
                    "docstring": ast.get_docstring(node),
                    "file": file_path,
                    "line_start": node.lineno,
                    "line_end": getattr(node, 'end_lineno', None)
                })
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                self.analysis_result["modules"].append({
                    "module": self._get_module_name(node),
                    "file": file_path
                })

    def _get_module_name(self, node):
        if isinstance(node, ast.Import):
            return [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            return node.module

    def analyze_project(self):
        for root, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(".py"):
                    self.analyze_file(os.path.join(root, file))

    def get_analysis_result(self):
        return self.analysis_result

    def save_result(self, output_path):
        with open(output_path, "w", encoding="utf-8") as output_file:
            json.dump(self.analysis_result, output_file, indent=4, ensure_ascii=False)

# 実行例
if __name__ == "__main__":
    project_path = "./example_project"
    output_path = "./analysis_result.json"

    analyzer = CodeAnalyzer(project_path)
    analyzer.analyze_project()
    analyzer.save_result(output_path)

    print(f"Analysis completed. Results saved to {output_path}")
