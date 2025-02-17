import whisper
# from transformers import pipeline


# 加载 Whisper 模型并转录音频
model = whisper.load_model("small")  # 根据需求选择模型大小，例如 small/medium/large
output_audio = "audio.mp3"  # 请确保音频文件路径正确
result = model.transcribe(output_audio, fp16=False)
transcription = result["text"]
print("转录文本：", transcription)

# 将转录文本保存到 transcription.txt 文件中
with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(transcription)

# # 3. 使用Transformers进行文本摘要
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# words = transcription.split()
# max_chunk_length = 1024
# chunks = []
# current_chunk = []

# for word in words:
#     current_chunk.append(word)
#     if len(current_chunk) >= max_chunk_length:
#         chunks.append(" ".join(current_chunk))
#         current_chunk = []
# if current_chunk:
#     chunks.append(" ".join(current_chunk))

# intermediate_summaries = []

# for chunk in chunks:
#     summary_part = summarizer(chunk, max_length=350, min_length=200, do_sample=False)[0]['summary_text']
#     intermediate_summaries.append(summary_part)

# # 对中间摘要再次合并并摘要
# combined_summary_text = " ".join(intermediate_summaries)
# print("intermediate_summaries: ", intermediate_summaries)
# print('combined_summary_text: ', combined_summary_text)
# final_summary = summarizer(combined_summary_text, max_length=300, min_length=200, do_sample=False)[0]['summary_text']

# print("最终摘要：", final_summary)