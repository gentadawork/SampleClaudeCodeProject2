"""UI層 (display.py) のテスト。"""

import io
import sys

from timer.display import render
from timer.state import TimerState


def _capture_render(state: TimerState) -> str:
    """render() の出力文字列を取得するヘルパー。"""
    buf = io.StringIO()
    sys.stdout = buf
    try:
        render(state)
    finally:
        sys.stdout = sys.__stdout__
    return buf.getvalue()


def test_render_shows_correct_block_count() -> None:
    """残り24分35秒のとき 🟩 が24個表示されるか確認する。"""
    state = TimerState()
    state.remaining_sec = 24 * 60 + 35  # 24分35秒

    output = _capture_render(state)

    assert output.count("🟩") == 24


def test_render_shows_focus_label() -> None:
    """フェーズが focus のとき [集中] と表示されるか確認する。"""
    state = TimerState()
    state.phase = "focus"

    output = _capture_render(state)

    assert "[集中]" in output


def test_render_shows_break_label() -> None:
    """フェーズが break のとき [休憩] と表示されるか確認する。"""
    state = TimerState()
    state.phase = "break"
    state.remaining_sec = 5 * 60

    output = _capture_render(state)

    assert "[休憩]" in output
