import chromadb

client = chromadb.PersistentClient(path="D:/Agent_AI_Levelup/Agent_AI_Levelup/vector_store")
print("Các collection hiện có:", client.list_collections())