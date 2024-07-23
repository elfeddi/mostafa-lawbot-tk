from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_voyageai import VoyageAIEmbeddings
from langchain.memory import ConversationSummaryMemory

import chromadb
query_bp = Blueprint('query', __name__)
voyemb = VoyageAIEmbeddings(
    voyage_api_key="pa-KT8QqDg8iYbFJTOLt6q-HqQRBftEghWmf9rJw7PBDco", model="voyage-law-2"
)

@query_bp.route('/query', methods=['POST'])
@jwt_required()
def query():
    data = request.json
    user_query = data['query']
    current_user = get_jwt_identity()
    memory=ConversationSummaryMemory(llm=ChatOpenAI(temperature=0))


    client = chromadb.PersistentClient(path="vectorstore")
    collection_name = current_user
    langchain_chroma = Chroma(client=client, collection_name=collection_name, embedding_function=voyemb)
    retriever = langchain_chroma.as_retriever(search_type="similarity", search_kwargs={"k": 25})

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    prompt_template = (
        "This is the summary of the previous conversation. Use it if needed: {summary}\n\n"
        "User Question: {question}\n\n"
        "Please use all the context provided by the system to generate a comprehensive and accurate response and display it. Answer primarily in French, but if the question is in another language, answer in that language."
    )

    formatted_prompt = PromptTemplate.from_template(prompt_template).format(summary=memory.buffer, question=user_query)
    generated_answer = qa_chain({"query": formatted_prompt})
    memory.save_context({"input": user_query}, {"output": generated_answer["result"]})


    return jsonify({"response": generated_answer['result']})
