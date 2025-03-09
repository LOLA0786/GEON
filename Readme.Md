# AI Web Scraper

An AI-powered web scraper that extracts website content using Selenium and processes it with AI models like Gemini to generate insights based on user prompts. The application features an interactive Streamlit frontend for real-time content analysis.

## Features
- Extracts website content using **Selenium**
- Cleans and structures scraped data with **BeautifulSoup**
- Uses **Gemini API** for AI-driven insights and analysis
- Accepts user-provided **URL and prompt** for customized scraping
- Displays results in a **Streamlit-based interactive UI**

## Tech Stack
- **Backend:** Python, Selenium, BeautifulSoup
- **AI Processing:** Gemini API, LangChain, OpenAI
- **Frontend:** Streamlit, HTML, CSS, JavaScript

## Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/ai-web-scraper.git
   cd ai-web-scraper
   ```

2. **Create and Activate Virtual Environment**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up API Key**
   - Create a `.env` file in the project directory and add your Gemini API key:
     ```sh
     GEMINI_API_KEY=your_api_key_here
     ```

5. **Run the Application**
   ```sh
   streamlit run app.py
   ```

## Usage
1. Open the Streamlit web UI.
2. Enter a website URL and a prompt describing the data you want to extract.
3. Click the "Scrape" button to retrieve and process the data.
4. View the extracted content and AI-generated insights.

## Example Prompt
```
Extract all product names and prices from this e-commerce website.
```

## Future Enhancements
- Support for multiple AI models (e.g., OpenAI, Groq, Ollama)
- Improved data visualization in Streamlit
- Integration with databases for storing scraped content

## License
This project is licensed under the MIT License.

## Contributing
Pull requests are welcome! Feel free to submit issues or feature requests.

## Contact
For any inquiries, reach out via [your email] or open an issue on GitHub.

