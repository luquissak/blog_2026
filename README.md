# blog_2026
Filosofia e IA

# getting started

1. Requirements: Python, VSCode
2. Clone repo

```bash
git clone git@github.com:luquissak/blog_2026.git
```

3. Create env
```bash
py -m venv .venv
.venv\scripts\activate
.venv\scripts\python -m pip install --upgrade pip
.venv\scripts\activate && .venv\Scripts\pip install -r requirements.txt
```

4. Enable GCP Services

```bash
gcloud services enable drive.googleapis.com --project=llm-studies
```

# build and text

1. Load env var
```bash
# More robust way to load .env in PowerShell
Get-Content .env | Where-Object { $_ -match '=' -and $_ -notmatch '^#' } | ForEach-Object {
    $name, $value = $_ -split '=', 2
    $name = $name.Trim()
    $value = $value.Trim().Trim('"').Trim("'")
    [System.Environment]::SetEnvironmentVariable($name, $value, "Process")
    Write-Host "Set $name" -ForegroundColor Cyan
}
```

2. Login

```bash
gcloud config configurations create pessoal
gcloud config set account lquissakng@gmail.com
gcloud config set project llm-studies
#gcloud config configurations activate default (ou o nome que estiver lá)

gcloud auth login lquissakng@gmail.com --no-launch-browser
gcloud config set project $Env:GCP_PROJECT_ID
gcloud components update
gcloud auth application-default login lquissakng@gmail.com
gcloud auth application-default set-quota-project $Env:GCP_PROJECT_ID
gcloud config list

gcloud ai models list --region=us-east1 --project=llm-studies
```

3. GCP scripts
```bash
.venv\scripts\activate 
.venv\Scripts\python src\gcp\create_post_table.py
.venv\Scripts\python src\gcp\insert_posts_into_bq.py
.venv\Scripts\python src\gcp\create_model_baseline.py
.venv\Scripts\python src\gcp\create_authors_table.py
.venv\Scripts\python -m src.gcp.extract_authors_into_bq
```

4. GCP Data Agent
```bash
.venv\scripts\activate 
jupyter notebook notebooks/blog_gemini_data_analytics.ipynb
```

5. RAG NotebookLM
```bash
.venv\scripts\activate 
.venv\Scripts\python src\send_posts_to_word.py
.venv\Scripts\python src\send_words_to_drive.py
```

5. Análises
```bash
.venv\scripts\activate 
.venv\Scripts\python src\nuvens_filosoficas.py
```

# deploy
```bash
```


# references

- [posts_mar_2026](https://console.cloud.google.com/bigquery?ws=!1m5!1m4!4m3!1sllm-studies!2sblog!3sposts_mar_2026)
- [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
- [Vertex AI / Studio](https://console.cloud.google.com/vertex-ai/studio/multimodal?model=gemini-2.0-flash-001&project=llm-studies)
- []()