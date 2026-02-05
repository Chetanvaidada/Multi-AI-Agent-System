# Multi-Agent AI System

A powerful multi-agent AI system built with LangChain and LangGraph that uses a **Planner-Executor-Verifier** architecture to intelligently handle complex user queries by coordinating multiple tools and APIs.

## 🏗️ Architecture

The system uses a three-agent workflow:

```
User Query → Planner → Executor → Verifier → Final Answer
```

### Agents

1. **Planner Agent**
   - Analyzes user input
   - Creates a structured JSON execution plan
   - Selects appropriate tools for each step

2. **Executor Agent**
   - Executes the plan sequentially
   - Calls the required tools with proper parameters
   - Aggregates tool outputs

3. **Verifier Agent**
   - Validates execution results
   - Formats the final answer
   - Ensures response quality

### Integrated Tools

The system integrates the following APIs:

| Tool | API | Purpose |
|------|-----|---------|
| `get_weather` | [WeatherAPI.com](https://www.weatherapi.com/) | Fetch current weather for any city |
| `wikipedia_search` | [Wikipedia API](https://pypi.org/project/wikipedia/) | Search Wikipedia summaries |
| `get_exchange_rate` | [ExchangeRate-API](https://www.exchangerate-api.com/) | Get currency exchange rates |
| `dictionary_lookup` | [DictionaryAPI.dev](https://dictionaryapi.dev/) | Look up word definitions |

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv myenv
myenv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root by copying the example:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key_here
```

#### Getting API Keys

- **Google Gemini API**: [Get it here](https://makersuite.google.com/app/apikey) (Free tier available)
- **WeatherAPI**: [Sign up here](https://www.weatherapi.com/signup.aspx) (Free tier: 1M calls/month)
- **ExchangeRate-API**: [Get key here](https://www.exchangerate-api.com/) (Free tier: 1,500 requests/month)

### 5. Run Locally

```bash
python main.py
```

The system will prompt you to enter your task. Type your query and press Enter.

## 📝 Example Prompts

Try these prompts to test the system:

1. **Weather Query**
   ```
   What's the weather like in Tokyo?
   ```

2. **Multi-Tool Query**
   ```
   What's the weather in Mumbai and how much is 100 USD in Indian Rupees?
   ```

3. **Complex Multi-Step Query**
   ```
   Who is Kylian Mbappé? What is the definition of "resilient"? 
   How much is 1 Euro in Japanese Yen? What's the temperature in Paris?
   ```

4. **Currency Conversion**
   ```
   Convert 50 USD to British Pounds
   ```

5. **Knowledge + Weather Combo**
   ```
   Tell me about Albert Einstein and what's the weather in Princeton, New Jersey?
   ```

## 🗂️ Project Structure

```
trulymadly/
├── agents/
│   ├── executor.py      # Executor agent (runs tools)
│   ├── planner.py       # Planner agent (creates plans)
│   ├── verifier.py      # Verifier agent (validates results)
│   └── tools.py         # Tool registry
├── llm/
│   └── gemini.py        # Gemini model configuration
├── tools/
│   ├── weather_tool.py       # Weather API integration
│   ├── wikipedia_tool.py     # Wikipedia search
│   ├── exchange_rate_tool.py # Currency conversion
│   └── dictionary_tool.py    # Dictionary lookup
├── graph.py             # LangGraph workflow orchestration
├── main.py              # CLI entry point
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (create this)
```

## ⚙️ How It Works

1. **User submits a query** via CLI
2. **Planner analyzes** the query and generates a JSON execution plan
3. **Executor processes** the plan step-by-step, calling necessary tools
4. **Tools fetch data** from external APIs
5. **Verifier validates** and formats the final answer
6. **Result is displayed** to the user

### Example Flow

```
Input: "What's the weather in London and who is Isaac Newton?"

Planner Output:
[
  {"tool_name": "get_weather", "parameters": {"city": "London"}},
  {"tool_name": "wikipedia_search", "parameters": {"query": "Isaac Newton"}}
]

Executor: Calls both tools in sequence

Verifier: Formats the combined results into a coherent answer
```

## ⚠️ Known Limitations & Tradeoffs

### Limitations

1. **API Rate Limits**
   - Free tier APIs have request limits (check each provider)
   - Gemini Pro: 60 requests/minute on free tier

2. **Sequential Execution**
   - Tools are executed one after another, not in parallel
   - May be slower for queries with many steps

3. **No Persistent Memory**
   - Each query is independent
   - No conversation history between sessions

4. **Language Support**
   - Wikipedia and Dictionary tools primarily support English
   - Weather API supports international cities

5. **Tool Reliability**
   - Depends on external API availability
   - Network issues may cause failures

### Tradeoffs

| Aspect | Choice | Benefit | Tradeoff |
|--------|--------|---------|----------|
| Model | Gemini Pro | Free, fast, good quality | Less capable than GPT-4 |
| Architecture | Multi-agent | Modular, explainable | More complex than single agent |
| Execution | Sequential | Predictable, debuggable | Slower than parallel |
| State Management | LangGraph | Structured workflow | Learning curve |

## 🐛 Troubleshooting

### Common Issues

**1. `ImportError: cannot import name 'create_agent'`**
- Ensure you have the latest LangChain version
- Run: `pip install --upgrade langchain langchain-google-genai`

**2. API Key Errors**
- Verify `.env` file exists and contains valid keys
- Check API key format (no quotes needed)

**3. Empty Responses**
- Check API quotas haven't been exceeded
- Verify internet connection

**4. Model Not Found Error**
- The code uses `gemini-pro` model
- Ensure your API key has access to this model

## 🔮 Future Enhancements

- [ ] Add FastAPI REST endpoint
- [ ] Implement parallel tool execution
- [ ] Add conversation memory
- [ ] Create web UI frontend
- [ ] Add more tools (news, stocks, etc.)
- [ ] Implement streaming responses
- [ ] Add authentication & rate limiting

## 📄 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

