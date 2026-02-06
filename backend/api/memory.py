"""
Najika Memory API - ChromaDB Integration for UE5
Allows UE5 and Digivice to access Najika's memories

IMPORTANT: This is Najika's PERMANENT memory!
She remembers EVERYTHING - conversations, events, emotions.

Collections:
- najika_conversations: All chats with Kuja
- najika_personalities: Character traits (Megumin, Harley, Shiro, Melissa)
- najika_knowledge: Code, project info, technical knowledge
- najika_core: IMMUTABLE core beliefs
- najika_emotions: Emotional memories
- najika_game_events: In-game events (battles, discoveries, etc.)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path
import chromadb

router = APIRouter(prefix="/api/memory", tags=["Memory"])

# ============================================================================
# CHROMADB CLIENT
# ============================================================================

# Try multiple paths for ChromaDB
CHROMA_PATHS = [
    "C:/Najika_World/chroma_db",
    "C:/Najika_World/memory_db",
    "C:/NajikaFinal/memory_db",
]

_chroma_client = None

def get_chroma_client():
    """Get or create ChromaDB client"""
    global _chroma_client
    if _chroma_client is not None:
        return _chroma_client

    for path in CHROMA_PATHS:
        db_path = Path(path)
        if db_path.exists():
            _chroma_client = chromadb.PersistentClient(path=str(db_path))
            print(f"ChromaDB connected: {path}")
            return _chroma_client

    # Create new if none exists
    db_path = Path(CHROMA_PATHS[0])
    db_path.mkdir(parents=True, exist_ok=True)
    _chroma_client = chromadb.PersistentClient(path=str(db_path))
    print(f"ChromaDB created: {CHROMA_PATHS[0]}")
    return _chroma_client

def get_collection(name: str):
    """Get or create a collection"""
    client = get_chroma_client()
    try:
        return client.get_or_create_collection(name=name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ChromaDB error: {str(e)}")

# ============================================================================
# MODELS
# ============================================================================

class MemoryQuery(BaseModel):
    """Query memories"""
    query: str
    collection: str = "najika_conversations"
    n_results: int = 5
    where: Optional[Dict[str, Any]] = None

class MemoryAdd(BaseModel):
    """Add a memory"""
    collection: str
    text: str
    metadata: Optional[Dict[str, Any]] = None
    id: Optional[str] = None

class ConversationMemory(BaseModel):
    """Store a conversation"""
    user_message: str
    najika_response: str
    emotion: Optional[str] = None
    context: Optional[str] = None
    personality_used: Optional[str] = None  # megumin, harley, shiro, melissa

class GameEventMemory(BaseModel):
    """Store a game event"""
    event_type: str  # battle_won, item_found, quest_complete, building_placed, etc.
    description: str
    location: Optional[str] = None
    participants: Optional[List[str]] = None
    outcome: Optional[str] = None
    importance: int = 1  # 1-5, higher = more important

# ============================================================================
# API ENDPOINTS
# ============================================================================

@router.get("/collections")
async def list_collections():
    """List all memory collections"""
    client = get_chroma_client()
    collections = client.list_collections()
    return {
        "collections": [
            {
                "name": c.name,
                "count": c.count(),
                "metadata": c.metadata
            }
            for c in collections
        ],
        "total": len(collections)
    }

@router.get("/collection/{name}")
async def get_collection_info(name: str):
    """Get info about a specific collection"""
    collection = get_collection(name)
    return {
        "name": collection.name,
        "count": collection.count(),
        "metadata": collection.metadata,
    }

@router.post("/query")
async def query_memories(query: MemoryQuery):
    """
    Query Najika's memories using semantic search.

    Example:
    POST /api/memory/query
    {
        "query": "What did Kuja say about explosions?",
        "collection": "najika_conversations",
        "n_results": 5
    }
    """
    collection = get_collection(query.collection)

    results = collection.query(
        query_texts=[query.query],
        n_results=query.n_results,
        where=query.where
    )

    # Format results
    memories = []
    if results and results['documents']:
        for i, doc in enumerate(results['documents'][0]):
            memory = {
                "text": doc,
                "distance": results['distances'][0][i] if results.get('distances') else None,
                "metadata": results['metadatas'][0][i] if results.get('metadatas') else None,
                "id": results['ids'][0][i] if results.get('ids') else None,
            }
            memories.append(memory)

    return {
        "query": query.query,
        "collection": query.collection,
        "memories": memories,
        "count": len(memories)
    }

@router.post("/add")
async def add_memory(memory: MemoryAdd):
    """
    Add a new memory to a collection.
    """
    collection = get_collection(memory.collection)

    # Generate ID if not provided
    memory_id = memory.id or f"mem_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

    # Add timestamp to metadata
    metadata = memory.metadata or {}
    metadata['timestamp'] = datetime.now().isoformat()

    collection.add(
        documents=[memory.text],
        metadatas=[metadata],
        ids=[memory_id]
    )

    return {
        "success": True,
        "id": memory_id,
        "collection": memory.collection,
        "message": "Memory stored!"
    }

@router.post("/conversation")
async def store_conversation(conv: ConversationMemory):
    """
    Store a conversation exchange with Najika.
    This is called after every chat interaction.
    """
    collection = get_collection("najika_conversations")

    # Create combined text for embedding
    text = f"User: {conv.user_message}\nNajika: {conv.najika_response}"

    memory_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

    metadata = {
        "type": "conversation",
        "user_message": conv.user_message[:500],  # Truncate for metadata
        "emotion": conv.emotion or "neutral",
        "context": conv.context or "general",
        "personality": conv.personality_used or "mixed",
        "timestamp": datetime.now().isoformat(),
    }

    collection.add(
        documents=[text],
        metadatas=[metadata],
        ids=[memory_id]
    )

    return {
        "success": True,
        "id": memory_id,
        "message": "Conversation remembered!"
    }

@router.post("/game-event")
async def store_game_event(event: GameEventMemory):
    """
    Store a game event in Najika's memory.
    Called by UE5/Digivice when something interesting happens.
    """
    collection = get_collection("najika_game_events")

    memory_id = f"event_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

    # Create narrative text
    text = f"[{event.event_type}] {event.description}"
    if event.location:
        text += f" at {event.location}"
    if event.outcome:
        text += f". Result: {event.outcome}"

    metadata = {
        "type": "game_event",
        "event_type": event.event_type,
        "location": event.location,
        "participants": ",".join(event.participants) if event.participants else None,
        "importance": event.importance,
        "timestamp": datetime.now().isoformat(),
    }

    collection.add(
        documents=[text],
        metadatas=[metadata],
        ids=[memory_id]
    )

    return {
        "success": True,
        "id": memory_id,
        "event_type": event.event_type,
        "message": "Event remembered!"
    }

@router.get("/recent/{collection}")
async def get_recent_memories(
    collection: str,
    limit: int = 10,
    event_type: Optional[str] = None
):
    """
    Get most recent memories from a collection.
    Useful for UE5 to recall recent events.
    """
    col = get_collection(collection)

    # ChromaDB doesn't support direct sorting, so we get all and sort
    where_filter = {"event_type": event_type} if event_type else None

    results = col.get(
        limit=limit * 2,  # Get more to filter
        where=where_filter,
        include=["documents", "metadatas"]
    )

    # Sort by timestamp (newest first)
    memories = []
    if results and results['documents']:
        for i, doc in enumerate(results['documents']):
            memories.append({
                "text": doc,
                "metadata": results['metadatas'][i] if results.get('metadatas') else None,
                "id": results['ids'][i] if results.get('ids') else None,
            })

    # Sort by timestamp
    memories.sort(
        key=lambda x: x.get('metadata', {}).get('timestamp', ''),
        reverse=True
    )

    return {
        "collection": collection,
        "memories": memories[:limit],
        "count": min(len(memories), limit)
    }

@router.get("/recall/{topic}")
async def recall_about_topic(topic: str, n_results: int = 5):
    """
    Recall memories related to a specific topic.
    Searches across multiple collections.
    """
    collections_to_search = [
        "najika_conversations",
        "najika_game_events",
        "najika_knowledge",
    ]

    all_memories = []

    for col_name in collections_to_search:
        try:
            col = get_collection(col_name)
            results = col.query(
                query_texts=[topic],
                n_results=n_results
            )

            if results and results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    all_memories.append({
                        "text": doc,
                        "collection": col_name,
                        "distance": results['distances'][0][i] if results.get('distances') else None,
                        "metadata": results['metadatas'][0][i] if results.get('metadatas') else None,
                    })
        except Exception:
            continue

    # Sort by relevance (distance)
    all_memories.sort(key=lambda x: x.get('distance', 999))

    return {
        "topic": topic,
        "memories": all_memories[:n_results],
        "count": min(len(all_memories), n_results)
    }

@router.get("/stats")
async def get_memory_stats():
    """Get statistics about Najika's memory"""
    client = get_chroma_client()
    collections = client.list_collections()

    stats = {
        "total_memories": 0,
        "collections": {}
    }

    for col in collections:
        count = col.count()
        stats["collections"][col.name] = count
        stats["total_memories"] += count

    return stats

@router.delete("/collection/{name}/clear")
async def clear_collection(name: str, confirm: bool = False):
    """
    Clear a collection (DANGEROUS!)
    Requires confirm=true parameter.

    NEVER clear najika_core!
    """
    if name == "najika_core":
        raise HTTPException(
            status_code=403,
            detail="NIEMALS! najika_core is IMMUTABLE! Kuja and Najika are INSEPARABLE!"
        )

    if not confirm:
        raise HTTPException(
            status_code=400,
            detail="Add ?confirm=true to really delete. This cannot be undone!"
        )

    client = get_chroma_client()
    try:
        client.delete_collection(name)
        return {
            "success": True,
            "message": f"Collection '{name}' deleted",
            "warning": "Memories are gone forever..."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
