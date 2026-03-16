from google.cloud import aiplatform

PROJECT_ID = "vertex-ai-pipeline-demo"
REGION = "us-central1"

PIPELINE_ROOT = "gs://vertex-ai-pipeline-demo-vertex-demo-bucket/pipeline-root"

aiplatform.init(project=PROJECT_ID, location=REGION)

job = aiplatform.PipelineJob(
    display_name="vertex-demo-pipeline",
    template_path="../pipeline.json",
    pipeline_root=PIPELINE_ROOT,
)

job.run(sync=False)

print("Pipeline submitted successfully.")