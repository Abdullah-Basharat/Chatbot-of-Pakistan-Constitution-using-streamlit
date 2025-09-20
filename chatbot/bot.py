from langchain_community.vectorstores import Pinecone
from langchain.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone as pc_client

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import openai
import streamlit as st
from . import prompts


class Bot():
    def __init__(self):
        self._embeddings = HuggingFaceEmbeddings(model_name=st.secrets["models"]["embedding_model"])
        self.pc = pc_client(api_key=st.secrets["pinecone"]["api_key"])
        index = self.pc.Index(st.secrets["pinecone"]["index"])
        self.vectorstore = Pinecone(index=index, embedding=self._embeddings,text_key= 'text')

        self.llm_api = openai.OpenAI(
            base_url=st.secrets["urls"]["base_url"],
            api_key=st.secrets["api_keys"]["grok_api_key"]
        )
        self.llm = ChatGroq(temperature=0,model=st.secrets["models"]["llm_model"],api_key=st.secrets["api_keys"]["grok_api_key"])
        self.topic_llm = ChatGroq(temperature=0,model=st.secrets["models"]["llm_model"],api_key=st.secrets["api_keys"]["grok_api_key"],max_tokens=10)


        self.refine_query_chain = self.__get_refine_query_chain()
        self.topic_chain = self.__get_topic_chain()
        self.suggested_prompts_chain = self.__get_suggested_prompts_chain()
        # self.router_chain = self.__get_router_chain()

        

    def __get_refine_query_chain(self):
        prompt = PromptTemplate.from_template(template=prompts.refine_query_prompt)
        chain = prompt | self.llm
        return chain  
    
    def __get_topic_chain(self):
        prompt = PromptTemplate.from_template(template=prompts.topic_prompt)
        chain = prompt | self.topic_llm
        return chain
    
    def __get_suggested_prompts_chain(self):
        prompt = PromptTemplate.from_template(template=prompts.suggested_prompts_prompt)
        chain = prompt | self.llm
        return chain
    
    def __get_router_chain(self):
        prompt = PromptTemplate.from_template(template=prompts.router_prompt)
        chain = prompt | self.llm
        return chain
    
    def get_topic(self, query,assistant_response=None):
        response = self.topic_chain.invoke({"user_query": query, "assistant_response": assistant_response})
        return response.content
    
    def get_suggested_prompts(self, query,assistant_response=None):
        response = self.suggested_prompts_chain.invoke({"user_query": query, "assistant_response": assistant_response})
        return response.content
    
    def get_system_prompt(self, resources_context=None, history=None, system_prompt=None):
    
        template_inputs= f""" **Resources Context**: ```{resources_context}```
        --------------------------------------

        **Chat history**: ``{history}```

        """
        system_prompt = f"""{system_prompt}\n{template_inputs}"""
        return system_prompt
        
    def get_query_response(self,query, history=None):
        ref_data = []
        resources_context = self.vectorstore.similarity_search_with_score(query, k=10)
        for doc, score in resources_context:
            ref_data.append({
                "page_content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(score)  # Convert score to float for JSON serialization
            })
        messages = [
                {
                    "role": "system",
                    "content": self.get_system_prompt(
                        system_prompt=prompts.SYSTEM_PROMPT,
                        resources_context=resources_context,
                        history=history,
                    )
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        response = self.llm_api.chat.completions.create(
            model=st.secrets["models"]["llm_model"],
            messages=messages,
            stream=True,
        )

        return response, ref_data