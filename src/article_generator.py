import openai

openai.api_key = "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"

text = "Bio\n私はしがない小説家である。名前はまだ無い。どこで書いたかとんと見当がつかぬ。何でも陰湿なせせこましい所でワーワー喚いていた事だけは記憶している。\nBlog\n2021年12月3日\nTitle:\nとある惑星での出来事\ntags\n宇宙、不条理、生物、珍妙、悲哀\nSummary:\n宇宙のどこか、とある惑星には変わった生物がいた。彼らは特徴的な身体をしていたが、哀れなことに絶滅してしまったようだ。\nFull text:\n"

response = openai.Completion.create(
    engine="davinci",
    prompt=text,
    temperature=1,
    max_tokens=1500,
    presence_penalty=1
)

with open("../output/article_sentence.txt", mode="a") as f:
    f.write(response["choices"][0]["text"])
    f.write("\n\n")
