# AI-Driven Code Reviewer

An intelligent Python code reviewer powered by Groq's LLaMA AI. This Streamlit application analyzes your code and provides detailed feedback on readability, performance, best practices, and PEP8 compliance.

## Features

✨ **AI-Powered Code Analysis** - Leverages Groq's LLaMA 3.1 model for intelligent code review
📊 **Comprehensive PEP8 Compliance Check** - Detects style issues and provides improvement suggestions
🔍 **Error Detection** - Identifies potential bugs and logical errors in your code
💡 **Code Suggestions** - Receives AI-powered recommendations for code improvements
✅ **Corrected Code** - Get a fully corrected version of your code with all issues fixed
📈 **PEP8 Score** - Receives a score before and after corrections

## Tech Stack

- **Streamlit** - Web UI framework
- **LangChain** - LLM orchestration
- **Groq API** - Fast AI inference
- **Python** - Core language

## Installation

### Prerequisites
- Python 3.13+
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/sagar-p-mtr/AI-Driven-Code-Reviewer.git
cd "Development of Ai Driven Code Reviewer"
```

2. **Create a virtual environment**
```bash
python -m venv .venv
.\.venv\Scripts\Activate  # On Windows
source .venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

Get your Groq API key from: https://console.groq.com/keys

5. **Run the application**
```bash
streamlit run app.py
```

The app will be available at: `http://localhost:8501`

## Usage

1. **Paste your Python code** in the "Code Input" text area
2. **Click "Analyze"** to start the review
3. **View results** including:
   - Original code formatting
   - Suggestions for readability, performance, and best practices
   - PEP8 compliance analysis with issues identified
   - Corrected code with all improvements applied
   - PEP8 score comparison (before and after)

## Project Structure

```
├── app.py                 # Main Streamlit application
├── ai_suggester.py       # AI code review logic using Groq
├── code_parser.py        # Python code parsing and validation
├── error_detector.py     # Error detection module
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in repo)
└── README.md            # This file
```

## Features Breakdown

### Code Parser
- Validates Python syntax
- Checks for parsing errors

### Error Detector
- Identifies logical errors
- Detects potential runtime issues

### AI Suggester
- Sends code to Groq's LLaMA model
- Receives structured feedback including:
  - Original code display
  - Readability suggestions
  - Performance recommendations
  - Best practices guidance
  - PEP8 style analysis
  - Corrected code
  - PEP8 compliance score

## API Response Format

The AI returns structured analysis with:
```
1. ORIGINAL CODE
2. SUGGESTIONS (Readability, Performance, Best Practices)
3. CODING STYLE ANALYSIS (PEP8)
   - Naming Issues
   - Structure Issues
   - Logic & Type Issues
   - Score: X/10
4. CORRECTED CODE
5. PEP8 SCORE (After corrections)
```

## Requirements

- `streamlit` - Web UI
- `langchain` - LLM framework
- `langchain-core` - Core LLM utilities
- `langchain-groq` - Groq integration
- `huggingface-hub` - Hugging Face integrations
- `python-dotenv` - Environment variable management

## Configuration

### Streamlit Settings
Config file location: `~/.streamlit/config.toml`

### LLM Settings
- **Model**: LLaMA 3.1 8B Instant
- **Temperature**: 0.3 (balanced creativity and consistency)
- **Max Tokens**: 2048
- **Timeout**: 120 seconds

## Troubleshooting

### "ModuleNotFoundError" errors
```bash
pip install -r requirements.txt
```

### "GROQ_API_KEY is missing"
- Ensure `.env` file exists in project root
- Add your Groq API key: `GROQ_API_KEY=your_key_here`

### Streamlit cache issues
```bash
streamlit cache clear
streamlit run app.py
```

## Performance

- **Fast inference** powered by Groq's optimized LLaMA
- **Real-time analysis** with streaming capabilities
- **Typical response time**: 2-5 seconds per code review

## Future Improvements

- Support for multiple programming languages
- Customizable analysis depth
- Code metrics and complexity analysis
- Batch processing for multiple files
- Integration with CI/CD pipelines
- Custom review rules and guidelines

## License

This project is open source and available under the MIT License.

## Support

For issues, feature requests, or contributions, please visit:
https://github.com/sagar-p-mtr/AI-Driven-Code-Reviewer

## Author

**Sagar P. MTR**
- GitHub: https://github.com/sagar-p-mtr
- Project: AI-Driven Code Reviewer
