"""
Najika ChromaDB Initialization
Version: 2.5
"""
import chromadb
from chromadb.config import Settings
import os

def initialize_chromadb():
    """Initialize ChromaDB with Najika's memory collection"""
    
    db_path = "backend/ai/chromadb"
    os.makedirs(db_path, exist_ok=True)
    
    client = chromadb.PersistentClient(
        path=db_path,
        settings=Settings(
            anonymized_telemetry=False,
            allow_reset=True
        )
    )
    
    # Create main memory collection
    try:
        collection = client.create_collection(
            name="najika_memory",
            metadata={"description": "Najika's persistent memory"}
        )
        print("✅ ChromaDB collection 'najika_memory' created")
    except:
        collection = client.get_collection("najika_memory")
        print("✅ ChromaDB collection 'najika_memory' already exists")
    
    # Create conversation history collection
    try:
        conv_collection = client.create_collection(
            name="conversation_history",
            metadata={"description": "All conversations with Kuja"}
        )
        print("✅ Collection 'conversation_history' created")
    except:
        print("✅ Collection 'conversation_history' already exists")
    
    # Create game state collection
    try:
        game_collection = client.create_collection(
            name="game_state",
            metadata={"description": "Game progress and decisions"}
        )
        print("✅ Collection 'game_state' created")
    except:
        print("✅ Collection 'game_state' already exists")
    
    print("\n🎉 ChromaDB initialized successfully!")
    return client

if __name__ == "__main__":
    initialize_chromadb()
