# TalentFlow AI 🚀

**Next-Gen Job Recommendation System**

TalentFlow AI is a smart job search assistant that helps you find the perfect role by analyzing your resume against live job listings. Instead of just keyword matching, we use **Google's Gemini AI** to "read" your resume and tell you exactly *why* a job is a good fit (or why it isn't) and give you tips to improve your chances.

## How It Works 🧠

1.  **Scan**: We search major platforms like **LinkedIn** and **Workday** (checking top tech companies like NVIDIA, Adobe, etc.) for jobs matching your role.
2.  **Analyze**: You upload your PDF resume.
3.  **Match**: Our AI compares your resume to each job description, scoring your compatibility and generating personalized advice.

## Why We Built Our Own Scraper 🛠️

Initially, I planned to use **Apify's API** to fetch job data. It’s a great tool, but I realized I wanted more control and zero cost for the users.

So, I decided to build a **custom scraper from scratch**:
*   **Cost-Effective**: No expensive API credits needed.
*   **Real-Time**: It fetches fresh data directly from career pages.
*   **Advance Filtering**: I could teach it to act like a human (e.g., ignoring jobs with hidden titles like "***" or strictly filtering for "India" when requested).
*   **Flexibility**: Changing from just one company to scanning multiple Workday sites (Amazon, Workday, etc.) was easy because I owned the code.

## Setup & Run 🏃‍♂️

It's super easy to get started.

### 1. Prerequisites
*   Python installed on your machine.
*   A Google Gemini API Key (It's free!).

### 2. Install
Clone the repo and install the dependencies:
```bash
git clone https://github.com/Vidhi-bhutia/Job-Recommendation-System.git
cd Job-Recommendation-System
pip install -r requirements.txt
```

### 3. Configure
Create a `.env` file in the root folder and add your API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 4. Launch
Start the application:
```bash
python app.py
```
Open your browser and search for your dream job! ✨

## Technologies Used 💻
*   **Backend**: Flask (Python)
*   **AI**: Google Gemini 1.5 Flash
*   **Frontend**: HTML5, CSS3 (Custom Design)
*   **Scraping**: BeautifulSoup4, Requests

---
*Built with ❤️ by Vidhi Bhutia*
