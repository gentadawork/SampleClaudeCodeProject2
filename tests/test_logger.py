"""logger.py のテスト。"""

import os

from timer.logger import end_entry, save_to_csv, start_entry


def test_start_entry_sets_title_and_start() -> None:
    """start_entry() がタイトルと開始時刻を設定し、終了時刻が None であるか確認する。"""
    entry = start_entry("テスト作業")
    assert entry.title == "テスト作業"
    assert entry.start is not None
    assert entry.finish is None


def test_end_entry_sets_finish() -> None:
    """end_entry() が終了時刻を設定するか確認する。"""
    entry = start_entry("テスト作業")
    end_entry(entry)
    assert entry.finish is not None


def test_save_to_csv_creates_file(tmp_path) -> None:
    """save_to_csv() がCSVファイルを生成するか確認する。"""
    entry = start_entry("テスト作業")
    end_entry(entry)
    filepath = str(tmp_path / "test_log.csv")
    save_to_csv([entry], filepath)
    assert os.path.exists(filepath)
