import os
from langchain_community.llms import OCIGenAI
 
from langchain import PromptTemplate
from langchain.chains import LLMChain 
from langchain_core.documents import Document 
from langchain.memory import ConversationBufferMemory 
from langchain.chains import SequentialChain

import streamlit as st

llm = OCIGenAI(
    model_id="cohere.command",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id="ocid1.compartment.oc1..aaaaaaaaud6tkXXXXXXcmj54u32q", 
     model_kwargs={"temperature": 0, "max_tokens": 200}, 
)  

# streamlit framework 
st.title('Enter a disease name')
input_text=st.text_input("Enter a disease name to know about the disease, symptoms and first aid")

# Prompt Templates 
first_input_prompt=PromptTemplate(
    input_variables=['name'],
    template="What is {name}"
)
second_input_prompt=PromptTemplate(
    input_variables=['aboutinfo'],
    template="what are the symptoms of {aboutinfo} "
)
third_input_prompt=PromptTemplate(
    input_variables=['name'],
    template="what is the first aid for {name} "
)
# Memory

name_memory = ConversationBufferMemory(input_key='name', 
                                            memory_key='chat_history')
aboutinfo_memory = ConversationBufferMemory(input_key='aboutinfo', 
                                           memory_key='chat_history')
symptoms_memory = ConversationBufferMemory(input_key='symptoms', 
                                        memory_key='description_history')
  
chain=LLMChain(
    llm=llm,prompt=first_input_prompt,
    verbose=True,
    output_key='aboutinfo',memory=name_memory)
   
chain2=LLMChain(
    llm=llm,prompt=second_input_prompt,verbose=True,
    output_key='symptoms',memory=aboutinfo_memory)

chain3=LLMChain(llm=llm,prompt=third_input_prompt,verbose=True,
    output_key='firstaid',memory=symptoms_memory)

parent_chain=SequentialChain(
    chains=[chain,chain2,chain3 ],input_variables=['name'],
    output_variables=['aboutinfo','symptoms','firstaid' ],verbose=True)
 
if input_text:
    st.write(parent_chain({'name':input_text}))

    with st.expander('Disease Name'): 
        st.info(name_memory.buffer)

    with st.expander('Disease About Information'): 
        st.info(aboutinfo_memory.buffer)

    with st.expander('Disease Symptoms'): 
        st.info(symptoms_memory.buffer)