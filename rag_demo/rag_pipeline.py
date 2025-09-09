from .logger import logger
from .config import Config
from .document_preparation import prepare_documents
from .indexing import create_index
from .query_processing import process_query
from .retrieval import retrieve_documents, format_retrieved_context
from .generation import generate_response, post_process_response

class RAGPipeline:
    """Main RAG pipeline that orchestrates all components"""
    
    def __init__(self):
        """Initialize RAG pipeline"""
        logger.info("Initializing RAG pipeline")
        self.vector_db = None
        
        # Validate configuration
        errors = Config.validate_config()
        if errors:
            for error in errors:
                logger.error(error)
            raise ValueError("Configuration validation failed. Please check your .env file.")
    
    def index_documents(self, doc_path: str):
        """
        Index documents from a file or directory
        
        Args:
            doc_path: Path to document file or directory
        """
        logger.info(f"Indexing documents from: {doc_path}")
        
        # Prepare documents
        documents = prepare_documents(doc_path)
        
        # Create index
        self.vector_db = create_index(documents)
        
        logger.info("Document indexing complete")
    
    def query(self, user_query: str) -> str:
        """
        Process user query and generate response
        
        Args:
            user_query: User's natural language query
            
        Returns:
            Generated response
        """
        if self.vector_db is None:
            raise ValueError("No documents indexed. Please call index_documents() first.")
        
        logger.info(f"Processing query: {user_query}")
        
        # Process query
        processed_query = process_query(user_query)
        
        # Retrieve relevant documents
        retrieved_docs = retrieve_documents(processed_query, self.vector_db)
        
        # Format context
        context = format_retrieved_context(retrieved_docs)
        
        # Generate response
        response = generate_response(processed_query, context)
        
        # Post-process response
        final_response = post_process_response(response)
        
        logger.info("Query processing complete")
        return final_response
    
    def interactive_chat(self):
        """Run interactive chat loop"""
        logger.info("Starting interactive chat")
        print("RAG Demo Chatbot")
        print("Type 'quit' to exit\n")
        
        # Check if documents are indexed
        if self.vector_db is None:
            print("Warning: No documents indexed. Responses will not use RAG.")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                response = self.query(user_input)
                print(f"Assistant: {response}\n")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                logger.error(f"Error during chat: {str(e)}")
                print(f"Error: {str(e)}")

def run_rag_demo(doc_path: str = None):
    """
    Run RAG demo with optional document indexing
    
    Args:
        doc_path: Path to document file or directory (optional)
    """
    logger.info("Running RAG demo")
    
    # Initialize pipeline
    pipeline = RAGPipeline()
    
    # Index documents if provided
    if doc_path:
        pipeline.index_documents(doc_path)
    
    # Run interactive chat
    pipeline.interactive_chat()
    
    logger.info("RAG demo complete")
