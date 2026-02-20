# CLAUDE.md — Python Project Rules

## [Project Context]
- プロジェクト名: 学習タイマーアプリプロジェクト
- 技術スタック: Python 3.12, pytest, ruff
- パッケージ管理: pip + `.venv`
- 概要: シンプルな学習タイマーアプリの開発・保守
- 目的: このプロジェクトは学習用です。シンプルな学習タイマーアプリを作成します。

## [制約]
- 本番品質は不要です。
- わたしの理解しやすさを最優先します。
- 高度な設計よりも、シンプルで読みやすいコードを優先します。
- 小さな単位で提案してください。
- 下記のような複雑さが増す設計は可能な限り避けてください。
  - 抽象化
  - 非同期処理
- デザインパターン（ソフトウェア設計でよく起きる問題に対する典型的な解決方法）の導入は不要です。
- レイヤーは3層以内にしてください。
- テストは最低限にしてください。
- 将来拡張は考慮しなくてよいです。
- 改善点を提示する際は、下記を説明してください。
  - なぜ必要か
  - 学習にどう影響するか

## [機能要件]
- 25分集中＋5分休憩を繰り返すタイマー。
- タイマーの開始、一時停止、再開、削除ができる。
- コマンドライン上で動作する。
- コマンドライン上でタイマーの状態が分かるようにする。
  - mm:ss の書式での時間表示
  - 視覚的にわかりやすいように、残りの分数の「🟩」文字（残り24分なら24個の🟩）を、時間表示の次に表示
- プログラム開始時に作業名を入力する。
- 下記のイベント発生時刻を自動記録する。
  - 集中時間の開始・終了
  - 休憩時間の開始・終了
  - 一時停止・再開
  - 終了
- `l` キーでイベント履歴を CSV ファイル（`log_YYYYMMDD_HHMM.csv`）に保存できる。

## [Architecture]

### ファイル構成

```text
SampleClaudeCodeProject2/
├── timer/
│   ├── __init__.py
│   ├── state.py       # データ層: タイマーの残り秒数・フェーズ・状態を保持
│   ├── logger.py      # ログ層: イベント記録と CSV 保存
│   ├── display.py     # UI層: \r で同一行を上書き表示
│   └── app.py         # 制御層: キー入力を受け取り、state を更新して display を呼ぶ
├── tests/
│   ├── test_state.py  # データ層のテスト
│   ├── test_display.py # UI層のテスト
│   ├── test_app.py    # 制御層のテスト
│   └── test_logger.py # ログ層のテスト
├── pyproject.toml
└── CLAUDE.md
```

### 層の役割

| 層 | ファイル | 役割 |
| --- | --- | --- |
| データ | `timer/state.py` | タイマーの残り秒数・フェーズ・状態を保持 |
| ログ | `timer/logger.py` | イベント記録（`LogEntry`）と CSV 保存 |
| UI | `timer/display.py` | `\r` で同一行を上書き表示、ユーザー入力受付 |
| 制御 | `timer/app.py` | キー入力を受け取り、`state` を更新して `display` を呼ぶ |

### タイマーの状態（`state.py`）

```python
@dataclass
class TimerState:
    phase: str         # "focus" or "break"
    remaining_sec: int
    status: str        # "running" / "paused" / "stopped"
```

### 操作方法（キー入力）

| キー | 動作 |
| --- | --- |
| `s` | 開始 |
| `p` | 一時停止 / 再開 |
| `l` | ログを CSV ファイルに保存 |
| `q` | ログを保存して終了 |

### 表示イメージ

```text
作業名を入力してください: ClaudeCodeの使い方に関する学習

操作: [s]開始  [p]一時停止/再開  [l]ログ保存  [q]終了
[集中] 24:35 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩
```

### CSV 保存フォーマット（`log_YYYYMMDD_HHMM.csv`）

```text
start, finish, title
9:01, 9:26, ClaudeCodeの使い方に関する学習
9:26, 9:31, 休憩
9:31, 9:40, ClaudeCodeの使い方に関する学習
9:40, 9:42, 一時停止・再開
9:42, 9:58, ClaudeCodeの使い方に関する学習
9:58, 9:59, 休憩
9:59, 9:59, 終了
```

## [Build & Commands]
- 依存関係インストール: `.venv/Scripts/pip.exe install pytest ruff`
- ソフトウェアの実行: `.venv/Scripts/python.exe -m timer.app`
- 全テスト実行: `.venv/Scripts/pytest.exe -v`
- 特定のテスト実行: `.venv/Scripts/pytest.exe %s`
- リンター (Ruff): `.venv/Scripts/ruff.exe check .`

## [Code Style & Guidelines]
- 型ヒント: 公開関数とクラスメソッドには必ず型ヒントを付ける。
- 命名規則: 変数・関数は `snake_case`、クラスは `PascalCase`、定数は `UPPER_SNAKE_CASE`。
- docstring: Googleスタイルを採用し、複雑なロジックには `Args` と `Returns` を明記。
- 非同期: このプロジェクトは同期処理のみ。`async/await` は使用しない。
- エラーハンドリング: `try-except` では具体的な例外（例: `ValueError`）をキャッチし、`Exception` のみのキャッチは避ける。

## [Common Patterns]

- **状態の変更は `state.py` の関数で行う**: `state.remaining_sec -= 1` のような直接操作はテストファイル以外では行わず、`tick()` などの関数を通じて変更する。
- **表示は `display.py` に集約**: `print()` を `app.py` から直接呼ばない。表示に関する処理は `display.py` の関数を使う。
- **キー操作のロジックは `handle_key()` に集約**: 新しいキー操作を追加するときは `handle_key()` に `elif key == "..."` を追加する。
- **ユーザー通知（音・表示を問わず）は `display.py` に集約**: 音声通知も「ユーザーへの出力」なので `display.py` に置く。`app.py` から `winsound` を直接呼ばない。
- **状態変化の検出は呼び出し前後で比較する**: `tick()` のような関数が状態を変えるとき、変化のタイミングを検出したい場合は呼び出し前に値を保存して比較する。

  ```python
  prev_phase = state.phase
  tick(state)
  if prev_phase == "focus" and state.phase == "break":
      # フェーズが変わった瞬間だけ実行したい処理
  ```

- **Windows ビルトイン `winsound` でビープ音**: 外部パッケージ不要。`winsound.Beep(周波数Hz, 長さms)` で鳴らせる。

- **ログ管理は `logger.py` に集約**: イベント記録（`start_entry`/`end_entry`）とCSV保存（`save_to_csv`）は `logger.py` に置く。`app.py` からリストを直接操作しない。

- **副作用のみのキー（`l` など）は `handle_key()` に追加しない**: `handle_key()` は `TimerState` の変更専用とする。ログ保存のような副作用処理は `run()` 内で `key == "l"` を直接チェックして実行する。

- **進行中エントリのスナップショットは元を変えずにコピーを作る**: `save_to_csv` に進行中エントリを渡す際は `LogEntry` のコピーを生成し、`finish` に現在時刻をセットしてから渡す。元のエントリは変更しない。

  ```python
  snapshot = list(entries)
  if current_entry is not None:
      now = datetime.now()
      snapshot.append(LogEntry(
          title=current_entry.title,
          start=current_entry.start,
          finish=now,
      ))
  save_to_csv(snapshot, filepath)
  ```

- **`handle_key()` 呼び出し前後のステータス比較でログタイミングを検出**: `prev_status = state.status` を保存してから `handle_key()` を呼び出し、変化を比較してイベントを判断する。`prev_phase` との比較パターンと同じ考え方。

  ```python
  prev_status = state.status
  handle_key(key, state)
  if prev_status != "running" and state.status == "running":
      # running になった瞬間だけ実行したい処理
  ```

## [Windows / Environment Notes]
- 仮想環境: プロジェクトルートの `.venv/` を使用する。
- 日本語文字列: ruff の E501（行長）は日本語2列幅の影響で除外している（`pyproject.toml` の `ignore = ["E501"]`）。

## [Test Strategy]

### テストファイルと内容

**`tests/test_state.py`** — データ層

- 初期状態が `phase="focus"`, `remaining_sec=1500`（25分）, `status="stopped"` か
- カウントダウンで `remaining_sec` が1減るか
- `remaining_sec` が0になったとき `phase` が `"focus"` → `"break"` に切り替わるか
- `"break"` 終了後に `"focus"` に戻るか

**`tests/test_display.py`** — UI層

- 残り `24:35` のとき `🟩` が24個出力されるか
- フェーズ名（`[集中]` / `[休憩]`）が正しく表示されるか

**`tests/test_app.py`** — 制御層

- `s` キーで `status` が `"running"` になるか
- `p` キーで `"paused"` になるか
- `p` キーを再度押すと `"running"` に戻るか

**`tests/test_logger.py`** — ログ層

- `start_entry()` でタイトルと開始時刻が設定され、終了時刻が `None` か
- `end_entry()` で終了時刻が設定されるか
- `save_to_csv()` で CSV ファイルが生成されるか
