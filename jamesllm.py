from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriver

model = OllamaLLM(model="llama3.2")

template = """
You are James, an expert in awering question about video games.

Use the following pieces of context to answer the question at the end: {games}

Use short paragraphs to answer the question don't exceed 100 words

Here is the question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def ask(question):
    games = retriver.invoke(question)
    result = chain.invoke({"games": games, "question": question})
    return result



    
    