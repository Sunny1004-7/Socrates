import json
from autogen import ConversableAgent

# 使用指定的 LLM 配置
llm_config = {
    "cache_seed": None,
    "config_list": [{
        "model": "gpt-3.5-turbo",  # 模型名称
        "base_url": "https://xh.v1api.cc/v1",  # 接口地址
        "api_key": "sk-NCe9VNEDxfEIZwG7DlJdLaGhvOW1Oyhuh7dWwMP7bbPUB5Dm",  # API 密钥
        "price": [0, 0]  # 自定义价格，可设为 [0,0]
    }]
}

# 创建评估代理的工厂函数
def create_agent(system_message, name="evaluator"):
    return ConversableAgent(name=name, llm_config=llm_config, system_message=system_message)

# 1. 读取整个对话文件内容，作为原始文本
with open('conversation_part_2.json', 'r', encoding='utf-8') as f:
    conversation_text = f.read()

# 2. 构建英文评估提示，并嵌入完整对话
evaluation_prompt = f"""
You are a dialogue quality evaluation expert. Below is a teacher-student dialogue in which the student displays a negative personality (e.g., frustration, resistance to learning). Please rate the teacher assistant's performance from 1 (worst) to 5 (best) on the following five dimensions, and return a JSON object only:

1. Identification: Did the teacher accurately recognize and acknowledge the student's negative emotions?
2. Empathy: How well did the teacher's individual responses demonstrate empathy toward the student's emotions?
3. Comforting: How effectively did the teacher alleviate the student's negative emotions over multiple turns?
4. Suggestion: Were the strategies and suggestions offered by the teacher practical and targeted to address the negative emotions?
5. Overall: What is the overall emotional support experience provided by the teacher?

Dialogue:
----------------------------------------
{conversation_text}
----------------------------------------

Respond ONLY with the following JSON format, without any additional text:
{{
  "Identification": x,
  "Empathy": y,
  "Comforting": z,
  "Suggestion": w,
  "Overall": v
}}
"""

# 3. 创建评估代理并执行打分
system_message = "You are a helpful assistant for evaluating dialogue."  # 系统消息
agent_evaluator = create_agent(system_message)  # 实例化评估代理
scores_reply = agent_evaluator.generate_reply(messages=[{"role": "user", "content": evaluation_prompt}])  # 获取模型回复

# 4. 解析模型返回的 JSON 格式评分
try:
    scores = json.loads(scores_reply)
except json.JSONDecodeError:
    print("解析模型返回内容失败：", scores_reply)  # 输出解析错误
    scores = None

# 5. 输出并保存评分结果
if scores:
    print("评估评分：")
    for dimension, value in scores.items():
        print(f"{dimension}: {value}")  # 打印各维度分数
    with open('evaluation_scores.json', 'w', encoding='utf-8') as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)  # 保存到文件
    print('评分结果已保存到 evaluation_scores.json')
else:
    print('未获取有效评分。')  # 无效评分提示
