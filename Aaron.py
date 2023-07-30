import pandas as pd

class Aaron:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def extract_questions(self):
        # 读取Markdown文件
        with open('input.txt', 'r') as file:
            markdown_data = file.readlines()[2:]  # 忽略前两行内容

        # 将剩余的Markdown内容连接为单个字符串
        markdown_data = ''.join(markdown_data)

        # 以空行分割选择题
        questions = markdown_data.split('\n\n')

        # 创建一个DataFrame来存储选择题
        df = pd.DataFrame(columns=['题干', '选项A', '选项B', '选项C', '选项D', '答案', '详解'])

        # 遍历每个选择题
        for question in questions:
            # 按行分割选择题的内容
            lines = question.split('\n')

            # 查找题干的开始和结束位置
            question_start = 0
            question_end = 0
            while not lines[question_end].startswith('A. ') and question_end < len(lines) - 1:
                question_end += 1
            question_end -= 1  # 题干的结束行为选项A开始行的上一行

            # 处理题干，去除题干的序号
            question_text = '\n'.join(lines[question_start:question_end+1])
            question_text = '\n'.join(question_text.split('.')[1:]).strip()

            # 初始化选项、答案和详解的内容
            options = [''] * 4
            answer = ''
            explanation = ''

            # 查找选项、答案和详解的内容
            option_start = question_end + 1
            for i in range(option_start, len(lines)):
                line = lines[i]
                if line.startswith('【答案】'):
                    answer = line[4:].strip()
                elif line.startswith('【详解】'):
                    explanation = '\n'.join(lines[i:]).replace('【详解】', '').strip()
                    break
                else:
                    option_index = i - option_start
                    if option_index < 4:
                        options[option_index] = line[3:].strip()  # 删除选项开头的"A. "

            # 将提取的数据添加到DataFrame中
            df = df.append({
                '题干': question_text,
                '选项A': options[0],
                '选项B': options[1],
                '选项C': options[2],
                '选项D': options[3],
                '答案': answer,
                '详解': explanation
            }, ignore_index=True)

        # 统计查询到的题目数量
        num_questions = len(df)

        # 输出查询到的题目数量
        print(f'共查询到{num_questions}道题目')

        # 保存为CSV文件
        df.to_csv('output.csv', index=False)

# 示例用法
aaron = Aaron('input.txt', 'output.csv')
aaron.extract_questions()