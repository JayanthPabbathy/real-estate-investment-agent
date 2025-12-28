"""
Stage 2: Retrieval-Augmented Generation (RAG) System
Vector database and document retrieval
"""
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Tuple
import json
from pathlib import Path
from loguru import logger
import numpy as np


class DocumentChunker:
    """Intelligent document chunking strategies"""
    
    @staticmethod
    def chunk_by_paragraph(text: str, max_chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Chunk document by paragraphs with overlap"""
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = []
        current_size = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            para_words = para.split()
            para_size = len(para_words)
            
            if current_size + para_size > max_chunk_size and current_chunk:
                # Save current chunk
                chunks.append(' '.join(current_chunk))
                
                # Start new chunk with overlap
                overlap_words = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
                current_chunk = overlap_words + para_words
                current_size = len(current_chunk)
            else:
                current_chunk.extend(para_words)
                current_size += para_size
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    @staticmethod
    def chunk_by_sentences(text: str, chunk_size: int = 3) -> List[str]:
        """Chunk by sentences"""
        import re
        sentences = re.split(r'[.!?]+', text)
        chunks = []
        
        for i in range(0, len(sentences), chunk_size):
            chunk = '. '.join(sentences[i:i+chunk_size]).strip()
            if chunk:
                chunks.append(chunk)
        
        return chunks


class VectorStore:
    """Vector database for document storage and retrieval"""
    
    def __init__(self, collection_name: str = "real_estate_docs", 
                 persist_directory: str = "./data/vector_db"):
        self.collection_name = collection_name
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize embedding model
        logger.info("Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dim = 384  # Dimension for all-MiniLM-L6-v2
        
        # Initialize ChromaDB
        logger.info("Initializing ChromaDB...")
        self.client = chromadb.PersistentClient(path=str(self.persist_directory))
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            logger.info(f"Loaded existing collection: {self.collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for texts"""
        embeddings = self.embedding_model.encode(texts, show_progress_bar=False)
        return embeddings
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to vector store"""
        logger.info(f"Processing {len(documents)} documents...")
        
        all_chunks = []
        all_metadata = []
        all_ids = []
        
        for doc in documents:
            doc_id = doc['doc_id']
            title = doc['title']
            content = doc['content']
            category = doc.get('category', 'general')
            
            # Chunk document
            chunks = DocumentChunker.chunk_by_paragraph(content, max_chunk_size=400, overlap=50)
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc_id}_chunk_{i}"
                all_chunks.append(chunk)
                all_ids.append(chunk_id)
                all_metadata.append({
                    'doc_id': doc_id,
                    'title': title,
                    'category': category,
                    'chunk_index': i,
                    'city': doc.get('city', 'All'),
                    'date': doc.get('date', '')
                })
        
        # Generate embeddings
        logger.info(f"Generating embeddings for {len(all_chunks)} chunks...")
        embeddings = self.embed_texts(all_chunks)
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=all_chunks,
            metadatas=all_metadata,
            ids=all_ids
        )
        
        logger.info(f"Added {len(all_chunks)} chunks to vector store")
    
    def search(self, query: str, top_k: int = 5, 
               filter_metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Search for relevant documents"""
        # Generate query embedding
        query_embedding = self.embed_texts([query])[0]
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            where=filter_metadata if filter_metadata else None
        )
        
        # Format results
        retrieved_docs = []
        for i in range(len(results['ids'][0])):
            retrieved_docs.append({
                'chunk_id': results['ids'][0][i],
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None,
                'relevance_score': 1 - results['distances'][0][i] if 'distances' in results else None
            })
        
        return retrieved_docs
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        count = self.collection.count()
        return {
            'collection_name': self.collection_name,
            'total_chunks': count,
            'embedding_dimension': self.embedding_dim
        }


class RAGSystem:
    """Complete RAG system for real estate intelligence"""
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
    
    def index_documents(self, market_docs: List[Dict], regulatory_docs: List[Dict]):
        """Index all documents into vector store"""
        logger.info("Indexing documents...")
        
        # Combine all documents
        all_docs = market_docs + regulatory_docs
        
        # Add to vector store
        self.vector_store.add_documents(all_docs)
        
        stats = self.vector_store.get_collection_stats()
        logger.info(f"Indexing complete: {stats}")
        
        return stats
    
    def retrieve_relevant_context(self, query: str, property_data: Dict[str, Any],
                                  top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant context for investment analysis"""
        
        # Extract key information from property data
        city = property_data.get('city', '')
        property_type = property_data.get('property_type', '')
        
        # Construct enhanced query
        enhanced_query = f"""
        Real estate investment analysis for {property_type} in {city}.
        Query: {query}
        Looking for: market trends, regulatory compliance, risk factors, infrastructure developments.
        """
        
        # Search without filter first
        results = self.vector_store.search(enhanced_query, top_k=top_k * 2)
        
        # Optionally filter by city if results are insufficient
        city_results = [r for r in results if r['metadata'].get('city') in [city, 'All', 'Multiple']]
        
        if len(city_results) >= top_k:
            return city_results[:top_k]
        else:
            return results[:top_k]
    
    def retrieve_regulatory_context(self, city: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve regulatory and compliance documents"""
        query = f"RERA compliance, stamp duty, building regulations, legal requirements for {city}"
        
        results = self.vector_store.search(
            query, 
            top_k=top_k,
            filter_metadata={'category': 'rera_compliance'}
        )
        
        return results
    
    def retrieve_market_intelligence(self, city: str, locality: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve market analysis and trends"""
        query = f"Market analysis, price trends, investment outlook for {locality}, {city}"
        
        results = self.vector_store.search(
            query,
            top_k=top_k
        )
        
        return results


def setup_rag_system(data_dir: Path, vector_db_path: Path) -> RAGSystem:
    """Setup complete RAG system"""
    
    # Initialize vector store
    vector_store = VectorStore(
        collection_name="real_estate_docs",
        persist_directory=str(vector_db_path)
    )
    
    # Check if already indexed
    stats = vector_store.get_collection_stats()
    if stats['total_chunks'] > 0:
        logger.info(f"Vector store already contains {stats['total_chunks']} chunks")
        return RAGSystem(vector_store)
    
    # Load documents
    logger.info("Loading documents...")
    with open(data_dir / 'market_documents.json', 'r') as f:
        market_docs = json.load(f)
    
    with open(data_dir / 'regulatory_documents.json', 'r') as f:
        regulatory_docs = json.load(f)
    
    # Create RAG system and index documents
    rag_system = RAGSystem(vector_store)
    rag_system.index_documents(market_docs, regulatory_docs)
    
    return rag_system


if __name__ == "__main__":
    from pathlib import Path
    
    data_dir = Path("./data")
    vector_db_path = Path("./data/vector_db")
    
    # Setup RAG system
    rag_system = setup_rag_system(data_dir, vector_db_path)
    
    # Test retrieval
    test_query = "Investment potential for property in Mumbai Andheri"
    test_property = {'city': 'Mumbai', 'property_type': 'Apartment'}
    
    results = rag_system.retrieve_relevant_context(test_query, test_property, top_k=3)
    
    print("\nRetrieved Documents:")
    for i, doc in enumerate(results, 1):
        print(f"\n{i}. {doc['metadata']['title']}")
        print(f"   Relevance: {doc['relevance_score']:.3f}")
        print(f"   Content: {doc['content'][:200]}...")
