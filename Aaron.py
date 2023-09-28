"""
模块名称: question_extractor.py

这个模块包含了一个用于从Markdown文件中提取题目并保存为CSV文件的工具类 QuestionExtractor。

用法示例：
    aaron = QuestionExtractor('input.txt', 'output.csv')
    aaron.extract_questions()
"""
import re
import pandas as pd


class AaronPro:
    """
    Aaron 类用于从Markdown文件中提取题目并保存为CSV文件。

    该类包括以下方法：
    - __init__: 构造函数，接受输入文件和输出文件的路径。
    - determine_question_type: 判断题目类型的方法。
    - extract_questions: 提取题目并保存为CSV文件的方法。
    """

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def determine_question_type(self, question):
        """
        判断题目类型的方法。

        参数:
        - question (str): 输入的题目字符串。

        返回值:
        - str: 题目类型，可以是 "填空题"、"选择题" 或 "解答题"。
        """
        if re.search(r'\{.*?\}', question):  # 填空题判断，检查是否有{}
            return "填空题"
        if re.search(r'[A-D]\.', question):  # 选择题判断，检查是否有A.、B.、C.、D.
            return "选择题"
        return "解答题"

    def extract_questions(self):
        """
        提取题目并保存为CSV文件的方法。

        该方法会读取输入文件，并提取题目并保存为CSV文件。
        """
        # 读取Markdown文件
        with open(self.input_file, 'r', encoding='utf-8') as file:
            markdown_data = file.readlines()[2:]  # 忽略前两行内容

        # 将剩余的Markdown内容连接为单个字符串
        markdown_data = ''.join(markdown_data)
        try:
            # 读取Markdown文件
            with open('input.txt', 'r', encoding='utf-8') as file:
                markdown_data = file.readlines()[2:]  # 忽略前两行内容

            # 将剩余的Markdown内容连接为单个字符串
            markdown_data = ''.join(markdown_data)

            # 以空行分割选择题
            questions = markdown_data.split('\n\n')

            # 创建一个DataFrame来存储选择题
            df = pd.DataFrame(
                columns=['题干', '选项A', '选项B', '选项C', '选项D', '答案', '详解'])

            # 遍历每个选择题
            for question in questions:
                # 获取题型
                question_type = self.determine_question_type(question)
                match question_type:
                    # 填空题
                    case '填空题':
                        return 2
                    # 选择题
                    case '选择题':
                        # 定义正则表达式模式
                        pattern = r"(?P<题干>[0-9]+\..+?)\n(?P<选项A>A\..+?)\n(?P<选项B>B\..+?)\n(?P<选项C>C\..+?)\n(?P<选项D>D\..+?)\n【答案】(?P<答案>.+)\n【详解】(?P<详解>.+)"
                        # 使用正则表达式进行匹配
                        match = re.search(pattern, question, re.DOTALL)
                        # 提取匹配的变量，微调
                        data_df = pd.DataFrame({
                            # 去除题干的序号
                            '题干': re.sub(r"^[0-9]+\.", "", match.group("题干")).strip(),
                            '选项A': match.group("选项A")[3:],  # 去除选项开头的字母和点,
                            '选项B': match.group("选项B")[3:],
                            '选项C': match.group("选项C")[3:],
                            '选项D': match.group("选项D")[3:],
                            '答案': match.group("答案"),
                            '详解': match.group("详解")
                        }, index=[0])
                        # 将提取的数据添加到DataFrame中
                        if match:
                            df = pd.concat([df, data_df], ignore_index=True)
                        else:
                            print("未找到匹配")
        except FileNotFoundError:
            print(f'文件"{self.input_file}"不存在')
        # 统计查询到的题目数量
        num_questions = len(df)

        # 输出查询到的题目数量
        print(f'共查询到{num_questions}道题目')

        # 保存为CSV文件
        df.to_csv('output.csv', index=False)


# 示例用法
aaron = AaronPro('input.txt', 'output.csv')
aaron.extract_questions()
