from ollama import embed
from scipy import spatial

filmes = [
    "Interestelar: ficção científica, espaço, drama, viagem no tempo",
    "Gravidade: ficção científica, espaço, sobrevivência, tensão",
    "Toy Story: animação, amizade, aventura, comédia",
    "O Poderoso Chefão: máfia, crime, família, drama"
]

filme_base = "Tropa de Elite: polícia, estratégia, crime, violência"

todos = [filme_base] + filmes

response = embed(
    model="embeddinggemma",
    input=todos
)

embeddings = response["embeddings"]
embedding_base = embeddings[0]

for i in range(1, len(embeddings)):
    score = 1 - spatial.distance.cosine(embedding_base, embeddings[i])
    print(f"Similaridade com '{filmes[i-1]}': {score:.4f}")