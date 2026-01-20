from langchain_google_genai import GoogleGenerativeAIEmbeddings

from dotenv import load_dotenv

from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model='gemini-embedding-001', dimension =
100)

documents = [

"Virat Kohli is an Indian cricketer known for his aggressive batting andleadership.",

"MS Dhoni is a former Indian captain famous for his calm demeanor and finishingskills.",

"Sachin Tendulkar, also known as the 'God of Cricket', holds many batting records.",

"Rohit Sharma is known for his elegant batting and record-breaking doublecenturies.",

"Jasprit Bumrah is an Indian fast bowler known for his unorthodox action andyorkers."

]

query = 'tell me about virat kohli'