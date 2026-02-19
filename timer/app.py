"""タイマーのメインループとキー入力を担当する制御層。"""

import msvcrt
import time

from timer.display import play_break_end_sound, play_focus_end_sound, print_help, render
from timer.state import TimerState, tick

POLL_INTERVAL = 0.1  # キー入力をチェックする間隔（秒）


def handle_key(key: str, state: TimerState) -> bool:
    """キー入力に応じて状態を更新する。

    Args:
        key: 押されたキー文字。
        state: 更新対象の TimerState。

    Returns:
        False を返すとメインループを終了する。それ以外は True。
    """
    if key == "s":
        state.status = "running"
    elif key == "p":
        if state.status == "running":
            state.status = "paused"
        elif state.status == "paused":
            state.status = "running"
    elif key == "q":
        return False
    return True


def run() -> None:
    """タイマーのメインループを実行する。"""
    state = TimerState()
    print_help()

    elapsed = 0.0

    while True:
        # キー入力をチェック
        if msvcrt.kbhit():
            key = msvcrt.getch().decode("utf-8", errors="ignore").lower()
            if not handle_key(key, state):
                print("\n終了しました。")
                break

        # 1秒ごとにカウントダウン
        if state.status == "running":
            elapsed += POLL_INTERVAL
            if elapsed >= 1.0:
                elapsed = 0.0
                prev_phase = state.phase
                tick(state)
                if prev_phase == "focus" and state.phase == "break":
                    play_focus_end_sound()
                elif prev_phase == "break" and state.phase == "focus":
                    play_break_end_sound()

        render(state)
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run()
