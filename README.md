# RAG Demo - Retrieval Augmented Generation Demo

This is a simple demonstration of a Retrieval Augmented Generation (RAG) system implemented in Python. The demo showcases how to build a knowledge chatbot that can answer questions based on indexed documents.

## Features

- **Modular Design**: Each component of the RAG pipeline is implemented as a separate module
- **Configurable**: All settings can be configured via `.env` file with sensible defaults
- **Logging**: Comprehensive logging with configurable levels and debug mode
- **Multiple LLM Support**: Supports different LLMs for indexing and chat generation
- **OpenAI Compatible**: Works with any OpenAI-compatible API endpoints
- **Easy to Understand**: Simple implementation perfect for learning RAG concepts

## Project Structure

```
├── main.py            # Entry point for the demo application
├── requirements.txt   # Python dependencies
├── .env.example       # Example environment configuration
├── rag_demo/
│   ├── config.py          # Configuration management
│   ├── logger.py          # Logging functionality
│   ├── document_preparation.py  # Document loading and chunking
│   ├── indexing.py        # Vector database and embedding generation
│   ├── query_processing.py     # Query preprocessing
│   ├── retrieval.py       # Document retrieval from vector database
│   ├── generation.py      # Response generation with LLM
│   ├── rag_pipeline.py    # Main RAG pipeline orchestration
└── README.md          # This file
```

## Installation

1. Clone or download this repository
2. Navigate to the `rag_demo` directory
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the `rag_demo` directory with your configuration. See `.env.example` for available options:

```bash
# Copy the example file to create your own configuration
cp .env.example .env
```

### Required Configuration

For OpenAI:
- `INDEX_LLM_API_KEY`: Your OpenAI API key for indexing (embedding generation)
- `CHAT_LLM_API_KEY`: Your OpenAI API key for chat generation

For other OpenAI-compatible APIs:
- `INDEX_LLM_API_BASE`: Base URL for indexing API
- `CHAT_LLM_API_BASE`: Base URL for chat API

### Optional Configuration

- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `ENABLE_LOGGING`: Enable/disable logging (True/False)
- `DEBUG_MODE`: Enable/disable debug mode (True/False)
- `CHUNK_SIZE`: Size of document chunks (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `TOP_K_RESULTS`: Number of documents to retrieve (default: 3)

## Usage

### Command Line Interface

```bash
# Run interactive chat without indexing documents
python main.py

# Index documents and then run interactive chat
python main.py --docs ./sample_docs

# Index documents from a single file
python main.py --docs ./knowledge.txt
```

### Interactive Chat

Once running, you can interact with the chatbot by typing questions. Type `quit` to exit.

If you've indexed documents, the chatbot will use RAG to answer your questions based on the indexed content. If no documents are indexed, the chatbot will still respond but without the RAG augmentation.

## How It Works

The RAG pipeline consists of the following steps:

1. **Document Preparation**: Load and split documents into manageable chunks
2. **Indexing**: Convert document chunks into embeddings and store in a vector database
3. **Query Processing**: Preprocess user queries for better matching
4. **Retrieval**: Find the most relevant document chunks using vector similarity search
5. **Generation**: Use an LLM to generate a response based on the query and retrieved context
6. **Post-processing**: Format and clean the final response

## Example Documents

To test the RAG demo, create a `sample_docs` directory with text files containing your knowledge base. For example:

```
sample_docs/
├── company_info.txt
├── product_manual.txt
└── faq.txt
```

## Limitations

This is a simplified demonstration for educational purposes:

- Uses mock embeddings (random vectors) instead of real LLM embeddings
- Implements a basic in-memory vector database
- Simulates LLM responses instead of calling actual APIs
- Limited preprocessing and post-processing

In a production implementation, you would:

- Use real embedding models
- Implement a persistent vector database (e.g., FAISS, Chroma, Pinecone)
- Integrate with actual LLM APIs
- Add more sophisticated text processing
- Implement error handling and retry logic

## Learning Resources

For more information about RAG:
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
- [LangChain Documentation](https://docs.langchain.com/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)

## Contributing

This is a educational demo. Feel free to fork and modify for your own learning purposes.
