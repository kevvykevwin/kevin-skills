import sys

import debate


def test_profile_doc_type_is_used_when_cli_doc_type_omitted(monkeypatch):
    captured = {}

    monkeypatch.setattr(
        sys,
        "argv",
        ["debate.py", "critique", "--profile", "prd-profile", "--models", "gpt-4o"],
    )
    monkeypatch.setattr(debate, "load_profile", lambda name: {"doc_type": "prd"})

    def capture_args(args):
        captured["doc_type"] = args.doc_type

    monkeypatch.setattr(debate, "run_debate", capture_args)

    debate.main()

    assert captured["doc_type"] == "prd"


def test_critique_doc_type_defaults_to_tech_without_profile(monkeypatch):
    captured = {}

    monkeypatch.setattr(
        sys,
        "argv",
        ["debate.py", "critique", "--models", "gpt-4o"],
    )

    def capture_args(args):
        captured["doc_type"] = args.doc_type

    monkeypatch.setattr(debate, "run_debate", capture_args)

    debate.main()

    assert captured["doc_type"] == "tech"
