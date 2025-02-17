import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 设置 OpenAI API Key（建议通过环境变量设置）
# 或直接赋值，例如：openai.api_key = "YOUR_API_KEY"

# 从 transcription.txt 文件中读取转录文本
with open("transcription.txt", "r", encoding="utf-8") as f:
    transcription = f.read()

def split_text(text, max_chars=3500):
    """
    将文本分成多个块，每个块不超过 max_chars 个字符，尽量在换行或空格处切分，避免在单词中间截断。
    """
    chunks = []
    while len(text) > max_chars:
        # 尽量在换行符处切分
        split_idx = text.rfind("\n", 0, max_chars)
        if split_idx == -1:
            # 如果没有换行符，则在空格处切分
            split_idx = text.rfind(" ", 0, max_chars)
        if split_idx == -1:
            split_idx = max_chars
        chunks.append(text[:split_idx])
        text = text[split_idx:]
    chunks.append(text)
    return chunks

# 将长文本分成若干段（每段不超过3500个字符）
chunks = split_text(transcription, max_chars=3500)

# 针对每个分段调用 OpenAI 的 API 生成摘要
intermediate_summaries = []

for i, chunk in enumerate(chunks):
    prompt = (
        "请阅读下面这段视频转录文本，并生成一份简洁而全面的摘要，"
        "包括主要观点和关键信息：\n\n" + chunk
    )
    response = client.chat.completions.create(model="gpt-4o-mini",  # 如果 token 数不足，也可以尝试 gpt-3.5-turbo
    messages=[
        {"role": "system", "content": "你是一个专业的内容摘要助手。"},
        {"role": "user", "content": prompt},
    ],
    temperature=0.7,
    max_tokens=500)
    summary_chunk = response.choices[0].message.content.strip()
    print(f"第 {i+1} 段摘要：\n{summary_chunk}\n")
    intermediate_summaries.append(summary_chunk)

# 将所有中间摘要合并，再生成最终摘要
combined_summary_text = "\n".join(intermediate_summaries)
final_prompt = (
    "请阅读下面这些摘要内容，并生成一份综合的最终摘要，确保涵盖所有关键点：\n\n" 
    + combined_summary_text
)
final_response = client.chat.completions.create(model="gpt-4",
messages=[
    {"role": "system", "content": "你是一个专业的内容摘要助手。"},
    {"role": "user", "content": final_prompt},
],
temperature=0.7,
max_tokens=500)
final_summary = final_response.choices[0].message.content.strip()
print("最终摘要：\n", final_summary)
