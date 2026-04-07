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

# build and text

1. Load env var
```bash
get-content .env | foreach {
    $name, $value = $_.split('=')
    set-content env:\$name $value
    echo $name $value
}
```

2. Login

```bash
gcloud auth login lquissakng@gmail.com --no-launch-browser
gcloud config set project $Env:GCP_PROJECT_ID
gcloud components update
gcloud auth application-default login lquissakng@gmail.com --no-launch-browser
gcloud auth application-default set-quota-project $Env:GCP_PROJECT_ID
gcloud config list
```

2. GCP scripts
```bash
.venv\scripts\activate 
.venv\Scripts\python src\gcp\create_post_table.py
.venv\Scripts\python src\gcp\insert_posts_into_bq.py
```

# deploy
```bash
```


# references

- [posts_mar_2026](https://console.cloud.google.com/bigquery?ws=!1m5!1m4!4m3!1sllm-studies!2sblog!3sposts_mar_2026)
- []()
- []()
- []()

