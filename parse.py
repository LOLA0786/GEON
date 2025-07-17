import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"] = api_key
# Initialize Gemini Pro model
gemini_model = ChatGoogleGenerativeAI(api_key=api_key,model="gemini-1.5-flash", temperature=0.2)

# Function to parse data using Gemini
def parse_with_gemini(dom_chunks):
    parsed_results = {}

    template = (
        f"You are tasked with analyzing the following web page content for Generative Engine Optimization (GEO): {dom_chunks}.\n"
        f"Please follow these instructions carefully:\n\n"
        f"1. **GEO Score:** Evaluate the content and provide a GEO score out of 100 based on how well the content is optimized for AI-generated search engines (such as ChatGPT, Perplexity, and Google SGE).\n"
        f"2. **Improvement Suggestions:** Provide specific, actionable GEO-focused suggestions to improve visibility and summarizability by generative AI systems.\n"
        f"3. **Focus Areas:** Pay special attention to the following factors:\n"
        f"   - Use of semantic HTML and structured content (headings, lists, tables, etc.)\n"
        f"   - Presence of schema markup (JSON-LD) such as Article, FAQPage, Product, etc.\n"
        f"   - Factual, clear, and verifiable information with external references\n"
        f"   - Natural language Q&A formatting\n"
        f"   - Authoritative tone, brand credibility, and updated content\n"
        f"   - Internal linking, page discoverability, and mobile responsiveness\n"
        f"4. **No Extra Content:** Do not include any additional text or explanation beyond the score and suggestions.\n"
        f"5. **Format:** Respond strictly in the following format:\n"
        f"GEO Score: <score>/100\n"
        f"Suggestions:\n"
        f"- <suggestion 1>\n"
        f"- <suggestion 2>\n"
        f"...\n"
    )

    # Send request to Gemini model
    try:
        response = gemini_model.invoke(template)
        lines = response.content.split('\n')
        for idx, line in enumerate(lines, 1):
            parsed_results[str(idx)] = line
    except Exception as e:
        parsed_results["error"] = f"Error occurred: {e}"

    return parsed_results