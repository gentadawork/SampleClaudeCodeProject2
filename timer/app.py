"""タイマーのメインループとキー入力を担当する制御層。"""

import msvcrt
import time
from datetime import datetime

from timer import display, logger
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
    task_name = display.get_task_name()
    state = TimerState()
    print_help()

    entries: list[logger.LogEntry] = []       # 完了済みエントリの蓄積
    current_entry: logger.LogEntry | None = None  # 進行中エントリ
    elapsed = 0.0

    while True:
        # キー入力をチェック
        if msvcrt.kbhit():
            key = msvcrt.getch().decode("utf-8", errors="ignore").lower()
            prev_status = state.status
            keep_running = handle_key(key, state)

            if not keep_running:
                # q キー: 進行中エントリを閉じ、終了エントリを追加してループ終了
                if current_entry is not None:
                    logger.end_entry(current_entry)
                    entries.append(current_entry)
                quit_entry = logger.start_entry("終了")
                logger.end_entry(quit_entry)
                entries.append(quit_entry)
                print("\n終了しました。")
                break

            elif key == "l":
                # l キー: 完了済みエントリ + 進行中エントリのスナップショットを保存
                filepath = datetime.now().strftime("log_%Y%m%d_%H%M.csv")
                snapshot = list(entries)
                if current_entry is not None:
                    now = datetime.now()
                    snapshot.append(logger.LogEntry(
                        title=current_entry.title,
                        start=current_entry.start,
                        finish=now,
                    ))
                logger.save_to_csv(snapshot, filepath)
                display.print_log_saved(filepath)

            else:
                # ステータス変化を検出してログ記録
                if prev_status != "running" and state.status == "running":
                    # 開始（stopped → running）
                    if prev_status == "stopped":
                        current_entry = logger.start_entry(task_name)
                    # 再開（paused → running）
                    elif prev_status == "paused":
                        if current_entry is not None:
                            logger.end_entry(current_entry)
                            entries.append(current_entry)
                        phase_title = task_name if state.phase == "focus" else "休憩"
                        current_entry = logger.start_entry(phase_title)
                elif prev_status == "running" and state.status == "paused":
                    # 一時停止（running → paused）
                    if current_entry is not None:
                        logger.end_entry(current_entry)
                        entries.append(current_entry)
                    current_entry = logger.start_entry("一時停止・再開")

        # 1秒ごとにカウントダウン（running のときのみ）
        if state.status == "running":
            elapsed += POLL_INTERVAL
            if elapsed >= 1.0:
                elapsed = 0.0
                prev_phase = state.phase
                tick(state)
                if prev_phase == "focus" and state.phase == "break":
                    play_focus_end_sound()
                    # 集中エントリを閉じ、休憩エントリを開始
                    if current_entry is not None:
                        logger.end_entry(current_entry)
                        entries.append(current_entry)
                    current_entry = logger.start_entry("休憩")
                elif prev_phase == "break" and state.phase == "focus":
                    play_break_end_sound()
                    # 休憩エントリを閉じ、集中エントリを開始
                    if current_entry is not None:
                        logger.end_entry(current_entry)
                        entries.append(current_entry)
                    current_entry = logger.start_entry(task_name)

        render(state)
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run()
