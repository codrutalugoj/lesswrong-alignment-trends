# BertTopic using a pretrained model
from bertopic import BERTopic
import json
import os

topic_model = BERTopic.load("MaartenGr/BERTopic_Wikipedia")

with open(os.path.join(os.getcwd(), "lesswrong_data.json")) as f:
    json_data = json.load(f)["posts"]

corpus = []
for post in json_data:
    corpus.append(post["text"])

topics, prob = topic_model.transform(corpus)

for topic in topics:
    print(topic_model.topic_labels_[topic])
    # BERTopic identifies these topics:
    # 1082_robots_robot_robotic_robotics
    # 1212_caffeine_caffeinated_drowsiness_coffee