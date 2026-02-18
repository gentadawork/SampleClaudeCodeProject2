"""タイマーの状態を管理するデータ層。"""

from dataclasses import dataclass, field

FOCUS_SEC = 25 * 60   # 集中時間: 25分
BREAK_SEC = 5 * 60    # 休憩時間: 5分


@dataclass
class TimerState:
    """タイマーの状態を保持するデータクラス。

    Attributes:
        phase: 現在のフェーズ。"focus"（集中）または "break"（休憩）。
        remaining_sec: 残り秒数。
        status: タイマーの動作状態。"stopped" / "running" / "paused"。
    """

    phase: str = "focus"
    remaining_sec: int = field(default_factory=lambda: FOCUS_SEC)
    status: str = "stopped"


def tick(state: TimerState) -> None:
    """残り時間を1秒減らし、0になったらフェーズを切り替える。

    Args:
        state: 更新対象の TimerState。
    """
    if state.remaining_sec > 0:
        state.remaining_sec -= 1

    if state.remaining_sec == 0:
        if state.phase == "focus":
            state.phase = "break"
            state.remaining_sec = BREAK_SEC
        else:
            state.phase = "focus"
            state.remaining_sec = FOCUS_SEC
