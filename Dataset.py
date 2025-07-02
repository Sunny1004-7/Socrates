import pandas as pd
import random

# 1. 先读入所有基础表
problem            = pd.read_csv("subject_data/problem.csv")
problem_concept    = pd.read_csv("subject_data/problem_concept.csv").drop_duplicates("problem_id")
user_problem       = pd.read_csv("subject_data/user_problem.csv")
course_problem     = pd.read_csv("subject_data/course_problem.csv")
course_profile     = pd.read_csv("subject_data/course_profile.csv")[["course_id", "name"]]

# 2. 随机采样 1000 个用户
all_users = user_problem["user_id"].unique().tolist()
n_users = len(all_users)
sample_size = min(1000, n_users)
sample_users = random.sample(all_users, sample_size)
print(f"总共有 {n_users} 位用户，采样 {sample_size} 位。")


# 3. 过滤出这 1000 个用户的做题记录
stu1000 = user_problem[user_problem["user_id"].isin(sample_users)]

# 4. 依次合并：题目元数据 → 题目概念 → 课程映射 → 课程名称
df = (
    stu1000
    .merge(problem[["problem_id", "content", "option", "answer"]], on="problem_id", how="left")
    .merge(problem_concept[["problem_id", "concept_id"]], on="problem_id", how="left")
    .merge(course_problem[["problem_id", "course_id"]], on="problem_id", how="left")
    .merge(course_profile, on="course_id", how="left")
)

# 5. 重命名列／选取列，生成最终 CSV
df = df[[
    "user_id",
    "problem_id",
    "content",
    "option",
    "answer",
    "concept_id",
    "course_id",
    "name",        # 课程名称
    "is_correct",
    "score",
    "attempts",
    "submit_time"
]]
df.rename(columns={"name":"course_name"}, inplace=True)

df.to_csv("subject_data/Student_Record.csv", index=False)
print("导出完成：", df.shape)
