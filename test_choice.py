"""
请用Python写一段脚本，脚本功能是用正则表达式匹配8个变量：序号、题干、选项A、选项B、选项C、选项D、答案、详解。其中每个变量都可能由多行组成。我的题目格式为：
1. 在太空实验室中可以利用匀速圆周运动测量小球质量。如图所示, 不可伸长的轻绳一端固定于 $O$ 点, 另 一端系一待测小球, 使其绕 $O$ 做匀速圆周运动, 用力传感器测得绳上的拉力为 $F$, 用停表测得小球转过 $n$ 圈 所用的时间为 $t$, 用刻度尺测得 $O$ 点到球心的距离为圆周运动的半径 $R$ 。下列说法正确的是 ( )
![](https://raw.githubusercontent.com/Campanulata/physics_paper_img/master/img/202307162244662.png)
A. 圆周运动轨道可处于任意平面内
B. 小球的质量为 $\frac{F R t^{2}}{4 \pi^{2} n^{2}}$
C. 若误将 $\mathrm{n}-1$ 圈记作 $n$ 圈, 则所得质量偏大
D. 若测 $R$ 时末计入小球半径, 则所得质量偏小
【答案】A
【详解】A. 空间站内的物体都处于完全失重状态, 可知圆周运动的轨道可处于任意平面内, 故 A 正确; B. 根据
$$
\begin{gathered}
F=m \omega^{2} R \\
\omega=\frac{2 \pi n}{t}
\end{gathered}
$$
解得小球质量
"""

import re

# 示例题目文本
CONTENT = """
11. 在太空实验室中可以利用匀速圆周运动测量小球质量。如图所示, 不可伸长的轻绳一端固定于 $O$ 点,
另一端系一待测小球, 使其绕 $O$ 做匀速圆周运动, 用力传感器测得绳上的拉力为 $F$,
用停表测得小球转过 $n$ 圈所用的时间为 $t$, 用刻度尺测得 $O$ 点到球心的距离为圆周运动的半径 $R$ 。
下列说法正确的是 ( )
A. 圆周运动轨道可处于任意平面内
B. 小球的质量为 $\\frac{F R t^{2}}{4 \\pi^{2} n^{2}}$
C. 若误将 $\\mathrm{n}-1$ 圈记作 $n$ 圈, 则所得质量偏大
D. 若测 $R$ 时末计入小球半径, 则所得质量偏小
【答案】A
【详解】A. 空间站内的物体都处于完全失重状态, 可知圆周运动的轨道可处于任意平面内, 故 A 正确;
B. 根据公式: $F=m \\omega^{2} R$, $\\omega=\\frac{2 \\pi n}{t}$ 解得小球质量
"""

# 定义正则表达式模式
PATTERN = r"(?P<题干>[0-9]+\..+?)\n(?P<选项A>A\..+?)\n(?P<选项B>B\..+?)\n(?P<选项C>C\..+?)\n(?P<选项D>D\..+?)\n【答案】(?P<答案>.+)\n【详解】(?P<详解>.+)"
# PATTERN = r"(?P<题干>[0-9]+\..+?)\n(?P<选项A>A\..+?)(?=B\.)\n(?P<选项B>B\..+?)(?=C\.)\n(?P<选项C>C\..+?)(?=D\.)\n(?P<选项D>D\..+?)(?=【答案】)\n【答案】(?P<答案>.+?)(?=【详解】)\n【详解】(?P<详解>.+)"
# 使用正则表达式进行匹配
match = re.search(PATTERN, CONTENT, re.DOTALL)

# 提取匹配的变量
if match:
    content = match.group("题干")
    option_A = match.group("选项A")[3:]  # 去除选项开头的字母和点
    option_B = match.group("选项B")[3:]
    option_C = match.group("选项C")[3:]
    option_D = match.group("选项D")[3:]
    answer = match.group("答案")
    explanation = match.group("详解")

    # 去除题干的序号
    content = re.sub(r"^[0-9]+\.", "", content).strip()
    # 打印提取的变量
    print("题干:", content)
    print("选项A:", option_A)
    print("选项B:", option_B)
    print("选项C:", option_C)
    print("选项D:", option_D)
    print("答案:", answer)
    print("详解:", explanation)
else:
    print("未找到匹配")
