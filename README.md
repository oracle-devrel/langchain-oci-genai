# langchain-oci-genai

[![License: UPL](https://img.shields.io/badge/license-UPL-green)](https://img.shields.io/badge/license-UPL-green)<!--[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=oracle-devrel_langchain-oci-genai)](https://sonarcloud.io/dashboard?id=oracle-devrel_langchain-oci-genai)-->

# How to work with LangChain and Oracle Generative AI

In this demo, we will learn how to work with **#LangChain**'s open-source building blocks, components & **#LLMs **integrations, **#Streamlit**, an open-source **#Python** framework for **#DataScientists** and AI/ML engineers and **#OracleGenerativeAI** to build the next generation of Intelligent Applications. 

We will lay the groundwork by setting up the OCI Command line interface, Creating a simple LongChain app, writing an interactive **#Healthcare** application, and creating a search application that can scan through a training **#PDF** document. 

**What is LangChain?**

[**LangChain**][6] is a framework for developing applications powered by large language models (LLMs). 


[6]: https://www.langchain.com/

LangChain simplifies every stage of the LLM application lifecycle: 

- **Development**: Build your applications using LangChain's open-source building blocks and components. Hit the ground running using third-party integrations and Templates.
- **Productionization**: Use [LangSmith][7] to inspect, monitor and evaluate your chains, so that you can continuously optimize and deploy with confidence.

[7]: https://python.langchain.com/docs/langsmith/

With LangChain we can build **context-aware** reasoning applications with LangChain's flexible framework that leverages your company's data and APIs. Future-proof your application by making vendor optionality part of your LLM infrastructure design. 

**What is Streamlit?**

A faster way to build and share data apps. [Streamlit][8] turns data scripts into shareable web apps in minutes. All in pure Python. No front‑end experience is required. 

[8]: https://streamlit.io/


### How does LangChain work with Oracle Generative AI?

This is a 3-step process. 

1. Set up the OCI Command Line Interface on your laptop or use a Cloud Compute Instance.
2. Install required Python libraries.
3. Write and Run the Python code.

**Assumption:**

1. You already have an Oracle cloud account and access to Oracle Generative AI in the Chicago region. 
2. You have a default compartment created.
3. You have administrative rights in the tenancy or your Administrator has set up required policies to access [Generative AI Services][9].
4. [Download Python Code][10] and [Budget PDF.][11] used in this article.


[9]: https://docs.oracle.com/en-us/iaas/Content/generative-ai/iam-policies.htm
[10]: https://github.com/langchain-oci-genai/tree/main/assets/GenAI
[11]: https://github.com/langchain-oci-genai/tree/main/assets/budget_speech.pdf

### Step 1: Installing OCI CLI and Configuring

### Get User's OCID

1. After logging into the cloud console, click on User Settings under the top right navigation; this will take you to **the User Details** page. Copy the OCID into a text file. We will need this later..

    ![][12]


2. Under the same page click on **Add API Key** button 

    ![][13]

[12]: images/1712837918418.jpg
[13]: images/1712837944195.jpg

### Generate and Download RSA Key Pair

1. Choose an Option to Generate a new key pair; if you already have keys generated, you can upload them here, The most important is when you generate the key pair, download both of them, Click **the Add** button

    ![][14]

    You should now be able to see the Configuration file. Copy and paste this into a file we will need later. 

    ![][15]

    Click on **Close** button 

2. We can now see our newly created fingerprint 

    ![][16]


[14]: images/1712837990031.jpg
[15]: images/1712838022822.jpg
[16]: images/1712838294532.jpg

### Get Compartment OCID

Under Identity > Compartments, note your compartment OCID; we will need this OCID later. 

![][17]


[17]: images/1712895249226.jpg

### Install OCI Command Line Interface (CLI)

1. **Install OCI CLI on MAC OS**
2. If you have not installed Brew on your MacOS, please refer to their official guide, [Install Brew on Mac][18]:

        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
        brew update && brew install oci-cli

    For Other Operating systems and more details on OCI CLI [please check this link][19]. 

[18]: https://docs.brew.sh/Installation
[19]: https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm#

### Update OCI Configuration file

Update DEFAULT values as per your OCI parameters :

    vi ~/.oci/config

The parameters will look something like this:

    [DEFAULT]
    user=ocid1.user.oc1..aaaaaaXXXX63smy6knndy5q
    fingerprint=d5:84:a7:0e:XXXX:ed:11:1a:50
    tenancy=ocid1.tenancy.oc1..aaaaaaaaj4XXXymyo4xwxyv3gfa
    region=us-phoenix-1 #(replace-with-your-oci-region)
    key_file=/your-folder/your-oci-key.pem

See if we can list all buckets in a compartment to check if all configurations are correct. Provide your compartment ocid where the OCI buckets have been created 

```console
-- set chmod on .pem file  --
chmod 600 /your-folder/your-oci-key.pem

-- get tenancy namespace --
oci os ns get

{
  "data": "yournamespace"
}

-- run oci cli to list buckets in a OCI Object storage 
oci os bucket list --compartment-id ocid1.compartment.oc1..aXXXn4hgg

-- expect a similar JSON output without errors --

  {
      "compartment-id": "ocid1.compartment.oc1..aXXX32q", 
      "defined-tags": null,
      "etag": "25973f28-5125-4eae-a37c-73327f5c2644",
      "freeform-tags": null,
      "name": "your-bucket-name",
      "namespace": "your-tenancy-namespace",
      "time-created": "2023-03-26T16:18:17.991000+00:00"
    }
```

If this lists objects in an OCI bucket or the name of your tenancy namespace, we are good to move forward; you can create a bucket in OCI Object storage and test it. If there are issues, check the troubleshooting section in this article. 

### Step 2: Install the required Python libraries

Please add any additional libraries as required to run the Python code. 

```console
python3 --version
Python 3.10.4

pip install -U langchain oci
langchain-core
langchain-cli
langchain_cohere 
cohere
langgraph 
langsmith
streamlit 
```

### Step 3: Write and Run the Python code.

The basic command to get the Oracle LLM handle is shown below:

```python
from langchain_community.llms import OCIGenAI 

...

llm = OCIGenAI(
    model_id="cohere.command",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id="<Your-Compartment-Id>",
    model_kwargs={"temperature": 0.7, "top_p": 0.75, "max_tokens": 1000}
)
```

To get OCI Generative AI Embeddings 

```python
from langchain_community.llms import OCIGenAI 
from langchain_community.embeddings import OCIGenAIEmbeddings

...

embeddings = OCIGenAIEmbeddings(
    model_id="cohere.embed-english-light-v3.0",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com", 
    compartment_id="<Your-Compartment-Id>",
)
```

### Example 1: Simple Generative AI Console App

Let's start with a basic Python code in the console to check the connectivity, authentication and AI response. 

![][20]


[20]: images/1712895679841.jpg

Download [Basic.py][21] run the Python code, and view output 

[21]: http://Basic.py

```console
python3 basic.py

The Egyptians built the pyramids. The Egyptian pyramids are ancient pyramid-shaped masonry structures located in Egypt.
```

### Example 2: Simple Generative AI Web Application with Input

In this simple Generative AI Application, we will just take input prompt and display AI result. 

![][22]


[22]: images/1712895931279.jpg

Download [quickstart.py][23] and run the code.


[23]: https://github.com/langchain-oci-genai/tree/main/assets/GenAI

Run the code from your laptop or desktop command prompt 

```console
$ streamlit run quickstart.py

You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.X.Y:8501
```

![][24]


[24]: images/1712826035917.jpg

![][25]

[25]: images/1712826094620.jpg

### Example 3: Simple Healthcare AI Application

Build your first LangChain and Oracle Generative AI-based Healthcare Application. In this Application, we will take disease as input, and based on this, we will create a LangChain that will list the disease, symptoms and first aid. 

**Code:** Get the required imports and initialise Oracle Generative AI LLM 

![][26]

[26]: images/1712896566863.jpg

Build the Streamlit framework and input prompts. 

![][27]

[27]: images/1712896636612.jpg

Initialise Memory and Chains 

![][28]

[28]: images/1712896739610.jpg

Set SequentialChain and Print output on the browser 

![][29]

[29]: images/1712896835859.jpg

Download [symptoms.py][30] and run the code. 

[30]: https://github.com/langchain-oci-genai/tree/main/assets/GenAI

Run the Application:

```console
$ streamlit run symptoms.py

You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.X.Y:8501
```

![][31]


[31]: images/1712826990273.jpg

![][32]


[32]: images/1712827016788.jpg

### Example 4: PDF Search AI Application

A smart application that can read and search PDFs and provide AI output for a given prompt. Download and put the [Budget PDF][33] in the same directory as the Python code. 
    
    
[33]: https://github.com/langchain-oci-genai/tree/main/assets/budget_speech.pdf

Prompt: What is Amrit Kaal?  lets check in the PDF document

```python
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
    compartment_id="<Your-Compartment-Id>",
    model_kwargs={"temperature": 0.7, "top_p": 0.75, "max_tokens": 1000}
)

embeddings = OCIGenAIEmbeddings(
    model_id="cohere.embed-english-light-v3.0",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id="<Your-Compartment-Id>",
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
```

Run the code in the terminal:

![][34]

[34]: images/1712837027530.jpg

```console
$ python3 searchpdf.py

-- Output from Generative AI after searching the PDF --

The Indian Budget Speech outlines the government's plans and priorities for the fiscal year 2024-25. One of the key focus areas highlighted in the speech is the concept of "Amrit Kaal," which translates to "Era of Immortality" or "Golden Era." 

The government aims to foster inclusive and sustainable development to improve productivity, create opportunities for all, and contribute to the generation of resources to power investments and fulfill aspirations. 

To achieve this, the government intends to adopt economic policies that facilitate growth and transform the country. This includes ensuring timely and adequate finances, relevant technologies, and appropriate training for Micro, Small and Medium Enterprises (MSME) to compete globally.  

....
```

Change the prompt and re-run the same code 

    -- update the code --
    print(chain.invoke("What is India's fiscal deficit"))
    
    -- run the code --
    $ python3 searchpdf.py

AI Output after searching through the Budget PDF is. 

    India's fiscal deficit for the year 2024-25 is estimated to be 5.1% of GDP, according to a budget speech by the country's Finance Minister Nirmala Sitharaman. This is in line with the government's goal to reduce the fiscal deficit to below 4.5% by 2025-26. 
    
    Would you like me to tell you more about India's budgetary process or fiscal policies?

### Example 5: PDF Search AI Application Streamlit version

![][35]


[35]: images/1712976897287.jpg

![][36]

[36]: images/1712976912969.jpg

```python
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
    compartment_id="<Your-Compartment-Id>",
    model_kwargs={"temperature": 0.7, "top_p": 0.75, "max_tokens": 300}
  )  
  embeddings = OCIGenAIEmbeddings(
    model_id="cohere.embed-english-light-v3.0",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id="<Your-Compartment-Id>",
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
```

[Download Python Code][37] and [Budget PDF][38] used 


[37]: https://github.com/langchain-oci-genai/tree/main/assets/GenAI
[38]: https://github.com/langchain-oci-genai/tree/main/assets/budget_speech.pdf

### Troubleshooting:

Error Message:

```console
Traceback (most recent call last):
  File "/some-folder/basic.py", line 3, in <module>
    llm = OCIGenAI(
  File "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/langchain_core/load/serializable.py", line 120, in __init__
    super().__init__(**kwargs)
  File "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/pydantic/v1/main.py", line 341, in __init__
    raise validation_error
pydantic.v1.error_wrappers.ValidationError: 1 validation error for OCIGenAI
__root__
  Could not authenticate with OCI client. Please check if ~/.oci/config exists. If INSTANCE_PRINCIPLE or RESOURCE_PRINCIPLE is used, Please check the specified auth_profile and auth_type are valid. (type=value_error)
```

**Solution**: This is an Authentication issue, Verify the config file settings:

```console
$ vi ~/.oci/config

[DEFAULT]
user=ocid1.user.oc1..aaaaaaaaompuufgfXXXXndy5q
fingerprint=d5:84:a7:0e:bf:43:XXXXX:11:1a:50
tenancy=ocid1.tenancy.oc1..aaaaaaaaXXXXXgfa
region=us-phoenix-1
key_file=/Users/somefolder/oci_api_key_xxx.pem
```

References: 

[Oracle Cloud Infrastructure Generative AI][39]


[39]: https://python.langchain.com/docs/integrations/llms/oci_generative_ai/

[OCI CLI reference][40]


[40]: https://docs.oracle.com/en-us/iaas/tools/oci-cli/3.39.0/oci_cli_docs/cmdref/os/bucket/list.html

## Contributing

This project welcomes contributions from the community. Before submitting a pull
request, please [review our contribution guide](./CONTRIBUTING.md).

## Security

Please consult the [security guide](./SECURITY.md) for our responsible security
vulnerability disclosure process.

## License

Copyright (c) 2024 Oracle and/or its affiliates.

Licensed under the Universal Permissive License (UPL), Version 1.0.

See [LICENSE](LICENSE.txt) for more details.

ORACLE AND ITS AFFILIATES DO NOT PROVIDE ANY WARRANTY WHATSOEVER, EXPRESS OR IMPLIED, FOR ANY SOFTWARE, MATERIAL OR CONTENT OF ANY KIND CONTAINED OR PRODUCED WITHIN THIS REPOSITORY, AND IN PARTICULAR SPECIFICALLY DISCLAIM ANY AND ALL IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE.  FURTHERMORE, ORACLE AND ITS AFFILIATES DO NOT REPRESENT THAT ANY CUSTOMARY SECURITY REVIEW HAS BEEN PERFORMED WITH RESPECT TO ANY SOFTWARE, MATERIAL OR CONTENT CONTAINED OR PRODUCED WITHIN THIS REPOSITORY. IN ADDITION, AND WITHOUT LIMITING THE FOREGOING, THIRD PARTIES MAY HAVE POSTED SOFTWARE, MATERIAL OR CONTENT TO THIS REPOSITORY WITHOUT ANY REVIEW. USE AT YOUR OWN RISK.
