# MCP Servers Reference

## Available Servers

### Gemini (`mcp__gemini__*`)
**Use for:** Research, current info, image analysis, domain expertise

| Tool | Purpose |
|------|---------|
| `generate_text` | Text generation with optional grounding |
| `analyze_image` | Vision analysis of images |
| `embed_text` | Generate embeddings |
| `count_tokens` | Token counting |

**Key params:** `grounding: true` for current info, `model: "gemini-2.5-pro"` for complex tasks

**Setup:** `GEMINI_API_KEY` environment variable

---

### Playwright (`mcp__playwright__*`)
**Use for:** Browser automation, web scraping, UI testing

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Go to URL |
| `browser_snapshot` | Get page accessibility tree (preferred over screenshot) |
| `browser_click` | Click elements |
| `browser_type` | Type into inputs |
| `browser_take_screenshot` | Capture page image |

**Workflow:** `navigate` → `snapshot` → `click`/`type` → repeat

---

### Netlify (`mcp__netlify__*`)
**Use for:** Deployments, project management, env vars

| Tool | Purpose |
|------|---------|
| `netlify-deploy-services-updater` | Deploy sites |
| `netlify-project-services-reader` | Get project info |
| `netlify-project-services-updater` | Manage env vars, forms |

**Setup:** Netlify CLI authenticated

## When to Use What

| Need | Use |
|------|-----|
| Current/factual info | Gemini with `grounding: true` |
| Complex analysis | Gemini `gemini-2.5-pro` |
| Quick queries | Gemini `gemini-2.5-flash` |
| Web interaction | Playwright |
| Deploy/hosting | Netlify |
| Code implementation | Claude native tools |
