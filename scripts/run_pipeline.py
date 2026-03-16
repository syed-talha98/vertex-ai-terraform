from pathlib import Path

from google.cloud import aiplatform

PROJECT_ID = "vertex-ai-pipeline-demo"
REGION = "us-central1"

PIPELINE_ROOT = "gs://vertex-ai-pipeline-demo-vertex-demo-bucket/pipeline-root"
TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "pipeline.json"

aiplatform.init(project=PROJECT_ID, location=REGION)

job = aiplatform.PipelineJob(
    display_name="vertex-demo-pipeline",
    template_path=str(TEMPLATE_PATH),
    pipeline_root=PIPELINE_ROOT,
)

job.submit()

print("Pipeline submitted successfully.")
