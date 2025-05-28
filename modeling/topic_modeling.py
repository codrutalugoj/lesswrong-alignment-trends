# BertTopic using a pretrained model
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import json
import os
import nltk
from nltk.tokenize import sent_tokenize

#nltk.download("punkt_tab")
with open(os.path.join(os.getcwd(), "lesswrong_data.json")) as f:
    json_data = json.load(f)["posts"]

preprocessed_corpus = []
for post in json_data:
    # Split into sentences for better context
    sentences = sent_tokenize(post["text"])
    preprocessed_corpus.extend(sentences)

corpus = []
for post in json_data:
    corpus.append(post["text"])

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

topic_model = BERTopic(
    embedding_model=embedding_model,
    min_topic_size=5,  # Adjust based on corpus size
    nr_topics="auto"
)
# embeddings = embedding_model.encode(corpus, show_progress_bar=False)
# print(embeddings.shape)

topics, probs = topic_model.fit_transform(preprocessed_corpus)

topic_model.visualize_topics()

# Get more detailed topic info
topic_info = topic_model.get_topic_info()
for col in topic_info.values():
    print(col)
#print(topic_info.head(1))

# Get representative docs per topic
for topic_id in topic_info.Topic[:5]:
    docs = topic_model.get_representative_docs(topic_id)
    print(f"\nTopic {topic_id}:")
    print(docs[:2])  # First 2 representative documents

# #topics, prob = topic_model.transform(corpus)

# for topic in topics:
#     print(topic_model.topic_labels_[topic])
#     # BERTopic identifies these topics:
#     # 1082_robots_robot_robotic_robotics
#     # 1212_caffeine_caffeinated_drowsiness_coffee