# 学習タイマーアプリ

コマンドライン上で動作する、シンプルなポモドーロタイマーです。
25分集中＋5分休憩を繰り返します。

## 表示イメージ

```text
操作: [s]開始  [p]一時停止/再開  [q]終了
[集中] 24:35 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩
```

## セットアップ

```bash
# 仮想環境を作成（初回のみ）
python -m venv .venv

# 依存パッケージをインストール
.venv/Scripts/pip.exe install pytest ruff
```

## 起動方法

```bash
.venv/Scripts/python.exe -m timer.app
```

## 操作方法

| キー | 動作 |
| --- | --- |
| `s` | 開始 |
| `p` | 一時停止 / 再開 |
| `q` | 終了 |

## 開発用コマンド

```bash
# テスト実行
.venv/Scripts/pytest.exe -v

# リンター
.venv/Scripts/ruff.exe check .
```

## ファイル構成

```text
├── timer/
│   ├── state.py     # データ層: タイマーの状態管理
│   ├── display.py   # UI層: コマンドラインへの表示
│   └── app.py       # 制御層: キー入力とメインループ
└── tests/
    ├── test_state.py
    ├── test_display.py
    └── test_app.py
```
