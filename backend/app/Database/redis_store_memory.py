from langgraph.store.redis import RedisStore

# Redis connection string (Apne setup ke mutabiq change kar sakte hain)
REDIS_URI = "redis://localhost:6379"

# RedisStore ko context manager ke sath initialize karna
with RedisStore.from_conn_string(REDIS_URI) as store:
    # 1. Setup tables/indices (Phli baar chalane par zaroori hai)
    store.setup()
    
    # Namespace aur Key define karna
    namespace = ("user_memories", "manish_001")
    key = "preference_1"
    
    print("================ 1. PUT OPERATION ================")
    # Data save ya update karna
    data_to_store = {
        "topic": "LangGraph & Redis",
        "description": "Learning how to use RedisStore for long-term memory.",
        "status": "Active"
    }
    store.put(namespace, key, data_to_store)
    print(f"Data successfully stored under key: '{key}'")
    
    
    print("\n================ 2. GET OPERATION ================")
    # Specific key aur namespace se data fetch karna
    retrieved_item = store.get(namespace, key)
    
    if retrieved_item:
        print(f"Key Found: {retrieved_item.key}")
        print(f"Namespace: {retrieved_item.namespace}")
        print(f"Retrieved Value: {retrieved_item.value}")
    else:
        print("Item not found!")
        
        
    print("\n================ 3. SEARCH OPERATION ================")
    # Usi namespace ke andar saare items search/list karna
    search_results = store.search(namespace)
    
    print(f"Total items found in namespace: {len(search_results)}")
    for item in search_results:
        print(f"-> Key: {item.key} | Value: {item.value}")
        
        
    print("\n================ 4. DELETE OPERATION ================")
    # Data ko delete karna
    store.delete(namespace, key)
    print(f"Item with key '{key}' has been deleted.")
    
    # Verify karne ke liye dobara GET karke check karna
    verify_item = store.get(namespace, key)
    if not verify_item:
        print("Verification: Item successfully deleted (Returns None).")