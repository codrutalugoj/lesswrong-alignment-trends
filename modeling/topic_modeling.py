# BertTopic using pretrained models
from bertopic import BERTopic
import json

topic_model = BERTopic.load("MaartenGr/BERTopic_Wikipedia")

json_data = json.load("./../lesswrong_data.json")
print(json_data)
corpus = []

# topic, prob = topic_model.transform("")
# topic_model.topic_labels_[topic]