---
# ============================================================
# MA = Media Asset（媒體資產）
# 應用層：引用原典，支援music／video／image
# canonical: false
# ============================================================

# 【身份識別】
ma_id: MA-YYYYMMDD-TYPE-NNN
source_type: MA
canonical: false

# 【媒體屬性】
media_type: music
title: ''
description: ''
derivative_type: music_adaptation

# 【原典引用（必填）】
source_mn_id: ''
source_tx_id: ''
source_ek_id: ''
source_pb_id: ''

# 【使用規範】
usage_level: 公開
usage_occasion: 推廣

# 【內容分類】
domain: T3
use: A4
level: 素
level_note: ''

# 【引用權限】
citation_allowed: false
reference_allowed: true

# 【技術屬性】
duration_seconds: 0
file_format: ''
file_path: ''

# 【發布狀態】
production_status: 製作中
published_platforms: []

# 【授權】
license: CC BY-ND 4.0

# 【版本追蹤】
created_date: 'YYYY-MM-DD'
created_by: ''
created_at: 'YYYY-MM-DDTHH:MM:SS'
updated_at: ''

# 【審核】
reviewed_by: ''
reviewed_at: ''
---

# MA-YYYYMMDD-TYPE-NNN｜媒體資產名稱

## 基本資料

| 欄位 | 內容 |
|---|---|
| 編號 | MA-YYYYMMDD-TYPE-NNN |
| 名稱 | （填入媒體資產名稱） |
| 類型 | music／video／image |
| 衍生類型 | music_adaptation／visual_quote／short_video／reading_audio／poster／thumbnail |
| 適用層級 | 素／醒／覺／公開 |
| 使用場合 | 課誦／共修／推廣／個人修行 |
| 時長 | （填入秒數）秒 |
| 格式 | mp3／mp4／jpg／png |
| 製作狀態 | 製作中／已完成／已發布 |

## 原典來源

⚠️ 本媒體資產引用以下原典。原典永遠保持原典身份，不因引用而改變。

| 原典編號 | 類型 | 關聯說明 |
|---|---|---|
| MN-YYYYMMDDHHMMSS-NNN | MN | （音樂化的咒語來源） |
| TX-YYYYMMDDHHMMSS-NNN | TX | （引用的天訊文來源） |

## 內容說明

（填入媒體資產的內容說明、製作說明、使用說明）

## 檔案路徑

```text
archive/MA/music/MA-YYYYMMDD-music-NNN.mp3
archive/MA/video/MA-YYYYMMDD-video-NNN.mp4
archive/MA/image/MA-YYYYMMDD-image-NNN.jpg
```

## 授權聲明

CC BY-ND 4.0　須標明原典來源
