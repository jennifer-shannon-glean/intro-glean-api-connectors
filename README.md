# Intro to Glean API Connectors

A hands-on lab for learning how to use Glean's **Search** and **Indexing** REST APIs to build custom data connectors.

---

## 📚 What You'll Learn

In this lab you will:

- **Search** Glean using the Client API
- **Index documents** into custom data sources using the Indexing API
- **Check status** of data sources and documents
- **Bulk upload** multiple documents
- Understand how to **build custom connectors** that push content into Glean

---

## 🧩 What You Need

- Access to a **Glean instance**  
  - Default for this lab: `https://support-lab-be.glean.com`
- Two API tokens created in **Admin Console → API Tokens**:
  - **Client API Token** (for search operations / Client API)
  - **Indexing API Token** (for document upload / Indexing API)
- A **custom data source** configured in your Glean instance  
  (often one per team, e.g. `gleangroup1`)

> In many classes, the **Indexing API token** and **custom data source** are pre-created by an admin or instructor and handed out per group. Students only create the **Client API token**.

### Using a Different Glean Instance

The notebook assumes `support-lab`:

```python
GLEAN_INSTANCE = "support-lab"
# → https://support-lab-be.glean.com
```

To use another instance, change:

```python
GLEAN_INSTANCE = "your-company"
# → https://your-company-be.glean.com
```

and re-run the configuration cell.

---

## 🚀 Start Here (Recommended: Google Colab)

For workshops and new users, **Google Colab is the primary path**. Local VS Code/Cursor setup is optional and documented later.

### Open the Notebook in Colab

**Preferred (works if Colab can read from GitHub):**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/askscio/glean-enablement/blob/main/intro-glean-api-connectors/notebooks/01-intro-glean-api-connectors.ipynb)

If this opens successfully, continue with **Setup in Colab** below.

> If you see a 403/OAuth error, use the "Download & Upload" option.

#### Download & Upload (fallback, works for everyone)

1. **Download the project**
   - Go to the main repo: https://github.com/askscio/glean-enablement
   - Click **Code → Download ZIP**
   - Extract the ZIP and open `intro-glean-api-connectors/notebooks/`

2. **Upload to Colab**
   - Go to https://colab.research.google.com
   - Click **File → Upload notebook**
   - Select `01-intro-glean-api-connectors.ipynb`

3. **Upload helper files**
   - In Colab, click the **📁 Files** icon in the left sidebar
   - Upload (from the same `notebooks/` folder):
     - `setup_helper.py`
     - `glean_api_helpers.py`

---

### Setup in Colab

#### 1. Add your API tokens as Colab secrets

1. In Colab, click the **🔑 key** icon in the left sidebar.
2. Click **"+ Add new secret"** and add **two** secrets:

   - **Name:** `GLEAN-CLIENT-API`  
     **Value:** your **Client API token**

   - **Name:** `GLEAN-INDEX-API`  
     **Value:** your **Indexing API token** (or the one your instructor provided)

3. Make sure **"Notebook access"** is enabled for both.

#### 2. Run the notebook

1. Click **Runtime → Run all** (or run cells top to bottom).
2. In the output of the setup/key-loading cells, confirm you see:

   - `GLEAN-CLIENT-API: Loaded`
   - `GLEAN-INDEX-API: Loaded`

3. Follow the notebook steps to:

   - Call **Search** via `POST /rest/api/v1/search`
   - Bulk index sample documents via `POST /api/index/v1/bulkindexdocuments`
   - Check datasource and document status via `POST /api/index/v1/debug/...`
   - Verify your documents appear in the **Glean UI** under your custom data source

That is all you need for the lab in Colab.

---

## 💻 Optional: Run Locally (VS Code / Cursor)

Only use this section if you specifically want to run the lab on your machine. For most enablement sessions, **Colab is recommended**.

### Local Prerequisites

- **Python 3.12** (`python3.12 --version`)
- Git
- VS Code or Cursor

### 1. Clone the repository

```bash
git clone https://github.com/askscio/glean-enablement.git
cd glean-enablement/intro-glean-api-connectors
```

### 2. Create a virtual environment & install dependencies

**Option A (recommended)** – virtual env inside the repo:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Option B** – virtual env outside the repo:

```bash
mkdir -p ~/venvs
cd ~/venvs
python3.12 -m venv intro-glean-api-connectors
source intro-glean-api-connectors/bin/activate
cd ~/glean-enablement/intro-glean-api-connectors   # adjust path as needed
pip install -r requirements.txt
```

### 3. Configure API keys in `.env`

```bash
cp env_example.txt .env
```

Edit `.env` and set your tokens:

```env
GLEAN_CLIENT_API=your_client_api_token_here
GLEAN_INDEX_API=your_indexing_api_token_here
```

### 4. Open in VS Code / Cursor

```bash
# VS Code
code .

# Cursor
cursor .
```

When prompted about Python environments, select the venv you created above; do **not** create a new one via the UI.

### 5. Run the notebook locally

1. Open `notebooks/01-intro-glean-api-connectors.ipynb`.
2. In the top-right, click **Select Kernel** and choose your venv (or system Python 3.12).
3. Run all cells in order.

The notebook behavior (Search, Indexing, Debug) is the same as in Colab.

---

## 📁 Project Structure

```
intro-glean-api-connectors/
├── .vscode/
│   ├── settings.json              # Pre-configured workspace settings
│   └── extensions.json             # Recommended VS Code extensions
├── notebooks/
│   ├── 01-intro-glean-api-connectors.ipynb   # Main hands-on lab
│   ├── glean_api_helpers.py        # API key management helper module
│   └── setup_helper.py             # Dependency installation helper module
├── requirements.txt               # Python dependencies
├── env_example.txt                # Template for .env file
└── README.md                      # This file
```

---

## 📖 Additional Resources

- Glean Developer Docs: https://developers.glean.com/
- Custom Data Sources Guide: https://help.glean.com/en/articles/custom-data-sources
- API Authentication: https://developers.glean.com/docs/authentication

---

## 📝 License

This project is for educational purposes as part of Glean enablement training.
