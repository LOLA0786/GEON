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

def get_score(dom_chunks, html_structure):
    WEIGHTS = {
        'content_quality': 0.20,
        'structure_score': 0.15,
        'entity_linking_score': 0.15,
        'prompt_visibility': 0.15,
        'response_alignment': 0.10,
        'ai_readable_format': 0.15,
        'freshness_score': 0.10
    }

    template = f"""
        You are evaluating a web page's AI visibility and Generative Engine Optimization (GEO).
        Please assess the content based on the following 7 criteria and return scores for each on a scale of 0 to 100.

        Input data:
        -------------
        raw_text_content:
        \"\"\"
        {dom_chunks}
        \"\"\"

        html_structure:
        \"\"\"
        {html_structure}
        \"\"\"

        Evaluation Criteria (with weights):
        -----------------------------------
        1. *content_quality* (20%) – How informative, relevant, and well-written is the content?
        2. *structure_score* (15%) – How well is the HTML structured with headings, hierarchy, and sections?
        3. *entity_linking_score* (15%) – Are there proper mentions and hyperlinks to recognized entities (people, products, organizations)?
        4. *prompt_visibility* (15%) – How well does the content answer typical user prompts or queries?
        5. *response_alignment* (10%) – Does the content align with how LLMs are expected to generate responses?
        6. *ai_readable_format* (15%) – Is the content easily readable by AI (minimal ads, proper formatting, semantic HTML)?
        7. *freshness_score* (10%) – Is the content recent and regularly updated?

        Response format:
        ----------------
        Only return a valid JSON object (no commentary or extra text), like:

        {{
          "content_quality": 85,
          "structure_score": 70,
          "entity_linking_score": 60,
          "prompt_visibility": 75,
          "response_alignment": 80,
          "ai_readable_format": 72,
          "freshness_score": 68
        }}

        Ensure your response is strict JSON.
        """


    try:
        response = gemini_model.invoke(template)
        raw_output = response.content.strip()

        if raw_output.startswith("json"):
            raw_output = re.sub(r"^json\s*|\s*```$", "", raw_output, flags=re.DOTALL)

        parsed_scores = json.loads(raw_output)

        # Compute final weighted GEO score
        final_score = 0
        for key, weight in WEIGHTS.items():
            if key in parsed_scores:
                final_score += parsed_scores[key] * weight
            else:
                raise ValueError(f"Missing score: {key}")

        return {
            "individual_scores": parsed_scores,
            "final_geo_score": round(final_score, 2)
        }

    except json.JSONDecodeError as e:
        return {
            "error": f"JSON decode error: {e}",
            "raw_output": response.content
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {e}",
            "raw_output": str(response.content) if 'response' in locals() else ""
        }