import math
import json


def cosine_similarity(
    vector1: list[float],
    vector2: list[float]
) -> float:

    dot_product = sum(
        a * b
        for a, b in zip(vector1, vector2)
    )


    norm1 = math.sqrt(
        sum(
            a * a
            for a in vector1
        )
    )


    norm2 = math.sqrt(
        sum(
            b * b
            for b in vector2
        )
    )


    return dot_product / (norm1 * norm2)


class VectorStore:

    def __init__(self):
        self.documents = []


    def add_document(
        self,
        text: str,
        vector: list[float],
        metadata: dict | None = None
    ):
        self.documents.append(
            {
                "text": text,
                "vector": vector,
                "metadata": metadata or {}
            }
        )


    def search(
        self,
        query_vector: list[float],
        top_k: int = 3,
        threshold: float = 0.0
    ):

        results = []


        for doc in self.documents:

            score = cosine_similarity(
                query_vector,
                doc["vector"]
            )

            if score >= threshold:

                results.append(
                    {
                        "text": doc["text"],
                        "score": score,
                        "metadata": doc.get(
                            "metadata",
                            {}
                        )
                    }
                )


        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )


        return results[:top_k]

    
    def save(self, path: str):

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.documents,
                f,
                ensure_ascii=False,
                indent=2
            )


    @classmethod
    def load(
        cls,
        path: str
    ):

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            documents = json.load(f)


        store = cls()

        store.documents = documents


        return store