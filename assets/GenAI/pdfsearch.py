import streamlit as st
from langchain_community.llms import OCIGenAI 
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_community.embeddings import OCIGenAIEmbeddings
from langchain_community.vectorstores import Chroma

st.title('🦜🔗 PDF AI Search Application')
 
def generate_response(input_text): 
  loader = PyPDFLoader("budget_speech.pdf")
  pages = loader.load_and_split()
  llm = OCIGenAI(
    model_id="cohere.command",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id="ocid1.compartment.oc1..aaaaaaaaud6tkXXXXX32q",
    model_kwargs={"temperature": 0.7, "top_p": 0.75, "max_tokens": 300}
  )  
  embeddings = OCIGenAIEmbeddings(
    model_id="cohere.embed-english-light-v3.0",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id="ocid1.compartment.oc1..aaaaaaaaud6tXXXXXcmj54u32q",
  ) 
  vectorstore = Chroma.from_documents(
        pages,
        embedding=embeddings    
    )
  retriever = vectorstore.as_retriever()
  template = """ 
  {context}
  Indian Budget Speech : {input} 
  """
  prompt = PromptTemplate.from_template(template) 
  st.info(llm(input_text))

with st.form('my_form'):
  text = st.text_area('Enter Search:','What is Amrit Kaal?')
  submitted = st.form_submit_button('Submit') 
generate_response(text)

#streamlit run pdfsearch.py