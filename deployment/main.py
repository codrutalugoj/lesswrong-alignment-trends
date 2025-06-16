from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/")
def root(): 
    return {"Hello": "World"}


@app.post("/topic_distribution_over_time")
def predict_topic(date_from: datetime):
    """
    The input should be a valid date in the past.
    This endpoint will return the topic distribution over time starting from the given date up to the current date. 
    """

    assert date_from < datetime.now(), "The date must be in the past."