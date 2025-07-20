import logging
from typing import List, Any
from app.rag.chroma_store import vectorstore

logger = logging.getLogger(__name__)


def get_retriever(k: int = 3, use_scores: bool = False, max_score: float = 1.2):
    if use_scores:
        logger.info("Creating retriever with score filtering: k=%d, max_score=%.2f", k, max_score)
        return ScoreFilteringRetriever(k=k, max_score=max_score)
    else:
        logger.info("Creating standard retriever: k=%d", k)
        return vectorstore.as_retriever(search_kwargs={"k": k})


class ScoreFilteringRetriever:    
    def __init__(self, k: int = 3, max_score: float = 1.2):
        self.k = k
        self.max_score = max_score
        self.vectorstore = vectorstore

    def invoke(self, query: str) -> List[Any]:
        try:
            logger.info("Retrieving documents with score filtering for: '%s'", query)
            
            docs_with_scores = self.vectorstore.similarity_search_with_score(query, k=self.k * 2)
            
            filtered_docs = [doc for doc, score in docs_with_scores if score < self.max_score]
            
            result = filtered_docs[:self.k]
            
            logger.info("Found %d documents after score filtering (requested %d)", len(result), self.k)
            return result
            
        except Exception as e:
            logger.error("Error in score filtering retriever: %s", str(e))
            raise
    
    def get_relevant_documents(self, query: str) -> List[Any]:
        return self.invoke(query)