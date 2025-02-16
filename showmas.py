from flask import Flask, render_template_string, request
from mastodon import Mastodon
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("mastodon.env")

app = Flask(__name__)

# Move our MastodonFetcher class here but simplify it for web use
class MastodonFetcher:
    def __init__(self, instance_url, access_token):
        self.mastodon = Mastodon(
            access_token=access_token,
            api_base_url=instance_url
        )

    def fetch_original_posts(self, account_id, days_back=90, max_posts=50, hashtag=None):
        if not str(account_id).isdigit():
            account = self.mastodon.account_lookup(account_id)
            account_id = account['id']
        
        start_date = datetime.now(datetime.now().astimezone().tzinfo) - timedelta(days=days_back)
        posts = []
        max_id = None
        
        while len(posts) < max_posts:
            batch = self.mastodon.account_statuses(
                account_id,
                max_id=max_id,
                limit=40,
                exclude_reblogs=True
            )
            
            if not batch:
                break
                
            for post in batch:
                post_date = post['created_at'] if isinstance(post['created_at'], datetime) else datetime.strptime(post['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
                if post_date < start_date:
                    return posts
                    
                if (not post['reblog'] and 
                    post['in_reply_to_id'] is None and 
                    post['visibility'] != 'direct'):
                    
                    # Apply hashtag filter if specified
                    if hashtag:
                        post_tags = [tag['name'].lower() for tag in post['tags']]
                        if hashtag.lower() not in post_tags:
                            continue
                            
                    posts.append(post)
                    
                if len(posts) >= max_posts:
                    return posts
            
            max_id = batch[-1]['id']
        
        return posts

# HTML template
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Mastodon Original Posts Viewer</title>
    <style>
        body {
            font-family: system-ui, -apple-system, sans-serif;
            line-height: 1.5;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .search-form {
            margin: 20px 0;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        input[type="text"] {
            width: 70%;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background: #2b90d9;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background: #2483c5;
        }
        .mastodon-post {
            margin: 20px 0;
            padding: 20px;
            font-size: 16px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .post-header {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        .post-stats {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 15px;
        }
        .post-content {
            margin-bottom: 15px;
            overflow-wrap: break-word;
            word-wrap: break-word;
            word-break: normal;
            hyphens: none;
        }
        .post-content a {
            max-width: 100%;
            display: inline-block;
        }
        .media-attachments img {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            margin-top: 10px;
        }
        .hashtags {
            margin-top: 15px;
            color: #1976d2;
        }
        .post-link {
            margin-top: 15px;
            text-align: right;
        }
        .post-link a {
            color: #666;
            text-decoration: none;
            font-size: 0.9em;
        }
        .post-link a:hover {
            text-decoration: underline;
        }
        .error {
            color: red;
            padding: 20px;
            background: #ffe6e6;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    {% if message %}
    <h1>{{ message }}</h1>
    {% else %}
    <h1>Mastodon Original Posts Viewer</h1>
    Created using Claude 3.5, guided by Florian Marquardt. Shows original posts (no boosts, no replies) of the last 90 days (max 50).
    <div class="search-form">
        <form method="GET" action="/">
            <input type="text" name="account" placeholder="@user@instance.social" value="{{ account }}">
            <input type="text" name="hashtag" placeholder="hashtag (optional)" value="{{ hashtag }}">
            <button type="submit">View Posts</button>
        </form>
    </div>
    {% endif %}

    {% if error %}
    <div class="error">{{ error }}</div>
    {% endif %}
    
    {% if posts %}
    <div class="results">
        {% for post in posts %}
        <div class="mastodon-post">
            <div class="post-header">
                Posted on: {{ post.created_at.strftime('%Y-%m-%d at %H:%M') if post.created_at is not string else post.created_at[:16] }}
            </div>
            <div class="post-stats">
                Favorites: {{ post.favourites_count }} | Reblogs: {{ post.reblogs_count }}
            </div>
            <div class="post-content">
                {{ post.content|safe }}
            </div>
            {% if post.media_attachments %}
            <div class="media-attachments">
                {% for media in post.media_attachments %}
                    {% if media.type == 'image' %}
                        <img src="{{ media.url }}" alt="Media attachment">
                    {% else %}
                        <a href="{{ media.url }}">{{ media.type }} attachment</a>
                    {% endif %}
                {% endfor %}
            </div>
            {% endif %}
            {% if post.tags %}
            <div class="hashtags">
                {% for tag in post.tags %}
                    #{{ tag.name }}
                {% endfor %}
            </div>
            {% endif %}
            <div class="post-link">
                <a href="{{ post.url }}" target="_blank">View original post</a>
            </div>
        </div>
        {% endfor %}
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    account = request.args.get('account', '')
    hashtag = request.args.get('hashtag', '')
    message = request.args.get('message', '')

    if not account:
        return render_template_string(TEMPLATE, account='', hashtag='', posts=None, error=None)
    
    try:
        # You should store these securely in environment variables
        instance_url = os.getenv('MASTODON_INSTANCE_URL')
        access_token = os.getenv('MASTODON_ACCESS_TOKEN')
        
        if not instance_url or not access_token:
            raise ValueError("Missing Mastodon configuration. Please set MASTODON_INSTANCE_URL and MASTODON_ACCESS_TOKEN environment variables.")
        
        try:
            fetcher = MastodonFetcher(instance_url, access_token)
            posts = fetcher.fetch_original_posts(account, hashtag=hashtag)
            return render_template_string(TEMPLATE, account=account, hashtag=hashtag, posts=posts, error=None, message=message)
        except Exception as api_error:
            print(f"Mastodon API error: {str(api_error)}")  # This will go to the error log
            return render_template_string(TEMPLATE, 
                account=account, 
                hashtag=hashtag, 
                posts=None,
                message=message,
                error=f"Mastodon API error: {str(api_error)} (Instance URL: {instance_url})")
            
    except Exception as e:
        return render_template_string(TEMPLATE, account=account, hashtag=hashtag, posts=None, error=str(e))

if __name__ == '__main__':
    app.run(debug=False)
