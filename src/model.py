from __future__ import annotations


class SentimentModel:

    positive_words = {
        "bien",
        "super",
        "excellent",
        "parfait",
        "bon",
        "aime",
        "adore",
        "genial",
        "génial",
    }

    negative_words = {
        "mal",
        "nul",
        "horrible",
        "mauvais",
        "déteste",
        "deteste",
        "pire",
        "decevant",
        "décevant",
    }

    def __init__(self) -> None:
        print("[SentimentModel] Ready")

    def predict(self, text: str) -> dict:
        text_lower = text.lower()

        positive_hits = sum(1 for word in self.positive_words if word in text_lower)
        negative_hits = sum(1 for word in self.negative_words if word in text_lower)

        if positive_hits > negative_hits:
            label = "POSITIVE"
            score = self._confidence(positive_hits, negative_hits)
        elif negative_hits > positive_hits:
            label = "NEGATIVE"
            score = self._confidence(negative_hits, positive_hits)
        else:
            label = "NEUTRAL"
            score = 0.5

        return {"label": label, "score": score, "text": text}

    @staticmethod
    def _confidence(winner_hits: int, loser_hits: int) -> float:
        raw_score = 0.5 + (winner_hits - loser_hits) * 0.1
        return round(min(max(raw_score, 0.5), 1.0), 2)
