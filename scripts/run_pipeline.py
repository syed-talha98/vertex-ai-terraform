import os
from pathlib import Path

from google.cloud import aiplatform

TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "pipeline.json"


def get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


PROJECT_ID = get_required_env("PROJECT_ID")
REGION = get_required_env("REGION")
PIPELINE_ROOT = get_required_env("PIPELINE_ROOT")

aiplatform.init(project=PROJECT_ID, location=REGION)

job = aiplatform.PipelineJob(
    display_name="vertex-demo-pipeline",
    template_path=str(TEMPLATE_PATH),
    pipeline_root=PIPELINE_ROOT,
)

job.submit()

print("Pipeline submitted successfully.")
