import sqlite3
import random

class Aaron:
    def __init__(self, db_name='aaron.db'):  # 将数据库文件名改为'aaron.db'
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # 创建题目表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                question TEXT NOT NULL,
                question_type TEXT NOT NULL,
                options TEXT,
                answer TEXT NOT NULL
            )
        ''')

        # 创建试卷表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY,
                paper_name TEXT NOT NULL
            )
        ''')

        # 创建试卷-题目关系表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS paper_questions (
                id INTEGER PRIMARY KEY,
                paper_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                FOREIGN KEY (paper_id) REFERENCES papers (id),
                FOREIGN KEY (question_id) REFERENCES questions (id)
            )
        ''')
        self.conn.commit()

    def add_question(self, question, question_type, options, answer):
        # 添加单个题目到题库
        self.cursor.execute('INSERT INTO questions (question, question_type, options, answer) VALUES (?, ?, ?, ?)',
                           (question, question_type, options, answer))
        self.conn.commit()

    def delete_question(self, question_id):
        # 从题库中删除指定ID的题目
        self.cursor.execute('DELETE FROM questions WHERE id = ?', (question_id,))
        self.conn.commit()

    def add_questions_batch(self, questions_batch):
        # 批量添加题目到题库，questions_batch是一个列表，每个元素为一个元组(question, question_type, options, answer)
        self.cursor.executemany('INSERT INTO questions (question, question_type, options, answer) VALUES (?, ?, ?, ?)',
                                questions_batch)
        self.conn.commit()

    def display_all_questions(self):
        # 显示题库中的所有题目
        self.cursor.execute('SELECT * FROM questions')
        questions = self.cursor.fetchall()
        if questions:
            for q in questions:
                print(f"{q[0]}. {q[1]}")
                if q[2] in ['单选题', '多选题']:
                    options = q[3].split(',') if q[3] else []
                    for i, option in enumerate(options):
                        print(f"  {chr(65 + i)}. {option}")
                print(f"  Answer: {q[4]}\n")
        else:
            print("题库中没有题目。")

    def generate_paper(self, paper_name, num_single_choice=2, num_multiple_choice=2, num_fill_in_blank=2, num_free_response=1):
        # 生成试卷，将试卷与题目关联保存到关系表中
        self.cursor.execute("SELECT id FROM questions WHERE question_type='单选题'")
        single_choice_ids = [q[0] for q in self.cursor.fetchall()]
        if len(single_choice_ids) < num_single_choice:
            raise ValueError("单选题数量不足")

        self.cursor.execute("SELECT id FROM questions WHERE question_type='多选题'")
        multiple_choice_ids = [q[0] for q in self.cursor.fetchall()]
        if len(multiple_choice_ids) < num_multiple_choice:
            raise ValueError("多选题数量不足")

        self.cursor.execute("SELECT id FROM questions WHERE question_type='填空题'")
        fill_in_blank_ids = [q[0] for q in self.cursor.fetchall()]
        if len(fill_in_blank_ids) < num_fill_in_blank:
            raise ValueError("填空题数量不足")

        self.cursor.execute("SELECT id FROM questions WHERE question_type='解答题'")
        free_response_ids = [q[0] for q in self.cursor.fetchall()]
        if len(free_response_ids) < num_free_response:
            raise ValueError("解答题数量不足")

        single_choice_ids = random.sample(single_choice_ids, num_single_choice)
        multiple_choice_ids = random.sample(multiple_choice_ids, num_multiple_choice)
        fill_in_blank_ids = random.sample(fill_in_blank_ids, num_fill_in_blank)
        free_response_ids = random.sample(free_response_ids, num_free_response)

        all_question_ids = single_choice_ids + multiple_choice_ids + fill_in_blank_ids + free_response_ids
        random.shuffle(all_question_ids)

        # 将试卷与题目关联保存到关系表中
        self.cursor.execute('INSERT INTO papers (paper_name) VALUES (?)', (paper_name,))
        paper_id = self.cursor.lastrowid
        paper_question_data = [(paper_id, qid) for qid in all_question_ids]
        self.cursor.executemany('INSERT INTO paper_questions (paper_id, question_id) VALUES (?, ?)', paper_question_data)

        self.conn.commit()

    def display_paper(self, paper_id):
        # 显示指定试卷的内容
        self.cursor.execute('SELECT * FROM papers WHERE id = ?', (paper_id,))
        paper = self.cursor.fetchone()
        if paper:
            print(f"试卷名称: {paper[1]}")
            self.cursor.execute('''
                SELECT q.id, q.question, q.question_type, q.options, q.answer
                FROM questions q
                INNER JOIN paper_questions pq ON q.id = pq.question_id
                WHERE pq.paper_id = ?
            ''', (paper_id,))
            questions = self.cursor.fetchall()
            for q in questions:
                print(f"{q[0]}. {q[1]}")
                if q[2] in ['单选题', '多选题']:
                    options = q[3].split(',') if q[3] else []
                    for i, option in enumerate(options):
                        print(f"  {chr(65 + i)}. {option}")
                print(f"  Answer: {q[4]}\n")
        else:
            print("找不到该试卷。")

    def close(self):
        # 关闭数据库连接
        self.conn.close()

if __name__ == "__main__":
    aaron = Aaron(db_name='aaron.db')  # 创建'Aaron'类实例时传入数据库文件名'aaron.db'

    # 批量添加题目到题库
    questions_batch = [
        ("2 + 2 = ?", "单选题", "3,4,5,6", "B"),
        ("5 + 7 = ?", "单选题", "10,12,14,16", "B"),
        ("8 - 3 = ?", "单选题", "2,3,5,8", "B"),
        ("12 - 4 = ?", "多选题", "2,4,6,8", "B,D"),
        ("10 * 3 = ?", "填空题", "", "30"),
        ("简答题：描述牛顿第一定律。", "解答题", "", "牛顿第一定律也称为惯性定律，它指出：物体在没有外力作用时，如果处于静止状态，则会保持静止；如果处于运动状态，则会保持匀速直线运动。")
    ]
    aaron.add_questions_batch(questions_batch)

    # 显示题库中的所有题目
    print("题库中的所有题目：")
    aaron.display_all_questions()

    # 生成试卷
    aaron.generate_paper("物理试卷1", num_single_choice=2, num_multiple_choice=2, num_fill_in_blank=1, num_free_response=1)
    aaron.generate_paper("物理试卷2", num_single_choice=3, num_multiple_choice=2, num_fill_in_blank=1, num_free_response=1)

    # 显示试卷内容
    print("试卷1的内容：")
    aaron.display_paper(1)

    print("试卷2的内容：")
    aaron.display_paper(2)

    aaron.close()
