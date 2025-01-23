import re
import pandas as pd
from googleapiclient.discovery import build

API_KEY = "AIzaSyCZyIERF87OzHD_QbrkiYgXs68jjVZN7dQ"

class YouTubeOperations:
    def __init__(self, link):

        self.api_key = API_KEY
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.link = link

    def get_video_id_from_url(self, url):

        patterns = [
            r"youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})",  # Full URL
            r"youtu\.be/([a-zA-Z0-9_-]{11})"               # Shortened URL
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def get_video_title(self):

        try:
            video_id = self.get_video_id_from_url(self.link)
            request = self.youtube.videos().list(
                part="snippet",
                id=video_id
            )
            response = request.execute()
            if "items" in response and len(response["items"]) > 0:
                return response["items"][0]["snippet"]["title"]
            else:
                return "Title not found"
        except Exception as e:
            return f"An error occurred: {e}"

    def get_video_comments(self, max_results=100):
        comments = []
        try:
            video_id = self.get_video_id_from_url(self.link)
            if not video_id:
                raise ValueError("Invalid YouTube video URL.")

            request = self.youtube.commentThreads().list(
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
                    request = self.youtube.commentThreads().list(
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

        comments_df = pd.DataFrame(comments)

        # Limiting number of comments to 1100
        if len(comments_df) > 1100:
            comments_df = comments_df.head(1100)

        return comments_df



