import os
import json
from langchain_community.document_loaders import WebBaseLoader
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import LLMChain

# ✅ Set a default USER_AGENT to avoid warnings
os.environ["USER_AGENT"] = "Mozilla/5.0 (compatible; ColdEmailBot/1.0; +https://github.com/keerthanadevi)"

def extract_job_details(url):
    try:
        # Load webpage
        loader = WebBaseLoader(url)
        docs = loader.load()

        # Prepare LLM
        llm = ChatGroq(model="llama3-8b-8192", temperature=0)
        prompt = PromptTemplate(
            input_variables=["page_content"],
            template=(
                "Extract job details from the following page content. "
                "Respond ONLY in JSON with keys: title, role, skills.\n\n"
                "{page_content}"
            ),
        )

        chain = LLMChain(llm=llm, prompt=prompt)
        result = chain.run(page_content=docs[0].page_content)

        # Try to parse JSON
        try:
            job_info = json.loads(result)
        except json.JSONDecodeError:
            # Fallback: Try to extract JSON part only
            import re
            match = re.search(r"\{.*\}", result, re.DOTALL)
            if match:
                try:
                    job_info = json.loads(match.group())
                except:
                    job_info = {}
            else:
                job_info = {}

        # ✅ Safely get values without KeyError
        job_info = {
            "title": job_info.get("title", "").strip(),
            "role": job_info.get("role", "").strip(),
            "skills": job_info.get("skills", [])
            if isinstance(job_info.get("skills"), list)
            else [],
        }

        return job_info

    except Exception as e:
        print(f"❌ Error extracting job info: {e}")
        return {"title": "", "role": "", "skills": []}
