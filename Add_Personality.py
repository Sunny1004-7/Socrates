import pandas as pd
import random
from persona_loader import STUDENT_PERSONAS

input_path = "subject_data/Student_Record.csv"
df = pd.read_csv(input_path)

# 2. 性格池
personas = list(STUDENT_PERSONAS.keys())

# 3. 给每个用户随机选一个人格
unique_users = df['user_id'].unique()
user_persona = {uid: random.choice(personas) for uid in unique_users}

# 4. 在第一行记录加入人格，其余用户行保留空白
df['student_persona'] = ""  # 新列初始化为空字符串

# 找到每个 user 第一次出现的索引
first_indices = df.drop_duplicates(subset=['user_id'], keep='first').index

for idx in first_indices:
    uid = df.at[idx, 'user_id']
    df.at[idx, 'student_persona'] = user_persona[uid]

# 5. 保存新文件
output_path = "subject_data/stuRec_1000_with_persona.csv"
df.to_csv(output_path, index=False)
print(f"已生成带人格标签的文件：{output_path}")
