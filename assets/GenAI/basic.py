from langchain_community.llms import OCIGenAI

llm = OCIGenAI(
    model_id="cohere.command",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id="ocid1.compartment.oc1..aaaaaaaaudXXXXXixcmj54u32q", # replace with your OCID
)

response = llm.invoke("Who built pyramids", temperature=0.7)
print(response)