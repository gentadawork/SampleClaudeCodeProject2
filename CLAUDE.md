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

## [Architecture]

### ファイル構成

```text
SampleClaudeCodeProject2/
├── timer/
│   ├── __init__.py
│   ├── state.py       # データ層: タイマーの残り秒数・フェーズ・状態を保持
│   ├── display.py     # UI層: \r で同一行を上書き表示
│   └── app.py         # 制御層: キー入力を受け取り、state を更新して display を呼ぶ
├── tests/
│   ├── test_state.py  # データ層のテスト
│   ├── test_display.py # UI層のテスト
│   └── test_app.py    # 制御層のテスト
├── pyproject.toml
└── CLAUDE.md
```

### 層の役割

| 層 | ファイル | 役割 |
| --- | --- | --- |
| データ | `timer/state.py` | タイマーの残り秒数・フェーズ・状態を保持 |
| UI | `timer/display.py` | `\r` で同一行を上書き表示 |
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
| `q` | 終了（削除） |

### 表示イメージ

```text
[集中] 24:35 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩
操作: [s]開始  [p]一時停止/再開  [q]終了
```

## [Build & Commands]
- 依存関係インストール: `.venv/Scripts/pip.exe install ❓❓❓`
｛計画後に追記｝
- ソフトウェアの実行: `.venv/Scripts/python.exe -m ❓❓❓`｛計画後に追記｝
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
｛計画後に追記｝
｛開発後に追記｝

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

｛開発後に追記｝
