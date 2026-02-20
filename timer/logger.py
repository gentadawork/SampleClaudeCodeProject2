"""イベントログの管理とCSV保存を担当するモジュール。"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogEntry:
    """ログの1行分を表すデータクラス。

    Attributes:
        title: イベント名称（作業名、"休憩"、"一時停止・再開" など）。
        start: イベント開始時刻。
        finish: イベント終了時刻（終了時に設定される）。
    """

    title: str
    start: datetime
    finish: datetime | None = None


def start_entry(title: str) -> LogEntry:
    """開始時刻を記録した LogEntry を作成して返す。

    Args:
        title: イベントのタイトル。

    Returns:
        開始時刻が設定された LogEntry。
    """
    return LogEntry(title=title, start=datetime.now())


def end_entry(entry: LogEntry) -> None:
    """LogEntry に終了時刻を記録する。

    Args:
        entry: 更新対象の LogEntry。
    """
    entry.finish = datetime.now()


def save_to_csv(entries: list[LogEntry], filepath: str) -> None:
    """ログをCSVファイルに保存する。

    Args:
        entries: 保存する LogEntry のリスト。
        filepath: 保存先のファイルパス。
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("start, finish, title\n")
        for entry in entries:
            start_str = f"{entry.start.hour}:{entry.start.minute:02d}"
            finish_str = f"{entry.finish.hour}:{entry.finish.minute:02d}" if entry.finish else ""
            f.write(f"{start_str}, {finish_str}, {entry.title}\n")
