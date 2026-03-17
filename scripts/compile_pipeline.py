from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from kfp import compiler


REPO_ROOT = Path(__file__).resolve().parents[1]
PIPELINE_FILE = REPO_ROOT / "pipeline" / "pipeline.py"
OUTPUT_FILE = REPO_ROOT / "pipeline.json"


def load_pipeline_function():
    spec = spec_from_file_location("vertex_demo_pipeline", PIPELINE_FILE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load pipeline module from {PIPELINE_FILE}")

    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "pipeline"):
        raise RuntimeError(f"{PIPELINE_FILE} does not define a 'pipeline' function")

    return module.pipeline


def main():
    pipeline_func = load_pipeline_function()
    compiler.Compiler().compile(
        pipeline_func=pipeline_func,
        package_path=str(OUTPUT_FILE),
    )
    print(f"Compiled pipeline spec to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
