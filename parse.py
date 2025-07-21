import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
gemini_model = ChatGoogleGenerativeAI(api_key=api_key,model="gemini-1.5-flash", temperature=0.2)

def parse_with_gemini(dom_chunks, html_structure):
    template = (
    f"You are tasked with analyzing the following website data for Generative Engine Optimization (GEO). "
    f"The input includes both the raw content text and the HTML structural layout of the webpage.\n\n"
    
    f"raw_text_content: {dom_chunks}\n"
    f"html_structure: {html_structure}\n\n"
    
    f"### Evaluation Instructions\n"
    f"Please analyze the content and structure using the following criteria.\n\n"

    f"#### Content GEO Factors (AI Readability):\n"
    f"- Relevance to a specific topic or question\n"
    f"- Clear, factual, and well-structured language\n"
    f"- Depth and semantic richness of the content\n"
    f"- Use of AI-friendly formats (e.g., lists, FAQs, bullet points)\n"
    f"- Natural keyword usage and topic coverage\n"
    f"- Unique or valuable insights beyond generic content\n"
    f"- Helpful, Q&A, or instructional tone\n"
    f"- Readability and clarity for large language models (LLMs)\n\n"

    f"#### Structure GEO Factors (HTML Optimization):\n"
    f"- Proper use of semantic headings (H1–H6)\n"
    f"- Use of schema markup (FAQ, Product, Review, etc.)\n"
    f"- Correct metadata (title, description, Open Graph, etc.)\n"
    f"- Accessibility support (alt text, ARIA labels)\n"
    f"- Logical layout and separation of sections\n"
    f"- Use of semantic tags (article, section, nav, etc.)\n"
    f"- Structured and parsable layout for AI segmentation\n"

    f"\nReturn your evaluation strictly in the following JSON key-value format:\n\n"

    f"""{{
  "content_geo_evaluation": {{
    "geo_score": <score_out_of_100>,
    "strengths": ["<strength 1>", "<strength 2>", "..."],
    "improvements": ["<improvement 1>", "<improvement 2>", "..."],
    "notes": "Optional comments about the content GEO performance"
  }},
  "structure_geo_evaluation": {{
    "geo_score": <score_out_of_100>,
    "strengths": ["<strength 1>", "<strength 2>", "..."],
    "improvements": ["<improvement 1>", "<improvement 2>", "..."],
    "notes": "Optional comments about the structure GEO performance"
  }}
}}"""
    f"\n\nOnly return the structured JSON object above. Do not include any other text."
)


    try:
        response = gemini_model.invoke(template)
        raw_output = response.content.strip()

        # Remove markdown ```json ... ``` wrapping if present
        if raw_output.startswith("```json"):
            raw_output = re.sub(r"^```json\s*|\s*```$", "", raw_output, flags=re.DOTALL)

        parsed_results = json.loads(raw_output)

    except json.JSONDecodeError as e:
        parsed_results = {
            "error": f"JSON decode error: {e}",
            "raw_output": response.content
        }
    except Exception as e:
        parsed_results = {
            "error": f"Unexpected error: {e}",
            "raw_output": str(response.content) if 'response' in locals() else ""
        }

    return parsed_results