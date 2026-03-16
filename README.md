# Vertex AI Pipeline Demo with Terraform

This project demonstrates a simple **MLOps workflow using Terraform and Google Vertex AI Pipelines**.

It shows how to provision infrastructure using **Terraform** and execute a **Vertex AI pipeline** using the **Vertex AI Python SDK**.

---

# Architecture

```
Terraform → Create GCS bucket → Upload pipeline spec → Run Vertex AI Pipeline
```

Components used:

- **Terraform** – Infrastructure provisioning  
- **Google Cloud Storage** – Stores pipeline artifacts  
- **Vertex AI Pipelines** – Executes ML workflow  
- **Kubeflow Pipelines (KFP)** – Defines pipeline  
- **Vertex AI SDK** – Submits pipeline job  

---

# Project Structure

```
vertex-ai-terraform-demo
│
├── pipeline/pipeline.py        # Vertex AI pipeline definition
├── terraform/main.tf          # Terraform infrastructure
├── terraform/variables.tf     # Terraform variables
├── terraform/terraform.tfvars # Project configuration
├── scripts/run_pipeline.py    # Script to run pipeline
├── pipeline.json              # Compiled pipeline
├── requirements.txt
└── README.md
```

---

# Prerequisites

Install the following:

- **Google Cloud CLI**
- **Terraform**
- **Python 3.10+**

Install Python dependencies:

```
pip install -r requirements.txt
```

---

# Setup

### Authenticate with Google Cloud

```
gcloud auth login
gcloud auth application-default login
```

### Set your project

```
gcloud config set project YOUR_PROJECT_ID
```

---

# Configure Terraform

Edit:

```
terraform/terraform.tfvars
```

Example:

```
project_id = "your-project-id"
region     = "us-central1"
```

---

# Enable APIs

```
gcloud services enable \
aiplatform.googleapis.com \
storage.googleapis.com
```

---

# Compile Pipeline

```
python -m kfp.v2.compiler \
--pipeline_file pipeline/pipeline.py \
--output_file pipeline.json
```

---

# Deploy Infrastructure

```
cd terraform
terraform init
terraform apply
```

This will create the **GCS bucket required for pipeline artifacts**.

---

# Run Pipeline

```
python scripts/run_pipeline.py
```

---

# View Pipeline

Open:

**Vertex AI → Pipelines → Runs**

You will see the pipeline execution running in your project.

---

# Running in Another GCP Account

Only update:

```
terraform/terraform.tfvars
```

```
project_id = "your-project-id"
region     = "us-central1"
```

---

# Notes

- No credentials are stored in this repository.
- Terraform state and local files are ignored via `.gitignore`.