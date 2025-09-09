from typing import List, Union
import os
from .logger import logger, debug_log
from .config import Config

def load_documents(doc_path: str) -> List[str]:
    """
    Load documents from a file or directory
    
    Args:
        doc_path: Path to a file or directory containing documents
        
    Returns:
        List of document texts
    """
    documents = []
    
    if os.path.isfile(doc_path):
        # Load single file
        debug_log(logger, f"Loading document from file: {doc_path}")
        with open(doc_path, 'r', encoding='utf-8') as f:
            documents.append(f.read())
    elif os.path.isdir(doc_path):
        # Load all text files from directory
        debug_log(logger, f"Loading documents from directory: {doc_path}")
        for filename in os.listdir(doc_path):
            file_path = os.path.join(doc_path, filename)
            if os.path.isfile(file_path) and filename.endswith('.txt'):
                debug_log(logger, f"Loading document: {filename}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    documents.append(f.read())
    else:
        raise FileNotFoundError(f"Document path not found: {doc_path}")
    
    logger.info(f"Loaded {len(documents)} documents")
    return documents

def split_text_into_chunks(text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
    """
    Split text into chunks of specified size with overlap
    
    Args:
        text: Text to split
        chunk_size: Size of each chunk (uses config default if None)
        overlap: Overlap between chunks (uses config default if None)
        
    Returns:
        List of text chunks
    """
    if chunk_size is None:
        chunk_size = Config.CHUNK_SIZE
    if overlap is None:
        overlap = Config.CHUNK_OVERLAP
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        
        # Move start position for next chunk
        start = end - overlap
        if start >= len(text):
            break
            
        # If we're at the end of the text, stop
        if end == len(text):
            break
    
    debug_log(logger, f"Split text into {len(chunks)} chunks")
    return chunks

def prepare_documents(doc_path: str) -> List[str]:
    """
    Prepare documents for indexing by loading and splitting into chunks
    
    Args:
        doc_path: Path to document file or directory
        
    Returns:
        List of document chunks
    """
    logger.info("Starting document preparation")
    
    # Load documents
    documents = load_documents(doc_path)
    
    # Split documents into chunks
    all_chunks = []
    for i, doc in enumerate(documents):
        debug_log(logger, f"Processing document {i+1}/{len(documents)}")
        chunks = split_text_into_chunks(doc)
        all_chunks.extend(chunks)
    
    logger.info(f"Document preparation complete. Created {len(all_chunks)} chunks")
    return all_chunks
