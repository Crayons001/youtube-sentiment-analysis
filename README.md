# YouTube Sentiment Analysis

## **Project Summary**

This project performs sentiment analysis on YouTube comments using a Flask-powered web application. The platform enables users to analyze audience feedback on specific YouTube videos by classifying comments into **positive**, **negative**, or **neutral** categories. It provides detailed insights, including sentiment distribution and highlights of the most liked comments for each sentiment.

The project leverages the following technologies:

- **Flask**: Backend framework for the web application.
- **YouTube Data API**: For retrieving video details and comments.
- **Roberta Sentiment Model**: For robust natural language processing (NLP) analysis of comments.
- **Pandas**: For data manipulation and insights generation.

Key features include:

1. Extracting video title and comments from a given YouTube URL.
2. Classifying comments into sentiments (positive, neutral, or negative).
3. Generating insights such as sentiment distribution and the most liked comments per category.
4. A web-based user interface for seamless interaction.

---

## **Installation and Setup**

Follow the steps below to install and run the application locally:

### **1. Prerequisites**

- Python 3.8 or later installed.
- A Google Cloud account with the YouTube Data API enabled.
- Internet access to download the required Python packages and models.

### **2. Clone the Repository**

Clone the project repository to your local machine:

```bash
git clone https://github.com/Crayons001/youtube-sentiment-analysis.git
cd youtube-sentiment-analysis
```

### **3. Set Up Virtual Environment (Recommended)**

Create and activate a virtual environment to isolate dependencies:

```bash
python3 -m venv venv
source venv/bin/activate   # For Linux/MacOS
venv\Scripts\activate     # For Windows
```

### **4. Install Dependencies**

Install the required Python packages:

```bash
pip install -r requirements.txt
```
Or if requirements.txt file is unavailable, you may need to install dependencies while you run the app

### **5. Configure API Key**

Create a new file named `.env` in the project root and add your YouTube Data API key:

```
API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual API key.

### **6. Run the Application**

Start the Flask application:

```bash
python run.py
```

The application will run locally on `http://127.0.0.1:5000/`.

---

## **Usage Instructions**

1. Open your browser and navigate to `http://127.0.0.1:5000/`.
2. Enter a YouTube video URL into the input field and submit.
3. The app will:
   - Fetch the video title and comments.
   - Perform sentiment analysis on the comments.
   - Display the results, including:
     - Sentiment distribution (positive, neutral, negative).
     - Most liked comments for each sentiment.
4. View the insights on the results page.

---

## **Directory Structure**

```
/
|-- app/
|   |-- __init__.py       # Initializes the Flask app
|   |-- routes.py         # Defines application routes
|   |-- static/           # Static files (CSS, JS)
|   |-- templates/        # HTML templates
|
|-- config.py             # Configuration file for API keys
|-- requirements.txt      # Python dependencies
|-- run.py                # Entry point to start the Flask app
```

---
## NOTE
The code has a maximum limit of 1100 comments to cater for running on most local PCs. However, updates will be done soon to change this. 
If you, however, wish to run analysis on more comments, simply change the following line in the youtube_operations.py file in the app directory:
```
# Navigate to the get_video_comments() function

# Limiting number of comments to 1100 ----> Remove/comment out this 'if' block
        if len(comments_df) > 1100:
            comments_df = comments_df.head(1100)

        return comments_df
```
---
I wish you a sentimental time!

