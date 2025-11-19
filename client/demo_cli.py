import requests, os

BASE = os.environ.get("MCP-FILE-MANAGER", "http://localhost:8765")

def get(path): return requests.get(BASE+path).json()
def post(path, data): return requests.post(BASE+path, json=data).json()

print("== HEALTH ==")
print(get("/healthz"))

print("\n== LIST ==")
listing = get("/resources/files/list")
print(f"{len(listing['items'])} itens na sandbox")

print("\n== PREVIEW notes.md ==")
print(get("/resources/files/preview?path=notes.md")["text"])

print("\n== BUILD INDEX ==")
print(post("/tools/build_index", {"out":"index.md"}))
