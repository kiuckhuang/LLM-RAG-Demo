import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    """Configuration class for RAG demo"""
    
    # Logging configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    ENABLE_LOGGING = os.getenv("ENABLE_LOGGING", "True").lower() == "true"
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "false"
    
    # LLM configuration for indexing
    INDEX_LLM_PROVIDER = os.getenv("INDEX_LLM_PROVIDER", "openai")
    INDEX_LLM_MODEL = os.getenv("INDEX_LLM_MODEL", "text-embedding-ada-002")
    INDEX_LLM_API_KEY = os.getenv("INDEX_LLM_API_KEY", "")
    INDEX_LLM_API_BASE = os.getenv("INDEX_LLM_API_BASE", "https://api.openai.com/v1")
    
    # LLM configuration for chat
    CHAT_LLM_PROVIDER = os.getenv("CHAT_LLM_PROVIDER", "openai")
    CHAT_LLM_MODEL = os.getenv("CHAT_LLM_MODEL", "gpt-3.5-turbo")
    CHAT_LLM_API_KEY = os.getenv("CHAT_LLM_API_KEY", "")
    CHAT_LLM_API_BASE = os.getenv("CHAT_LLM_API_BASE", "https://api.openai.com/v1")
    
    # Vector database configuration
    VECTOR_DB_TYPE = os.getenv("VECTOR_DB_TYPE", "faiss")  # faiss, chroma, pinecone, etc.
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./vector_db")
    
    # Document processing configuration
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Retrieval configuration
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "3"))
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration values are set"""
        errors = []
        
        # Validate indexing LLM config if using OpenAI
        # Allow demo mode with placeholder keys
        is_demo_index_key = cls.INDEX_LLM_API_KEY.startswith("demo_placeholder")
        if cls.INDEX_LLM_PROVIDER == "openai" and not cls.INDEX_LLM_API_KEY and not is_demo_index_key:
            errors.append("INDEX_LLM_API_KEY is required when using OpenAI for indexing")
            
        # Validate chat LLM config if using OpenAI
        # Allow demo mode with placeholder keys
        is_demo_chat_key = cls.CHAT_LLM_API_KEY.startswith("demo_placeholder")
        if cls.CHAT_LLM_PROVIDER == "openai" and not cls.CHAT_LLM_API_KEY and not is_demo_chat_key:
            errors.append("CHAT_LLM_API_KEY is required when using OpenAI for chat")
            
        return errors
