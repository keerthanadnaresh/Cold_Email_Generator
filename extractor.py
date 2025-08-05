import os
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import json

load_dotenv()

def extract_job_details(url):
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        content = docs[0].page_content[:4000]  # limit input size

        prompt = PromptTemplate(
            input_variables=["page_data"],
            template="""
You are an AI assistant. Extract the following from the page content below and respond ONLY with JSON:

- title
- role (as a paragraph)
- skills (as a list of strings)

Return ONLY the JSON.

PAGE CONTENT:
{page_data}
"""
        )

        llm = ChatGroq(
            temperature=0.3,
            model_name="llama3-8b-8192",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

        chain = LLMChain(prompt=prompt, llm=llm)
        result = chain.invoke({"page_data": content})
        raw_text = result.get("text", result)

        # Try to extract JSON block
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1
        json_text = raw_text[start:end]
        job_info = json.loads(json_text)
        return job_info

    except Exception as e:
        print("❌ Error:", e)
        return None
