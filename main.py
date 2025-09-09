#!/usr/bin/env python3
"""
RAG Demo - Retrieval Augmented Generation Demo Application

This script demonstrates a simple RAG implementation with modular components.
It allows users to index documents and then query them using a language model
augmented with retrieved context.

Usage:
    python main.py [--docs PATH] [--interactive]
    
Examples:
    # Run interactive chat without indexing documents
    python main.py
    
    # Index documents and then run interactive chat
    python main.py --docs ./sample_docs
    
    # Index documents from a single file
    python main.py --docs ./knowledge.txt
"""

import argparse
import os
import sys
from pathlib import Path

# Add parent directory to path to import rag_demo modules
# sys.path.insert(0, str(Path(__file__).parent.parent))

from rag_demo.rag_pipeline import run_rag_demo
from rag_demo.logger import logger

def main():
    """Main entry point for the RAG demo application"""
    parser = argparse.ArgumentParser(description="RAG Demo - Retrieval Augmented Generation Demo")
    parser.add_argument(
        "--docs", 
        type=str, 
        help="Path to document file or directory to index"
    )
    parser.add_argument(
        "--interactive", 
        action="store_true", 
        help="Run in interactive mode (default behavior)"
    )
    
    args = parser.parse_args()
    
    logger.info("Starting RAG Demo Application")
    
    # Validate document path if provided
    doc_path = None
    if args.docs:
        doc_path = os.path.abspath(args.docs)
        if not os.path.exists(doc_path):
            logger.error(f"Document path does not exist: {doc_path}")
            print(f"Error: Document path does not exist: {doc_path}")
            sys.exit(1)
        logger.info(f"Using document path: {doc_path}")
    
    # Run the RAG demo
    try:
        run_rag_demo(doc_path)
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)
    
    logger.info("RAG Demo Application finished")

if __name__ == "__main__":
    main()
