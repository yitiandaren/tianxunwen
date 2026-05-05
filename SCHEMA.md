# SCHEMA.md ─ 天訊文 .md 檔結構規範

> 對齊「素行內容流水線發布格式標準 v1.1」  
> 版本：v1.0（2026/05/05）

---

## 一、檔名規範

```
TX-{YYYYMMDD}-{NNN}.md
```

- `TX`：固定前綴，識別本倉庫之天訊文檔
- `YYYYMMDD`：天訊文「現示時間」之日期（非發布日，非歸檔日）
- `NNN`：當日流水號，3 位數，不足補 0；當日順序依「現示時間」正序，最早為 001

範例：`TX-20260502-001.md`

---

## 二、YAML Frontmatter 欄位

每篇 .md 必須以 YAML frontmatter 起頭，包覆於兩條 `---` 之間。

### 識別欄位（必填）

| 欄位 | 型別 | 說明 |
|---|---|---|
| `tx_id` | string | TX 編號，與檔名一致 |
| `old_id` | string | 對應網站 v1.5 舊 ID（過渡期保留） |
| `subject` | string | 主題 = 標題 |
| `category` | string | 分類（破與強・新時代／本元覺醒／素行心法／…） |
| `show_time` | ISO 8601 | 現示時間 `YYYY-MM-DDTHH:MM:SS` |
| `publish_code` | string(14) | 14 碼純數字現示時間 `YYYYMMDDHHMMSS` |
| `char_count` | int | 原文字數 |
| `reading_minutes` | int | 預估閱讀分鐘數 |
| `tags` | string[] | 主題標籤陣列 |

### 整理層欄位（待補）

| 欄位 | 說明 | 撰寫者 |
|---|---|---|
| `editor_intro` | 1-3 句編者引言（不詮釋原意） | 一天行 |
| `open_question` | 1 句開放式結尾提問 | 一天行 |
| `related_ids` | 3 篇延伸閱讀 TX ID 陣列 | 系統推薦 + 一天行確認 |

### 索引層欄位

| 欄位 | 說明 |
|---|---|
| `keywords` | SEO 關鍵字最多 5 個（陣列） |
| `meta_description` | ≤150 字，含「一天大人」「天訊文」與主題關鍵字 |
| `og_image` | 1200×630 OG 圖片 URL |
| `url_slug` | `tianxunwen-TX-YYYYMMDD-NNN`（v1.1 規格） |
| `publish_status` | `待發布` / `已發布` / `全平台完成` |
| `published_platforms` | 已發布平台陣列 |
| `license` | `CC BY-ND 4.0`（固定） |

### 系列欄位（視篇而定）

| 欄位 | 說明 |
|---|---|
| `series_id` | 系列識別碼 |
| `series_title` | 系列名稱 |
| `series_order` | 在系列中的順序（1-based） |
| `series_total` | 系列總篇數 |

---

## 三、內文結構（Markdown 主體）

### 必要章節（依順序）

1. **H1 標題**：`# 天訊文 TX-YYYYMMDD-NNN　{主題}　一天大人 太素天尊`
2. **基本資料表格**：以 Markdown 表格列出編號、現示時間、主題、分類、關鍵字、字數、授權
3. **系列資訊**（視篇而定）
4. **天訊文原文**：`## 天訊文原文` 後接完整原文，**不得改寫、不得刪節、不得潤飾**
5. **來源標注**：`## 來源標注` 後接 v1.1 標準格式來源標注
6. **素行體系**：`## 素行體系` 後列出 8 條官方平台連結
7. **授權聲明**：`## 授權聲明` 後說明 CC BY-ND 4.0

### 來源標注硬規則

```
一天大人 太素天尊　天訊文 TX-YYYYMMDD-NNN　現示時間：YYYY年MM月DD日 HH:MM:SS
```

- 字元順序、空格寬度、全形半形不得更動
- `　`（全形空格）出現於「太素天尊」與「天訊文」之間，以及「TX-…」與「現示時間」之間

### 素行體系連結（標準版）

```
官網：https://yitiandaren.net
YouTube：https://www.youtube.com/@YitianGuide
Telegram：https://t.me/yitiandaren
LINE：https://lin.ee/w4RoTW9
Facebook：https://www.facebook.com/yitiandaren
Medium：https://medium.com/@yitiandaren
Matters：https://matters.town/@yitiandaren
GitHub：https://github.com/yitiandaren/tianxunwen
```

---

## 四、隱藏紀錄

下列篇目**不上架本倉庫**，但於系統內保留：

| TX-ID（保留位） | 現示時間 | 主題 | 隱藏原因 |
|---|---|---|---|
| 4/29 19:36 | 2026-04-29T19:36:55 | 素行生命能量之約 | 一天行裁示隱藏 |
| 4/28 10:29 | 2026-04-28T10:29:13 | 人性操控（重發） | 與 4/14 10:54〈人性操控〉內容相同，視為重發；以 4/14 為主篇 |

---

## 五、版本沿革

| 版本 | 日期 | 變動 |
|---|---|---|
| v1.0 | 2026/05/05 | 首次發布；對齊發布格式標準 v1.1 |
