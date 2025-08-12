# Concept Atlas – Visualizing Ideas in Documents

**Concept Atlas** is an interactive LLM-powered application that lets you upload any set of documents, automatically extract key themes and ideas, and explore how concepts are related through dynamic visualizations.

## ✨ What It Does

1. **Upload & Parse**
   - Supports PDF, TXT, and other common formats
   - Extracts text and basic metadata (title, author, date)

2. **Chunk & Embed**
   - Splits documents into semantically meaningful text chunks
   - Generates vector embeddings for each chunk (OpenAI or local models)

3. **Cluster & Label**
   - Groups related chunks into clusters using unsupervised learning (K-Means, HDBSCAN)
   - Automatically generates human-readable topic labels using c-TF-IDF and/or an LLM

4. **Visualize**
   - Projects embeddings into 2D space (UMAP)
   - Displays clusters on an interactive scatterplot
   - Hover for snippet previews, click for detailed summaries

5. **Explore**
   - View cluster abstracts, top keywords, and representative snippets
   - Lasso-select points for a custom “Summarize Selection” feature
   - Ask natural language questions grounded in your document set

## 🚀 Example Use Cases
- **Research analysis** – Summarize and explore large academic paper collections
- **Competitive intelligence** – Discover common themes in scraped market reports
- **Meeting archives** – Turn months of transcripts into a navigable knowledge map
- **Content audits** – Identify duplication and topic coverage across hundreds of files

## 🛠 Tech Stack

**Frontend**
- Next.js + Tailwind CSS
- Plotly.js for interactive visualization

**Backend**
- FastAPI for API and orchestration
- PostgreSQL + `pgvector` for storage and vector search
- RQ / Celery for background ingestion jobs

**ML / NLP**
- OpenAI `text-embedding-3-large` (MVP) → switchable to local models (`bge-large-en`, etc.)
- `umap-learn` for dimensionality reduction
- `scikit-learn` / `hdbscan` for clustering
- `c-TF-IDF` and LLM for topic labeling

## 🔄 Processing Pipeline

1. **Upload**
   - User uploads one or more documents via web UI
   - Files stored in S3-compatible object storage

2. **Parsing**
   - Text extracted via `pypdf` or `unstructured`
   - Cleaned and normalized

3. **Chunking**
   - Split into overlapping chunks (~800–1,200 tokens)
   - Metadata preserved (source doc, page number)

4. **Embedding**
   - Chunks converted into dense vectors
   - Stored in `pgvector` for fast similarity search

5. **Reduction & Clustering**
   - UMAP reduces embeddings to 2D
   - Clustering algorithm groups related content

6. **Labeling**
   - Extract top terms with c-TF-IDF
   - Optional LLM refinement to produce human-readable titles

7. **Visualization**
   - Client renders scatterplot
   - User can explore clusters, hover for previews, drill down for details

## 🗺 Roadmap

**MVP**
- Document upload & ingestion pipeline
- Embedding, clustering, and labeling
- Interactive cluster scatterplot

**Phase 2**
- Improved topic labeling with LLM refinement
- Lasso select & summarization
- Search + grounded Q&A

**Phase 3**
- Deploy open-source embedding model locally
- Optimize performance with batching, caching, and async serving
- Add evaluation metrics and admin tools for relabeling

**Phase 4**
- Incremental ingestion from cloud drives
- Entity extraction and co-occurrence graph
- Timeline mode to track topic changes over time

## 📦 Running Locally

> **Note:** This is the planned setup; details may evolve as the project matures.

```bash
# Clone repo
git clone https://github.com/your-username/concept-atlas.git
cd concept-atlas

# Start backend
cd api
uvicorn app:app --reload

# Start frontend
cd frontend
npm install
npm run dev
