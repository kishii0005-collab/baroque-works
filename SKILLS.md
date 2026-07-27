# 利用可能なSkills一覧

このセッションで利用可能な Claude Code Skills の記録（2026-07-27時点）。
新しいSkillsが追加/変更されたら随時更新すること。

## 自社・クライアント案件

- **baroque-works**: バロックワークス（自社）関連 — コーポレートサイト、社内経理/経費ツール、X/note発信（@kenta_juutaku）、M&Aアドバイザリー資料（Tekton Partners ロールアップファンド）、社内自動化パイプライン、バックオフィス業務。トリガー: "バロックワークス", "自社", "自分の会社", "Tekton Partners", "kenta_juutaku"
- **ecosmile**: エコすまいる（高知県・太陽光訪問販売）関連 — 営業資料、訪問販売トーク・スクリプト、特定商取引法チェック、マーケティング資料、SFA/CRM(GENIEE)/ANDPAD検討、議事録。2026年7月開始の新規案件。トリガー: "エコすまいる", "太陽光訪販", "太陽光", "訪問販売"
- **haruga-kensetsu**: はるが建設（高知県）関連 — ブランド資料、パンフレット、HP/LPコピー、SEO/MEO/AIO、Meta/Instagram広告、全社会議資料、議事録、採用・HR、安全衛生資料、倉庫事業(souko-katsuo.com)。トリガー: "はるが建設", "池内", "岡本", "吉野さん", "山中さん", "Casa", "Sereno", "はるが、はじまる。"
- **koyo-housing**: 向洋ハウジング（宮崎県延岡市）関連 — Meta広告、MEO/AIOクチコミ返信、SEOコラム、イベントLP、リフォーム単価表、SFA/CRM(GENIEE)、IT補助金申請、契約書類。トリガー: "向洋ハウジング", "谷岡", "延岡", "テクノストラクチャー工法"

## パーソナル

- **private-diary**: 個人的な日記・壁打ち・雑談用。仕事/クライアント案件には使わない。トリガー: "日記", "壁打ちしたい", "プライベートの話", "/diary"
- **morning**: モーニングブリーフをHTMLアーティファクトとして表示 or 定期実行の設定。/morning コマンド。

## ドキュメント/ファイル操作

- **pdf**: PDF読み取り/結合/分割/回転/透かし/フォーム入力/暗号化/OCR等
- **docx**: Word文書(.docx/.dotx)の作成/読み取り/編集
- **pptx**: PowerPoint(.pptx/.potx)の作成/読み取り/編集
- **xlsx**: Excel/CSV/TSVスプレッドシートの作成/読み取り/編集

## 開発・Claude Code運用系

- **session-start-hook**: Claude Code on the web用のSessionStartフック作成
- **update-config**: settings.json設定（フック、権限、環境変数）
- **keybindings-help**: キーバインドのカスタマイズ
- **fewer-permission-prompts**: 許可プロンプトを減らすためのallowlist追加
- **loop**: プロンプト/スラッシュコマンドを一定間隔で繰り返し実行
- **run**: プロジェクトのアプリを起動して動作確認
- **skill-creator**: 新規Skill作成・既存Skillの改善・評価
- **init**: CLAUDE.md初期化（コードベースのドキュメント化）
- **review**: GitHub PRのレビュー（作業中の差分は /code-review）
- **security-review**: 現在のブランチの変更点をセキュリティレビュー

## デザイン・可視化

- **artifact-design**: Artifactsのデザイン指針
- **artifact-capabilities**: Artifactに付与できるランタイム機能（ライブデータ、状態共有、自己更新等）
- **dataviz**: チャート/グラフ/ダッシュボード等のデータ可視化作成時の設計ガイド

## API/技術リファレンス

- **claude-api**: Claude API / Anthropic SDK リファレンス（モデルID、料金、パラメータ、ストリーミング、ツール利用、MCP、エージェント、キャッシング等）。Claude/Anthropicに言及するタスクでは必ず参照する。
