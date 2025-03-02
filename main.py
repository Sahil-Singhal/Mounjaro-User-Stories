import praw
import openai
import time
import streamlit as st

# --- Step 1: Set Up Reddit API (PRAW) ---
reddit = praw.Reddit(
    client_id="wl0S3QNc3l5m6O73PBs_Wg",
    client_secret="p8N1aZfgIQWdLv6RLBkLErJqhNwzow",
    user_agent="mjoscraper/1.0 by Zealousideal_Stay388",
)

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
                    "content": "I want you to create 3 patient stories out of this that highlight the pain points and successes of the posters and/or commenters. \
                                Feel free to quote entire posts or sentences or phrases. For each user story you create add a short takeaway for the marketing and commercial leadership team of Eli Lilly, \
                                so they use that leanirng to improve the patients' experience with Mounjaro and accelerate its adoption. \
                                Format this into a very pretty markdown format with just 3 user stories and no extra fluff. The post and comment should be in one paragraph and the takeaway from it in the next paragraph, for each user story. \
                                Keep it brief for busy executives in mind. Format the quoted posts/comments in quotes. Add the url of the post to the end of the user story.",
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
with st.spinner("Scraping Reddit and summarizing..."):
    # --- Step 3: Scrape Reddit Posts and Comments ---
    scraped_data = []

    subreddit = reddit.subreddit("Mounjaro")
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

    # Summarize the formatted text
    summary = summarize_text(formatted_text)

    # Display the summary
    st.markdown(summary)

# Run the app using the command: `streamlit run main.py`
