from langchain_community.document_loaders import PyPDFLoader
from langchain_community.llms import OCIGenAI 
from langchain_core.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.embeddings import OCIGenAIEmbeddings
from langchain_community.vectorstores import Chroma
  
loader = PyPDFLoader("budget_speech.pdf")
pages = loader.load_and_split()

llm = OCIGenAI(
    model_id="cohere.command",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id="ocid1.compartment.oc1..aaaaaaaaud6tkdn6n23cbvc4hexs6n4hggetkwo4viqyneyroixcmj54u32q",
    model_kwargs={"temperature": 0.7, "top_p": 0.75, "max_tokens": 1000}
)

embeddings = OCIGenAIEmbeddings(
    model_id="cohere.embed-english-light-v3.0",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id="ocid1.compartment.oc1..aaaaaaaaud6tkdn6n23cbvc4hexs6n4hggetkwo4viqyneyroixcmj54u32q",
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
 

chain = (
    {"context": retriever, 
     "input": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print(chain.invoke("What is Amrit Kaal"))
#print(chain.invoke("What is India's fiscal deficit"))
 