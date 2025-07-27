const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzYkBnbWFpbC5jb20iLCJleHAiOjE3NTMyODM3MTF9.1zENF7gUDhOPzjc3UlVAYr3hJ_sx3oeoNSk4dWP2BPk"

interface ScrapeResponse {
  session_id: string;
  [key: string]: unknown;
}

interface ParseResponse {
  session_id: string,
  [key: string]: unknown;
}

interface ScoreResponse {
  session_id: string,
  [key: string]: unknown;
}


export class GeoAnalysisService {
  private static readonly SCRAPE_ENDPOINT = 'http://localhost:8000/web/scrape';
  private static readonly PARSE_ENDPOINT = 'http://localhost:8000/web/parse';
  private static readonly SCORE_ENDPOINT = 'http://localhost:8000/web/get-score'

  static async scrapeWebsite(url: string): Promise<ScrapeResponse> {
    try {
      console.log('Attempting to scrape:', url);
      
      const response = await fetch(this.SCRAPE_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          "Authorization": `Bearer ${token}`,
          'Accept': 'application/json',
        },
        mode: 'cors',
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        throw new Error(`Scraping failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log('Scrape response:', data);
      return data;
    } catch (error) {
      console.error('Error scraping website:', error);
      
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Cannot connect to local API. Please ensure:\n1. Your API is running on localhost:8000\n2. CORS is enabled on your API\n3. Add these headers to your API:\n   - Access-Control-Allow-Origin: *\n   - Access-Control-Allow-Methods: POST, GET, OPTIONS\n   - Access-Control-Allow-Headers: Content-Type');
      }
      
      throw error;
    }
  }

  static async parseWebsite(sessionId: string): Promise<ParseResponse> {
    try {
      console.log('Attempting to parse with session ID:', sessionId);
      
      const response = await fetch(this.PARSE_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        mode: 'cors',
        body: JSON.stringify({ session_id: sessionId }),
      });

      if (!response.ok) {
        throw new Error(`Parsing failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log('Parse response:', data);
      return data;
    } catch (error) {
      console.error('Error parsing website:', error);
      
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Cannot connect to local API. Please ensure your API is running and CORS is enabled.');
      }
      
      throw error;
    }
  }
  static async getScores(sessionId: string): Promise<ScoreResponse> {
    try {
      console.log('Fetching scores from API');
      
      const response = await fetch(this.SCORE_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        mode: 'cors',
        body: JSON.stringify({ session_id: sessionId }),
      });

      if (!response.ok) {
        throw new Error(`Score fetch failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log('Score response:', data);
      
      // Parse the raw_output if it exists
      if (data.parsed_result?.raw_output) {
        try {
          // Extract JSON from markdown code block
          const jsonMatch = data.parsed_result.raw_output.match(/```json\n([\s\S]*?)\n```/);
          if (jsonMatch) {
            const parsedScores = JSON.parse(jsonMatch[1]);
            data.parsed_result.scores = parsedScores;
          }
        } catch (e) {
          console.warn('Could not parse raw_output JSON:', e);
        }
      }
      
      return data;
    } catch (error) {
      console.error('Error fetching scores:', error);
      
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Cannot connect to local API. Please ensure your API is running and CORS is enabled.');
      }
    }
  }

  static async analyzeWebsite(url: string): Promise<ParseResponse> {
    // First scrape the website
    const scrapeResult = await this.scrapeWebsite(url);
    
    // Then parse using the session ID
    const parseResult = await this.parseWebsite(scrapeResult.session_id);
    
    return parseResult;
  }
}