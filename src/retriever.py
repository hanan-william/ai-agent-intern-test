from sentence_transformers import SentenceTransformer, util

from src.chunker import chunk_document
from src.document_loader import load_knowledge_base
from src.policy_rules import (
    is_customer_authoritative,
    precedence_score,
)


class KnowledgeRetriever:
    """Semantic retriever for the Aster & Row knowledge base."""

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        documents = load_knowledge_base()

        self.chunks = []

        for document in documents:
            self.chunks.extend(chunk_document(document))

        texts = [
            f"{chunk['heading']}\n{chunk['content']}"
            for chunk in self.chunks
        ]

        self.embeddings = self.model.encode(
            texts,
            convert_to_tensor=True,
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
        customer_policy_only: bool = False,
    ) -> list[dict]:
        """Return the most relevant knowledge-base chunks."""

        query_embedding = self.model.encode(
            query,
            convert_to_tensor=True,
        )

        scores = util.cos_sim(
            query_embedding,
            self.embeddings,
        )[0]

        candidates = []

        for index, score in enumerate(scores):
            chunk = self.chunks[int(index)]

            if (
                customer_policy_only
                and not is_customer_authoritative(chunk)
            ):
                continue

            candidates.append(
                {
                    **chunk,
                    "score": float(score),
                    "precedence_score": precedence_score(chunk),
                }
            )

        candidates.sort(
            key=lambda result: (
                result["precedence_score"],
                result["score"],
            ),
            reverse=True,
        )

        return candidates[:top_k]