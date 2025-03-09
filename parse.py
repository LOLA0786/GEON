import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

os.environ["GOOGLE_API_KEY"] = api_key
# Initialize Gemini Pro model
gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

# Function to parse data using Gemini
def parse_with_gemini(dom_chunks, parse_description):
    parsed_results = []

    template = (
        f"You are tasked with extracting specific information from the following text content: {dom_chunks}. "
        f"Please follow these instructions carefully:\n\n"
        f"1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
        f"2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
        f"3. **Empty Response:** If no information matches the description, return data unavailabel"
        f"4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
    )

    # Send request to Gemini model
    response = gemini_model.invoke(template)
    parsed_results.append(response.content)

    return parsed_results
