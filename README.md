# 📊 CSV Data Agent

An intelligent, AI-powered web application that enables natural language interaction with CSV datasets. Ask questions about your data in plain English and get instant insights powered by LLM technology.

![CSV Data Agent](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## ✨ Features

- 🤖 **Natural Language Queries** - Ask questions about your data in plain English
- 📈 **Smart Analytics** - Automatic computation of averages, groupings, and filters
- 💬 **Chat Interface** - Beautiful, modern web UI with conversation history
- 🔧 **Tool Integration** - LLM intelligently selects and uses data analysis tools
- 🚀 **Fast & Responsive** - Built with FastAPI for high performance
- 🎨 **Terminal & Web interface** - Modern, gradient-based UI with smooth animations

## 🎯 Capabilities

The agent can:
- List all columns in your dataset
- Provide dataset overview (rows, columns, structure)
- Calculate averages for numeric columns
- Compute grouped averages (e.g., average sales by region)
- Filter rows based on conditions (>, <, ==)
- Explain results in clear, formatted Markdown

## 🏗️ Project Structure

```
csv-data-agent/
├── agent/
│   ├── __init__.py
│   └── chat_agent.py          # Main agent logic and LLM integration
├── tools/
│   ├── __init__.py
│   └── csv_tools.py            # CSV data manipulation tools
├── app.py                      # FastAPI web application
├── app_cli.py                  # Terminal/CLI interface
├── config.py                   # Configuration settings
|__.gitignore
|__.env.example 
|__students.csv
|            
├── requirements.txt            # Python dependencies
└── README.md                   
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- CSV dataset file

### Installation

1. **Clone or download the project**

```bash
cd csv-data-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create environment file**
```bash
cp .env.example .env
```

4. **Add your OpenRouter API key**

Open `.env` and add your API key:
```
OPENROUTER_API_KEY=your_api_key_here
```

5. **Run the application**

**Web Interface:**
```bash
uvicorn app:app --reload
```
Open browser to `http://localhost:8000`

**CLI Interface:**
```bash
python app_cli.py
```


## 💻 Usage Examples

### Web Interface

1. Start the web server
2. Open your browser to `http://localhost:8000`
3. Type your questions in natural language:

**Example Questions:**
- "What columns are in the dataset?"
- "Show me the dataset overview"
- "What's the average price?"
- "What's the average revenue by region?"
- "Show me all products with price greater than 100"

### CLI Interface

```bash
$ python app_cli.py

CSV Data Agent - Terminal Mode
============================================================
Commands: 'exit' or 'quit' to exit, 'clear' to reset

You: What columns are in the dataset?
Assistant: Your dataset contains the following columns:
- Product Name
- Category
- Price
- Quantity
- Revenue

You: What's the average price?
Assistant: The average price across all products is $45.67.
```

## 🛠️ Available Tools

The agent has access to the following data analysis tools:

### `list_columns`
Lists all column names in the CSV file.

### `dataset_overview`
Provides a summary of the dataset including row count and column information.

### `average`
Calculates the mean value of a numeric column.
- **Parameters**: `column` (string)

### `group_average`
Computes grouped averages - calculates the mean of a target column grouped by another column.
- **Parameters**: 
  - `group_by` (string) - Column to group by
  - `target` (string) - Numeric column to average

### `filter_rows`
Filters rows based on numeric conditions.
- **Parameters**:
  - `column` (string) - Column to filter on
  - `operator` (string) - One of: >, <, ==
  - `value` (number) - Value to compare against

## 🔧 Configuration

### Environment Variables

You can also use environment variables for configuration:

```bash
export API_KEY="your-api-key"
export CSV_PATH="data/sales.csv"
export MODEL="gpt-4"
```

### Custom System Prompt

Modify the `SYSTEM_PROMPT` in `config.py` to customize the agent's behavior and personality.

## 📦 Dependencies

- **fastapi** - Modern web framework for building APIs
- **uvicorn** - ASGI server for running FastAPI
- **pandas** - Data manipulation and analysis
- **openai** - OpenAI API client (or compatible LLM provider)
- **pydantic** - Data validation using Python type annotations

Install all dependencies:
```bash
pip install fastapi uvicorn pandas openai pydantic python-multipart
```

## 🎨 UI Features

- **Responsive Design** - Works on desktop and mobile devices
- **Smooth Animations** - Fade-in messages and loading indicators
- **Color-Coded Messages** - User and assistant messages are visually distinct
- **Loading States** - Visual feedback during processing
- **Session Management** - Maintains conversation history per session
- **Clear History** - Reset conversation with a single click

## 🔒 Security Notes

- Never commit your API keys to version control
- Use environment variables or a `.env` file for sensitive data
- Add `config.py` to `.gitignore` if it contains secrets
- Consider implementing rate limiting for production deployments

## 🚦 API Endpoints

### `GET /`
Serves the main web interface.

### `POST /chat`
Processes a chat message and returns the agent's response.

**Request Body:**
```json
{
  "message": "What columns are in the dataset?",
  "session_id": "default"
}
```

**Response:**
```json
{
  "response": "Your dataset contains...",
  "history": [...]
}
```

### `POST /clear`
Clears the conversation history for a session.

**Request Body:**
```json
{
  "session_id": "default"
}
```

### `GET /health`
Health check endpoint returning server status.

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use a different port
uvicorn app:app --reload --port 8001
```

### Module Not Found
```bash
# Ensure you're in the correct directory and have installed dependencies
pip install -r requirements.txt
```

### API Connection Errors
- Verify your API key is correct
- Check your internet connection
- Ensure the BASE_URL is correct for your LLM provider

### CSV Loading Issues
- Verify the CSV file path is correct
- Ensure the CSV file is properly formatted
- Check file permissions

## 📈 Future Enhancements

- [ ] Support for multiple CSV files
- [ ] Advanced visualizations (charts, graphs)
- [ ] Export analysis results
- [ ] Custom tool creation
- [ ] Database integration
- [ ] User authentication
- [ ] Sharing and collaboration features

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache License - see the LICENSE file for details.

## 👨‍💻 Author

Created with ❤️ by Marina Safwat

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: marina.safwat2002@gmail.com


---

**Note**: This is an AI-powered application. Always verify critical data analysis results independently.