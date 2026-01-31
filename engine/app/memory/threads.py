from typing import List
import re
from app.memory.store import ConversationStore


class ThreadInferencer:
    def __init__(self, update_interval: int = 3, max_threads: int = 5):
        self.update_interval = update_interval
        self.max_threads = max_threads
        self.stopwords = {
            "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
            "your", "yours", "yourself", "yourselves", "he", "him", "his",
            "himself", "she", "her", "hers", "herself", 
            "it", "its", "itself",
            "they", "them", "their", "theirs", "themselves", "what", "which",
            "who", "whom", "this", "that", "these", "those", "am", "is", "are",
            "was", "were", "be", "been", "being", "have", "has", "had", "having",
            "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if",
            "or", "because", "as", "until", "while", "of", "at", "by", "for",
            "with", "about", "against", "between", "into", "through", "during",
            "before", "after", "above", "below", "to", "from", "up", "down",
            "in", "out", "on", "off", "over", "under", "again", "further",
            "then", "once", "here", "there", "when", "where", "why", "how",
            "all", "each", "few", "more", "most", "other", "some", "such", "no",
            "nor", "not", "only", "own", "same", "so", "than", "too", "very",
            "s", "t", "can", "will", "just", "don", "should", "now", "d", "ll",
            "m", "o", "re", "ve", "y", "ain", "aren", "couldn", "didn", "doesn",
            "hadn", "hasn", "haven", "isn", "ma", "mightn", "mustn", "needn",
            "shan", "shouldn", "wasn", "weren", "won", "wouldn", "yeah", "yes",
            "no", "ok", "okay", "um", "uh", "like", "know", "think", "really",
            "just", "well", "got", "get", "going", "want", "need", "would",
            "could", "should", "might", "must", "shall", "may"
        }

    def extract_keywords(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r"[^a-z\s]", "", text)
        words = text.split()
        keywords = []
        for word in words:
            if word not in self.stopwords and len(word) > 2:
                keywords.append(word)
        return keywords

    def should_update(self, store: ConversationStore) -> bool:
        primary_count = store.get_primary_turn_count()
        return primary_count > 0 and primary_count % self.update_interval == 0

    def infer_threads(self, store: ConversationStore) -> List[str]:
        keyword_counts = {}
        for turn in store.turns:
            if turn.role == "primary":
                keywords = self.extract_keywords(turn.text)
                for keyword in keywords:
                    keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1

        sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
        threads = [keyword for keyword, count in sorted_keywords[:self.max_threads] if count >= 1]
        return threads

    def update_if_needed(self, store: ConversationStore) -> None:
        if self.should_update(store):
            threads = self.infer_threads(store)
            store.update_threads(threads)
