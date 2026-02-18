"""制御層 (app.py) のテスト。"""

from timer.app import handle_key
from timer.state import TimerState


def test_s_key_starts_timer() -> None:
    """s キーで status が running になるか確認する。"""
    state = TimerState()
    result = handle_key("s", state)
    assert state.status == "running"
    assert result is True


def test_p_key_pauses_running_timer() -> None:
    """running 中に p キーで paused になるか確認する。"""
    state = TimerState()
    state.status = "running"
    handle_key("p", state)
    assert state.status == "paused"


def test_p_key_resumes_paused_timer() -> None:
    """paused 中に p キーで running に戻るか確認する。"""
    state = TimerState()
    state.status = "paused"
    handle_key("p", state)
    assert state.status == "running"


def test_q_key_returns_false() -> None:
    """q キーでメインループ終了の False が返るか確認する。"""
    state = TimerState()
    result = handle_key("q", state)
    assert result is False
