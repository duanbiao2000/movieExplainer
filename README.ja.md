# MovieExplainer - IELTS字幕学習教材生成ツール

---

**[English](README.md)** | **[简体中文](README.zh-CN.md)** | **日本語**

---

> 数分で、任意の動画字幕から完全なIELTS学習教材を生成

動画字幕から構造化された英語学習教材を自動抽出するClaude Codeワークフローシステムです。

## MovieExplainer が必要な理由

### 解決される課題

| 課題 | MovieExplainerの解決策 |
|------|------------------------|
| **動画の内容を忘れる** | 重要なポイントを自動抽出し、構造化されたノートを作成 |
| **手動整理に数時間かかる** | ワンコマンドで自動抽出、数分で完了 |
| **練習教材が不足** | CSVワークシート + Ankiカードを生成、そのまま使用可能 |
| **発音学習が見過ごされる** | 単語カードに国際音声記号を含み、発音学習をサポート |
| **動画処理が面倒** | 動画をダウンロードする必要がなく、字幕/テキストだけでOK、軽量高效 |

### 特徴

**🎯 任意の動画を学習教材に**

- 興味深い、または感銘を受けた動画コンテンツを徹底的に復習
- 字幕ファイル（SRT/VTT/TXT）または転写テキストを提供するだけ
- 動画ファイルをダウンロード・処理する必要がありません

**⚡ 軽量・高効率**

- テキストから直接抽出、動画ストリーム処理不要
- 構造化された学習教材を生成：重要ポイント、単語、表現、コロケーション
- Ankiとリアルタイム連携、ワンクリックでインポート可能なカードパック

**📚 多様なシーンで活用**

- TED講演 → ポイントと表現を抽出
- IELTSリスニング教材 → 単語と演習を生成
- ニュースドキュメンタリー → トピック別単語を蓄積
- 興味のある任意の動画 → パーソナライズされた学習教材

### 誰に役立つ？

| ユーザー | ベネフィット |
|------|----------|
| **IELTS受験者** | 4技能すべてに対応した高スコア表現と単語を迅速に蓄積 |
| **英語学習者** | 実際の素材から自然な用法を学び、インプットからアウトプットへ |
| **教師/メンター** | 授業や課題のための練習教材を迅速に生成 |

### コア機能

- 🎯 重要ポイント、動詞フレーズ、単語、IELTS表現を自動抽出
- ✅ コンテンツ品質を保証するスマートレビューと反復最適化
- 📦 複数の出力形式：Markdown、CSV、Anki (.apkg)
- 🔊 単語カードは国際音声記号を含み、発音学習をサポート

## 前提条件

MovieExplainerは以下の環境に依存しており、コンポーネントごとに異なる要件があります。

### 必須環境

| 環境 | 目的 | 影響するモジュール |
|------|------|-------------------|
| **Claude Code** または Agent CLI | AIワークフローエンジン、字幕解析とコンテンツ抽出を実行 | コアワークフロー (`/extract-subtitle`) |
| **LLM API アクセス** | Claude / GPT-4 など、インテリジェントなコンテンツ抽出とレビューに使用 | すべてのAI駆動機能 |
| **VSCode**（オプション） | Claude Code拡張機能の推奨エディタ | 開発体験 |

### オプション環境

| 環境 | 目的 | 影響するモジュール |
|------|------|-------------------|
| **Python 3.8+** | .apkgファイルの生成 | `csv-to-anki.py` スクリプト |
| **pip** | Python依存関係のインストール | `genanki` ライブラリ |

### 環境依存関係図

```
字幕ファイル (.srt)
    │
    ▼
┌─────────────────────────────────────┐
│  Claude Code / Agent CLI           │  ← 必須
│  + LLM API (Claude/GPT-4)          │  ← 必須
├─────────────────────────────────────┤
│  /extract-subtitle ワークフロー実行 │
│  ↓                                  │
│  生成:                              │
│  • key-points.md                    │
│  • vocabulary.md                    │
│  • verb-phrases.md                  │
│  • ielts-expressions.md             │
│  • worksheet.csv                    │
│  • anki-deck.csv                   │
└─────────────────────────────────────┘
                │
                ▼ (オプション)
┌─────────────────────────────────────┐
│  Python 3.8+ + genanki             │  ← オプション
├─────────────────────────────────────┤
│  csv-to-anki.py を実行             │
│  ↓                                  │
│  生成: anki-deck.apkg              │
└─────────────────────────────────────┘
```

### インストールガイド

#### 1. Claude Code をインストール

```bash
# npmを使用してインストール
npm install -g @anthropic-ai/claude-code

# またはVSCodeで拡張機能をインストール
# "Claude Code"を検索してインストール
```

#### 2. LLM APIを設定

Claude Codeは複数のLLMプロバイダーをサポートしています。いずれかを選択：

- **Anthropic Claude**（推奨）- [API Key取得](https://console.anthropic.com/)
- **OpenAI GPT-4** - [API Key取得](https://platform.openai.com/)

設定方法：Claude Code設定にAPI Keyを追加。

#### 3. Python環境をインストール（オプション）

.apkgファイルを生成する場合：

```bash
# 仮想環境を作成（推奨）
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 依存関係をインストール
pip install genanki
```

## クイックスタート

### 1. VSCodeでプロジェクトを開く

[Claude Code](https://claude.com/claude-code)拡張機能がインストールされていることを確認してください。

### 2. ワークフローを使用

```bash
# 字幕ファイルを処理
/extract-subtitle examples/sample-lesson.srt

# 目標バンドスコアを指定
/extract-subtitle examples/sample-lesson.srt --target-band 7.5

# レビューステップをスキップ（より高速）
/extract-subtitle examples/sample-lesson.srt --no-review
```

### 3. 出力を確認

学習教材は字幕ファイルと同じディレクトリの `learning-materials/` フォルダーに生成されます：

```
learning-materials/
├── key-points.md          # 重要ポイント
├── vocabulary.md          # 単語リスト
├── verb-phrases.md        # 動詞フレーズ
├── ielts-expressions.md   # IELTS高スコア表現
├── worksheet.csv          # 練習ワークシート（Excelで開く）
├── anki-deck.csv          # Ankiインポートファイル（タブ区切り）
└── anki-deck.apkg         # Ankiデッキパッケージ（手動生成）
```

## Anki .apkgファイルの生成

.apkg形式はAnkiの公式パッケージ形式で、ダブルクリックするだけで追加設定なしにインポートできます。

### 自動生成（推奨）

ワークフローは自動的に `anki-deck.csv` を生成します。.apkg形式が必要な場合、ワークフロー内で変換スクリプトを自動的に呼び出すことができます。

### 手動生成

#### ステップ1: Python依存関係をインストール

**仮想環境の使用を強く推奨**（システムPythonを汚染しないため）：

```bash
# 仮想環境を作成
python -m venv .venv

# 仮想環境を有効化
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 依存関係をインストール
pip install genanki
```

#### ステップ2: .apkgファイルを生成

```bash
# 基本的な使用方法
python .claude/scripts/csv-to-anki.py learning-materials/anki-deck.csv

# 出力パスを指定
python .claude/scripts/csv-to-anki.py learning-materials/anki-deck.csv learning-materials/my-deck.apkg
```

#### ステップ3: Ankiにインポート

生成された `.apkg` ファイルをダブルクリックすると、Ankiが自動的にインポートします。デッキ名は **MovieExplainer** です。

## 出力形式ガイド

| 形式 | 目的 | 開き方 |
| :--- | :--- | :--- |
| `key-points.md` | 重要ポイントリファレンス | テキストエディタ |
| `vocabulary.md` | 単語学習 | テキストエディタ |
| `verb-phrases.md` | 動詞フレーズ学習 | テキストエディタ |
| `ielts-expressions.md` | 高スコア表現学習 | テキストエディタ |
| `worksheet.csv` | 練習ワークシート | **ダブルクリック（Excel）** |
| `anki-deck.csv` | Ankiタブ区切り形式 | Anki → ファイル → インポート |
| `anki-deck.apkg` | Ankiデッキパッケージ | **ダブルクリックでインポート** |

## プロジェクト構造

```
.claude/
├── skills/           # Claude Codeスキル
├── agents/           # SubAgent定義
├── hooks/            # セッションホック
├── scripts/          # ユーティリティスクリプト（csv-to-anki.pyなど）
└── memory/           # プロジェクト改善記録

examples/             # サンプル字幕ファイル
projects/             # あなたのワークスペース
```

## ワークフローコンポーネント

1. **字幕パーサー** - SRT/VTT/TXT形式を解析
2. **コンテンツ抽出器** - 学習コンテンツを抽出
3. **コンテンツレビュアー** - 品質チェック
4. **イテレーションオプティマイザー** - 複数回の改善

## 作者について

MovieExplainerは、著者のIELTS準備中に開発された学習ツールです。著者は現在Ankiカードを使用して単語と表現を蓄積・復習しています。

もしIELTS試験の準備中や英語力を向上させたい場合は、ぜひ著者に連絡して一緒に学びましょう：

> **Email**: [duanbiao2000@gmail.com](mailto:duanbiao2000@gmail.com)

## ライセンス

MIT License
