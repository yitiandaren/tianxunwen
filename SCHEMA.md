# SCHEMA.md｜天訊文典藏結構規範

版本：v2.1  
日期：2026-08-06

## 一、ID與檔名

### 1. YTS正式主ID

```text
YTS-TX-{YYYYMMDDHHMMSS}-{SEQ}
```

天訊文原始物件第一筆固定：

```text
YTS-TX-20260404124430-001
```

`yts_id`建立後永久不變；版本、語言、權限與審核狀態不得寫入ID。

### 2. GitHub典藏ID

```text
TX-{YYYYMMDDHHMMSS}
```

檔名固定使用：

```text
archive/TX-{YYYYMMDDHHMMSS}.md
```

`tx_id`是既有公開典藏與URL錨點，不因YTS ID導入而再次更名。

### 3. 舊ID

```text
TX-{YYYYMMDD}-{NNN}
```

只保存於`legacy_id`，不得再用於新檔名或新物件。

## 二、時間一致性

下列四項必須指向同一秒：

```yaml
yts_id: YTS-TX-20260404124430-001
tx_id: TX-20260404124430
show_time: '2026-04-04T12:44:30'
publish_code: '20260404124430'
```

## 三、最低Frontmatter

```yaml
---
yts_id: YTS-TX-20260404124430-001
tx_id: TX-20260404124430
legacy_id: TX-20260404-003
old_id: 20260404-1244
subject: 素語三百
source_author: 一天大人 太素天尊
source_type: 天訊文
show_time: '2026-04-04T12:44:30'
publish_code: '20260404124430'
category: 素語三百
keywords: []
related_ids: []
content_status: 原文已確認
publish_status: published
visibility: public
license: CC BY-ND 4.0
---
```

既有檔案尚未補入`yts_id`時仍可通過v2.1驗證；所有新建天訊文必須依模板建立`yts_id`。

## 四、內文結構

1. H1標題
2. 基本資料
3. 天訊文原文
4. 來源標注
5. 授權聲明

來源標注：

```text
一天大人 太素天尊　天訊文 TX-YYYYMMDDHHMMSS　現示時間：YYYY年MM月DD日 HH:MM:SS
```

## 五、不可變內容

`## 天訊文原文`以下的原始內容：

- 不得改寫
- 不得潤飾
- 不得節錄後冒充原文
- 不得由AI補字
- 不得以翻譯覆蓋原文

如需訂正，必須保留原始依據、變更紀錄、審核者與審核時間。

## 六、可編輯Metadata

可在不改動原文的前提下維護：

- 分類與標籤
- 關鍵詞
- 編者引言
- 開放問題
- 關聯ID
- SEO與GEO欄位
- 發布平台
- 權限、狀態及審核資訊

## 七、衍生資料

下列檔案由腳本生成：

- `data/tx_index.json`
- `data/metadata_audit.json`
- `id_mapping.csv`

生成資料不得反向覆蓋原典；若與`archive/`或`data/id_mapping.json`衝突，以原典及正式對照表為準。

## 八、版本沿革

| 版本 | 日期 | 內容 |
|---|---|---|
| v1.0 | 2026-05-05 | 舊日期流水號規格 |
| v2.0 | 2026-06-02 | 遷移為14碼現示時間規格 |
| v2.1 | 2026-08-06 | 導入YTS主ID並對齊驗證與文件 |
