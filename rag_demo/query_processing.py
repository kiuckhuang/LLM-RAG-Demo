import re
from .logger import logger, debug_log

def preprocess_query(query: str) -> str:
    """
    Preprocess user query by cleaning and normalizing text
    
    Args:
        query: Raw user query
        
    Returns:
        Preprocessed query
    """
    logger.info("Preprocessing user query")
    debug_log(logger, f"Original query: {query}")
    
    # Convert to lowercase
    processed_query = query.lower()
    
    # Remove extra whitespace
    processed_query = re.sub(r'\s+', ' ', processed_query).strip()
    
    # Remove special characters (keep alphanumeric, spaces, and basic punctuation)
    processed_query = re.sub(r'[^\w\s\.\,\?\!\-\']', '', processed_query)
    
    debug_log(logger, f"Preprocessed query: {processed_query}")
    logger.info("Query preprocessing complete")
    
    return processed_query

def process_query(query: str) -> str:
    """
    Process user query for RAG pipeline
    
    Args:
        query: User query
        
    Returns:
        Processed query ready for retrieval
    """
    logger.info("Processing query for RAG pipeline")
    
    # Preprocess the query
    processed_query = preprocess_query(query)
    
    logger.info("Query processing complete")
    return processed_query
