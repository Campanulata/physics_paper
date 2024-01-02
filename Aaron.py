"""
模块名称: question_extractor.py

这个模块包含了一个用于从Markdown文件中提取题目并保存为CSV文件的工具类 QuestionExtractor。

用法示例：
    aaron = QuestionExtractor('input.txt')
    aaron.extract_questions()
"""
import re
from enum import Enum
import pandas as pd

class QuestionType(Enum):
    """
    枚举类型，用于表示题目类型。
    """
    FILL_IN_THE_BLANK = "填空题"
    MULTIPLE_CHOICE = "选择题"
    RESPONSE = "解答题"

class AaronPro:
    """
    Aaron 类用于从Markdown文件中提取题目并保存为CSV文件。

    该类包括以下方法：
    - __init__: 构造函数，接受输入文件和输出文件的路径。
    - determine_question_type: 判断题目类型的方法。
    - extract_questions: 提取题目并保存为CSV文件的方法。
    """

    def __init__(self, input_file):
        self.input_file = input_file

    def _parse_markdown_file(self):
        try:
            with open(self.input_file, 'r', encoding='utf-8') as file:
                return file.readlines()
        except (FileNotFoundError, IOError) as e:
            print(f'在打开文件"{self.input_file}"时发生错误: {str(e)}')
            return []

    def determine_question_type(self, question):
        """
        判断题目类型的方法。

        参数:
        - question (str): 输入的题目字符串。

        返回值:
        - str: 题目类型，可以是 "填空题"、"选择题" 或 "解答题"。
        """
        if re.search(r'\{\}', question):
            return QuestionType.FILL_IN_THE_BLANK
        if re.search(r'[A-D]\.', question):
            return QuestionType.MULTIPLE_CHOICE
        return QuestionType.RESPONSE

    def _handle_multiple_choice(self, question, df):
        """
        处理选择题的方法。

        参数:
        - question (str): 输入的题目字符串。
        - df (pandas.DataFrame): 保存题目数据的DataFrame。
        """
        pattern = r"(?P<题干>[0-9]+\..+?)\n(?P<选项A>A\..+?)\n(?P<选项B>B\..+?)\n(?P<选项C>C\..+?)\n(?P<选项D>D\..+?)\n【答案】(?P<答案>.+)\n【详解】(?P<详解>.+)"
        match = re.search(pattern, question, re.DOTALL)

        if not match:
            print("未找到匹配")
            return

        df.loc[len(df)] = {
            '题干': re.sub(r"^[0-9]+\.", "", match.group("题干")).strip(),
            '选项A': match.group("选项A")[3:],
            '选项B': match.group("选项B")[3:],
            '选项C': match.group("选项C")[3:],
            '选项D': match.group("选项D")[3:],
            '答案': match.group("答案"),
            '详解': match.group("详解")
        }

    def extract_questions(self):
        """
        提取题目数据的入口方法。
        """
        markdown_data = self._parse_markdown_file()

        if not markdown_data:
            return

        questions = ''.join(markdown_data).split('\n\n')

        df = pd.DataFrame(columns=['题干', '选项A', '选项B', '选项C', '选项D', '答案', '详解'])

        for question in questions:
            question_type = self.determine_question_type(question)

            if question_type == QuestionType.MULTIPLE_CHOICE:
                self._handle_multiple_choice(question, df)

        print(f'共查询到{len(df)}道题目')

        df.to_csv('output.xlsx', index=False)


# 示例用法
aaron = AaronPro('input.txt')
aaron.extract_questions()
