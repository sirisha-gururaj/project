# 🤖 MyCampusBot

MyCampusBot is a smart, AI-powered chatbot built to help students easily access information related to their college. It works by first searching a locally built college website, which acts as its primary knowledge base. If the information isn't found there, it automatically switches to a live web search—ensuring the user always receives a relevant and helpful response.

Students can choose whether they want brief summaries or detailed explanations, making the experience flexible and personalized.

This chatbot significantly reduces the time students spend searching through PDFs or scattered web pages, while also minimizing the repetitive queries faced by college staff. It’s like having a 24/7 digital assistant that understands both your question and where to find the answer.

---

## ✨ Key Features

* **RAG from Local Data**: Answers questions with high accuracy using a knowledge base built from a local website.
* **Live Web Search Fallback**: Intelligently searches the web if campus documents don't have the answer.
* **Customizable Responses**: Users can instantly switch between "Detailed" and "Concise" answers.
* **Advanced Web Scraper**: Uses Selenium to crawl the website, handle JavaScript, and extract text from both pages and PDFs.

---

## 🛠️ Tech Stack

* **Application Framework**: Streamlit
* **LLM Orchestration**: LangChain
* **LLM Provider**: Groq (Llama 3.1)
* **Vector Store**: FAISS
* **Embeddings**: Hugging Face sentence-transformers
* **Web Search**: Tavily API
* **Web Scraping**: Selenium & BeautifulSoup4
* **PDF Processing**: PyPDF2

---

## 📁 Project Structure

```
AI_UseCase/
├── .venv/                    # Virtual environment
├── app.py                    # Main Streamlit application
├── config/
│   └── config.py             # API Key configuration
├── data/                     # Scraped text files stored here
├── models/
│   ├── embeddings.py         # Embedding model initialization
│   └── llm.py                # LLM (Groq) initialization
├── utils/
│   ├── rag_utils.py          # RAG pipeline logic
│   └── search_utils.py       # Web search logic
├── scraper.py                # Script to scrape website and populate the data folder
├── requirements.txt          # Project dependencies
└── college-website/          # Local dummy college website
    ├── index.html
    └── ...
```

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Prerequisites

* Python 3.10+
* Google Chrome (installed)
* ChromeDriver (must match your Chrome version)

  * Download: [Chrome for Testing Dashboard](https://googlechromelabs.github.io/chrome-for-testing/)
  * Place `chromedriver.exe` in your project root or system PATH

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/mycampusbot.git
cd mycampusbot
```

### 3. Set Up a Virtual Environment

```bash
python -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API Keys

Open `config/config.py` and add your API keys:

```python
GROQ_API_KEY = "gsk_YourGroqApiKeyHere"
TAVILY_API_KEY = "tvly-YourTavilyApiKeyHere"
```

### 6. Build the Knowledge Base

Run the scraper to extract and store website content:

```bash
python scraper.py
```

### 7. Run the Chatbot

```bash
streamlit run app.py
```

---

## 🚀 Status

This project is functional and under active development for enhancements.

---

## 🙏 Acknowledgments

* [Streamlit](https://streamlit.io/)
* [LangChain](https://www.langchain.com/)
* [Groq](https://groq.com/)
* [Tavily](https://www.tavily.com/)
* [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/)
* [Hugging Face](https://huggingface.co/)
