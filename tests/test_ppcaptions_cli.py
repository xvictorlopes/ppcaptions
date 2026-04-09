import sys
import types

import ppcaptions_cli


def test_main_delegates_to_package_main(monkeypatch):
    captured = {}

    def fake_main(argv):
        captured['argv'] = argv
        return 0

    module = types.ModuleType("ppcaptions")
    module.main = fake_main

    monkeypatch.setitem(sys.modules, "ppcaptions", module)

    ppcaptions_cli.main(["--input", "video.mp4"])

    assert captured['argv'] == ["--input", "video.mp4"]


def test_main_falls_back_when_main_missing(monkeypatch, capsys):
    module = types.ModuleType("ppcaptions")

    monkeypatch.setitem(sys.modules, "ppcaptions", module)

    # Simulate caller-provided argv to ensure sys.argv restoration works.
    original_argv = sys.argv.copy()
    try:
        ppcaptions_cli.main(["--foo"])
    finally:
        # Ensure test leaves sys.argv untouched if the CLI adjusts it.
        sys.argv = original_argv

    captured = capsys.readouterr()
    assert "legacy ppcaptions CLI fallback" in captured.err
    assert captured.out == ""
