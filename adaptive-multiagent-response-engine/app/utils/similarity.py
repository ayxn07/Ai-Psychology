from typing import List
import re


class SimilarityChecker:
    def __init__(self, threshold: float = 0.6):
        self.threshold = threshold

    def normalize(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def tokenize(self, text: str) -> set:
        normalized = self.normalize(text)
        return set(normalized.split())

    def jaccard_similarity(self, text1: str, text2: str) -> float:
        tokens1 = self.tokenize(text1)
        tokens2 = self.tokenize(text2)

        if not tokens1 or not tokens2:
            return 0.0

        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)

        return len(intersection) / len(union)

    def is_too_similar(self, candidate: str, recent_outputs: List[str]) -> bool:
        for output in recent_outputs:
            similarity = self.jaccard_similarity(candidate, output)
            if similarity >= self.threshold:
                return True
        return False
