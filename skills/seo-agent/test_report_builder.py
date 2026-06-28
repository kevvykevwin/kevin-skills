import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("report_builder.py")


def load_report_builder():
    spec = importlib.util.spec_from_file_location("report_builder", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_build_report_handles_null_presence_details():
    report_builder = load_report_builder()

    report = report_builder.build_report(
        {
            "brand": "Example Brand",
            "technical_scores": {"overall": 80},
            "content_scores": {
                "answer_capsule": 80,
                "structure": 80,
                "entity_clarity": 80,
                "faq_howto": 80,
            },
            "presence_scores": {"overall": 75},
            "citation_scores": {
                "chatgpt": {"citation_rate": 50},
                "google_aio": {"citation_rate": 50},
            },
            "presence_details": {
                "Wikipedia": None,
                "LinkedIn": {"present": True, "notes": "Company page found"},
            },
        }
    )

    assert "- **Wikipedia:** ❌" in report
    assert "- **LinkedIn:** ✅ - Company page found" in report
