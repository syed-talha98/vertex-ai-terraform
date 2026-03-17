# Vertex AI Pipeline Demo with Terraform

This repository shows a simple MLOps flow on Google Cloud:

1. Terraform creates the required Google Cloud Storage bucket.
2. Kubeflow Pipelines compiles the pipeline definition into `pipeline.json`.
3. The Vertex AI Python SDK submits the compiled pipeline to Vertex AI Pipelines.

## Architecture

```text
Terraform -> Create GCS bucket -> Compile pipeline.json -> Submit Vertex AI Pipeline
```

Main services used:

- Terraform
- Google Cloud Storage
- Vertex AI Pipelines
- Kubeflow Pipelines (KFP)
- Vertex AI Python SDK
- GitHub Actions

## Project Structure

```text
vertex-ai-terraform-demo
├── pipeline/pipeline.py        # Vertex AI pipeline definition
├── terraform/main.tf          # Terraform infrastructure
├── terraform/variables.tf     # Terraform variables
├── terraform/terraform.tfvars # Project configuration
├── scripts/run_pipeline.py    # Script to submit the pipeline
├── pipeline.json              # Compiled pipeline spec
├── requirements.txt
└── README.md
```

## Prerequisites

Install the following locally:

- Google Cloud CLI
- Terraform
- Python 3.11+

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## GCP Prerequisites

This project needs a Google Cloud project with billing enabled.

You must decide which identity will run the project:

- Local development identity: your user account from `gcloud auth login`
- CI identity: a Google Cloud service account used by GitHub Actions

If you use GitHub Actions, the workflow in `.github/workflows/pipeline.yml` expects a JSON service account key in the GitHub secret `GCP_SA_KEY`.

## Required APIs

Enable these APIs in the target GCP project:

```bash
gcloud services enable \
  aiplatform.googleapis.com \
  storage.googleapis.com \
  iam.googleapis.com \
  cloudresourcemanager.googleapis.com \
  serviceusage.googleapis.com
```

Why they are needed:

- `aiplatform.googleapis.com`: required to create and run Vertex AI pipeline jobs
- `storage.googleapis.com`: required for the pipeline root bucket and uploaded `pipeline.json`
- `iam.googleapis.com`: required when working with service accounts and keys
- `cloudresourcemanager.googleapis.com`: commonly required by Terraform/provider project operations
- `serviceusage.googleapis.com`: required if you want to enable services by command or automation

## Required Permissions

### Minimum roles for the identity running Terraform and submitting the pipeline

If you use one identity for everything, assign these roles at the project level:

- `roles/aiplatform.user`
- `roles/storage.admin`

You will also need this role if the same identity enables APIs:

- `roles/serviceusage.serviceUsageAdmin`

### If you create and manage the GitHub Actions service account yourself

The user or admin account creating the service account and its key typically also needs:

- `roles/iam.serviceAccountAdmin`
- `roles/iam.serviceAccountKeyAdmin`

### Practical recommendation

For this demo, the simplest setup is:

- Give the GitHub Actions service account `roles/aiplatform.user`
- Give the GitHub Actions service account `roles/storage.admin`
- Give your admin/setup identity `roles/serviceusage.serviceUsageAdmin`
- Give your admin/setup identity IAM permissions only if you are creating the service account and key yourself

## Service Account for GitHub Actions

If you want the GitHub Actions workflow to run successfully, create a dedicated service account.

Example:

```bash
gcloud iam service-accounts create github-vertex-pipeline \
  --display-name="GitHub Vertex Pipeline"
```

Grant the required roles:

```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-vertex-pipeline@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-vertex-pipeline@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"
```

If this same service account must also enable APIs, grant:

```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-vertex-pipeline@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/serviceusage.serviceUsageAdmin"
```

## Create the Service Account Key

The GitHub Actions workflow uses this block:

```yaml
with:
  credentials_json: ${{ secrets.GCP_SA_KEY }}
```

That means `GCP_SA_KEY` must contain the full contents of a service account JSON key.

Create the key:

```bash
gcloud iam service-accounts keys create github-vertex-pipeline-key.json \
  --iam-account=github-vertex-pipeline@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

Then add that file's contents to GitHub:

1. Open your GitHub repository.
2. Go to `Settings -> Secrets and variables -> Actions`.
3. Create a new repository secret named `GCP_SA_KEY`.
4. Paste the entire JSON file contents into the secret.

Important:

- Do not commit the JSON key into this repository
- Do not rename the secret unless you also update the workflow
- If the key is rotated, update the GitHub secret immediately

## Local Authentication

For local runs, authenticate with Google Cloud:

```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

`gcloud auth application-default login` is important for local Python SDK calls.

## Configure Terraform

Edit `terraform/terraform.tfvars`:

```hcl
project_id = "your-project-id"
region     = "us-central1"
```

## Compile the Pipeline

Compile the pipeline definition into `pipeline.json`:

```bash
python -m kfp.v2.compiler \
  --pipeline_file pipeline/pipeline.py \
  --output_file pipeline.json
```

## Deploy Infrastructure

Run Terraform from the `terraform` directory:

```bash
cd terraform
terraform init
terraform apply
```

This creates the bucket used by the project:

- `${project_id}-vertex-demo-bucket`

The Terraform code uploads the compiled `pipeline.json` to that bucket.

## Run the Pipeline Locally

From the repository root:

```bash
export PROJECT_ID="your-project-id"
export REGION="us-central1"
export PIPELINE_ROOT="gs://your-project-id-vertex-demo-bucket/pipeline-root"
python scripts/run_pipeline.py
```

This submits the Vertex AI pipeline job using the compiled `pipeline.json`.

Required environment variables:

- `PROJECT_ID`: target Google Cloud project
- `REGION`: Vertex AI region, for example `us-central1`
- `PIPELINE_ROOT`: GCS path used by Vertex AI, for example `gs://your-project-id-vertex-demo-bucket/pipeline-root`

## Run the Pipeline in GitHub Actions

The workflow runs on pushes to `main` and does the following:

1. Checks out the repository
2. Sets up Python 3.11
3. Installs dependencies
4. Authenticates to GCP using `GCP_SA_KEY`
5. Compiles `pipeline.json`
6. Sets `PROJECT_ID`, `REGION`, and `PIPELINE_ROOT`
7. Submits the Vertex AI pipeline job

Before using GitHub Actions, make sure all of these are true:

- The target GCP project exists and billing is enabled
- Required APIs are enabled
- The GitHub Actions service account exists
- The service account has the required roles
- The `GCP_SA_KEY` GitHub secret contains a valid JSON key

## View the Pipeline Run

Open Vertex AI in Google Cloud Console:

`Vertex AI -> Pipelines -> Runs`

## Destroy Infrastructure

From the Terraform directory:

```bash
terraform destroy
```

Or from the repository root:

```bash
terraform -chdir=terraform destroy
```

## Notes

- No credentials should be stored in this repository
- The GitHub Actions workflow depends on the `GCP_SA_KEY` secret
- This demo currently uses a service account key for CI because that is what the workflow is configured for
