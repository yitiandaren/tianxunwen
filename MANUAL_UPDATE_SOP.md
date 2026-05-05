# 天訊文人工更新 SOP

> **目的**：在不消耗 Manus 點數的前提下，由素行（一天行）親手更新網站與 GitHub typed典藏的天訊文。  
> **適用範圍**：新增天訊文、修正錯字、補整理層欄位。  
> **不適用範圍**：網站功能調整、視覺改版、新增頁面（這些仍需 Manus）。

---

## 一、更新流程總覽

```
新天訊文現示
    │
    ├─→ ① 編輯 scriptures.json（網站 repo）
    │       └→ Vercel 自動 build & 部署 → 網站上線
    │
    └─→ ② 在 tianxunwen repo 新增 .md（GitHub 典藏）
            └→ INDEX.md 同步更新
```

兩條線路**獨立運作**，可分開操作或同步操作。

---

## 二、線路 ①：更新網站（最常用）

### 2.1 前置確認

- 您的 GitHub 帳號 `yitiandaren` 已是網站 repo 的 owner（或 collaborator）
- Vercel 已連結到網站 repo，main 分支推送會自動部署

### 2.2 操作步驟

1. **打開 GitHub 網頁版**  
   進入網站 repo → 找到 `client/src/data/scriptures.json`

2. **點右上角鉛筆「Edit」按鈕**

3. **複製下方 JSON 模板，貼到陣列「最前面」**（確保最新一筆在頂端）：

   ```json
   {
     "id": "20260505-1234",
     "datetime": "2026-05-05T12:34:56",
     "date_label": "2026/05/05",
     "time_label": "12:34",
     "title": "請填入主題（即為標題）",
     "summary": "請填入摘要（自動取原文前 60 字即可）",
     "category": "短偈金句",
     "tags": ["標籤1", "標籤2"],
     "char_count": 0,
     "reading_minutes": 1,
     "body": "請填入完整原文。\n換行用 \\n。\n\n空行用 \\n\\n。",
     "publish_code": "20260505123456",
     "published": true,
     "publish_label": "2026/05/05 12:34:56"
   },
   ```

4. **修改欄位**（只需改 7 處）：

   | 欄位 | 規則 | 範例 |
   |---|---|---|
   | `id` | 8 碼日期 + `-` + 4 碼時分 | `20260505-1234` |
   | `datetime` | ISO 8601，到秒 | `2026-05-05T12:34:56` |
   | `date_label` | 顯示用日期 | `2026/05/05` |
   | `time_label` | 顯示用時 + 分 | `12:34` |
   | `title` | 主題 / 標題 | `行，即是得；路，即是經` |
   | `category` | 必須是現有 9 種之一（見下表） | `短偈金句` |
   | `tags` | 1~5 個標籤 | `["道", "行"]` |
   | `body` | 完整原文，換行用 `\n` | （見下方範例） |
   | `publish_code` | 14 碼到秒 | `20260505123456` |
   | `publish_label` | 顯示完整時間 | `2026/05/05 12:34:56` |

5. **不用改的欄位**：
   - `char_count`：填 0 即可（系統會用 body 自動算）
   - `reading_minutes`：1（短文）／2~5（長文）／20+（〈素語三百〉那種）
   - `summary`：可填可不填（不填則網站列表用 body 前 60 字）
   - `published`：永遠 `true`（要隱藏才設 `false`）

6. **9 種分類**（必填，照寫）：
   - `破與強・新時代`
   - `本元覺醒`
   - `素行心法`
   - `素語三百`
   - `權力與真實`
   - `行動系統`
   - `財富平衡`
   - `眾生與守地`
   - `短偈金句`

7. **頁面下方 Commit 訊息**：寫成 `add: TX-20260505 主題`

8. **Commit changes** → 選 `Commit directly to the main branch` → 綠色按鈕送出

9. **等 1~3 分鐘**，到 `https://yitiandaren.net` 確認新一篇已出現在首頁與〈典藏〉

### 2.3 範例（5/4 第一則的真實內容）

```json
{
  "id": "20260504-1254",
  "datetime": "2026-05-04T12:54:40",
  "date_label": "2026/05/04",
  "time_label": "12:54",
  "title": "行，即是得；路，即是經",
  "summary": "行，即是得；路，即是經。",
  "category": "短偈金句",
  "tags": ["道", "行", "經"],
  "char_count": 0,
  "reading_minutes": 1,
  "body": "行，即是得\n路，即是經",
  "publish_code": "20260504125440",
  "published": true,
  "publish_label": "2026/05/04 12:54:40"
},
```

### 2.4 常見錯誤排查

| 錯誤 | 原因 | 解法 |
|---|---|---|
| Vercel build 失敗 | JSON 格式錯誤（少逗號、引號） | 用 https://jsonlint.com 貼上整個 scriptures.json 檢查 |
| 中文亂碼 | 編輯時編碼非 UTF-8 | 改用 GitHub 網頁編輯，不要用 Windows 記事本 |
| 換行沒生效 | body 中應使用 `\n` 不是真實換行 | JSON 字串內換行必須轉義成 `\n` |
| 文章順序亂跳 | `publish_code` 14 碼不對 | 重檢查：`YYYY` `MM` `DD` `HH` `MM` `SS` 各自正確補零 |

---

## 三、線路 ②：更新 GitHub 典藏（給未來 GEO / AI 引擎索引用）

### 3.1 是否必要？

| 情境 | 線路 ① 網站 | 線路 ② GitHub 典藏 |
|---|---|---|
| 給人類讀者 | ✅ 必要 | ⭕ 可選 |
| 給生成式 AI 索引（GEO） | △ 可被索引但不穩定 | ✅ **首選**，長期穩定 |
| 給研究者引用 | ⭕ 可 | ✅ **首選**，有 commit 歷史與 CC 授權 |

**Manus 建議**：每篇天訊文都應在 GitHub 典藏。但您可以**累積一週做一次批次**（到時候請 Manus 跑一次自動化腳本，僅消耗極少點數）。

### 3.2 手動操作（單篇）

1. 進入 `tianxunwen` repo → `archive/` 資料夾
2. 點右上 `Add file` → `Create new file`
3. 檔名填：`TX-YYYYMMDD-NNN.md`（NNN 為當日流水號 3 位數，從 001 起算）
4. 從現有任一篇 `.md` 複製格式（建議複製 `archive/TX-20260504-001.md` 作模板）
5. 修改 frontmatter 欄位 + `## 天訊文原文` 區塊
6. Commit 到 main

### 3.3 批次操作（建議）

每月底請 Manus 跑一次：
```
請 Manus 把網站 scriptures.json 上次同步以後新增的天訊文，補入 tianxunwen repo
```
此操作消耗極少點數（< 10 點）。

---

## 四、整理層欄位補述（讓內容更豐富）

`.md` 檔的 frontmatter 中有以下空欄位，**由您自己補**（不消耗點數）：

```yaml
editor_intro: "（您寫 1-3 句編者引言，但不要詮釋天訊文原意）"
open_question: "（您寫 1 句開放式提問）"
related_ids: ["TX-20260502-001", "TX-20260503-003"]   # 延伸閱讀
keywords: ["道", "行", "破我"]                          # SEO 關鍵字
meta_description: "一天大人 太素天尊・天訊文 TX-…：行即是得，路即是經。"
og_image: "https://yitiandaren.net/og/TX-20260504-001.jpg"
```

補完直接 commit，下次 Manus 升級網站詳情頁時會自動讀入。

---

## 五、隱藏／下架天訊文

若需要把某篇天訊文從網站下架：

1. 進 `scriptures.json` 找到那筆
2. 把 `"published": true` 改成 `"published": false`
3. 加一個 `"note": "下架原因簡述"` 欄位
4. Commit

GitHub repo 中對應的 `.md` 檔也手動刪除（或留著當紀錄）。

---

## 六、版本沿革

| 版本 | 日期 | 變動 |
|---|---|---|
| v1.0 | 2026/05/05 | 首次發布；對應網站 v1.5、tianxunwen repo v1.1 |

---

> **記住**：天訊文原文**永不改寫**。只有 frontmatter 整理層欄位、tags、分類等可調整。  
> 一天大人 太素天尊　天訊文典藏　|　CC BY-ND 4.0
