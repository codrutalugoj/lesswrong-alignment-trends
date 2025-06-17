from fastapi import FastAPI
from datetime import datetime
from bertopic import BERTopic
import os
import sys

# Add the parent directory of `elt` to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from elt.scraper_selenium import get_dynamic_content, extract_text_content
from bs4 import BeautifulSoup

app = FastAPI()
model = BERTopic.load(os.getcwd() + "/../modeling/bert_topic_model.pkl")

@app.get("/")
def root(): 
    return {"Hello": "World"}


@app.post("/predict_topic")
def predict_topic(post_url: str):
    """
    The input is a link to a post that should be categorized into a topic
    """
    # first get the post content
    post = get_dynamic_content(post_url)
    post_soup = BeautifulSoup(post, "html.parser")
    post_wrapper = post_soup.find("div", class_="InlineReactSelectionWrapper-root")
    post_text = extract_text_content(post_wrapper)
    pred_topics, pred_probs = model.transform(post_text)

    return {
        "predicted_topic": model.get_topic(pred_topics[0].item()),
        "probability": pred_probs[0]
    }

@app.post("/topic_distribution_over_time")
def topic_distribution_over_time(date_from: datetime):
    """
    The input should be a valid date in the past.
    This endpoint will return the topic distribution over time starting from the given date up to the current date. 
    """

    assert date_from < datetime.now(), "The date must be in the past."