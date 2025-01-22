from flask import render_template, request, redirect, url_for, session
from app.main import bp
from app.forms import VideoSubmitForm
from app.youtube_operations import YouTubeOperations
from analysis import RobertaAnalyzer

@bp.route('/', methods=['GET', 'POST'])
def index():
    form = VideoSubmitForm()
    if form.validate_on_submit():
        session['link'] = form.link.data  # Save link in session
        return redirect(url_for('main.results'))
    return render_template('index.html', form=form)

@bp.route('/results')
def results():
    link = session.get('link', None)
    video = YouTubeOperations(link)
    title = video.get_video_title()
    # Extract comments
    comments = video.get_video_comments()
    # Run analysis
    analysis = RobertaAnalyzer(comments)
    analysis_df = analysis.return_result()
    sentiment_distribution = analysis.sentiment_distribution(analysis_df)
    top_comments = analysis.top_comments(analysis_df)
    pos_dict = top_comments['positive']
    neu_dict = top_comments['neutral']
    neg_dict = top_comments['negative']

    return render_template('results.html', title=title, 
                           positive=round(sentiment_distribution['positive'], 2),
                           negative=round(sentiment_distribution['negative'], 2),
                           neutral=round(sentiment_distribution['neutral'], 2),
                           pos_comment=pos_dict['text'],
                           neu_comment=neu_dict['text'],
                           neg_comment=neg_dict['text'])

