import os
import json
import re
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import LLMChain

# ✅ Load environment variables
load_dotenv()
os.environ["USER_AGENT"] = "Mozilla/5.0 (compatible; ColdEmailBot/1.0; +https://github.com/keerthanadevi)"

def extract_job_details(url):
    try:
        # Load webpage
        loader = WebBaseLoader(url)
        docs = loader.load()

        # ✅ LLM with explicit API key
        llm = ChatGroq(
            model="llama3-8b-8192",
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY")
        )

        prompt = PromptTemplate(
            input_variables=["page_content"],
            template=(
                "Extract job details from the following careers/job page. "
                "Respond ONLY in JSON with keys: title, company, skills.\n\n"
                "{page_content}"
            ),
        )

        chain = LLMChain(llm=llm, prompt=prompt)
        result = chain.run(page_content=docs[0].page_content)

        # Try parsing JSON safely
        try:
            job_info = json.loads(result)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", result, re.DOTALL)
            job_info = json.loads(match.group()) if match else {}

        return {
            "title": job_info.get("title", "").strip(),
            "company": job_info.get("company", "").strip(),
            "skills": job_info.get("skills", []) if isinstance(job_info.get("skills"), list) else []
        }

    except Exception as e:
        print(f"❌ Error extracting job info: {e}")
        return {"title": "", "company": "", "skills": []}
