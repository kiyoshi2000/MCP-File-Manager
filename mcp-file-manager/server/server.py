import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

ROOT = Path(os.environ.get("SANDBOX_ROOT", "./server/sandbox")).resolve()

def safe(path: str) -> Path:
    p = (ROOT / path).resolve()
    if not str(p).startswith(str(ROOT)):
        raise HTTPException(400, "Path fora do sandbox")
    return p

app = FastAPI(title="mcp-file-manager")

class RenameReq(BaseModel):
    src: str
    dst: str

class MoveReq(BaseModel):
    src: str
    dst_dir: str

class SummarizeReq(BaseModel):
    path: str
    max_chars: int = 2000

class BuildIndexReq(BaseModel):
    out: str = "index.md"

@app.get("/healthz")
def health():
    return {"ok": True}

@app.get("/resources/files/list")
def list_files():
    items = []
    for p in ROOT.rglob("*"):
        rel = str(p.relative_to(ROOT))
        items.append({
            "path": rel,
            "is_dir": p.is_dir(),
            "size": (p.stat().st_size if p.is_file() else 0),
            "mtime": int(p.stat().st_mtime)
        })
    return {"root": str(ROOT), "items": items}

@app.get("/resources/files/preview")
def preview(path: str, max_lines: int = 40, max_bytes: int = 4000):
    p = safe(path)
    if not p.exists() or not p.is_file():
        raise HTTPException(404, "Arquivo não encontrado")
    with open(p, "rb") as f:
        chunk = f.read(max_bytes)
    text = chunk.decode("utf-8", errors="replace")
    lines = "\n".join(text.splitlines()[:max_lines])
    return {"path": path, "text": lines}

@app.post("/tools/rename_file")
def rename_file(req: RenameReq):
    src = safe(req.src)
    dst = safe(req.dst)
    if not src.exists():
        raise HTTPException(404, "src não existe")
    dst.parent.mkdir(parents=True, exist_ok=True)
    src.rename(dst)
    return {"ok": True, "from": req.src, "to": req.dst}

@app.post("/tools/move_file")
def move_file(req: MoveReq):
    src = safe(req.src)
    dst_dir = safe(req.dst_dir)
    if not src.exists():
        raise HTTPException(404, "src não existe")
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    src.rename(dst)
    return {"ok": True, "from": req.src, "to": str(dst.relative_to(ROOT))}

@app.post("/tools/summarize_text")
def summarize_text(req: SummarizeReq):
    p = safe(req.path)
    if not p.exists() or not p.is_file():
        raise HTTPException(404, "Arquivo não encontrado")
    text = p.read_text(errors="replace")[:req.max_chars]
    first_line = text.splitlines()[0] if text else ""
    summary = (first_line[:200] + " ...") if first_line else "(vazio)"
    return {"summary": f"(stub) {summary}"}

@app.post("/tools/build_index")
def build_index(req: BuildIndexReq):
    lines = ["# Índice da pasta\n"]
    for p in sorted(ROOT.rglob("*")):
        rel = str(p.relative_to(ROOT))
        if p.is_file():
            title = None
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    first = f.readline().strip()
                    if first:
                        title = first[:120]
            except Exception:
                pass
            lines.append(f"- `{rel}` — {title or 'arquivo'}")
        els
