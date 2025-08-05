import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

load_dotenv()

def generate_cold_email(job_info, links):
    prompt = PromptTemplate(
        input_variables=["role", "skills", "links"],
        template="""
Write a short cold email expressing interest in the following job role.

Job Role:
{role}

Skills required:
{skills}

Relevant project portfolio links:
{links}

Make it professional, enthusiastic, and include a call to action.
"""
    )

    llm = ChatGroq(
        temperature=0.4,
        model_name="llama3-8b-8192",
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    chain = LLMChain(prompt=prompt, llm=llm)
    result = chain.invoke({
        "role": job_info["role"],
        "skills": ", ".join(job_info["skills"]),
        "links": "\n".join(links)
    })
    return result.get("text", result)
