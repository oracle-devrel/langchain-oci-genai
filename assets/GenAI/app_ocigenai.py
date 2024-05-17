import streamlit as st
from langchain.prompts import PromptTemplate
#from langchain.llms import CTransformers
from langchain_community.llms import OCIGenAI 

## Function To get response from  model

def getLLamaresponse(input_text,no_words,movie_style):
 
    llm = OCIGenAI(
    model_id="cohere.command",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id="<your-compartment-ocid>", 
     model_kwargs={"temperature": 0, "max_tokens": 256}, 
    )  

    
    ## Prompt Template 
    template="""
        Write a movie script for {movie_style} on the topic {input_text}
        within {no_words} words.
        """
    
    prompt=PromptTemplate(input_variables=["movie_style","input_text",'no_words'],
                          template=template)
    
    ## Generate the ressponse from the LLama 2 model
    response=llm(prompt.format(movie_style=movie_style,input_text=input_text,no_words=no_words))
    print(response)
    return response
 
st.set_page_config(page_title="🦜🔗 Generate Movie Script",
                    page_icon='',
                    layout='centered',
                    initial_sidebar_state='collapsed')
 
st.header("Generate Movie Script")

input_text=st.text_input("Enter the Movie Subject - Oracle Generative AI")

## creating to more columns for additonal 2 fields

col1,col2=st.columns([5,5])

with col1:
    #no_words=st.text_input('No of Words')
    no_words=768
with col2:
    movie_style=st.selectbox('Writing the script for',
                            ('Horror Movie','Romantic Movie','Science Fiction','Hollywood Classic'),index=0)
    
submit=st.button("Generate")

## Final response
if submit:
    st.write(getLLamaresponse(input_text,no_words,movie_style))
 