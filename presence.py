import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
gemini_model = ChatGoogleGenerativeAI(api_key=api_key,model="gemini-1.5-flash", temperature=0.2)

def check_brand_visibility_with_gemini(brand_name):
    visibility_results = {}

    prompt = (
        f"You are an expert AI researcher tasked with evaluating the online presence and visibility of the brand **{brand_name}** "
        f"across different countries for AI-powered platforms like ChatGPT, Perplexity, and Google SGE.\n\n"
        f"Please assess how well-known and visible the brand is in the following countries:\n"
        f"- India\n"
        f"- United States (USA)\n"
        f"- United Kingdom (UK)\n\n"
        f"Instructions:\n"
        f"1. Assign a visibility score out of 100 for each country, based on your understanding of how prominently the brand appears in AI-generated responses, AI search results, and general brand awareness.\n"
        f"2. Briefly explain the reasoning behind each score.\n"
        f"3. If the brand is niche or not widely visible, mention possible reasons.\n"
        f"4. Suggest 2–3 ways the brand could improve its AI visibility if applicable.\n\n"
        f"Strict Response Format:\n"
        f"Brand: {brand_name}\n\n"
        f"Visibility by Country:\n"
        f"- India: <score>/100 – <reason>\n"
        f"- USA: <score>/100 – <reason>\n"
        f"- UK: <score>/100 – <reason>\n\n"
        f"Suggestions to Improve Visibility:\n"
        f"- <suggestion 1>\n"
        f"- <suggestion 2>\n"
        f"- <suggestion 3>\n"
    )

    # Send request to Gemini model
    try:
        response = gemini_model.invoke(prompt)
        lines = response.content.split('\n')
        for idx, line in enumerate(lines, 1):
            visibility_results[str(idx)] = line
    except Exception as e:
        visibility_results["error"] = f"Error occurred: {e}"

    return visibility_results
