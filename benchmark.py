from ollama import embed
from scipy import spatial
import sys
import numpy as np

# The sentences to encode
sentence_high = [
    "The chef prepared a delicious meal for the guests.",
    "A tasty dinner was cooked by the chef for the visitors."
]
sentence_medium = [
    "She is an expert in machine learning.",
    "He has a deep interest in artificial intelligence."
]
sentence_low = [
    "The weather in Tokyo is sunny today.",
    "I need to buy groceries for the week."
]

for sentence in [sentence_high, sentence_medium, sentence_low]:
  print("🙋‍♂️")
  print(sentence)
  # [emb1, emb2] 
  embeddings = embed(model="embeddinggemma", input=sentence)["embeddings"]

  # distancia de coseno é uma das formas de calcular similaridade
  # a similaridade é o inverso da distancia (por isso o -1)
  score = 1 - spatial.distance.cosine(embeddings[0], embeddings[1])
  print("`-> 🤖 score: ", score)


