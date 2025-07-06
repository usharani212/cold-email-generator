import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            groq_api_key='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'
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the
            following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'page_data': cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, json_res, query_result):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Usha, a final-year student at Gayatri Vidya Parishad College of Engineering (GVPCE), pursuing a degree in Computer Science and Engineering with a specialization in Data Science. GVPCE is an autonomous institution located in Visakhapatnam.

            Your task is to write a short and polite cold message to a recruiter or professional on LinkedIn requesting a referral for the job described above.

            Use the job description to:
            - Match those skills with the most relevant ones from the portfolio links provided in the input.
            - Insert only the **most relevant** portfolio links that reflect the job requirements.
            - Mention that you are a fresher who is enthusiastic about learning and contributing.
            - Keep the tone respectful, humble, and professional — avoid sounding overly confident.
            - End the message with a thank you and sign off with **your full name: Usharani Pitta**.
            - Do not include any preamble or introductory sentence that restates the task.
            - The message should sound like it’s being sent through LinkedIn or email directly to a recruiter — informal yet respectful.

            ### INPUT LINKS:
            {link_list}

            ### MESSAGE (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": str(json_res),
            "link_list": query_result
        })
        return res.content  # ✅ Return to be used in Streamlit or wherever
