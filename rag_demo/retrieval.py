from typing import List, Tuple
from .logger import logger, debug_log
from .config import Config

def retrieve_documents(query: str, vector_db, k: int = None) -> List[Tuple[dict, float]]:
    """
    Retrieve relevant documents for a query from the vector database
    
    Args:
        query: Processed user query
        vector_db: Vector database instance
        k: Number of documents to retrieve (uses config default if None)
        
    Returns:
        List of (document_metadata, similarity_score) tuples
    """
    if k is None:
        k = Config.TOP_K_RESULTS
    
    logger.info(f"Retrieving top {k} documents for query: {query}")
    
    # Search vector database for similar documents
    results = vector_db.search(query, k)
    
    logger.info(f"Retrieved {len(results)} documents")
    
    # Log top results
    for i, (metadata, score) in enumerate(results):
        debug_log(logger, f"Result {i+1}: Score={score:.4f}, Text={metadata.get('text', '')[:100]}...")
    
    return results

def format_retrieved_context(retrieved_docs: List[Tuple[dict, float]]) -> str:
    """
    Format retrieved documents as context for the LLM
    
    Args:
        retrieved_docs: List of (document_metadata, similarity_score) tuples
        
    Returns:
        Formatted context string
    """
    logger.info("Formatting retrieved documents as context")
    
    context_parts = []
    for i, (metadata, score) in enumerate(retrieved_docs):
        text = metadata.get('text', '')
        context_parts.append(f"[Document {i+1} (Relevance: {score:.4f})]: {text}")
    
    context = "\n\n".join(context_parts)
    
    debug_log(logger, f"Formatted context length: {len(context)} characters")
    logger.info("Context formatting complete")
    
    return context
