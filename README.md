# 📊 AI-Powered Smart Data Analyst

An interactive, web-based data analysis and visualization tool powered by **Python**, **Streamlit**, **Pandas**, and **Google Gemini API**. It allows users to upload CSV or Excel datasets and query their data using natural language to generate instant statistical insights and charts.

🔴 **Live Demo:** [Launch AI Data Analyst](https://ai-data-analyst-gzenqhfdxkwxxs8vhyama6.streamlit.app/)

## 🚀 Key Features
- **Natural Language to Code (Text-to-Pandas):** Translates plain English or Turkish questions into executable Python (`pandas` & `matplotlib`) scripts dynamically.
- **Automated Data Visualization:** Generates bar charts, pie charts, and statistical summaries on the fly based on user prompts.
- **Fault-Tolerant Model Fallback:** Implements an automatic fallback mechanism (`gemini-3.5-flash-lite` to `gemini-3.8-flash`) to ensure uninterrupted service during API rate limits or high-demand spikes (503 errors).
- **Code Transparency:** Includes a built-in code inspector allowing users and reviewers to view the exact Python script generated and executed behind the scenes.
- **Privacy-First Architecture:** User API keys are handled dynamically via session state without being stored on the server.

## 🛠️ Tech Stack
- **Language:** Python 3
- **Frontend / Web Framework:** Streamlit
- **Data Processing & Visualization:** Pandas, Matplotlib, OpenPyXL
- **AI / LLM Integration:** Google GenAI SDK (`gemini-3.5-flash-lite` / `gemini-3.8-flash`)

## 💻 Run Locally

1. **Clone the repository:**
   ```bash
  git clone https://github.com/umuterenkaplan1/ai-data-analyst.git
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python -m streamlit run app.py
   ```
