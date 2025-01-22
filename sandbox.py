import re
import pandas as pd
from googleapiclient.discovery import build
from tqdm.notebook import tqdm

# Running transformer models
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

# Your YouTube Data API key
API_KEY = "AIzaSyCZyIERF87OzHD_QbrkiYgXs68jjVZN7dQ"

# Initialize the YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

def get_video_id_from_url(url):
    """
    Extracts the video ID from a YouTube URL.
    
    Args:
        url (str): The YouTube video URL.
    
    Returns:
        str: The video ID if found, otherwise None.
    """
    # Patterns for YouTube video links
    patterns = [
        r"youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})",  # Full URL
        r"youtu\.be/([a-zA-Z0-9_-]{11})"               # Shortened URL
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_comments(video_id, max_results=100):
    """
    Retrieves comments for a given YouTube video ID.
    
    Args:
        video_id (str): The ID of the YouTube video.
        max_results (int): Maximum number of comments to fetch (per request).
    
    Returns:
        list: A list of comment dictionaries.
    """
    comments = []
    try:
        # Fetch comment threads
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results
        )
        response = request.execute()
        
        # Loop through pages of results
        while response:
            for item in response.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "author": comment["authorDisplayName"],
                    "text": comment["textDisplay"],
                    "like_count": comment["likeCount"],
                    "published_at": comment["publishedAt"]
                })
            
            # Check for more pages
            if "nextPageToken" in response:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=max_results,
                    pageToken=response["nextPageToken"]
                )
                response = request.execute()
            else:
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return comments

def comments_to_dataframe(comments):
    """
    Converts a list of comment dictionaries to a pandas DataFrame.
    
    Args:
        comments (list): A list of comment dictionaries.
    
    Returns:
        pd.DataFrame: A DataFrame containing the comments.
    """
    return pd.DataFrame(comments)

# Function that carries out roberta based sentiment analysis
def polarity_scores_roberta_label(review):
    encoded_text = tokenizer(review, return_tensors='pt')
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    # Reflects the sentiments of each of the three values that expressed it
    scores_dict = {
        scores[0] : 'negative',
        scores[1] : 'neutral',
        scores[2] : 'positive'
    }

    # Labelling logic
    final_score = max(scores[0], scores[1], scores[2])
    labelled_score = {
        'label' : scores_dict[final_score],
        'score': final_score
    }
    return labelled_score

# Parsing the link
video_url = "https://www.youtube.com/watch?v=bQffnhDxvgE" 
video_id = get_video_id_from_url(video_url)

if video_id:
    print(f"Extracted Video ID: {video_id}")
    comments = get_video_comments(video_id, max_results=50)  # Fetch first 50 comments
    print(f"Retrieved {len(comments)} comments.")
    
    # Store comments in a DataFrame
    comments_df = comments_to_dataframe(comments)
    print(comments_df.head())  # Display the first 5 rows of the DataFrame
    
    # Optionally, save to a CSV file
    comments_df.to_csv("youtube_comments.csv", index=False)
    print("Comments saved to youtube_comments.csv")
else:
    print("Could not extract video ID from the provided URL.")


# Sentiment Analysis part

# Specifying models and tokenizer
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)


# Capturing the results into a dictionary
res = {}
for i, row in tqdm(comments_df.iterrows(), total=len(comments_df)):
    try:
        text = row['text']
        author = row['author']
        res[author] = polarity_scores_roberta_label(text)
    except RuntimeError:
        print(f'Broke for id {myid}')

# Merging the columns of the data frame
results_df = pd.DataFrame(res).T
results_df = results_df.reset_index().rename(columns={'index':'author'})
results_df = results_df.merge(comments_df, how='left')

print(results_df.head())