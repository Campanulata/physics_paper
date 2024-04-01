import os
import subprocess

# 请替换为你的文件所在文件夹路径
directory = '高考备考/高考真题/2020/'

for filename in os.listdir(directory):
    if filename.endswith(".docx"):
        md_filename = os.path.splitext(filename)[0] + '.md'
        subprocess.run(['pandoc', '-s', os.path.join(directory, filename), '-t', 'markdown', '-o', os.path.join(directory, md_filename)])