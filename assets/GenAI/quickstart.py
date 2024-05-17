import streamlit as st
from langchain_community.llms import OCIGenAI 
 

st.title('🦜🔗 Quickstart App')
 
def generate_response(input_text): 
  llm = OCIGenAI(
    model_id="cohere.command",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id="ocid1.compartment.oc1..aaaaaaaaud6tkdXXXXoixcmj54u32q",
    model_kwargs={"temperature": 0.7, "top_p": 0.75, "max_tokens": 300}
  )  
  st.info(llm(input_text))

with st.form('my_form'):
  text = st.text_area('Enter text:', 
                      'What is Oracle Generative AI?')
  submitted = st.form_submit_button('Submit') 
generate_response(text)