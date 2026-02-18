"""タイマーの表示を担当するUI層。"""

import sys

from timer.state import TimerState

PHASE_LABEL = {
    "focus": "集中",
    "break": "休憩",
}


def render(state: TimerState) -> None:
    """タイマーの現在状態を同じ行に上書き表示する。

    Args:
        state: 表示する TimerState。
    """
    minutes = state.remaining_sec // 60
    seconds = state.remaining_sec % 60
    time_str = f"{minutes:02d}:{seconds:02d}"

    blocks = "🟩" * minutes
    phase_label = PHASE_LABEL.get(state.phase, state.phase)

    line = f"\r[{phase_label}] {time_str} {blocks}   "
    sys.stdout.write(line)
    sys.stdout.flush()


def print_help() -> None:
    """操作方法を表示する。"""
    print("\n操作: [s]開始  [p]一時停止/再開  [q]終了")
