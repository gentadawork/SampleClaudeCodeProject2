"""タイマーの表示を担当するUI層。"""

import sys
import winsound

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


def get_task_name() -> str:
    """作業名をユーザーから入力させる。

    Returns:
        入力された作業名。空の場合は "作業" を返す。
    """
    name = input("作業名を入力してください: ").strip()
    return name if name else "作業"


def print_log_saved(filepath: str) -> None:
    """CSVファイルへの保存完了メッセージを表示する。

    Args:
        filepath: 保存されたファイルのパス。
    """
    print(f"\nログを保存しました: {filepath}")


def print_help() -> None:
    """操作方法を表示する。"""
    print("\n操作: [s]開始  [p]一時停止/再開  [l]ログ保存  [q]終了")


def play_focus_end_sound() -> None:
    """集中時間終了時にビープ音を鳴らす。"""
    winsound.Beep(500, 500)


def play_break_end_sound() -> None:
    """休憩時間終了時にビープ音を鳴らす。"""
    winsound.Beep(1000, 500)
