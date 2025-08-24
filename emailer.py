import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import LLMChain

# ✅ Load environment variables
load_dotenv()

def generate_cold_email(job_info, portfolio_links):
    try:
        llm = ChatGroq(
            model="llama3-8b-8192",
            temperature=0.3,
            api_key=os.getenv("GROQ_API_KEY")
        )

        prompt = PromptTemplate(
            input_variables=["title", "company", "skills", "portfolio_links"],
            template=(
                "Write a professional cold email for a job opportunity.\n\n"
                "Job Title: {title}\n"
                "Company: {company}\n"
                "Skills Required: {skills}\n"
                "Portfolio Links: {portfolio_links}\n\n"
                "The email should:\n"
                "1. Mention the job role and company name.\n"
                "2. Highlight matching skills.\n"
                "3. Include portfolio links naturally.\n"
                "4. End with a polite call to action.\n\n"
                "📧 Email:"
            ),
        )

        chain = LLMChain(llm=llm, prompt=prompt)
        email = chain.run(
            title=job_info.get("title", ""),
            company=job_info.get("company", ""),
            skills=", ".join(job_info.get("skills", [])),
            portfolio_links="\n".join(portfolio_links),
        )

        return email

    except Exception as e:
        return f"❌ Could not generate email. Error: {e}"
