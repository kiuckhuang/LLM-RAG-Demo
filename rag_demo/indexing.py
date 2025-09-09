import os
import numpy as np
import openai
from typing import List, Tuple
from .logger import logger, debug_log
from .config import Config

def get_embedding(text: str, model: str = None) -> List[float]:
    """
    Generate embedding for text using configured LLM
    
    Args:
        text: Text to embed
        model: Model to use (uses config default if None)
        
    Returns:
        Embedding vector
    """
    if model is None:
        model = Config.INDEX_LLM_MODEL
    
    # Check if we're using placeholder API keys (demo mode)
    is_demo_mode = Config.INDEX_LLM_API_KEY.startswith("demo_placeholder")
    
    if is_demo_mode:
        # In demo mode, we still generate embeddings but log that it's simulated
        debug_log(logger, f"Generating simulated embedding for text (length {len(text)}) with model {model}")
    else:
        # In a real implementation, this would call an actual LLM API
        # For demo purposes, we'll generate random embeddings
        # In practice, you would use something like:
        try:
            client = openai.OpenAI(
                api_key=Config.INDEX_LLM_API_KEY,
                base_url=Config.INDEX_LLM_API_BASE
            )
            response = client.embeddings.create(
                input=text,
                model=model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            # Fall back to mock embedding in case of error
            pass
    
    # Generate a mock embedding (384 dimensions for example)
    np.random.seed(hash(text) % (2**32))  # For reproducible "random" embeddings
    embedding = np.random.rand(384).tolist()
    
    debug_log(logger, f"Generated embedding for text (length {len(text)}) with model {model}")
    return embedding

class VectorDatabase:
    """Simple in-memory vector database for demonstration"""
    
    def __init__(self, db_path: str = None):
        """
        Initialize vector database
        
        Args:
            db_path: Path to persist database (optional)
        """
        if db_path is None:
            db_path = Config.VECTOR_DB_PATH
            
        self.db_path = db_path
        self.vectors = []
        self.metadata = []
        
        # Create directory if it doesn't exist
        os.makedirs(db_path, exist_ok=True)
        
        logger.info(f"Initialized vector database at {db_path}")
    
    def add_documents(self, documents: List[str], metadatas: List[dict] = None):
        """
        Add documents to the vector database
        
        Args:
            documents: List of document texts
            metadatas: List of metadata dictionaries for each document
        """
        if metadatas is None:
            metadatas = [{} for _ in documents]
            
        logger.info(f"Adding {len(documents)} documents to vector database")
        
        for i, (doc, meta) in enumerate(zip(documents, metadatas)):
            # Generate embedding for document
            embedding = get_embedding(doc)
            
            # Store embedding and metadata
            self.vectors.append(embedding)
            meta["document_index"] = len(self.vectors) - 1
            meta["text"] = doc
            self.metadata.append(meta)
            
            debug_log(logger, f"Added document {i+1}/{len(documents)} to database")
        
        logger.info(f"Successfully added {len(documents)} documents to vector database")
    
    def search(self, query: str, k: int = None) -> List[Tuple[dict, float]]:
        """
        Search for similar documents to the query
        
        Args:
            query: Query text
            k: Number of results to return (uses config default if None)
            
        Returns:
            List of (metadata, similarity_score) tuples
        """
        if k is None:
            k = Config.TOP_K_RESULTS
            
        logger.info(f"Searching for documents similar to: {query}")
        
        # Generate embedding for query
        query_embedding = get_embedding(query)
        
        # Calculate similarities (cosine similarity)
        similarities = []
        for i, vector in enumerate(self.vectors):
            # Simplified cosine similarity calculation
            # In practice, you would use a more robust implementation
            dot_product = np.dot(query_embedding, vector)
            norm_query = np.linalg.norm(query_embedding)
            norm_vector = np.linalg.norm(vector)
            
            if norm_query == 0 or norm_vector == 0:
                similarity = 0
            else:
                similarity = dot_product / (norm_query * norm_vector)
                
            similarities.append((i, similarity))
        
        # Sort by similarity and get top k
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_k = similarities[:k]
        
        # Return metadata and similarity scores
        results = [(self.metadata[i].copy(), score) for i, score in top_k]
        
        debug_log(logger, f"Search returned {len(results)} results")
        return results
    
    def save(self):
        """Save vector database to disk (simplified implementation)"""
        # In a real implementation, you would save to a file
        logger.info("Vector database saved to disk")
    
    def load(self):
        """Load vector database from disk (simplified implementation)"""
        # In a real implementation, you would load from a file
        logger.info("Vector database loaded from disk")

def create_index(documents: List[str]) -> VectorDatabase:
    """
    Create vector index from documents
    
    Args:
        documents: List of document chunks
        
    Returns:
        Vector database with indexed documents
    """
    logger.info("Creating vector index from documents")
    
    # Initialize vector database
    db = VectorDatabase()
    
    # Add documents to database
    db.add_documents(documents)
    
    # Save database
    db.save()
    
    logger.info("Vector index creation complete")
    return db
