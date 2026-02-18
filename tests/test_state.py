"""データ層 (state.py) のテスト。"""

from timer.state import BREAK_SEC, FOCUS_SEC, TimerState, tick


def test_initial_state() -> None:
    """初期状態が正しいか確認する。"""
    state = TimerState()
    assert state.phase == "focus"
    assert state.remaining_sec == FOCUS_SEC  # 1500秒（25分）
    assert state.status == "stopped"


def test_tick_decrements_remaining_sec() -> None:
    """tick() で残り秒数が1減るか確認する。"""
    state = TimerState()
    tick(state)
    assert state.remaining_sec == FOCUS_SEC - 1


def test_tick_switches_focus_to_break() -> None:
    """残り0秒で focus → break に切り替わるか確認する。"""
    state = TimerState()
    state.remaining_sec = 1  # あと1秒で切り替わる状態にする

    tick(state)

    assert state.phase == "break"
    assert state.remaining_sec == BREAK_SEC  # 300秒（5分）


def test_tick_switches_break_to_focus() -> None:
    """break 終了後に focus に戻るか確認する。"""
    state = TimerState()
    state.phase = "break"
    state.remaining_sec = 1

    tick(state)

    assert state.phase == "focus"
    assert state.remaining_sec == FOCUS_SEC
