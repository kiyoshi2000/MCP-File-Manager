# MCP File Manager

Um **mini-servidor MCP** didático que dá a um agente acesso **controlado** a uma pasta *sandbox*:
- `resources` para **listar e pré-visualizar** arquivos;
- `tools` para **renomear**, **mover** e **gerar índice** (`index.md`);
- pronto para ser plugado a um cliente/LLM depois.

> **Sem monitoramento.** **Sem n8n.** Apenas **MCP básico** e seguro.

---

## 🚀 Como rodar (Docker)
```bash
docker compose up --build
# servidor disponível em http://localhost:8765
