# HuggingFace デイリーペーパーニュースレター

<div align="center">
  <a href="https://internlm.org/">
    <img src="https://internlm.org/assets/logo-a0611363.svg" alt="InternLM" height="80"/>
  </a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://huggingface.co/">
    <img src="https://huggingface.co/front/assets/huggingface_logo.svg" alt="HuggingFace" height="80"/>
  </a>
</div>

<p align="center">
  <em>InternLM を使用して HuggingFace の日次論文を翻訳</em>
</p>

<div align="center">

[English](README.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md)

</div>

---

このプロジェクトは、HuggingFace の日次論文データを自動的にダウンロードして処理し、InternLM（書生・浦語）大規模言語モデルを使用して複数の言語に翻訳します。プロジェクトは毎日自動的に実行され、最新の論文の取得と翻訳を確実に行います。

## 使用モデル

- **翻訳モデル**: [InternLM-3](https://internlm.org/)
  - 開発者: 上海人工知能研究所
  - バージョン: internlm3-latest
  - 特徴:
    - 強力な多言語翻訳能力
    - 学術テキストの正確な理解と翻訳
    - API によるリアルタイム翻訳

## 機能

- HuggingFace 日次論文データの自動ダウンロード
- 指定日付の履歴データのダウンロードをサポート
- 北京時間をデフォルトのタイムゾーンとして使用
- 完全なログ記録
- JSON 形式での論文メタデータの保存
- InternLM-3 による英語論文の多言語翻訳：
  - 日本語
  - 韓国語
  - スペイン語
  - フランス語
- 自動化ワークフロー：
  - 毎日の最新論文の自動ダウンロード
  - 自動多言語翻訳
  - リポジトリへの自動更新

## インストール

1. リポジトリのクローン：
```bash
git clone https://github.com/yourusername/hf-daily-paper-newsletter-multilingual.git
cd hf-daily-paper-newsletter-multilingual
```

2. 依存関係のインストール：
```bash
pip install -r requirements.txt
```

## 使用方法

### 手動実行

#### 当日の論文データのダウンロード

```bash
python download_papers.py
```

#### 指定日の論文データのダウンロード

```bash
python download_papers.py --date 2024-03-20
```

#### 論文データの翻訳

InternLM API キーを取得してから実行：

```bash
python translate_papers.py --date 2024-03-20 --api_key your_api_key_here
```

### 自動実行

プロジェクトには2つの GitHub Actions ワークフローが設定されています：

1. `daily-paper-download.yml`: 毎日北京時間 9:00 に最新論文を自動ダウンロード
2. `daily-paper-translate.yml`: ダウンロード完了後に自動翻訳

自動翻訳を有効にするには、リポジトリの Secrets に `INTERNLM_API_KEY` を設定する必要があります。

## データストレージ

- ダウンロードした原文（英語）論文データは `Paper_metadata_download` ディレクトリに保存
- 翻訳後の論文データは `Translated_papers` ディレクトリに言語コード別に保存：
  - ja/: 日本語翻訳
  - ko/: 韓国語翻訳
  - es/: スペイン語翻訳
  - fr/: フランス語翻訳
- すべてのファイルは JSON 形式で保存され、ファイル名は `YYYY-MM-DD.json` 形式

## リターンステータス

- 成功：終了コード 0
- エラー：終了コード 1
- データなし：終了コード 0（ただし、ログに警告を表示）

## 謝辞

- [InternLM](https://internlm.org/) - 強力な翻訳機能の提供
- [HuggingFace](https://huggingface.co/) - 日次論文データの提供 