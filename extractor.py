import re
import json
from langchain_community.document_loaders.web import WebBaseLoader
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

def extract_job_details(url):
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        page_content = docs[0].page_content.strip()[:4000]  # limit size

        prompt = PromptTemplate(
            input_variables=["page_data"],
            template="""
Extract ONLY this JSON object from the job description:

{
  "title": "...",
  "role": "...",
  "skills": ["...", "...", "..."]
}

No extra text, no markdown.

Job description:
{page_data}
"""
        )

        llm = ChatGroq(
            temperature=0,
            model_name="llama3-8b-8192",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

        chain = LLMChain(llm=llm, prompt=prompt)
        result = chain.invoke({"page_data": page_content})
        raw_text = result.get("text", "").strip()

        # Extract JSON from anywhere in the output
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if match:
            json_text = match.group()
            return json.loads(json_text)
        else:
            return {"title": "", "role": "", "skills": []}

    except Exception as e:
        print("❌ Error extracting job info:", e)
        return {"title": "", "role": "", "skills": []}
