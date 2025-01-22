from tqdm import tqdm
import pandas as pd

# Running transformer models
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

class RobertaAnalyzer:
    def __init__(self, comments):
        # Specifying models and tokenizer
        MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        self.comments_df = comments

    # Function that carries out roberta based sentiment analysis
    def polarity_scores_roberta_label(self, review):
        encoded_text = self.tokenizer(review, return_tensors='pt')
        output = self.model(**encoded_text)
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


    def return_result(self):
        # Capturing the results into a dictionary
        res = {}
        for i, row in tqdm(self.comments_df.iterrows(), total=len(self.comments_df)):
            try:
                text = row['text']
                author = row['author']
                res[author] = self.polarity_scores_roberta_label(text)
            except RuntimeError:
                print(f'Broke for author {author}')

        # Merging the columns of the data frame
        results_df = pd.DataFrame(res).T
        results_df = results_df.reset_index().rename(columns={'index':'author'})
        results_df = results_df.merge(self.comments_df, how='left')

        return results_df

    def sentiment_distribution(self, results_df):

        total_comments = len(results_df)
        if total_comments == 0:
            return {"positive": 0, "neutral": 0, "negative": 0}
        
        distribution = results_df['label'].value_counts(normalize=True) * 100
        return distribution.to_dict()

    def top_comments(self, results_df):

        most_liked = {}
        sentiments = ['positive', 'neutral', 'negative']
        
        for sentiment in sentiments:
            filtered_df = results_df[results_df['label'] == sentiment]
            if not filtered_df.empty:
                # Find the comment with the highest number of likes
                top_comment = filtered_df.loc[filtered_df['like_count'].idxmax()]
                most_liked[sentiment] = {
                    "text": top_comment['text'],
                    "likes": top_comment['like_count']
                }
            else:
                most_liked[sentiment] = {"text": None, "likes": 0}

        return most_liked




