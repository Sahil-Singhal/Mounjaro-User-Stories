import praw
import openai
import time
import streamlit as st
import os
from datetime import timedelta  # For caching

# --- Step 1: Set Up Reddit API (PRAW) ---
reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
    user_agent=os.environ.get("REDDIT_USER_AGENT"),
)

prompt = os.environ.get("MJO_PATIENT_STORY_PROMPT")

# --- Step 2: Set Up OpenAI API ---
openai.api_key = os.environ.get("OPENAI_API_KEY")


@st.cache_data(ttl=timedelta(hours=24))
def summarize_text(text, prompt=prompt):
    """Summarizes text using OpenAI's gpt-4o-mini with the updated API."""
    try:
        client = openai.OpenAI(api_key=openai.api_key)  # Use the new client object
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {"role": "user", "content": text},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error summarizing: {str(e)}"


# Streamlit app
st.title("Mounjaro Social Listening & Key Insights")

# subreddit_name = st.text_input("Enter Subreddit Name", "Mounjaro")
# num_posts = st.number_input(
#     "Number of Posts to Scrape", min_value=1, max_value=100, value=10
# )


# if st.button("Generate Summary"):
# Cache the function's output for 24 hours
@st.cache_data(ttl=timedelta(hours=24))
def scrape():
    with st.spinner("Scraping Reddit and summarizing..."):
        # --- Step 3: Scrape Reddit Posts and Comments ---
        scraped_data = []

        subreddit = reddit.subreddit("MounjaroAus")
        for post in subreddit.new(limit=10):  # Fetch top posts
            post_data = {
                "title": post.title,
                "selftext": post.selftext,
                "comments": [],
                "url": post.url,  # Fetch the link to the post
            }

            # Scrape comments
            post.comments.replace_more(limit=0)  # Expand comments
            for comment in post.comments.list():
                post_data["comments"].append(comment.body)

            scraped_data.append(post_data)
            time.sleep(1)  # Avoid hitting rate limits
            # Format scraped data into a single paragraph
            formatted_text = ""
            for data in scraped_data:
                formatted_text += f"Title: {data['title']}\n"
                formatted_text += f"URL: {data['url']}\n"
                formatted_text += f"Selftext: {data['selftext']}\n"
                formatted_text += "Comments:\n"
                for comment in data["comments"]:
                    formatted_text += f"- {comment}\n"
                formatted_text += "\n"

        return formatted_text


# Summarize the formatted text
summary = summarize_text(scrape(), prompt=prompt)

# Display the summary
st.markdown(summary)

# Run the app using the command: `streamlit run main.py`
