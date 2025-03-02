import praw
import openai
import time

# --- Step 1: Set Up Reddit API (PRAW) ---
reddit = praw.Reddit(
    client_id="wl0S3QNc3l5m6O73PBs_Wg",
    client_secret="p8N1aZfgIQWdLv6RLBkLErJqhNwzow",
    user_agent="mjoscraper/1.0 by Zealousideal_Stay388",
)

# Define subreddit and number of posts
subreddit_name = "Mounjaro"  # Change this to your target subreddit
num_posts = 10  # Number of posts to scrape

# --- Step 2: Set Up OpenAI API ---
openai.api_key = "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"


def summarize_text(text):
    """Summarizes text using OpenAI's gpt-4o-mini with the updated API."""
    try:
        client = openai.OpenAI(api_key=openai.api_key)  # Use the new client object
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Summarize this Reddit experience in one concise sentence.",
                },
                {"role": "user", "content": text},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error summarizing: {str(e)}"


# --- Step 3: Scrape Reddit Posts and Comments ---
scraped_data = []

subreddit = reddit.subreddit(subreddit_name)
for post in subreddit.top(limit=num_posts):  # Fetch top posts
    post_data = {"title": post.title, "selftext": post.selftext, "comments": []}

    # Scrape comments
    post.comments.replace_more(limit=0)  # Expand comments
    for comment in post.comments.list():
        post_data["comments"].append(comment.body)

    scraped_data.append(post_data)
    time.sleep(1)  # Avoid hitting rate limits

# --- Step 4: Summarize Reddit Experiences ---
print("\n=== Summarized Experiences ===\n")
for idx, data in enumerate(scraped_data):
    full_text = f"{data['title']} {data['selftext']} {' '.join(data['comments'])}"
    summary = summarize_text(full_text)
    print(f"Post {idx + 1}: {summary}\n")
