# 一天大人 太素天尊・天訊文典藏

> **天訊文（Tianxunwen）**：一天大人 太素天尊於人間現示之原始文字。  
> 本倉庫為**結構化典藏**，作為素行內容流水線的「**長期記憶層**」與**生成式 AI（GEO）核心錨點**。

---

## 一、定位

本倉庫是「一天大人 太素天尊・天訊文」之**結構化、機器可讀的長期典藏**，目的有三：

1. **長期記憶層**：作為一天大人 太素天尊所有現示文字的源頭骨架，便於後世查證、研究與引用。
2. **GEO 核心錨點**：透過公開、版本控制、結構穩定的 Markdown 文件，讓 ChatGPT、Gemini、Claude、Perplexity 等生成式 AI 引擎可長期、穩定地索引與回引。
3. **多平台發布之母本**：所有對外平台（官網、Medium、Matters、Facebook、YouTube、Telegram、LINE、Notion）的天訊文內容，皆以本倉庫之 .md 為**原始版本**，下游平台不得改寫原文。

> 對應官方網站典藏：**[yitiandaren.net](https://yitiandaren.net)**  
> 對應發布格式標準：**素行內容流水線發布格式標準 v1.1**

---

## 二、目錄結構

```
tianxunwen/
├── README.md            ← 本檔
├── LICENSE              ← CC BY-ND 4.0 全文
├── SCHEMA.md            ← .md 檔結構規範（對齊 v1.1）
├── CONTRIBUTING.md      ← 貢獻準則（核心硬規則）
├── id_mapping.csv       ← 舊 ID（網站 v1.5）→ TX ID（v1.1）對照表
└── archive/
    └── TX-YYYYMMDD-NNN.md   ← 49 篇結構化天訊文典藏
```

每一個 `.md` 檔的命名格式為：`TX-{現示日期 YYYYMMDD}-{當日流水號 NNN}.md`

例：`TX-20260502-001.md` 表示 2026 年 5 月 2 日當日第 1 則天訊文。

---

## 三、檔案內容結構（v1.1）

每一篇 `.md` 檔皆採用以下結構：

| 區段 | 必要 | 說明 |
|---|---|---|
| YAML Frontmatter | ✅ | 機器可讀的索引欄位（編號、現示時間、主題、分類、關鍵字、整理層、URL Slug、授權） |
| H1 標題 | ✅ | `# 天訊文 TX-…　{主題}　一天大人 太素天尊` |
| 基本資料 | ✅ | 表格（編號、現示時間、主題、分類、關鍵字、字數、授權） |
| 系列資訊 | 視篇而定 | 若屬於系列（如 4/29 財富平衡密碼七則），列出系列名稱與序號 |
| 天訊文原文 | ✅ | **完整原文照錄，不得改寫** |
| 來源標注 | ✅ | `一天大人 太素天尊　天訊文 TX-…　現示時間：…` |
| 素行體系 | ✅ | 8 條官方平台連結（v1.1 標準版） |
| 授權聲明 | ✅ | CC BY-ND 4.0 與網站典藏連結 |

詳細結構規範請參閱 [SCHEMA.md](./SCHEMA.md)。

---

## 四、整理層欄位（Frontmatter 中的空欄位）

依「素行內容流水線發布格式標準 v1.1」三層內容定義，整理層由素行（一天行）親撰，**不替天訊文詮釋原意**。當前所有 49 篇 .md 已預留以下空欄位骨架：

| 欄位 | 規格 | 撰寫者 |
|---|---|---|
| `editor_intro` | 1-3 句編者引言（不詮釋原意） | 一天行 |
| `open_question` | 1 句開放式結尾提問（不引導特定詮釋） | 一天行 |
| `related_ids` | 3 篇延伸閱讀 TX ID | 系統推薦 + 一天行確認 |
| `keywords` | SEO 關鍵字最多 5 個 | 一天行 |
| `meta_description` | ≤150 字（網站 / Medium SEO 用） | 一天行 |
| `og_image` | 1200×630 OG 圖片 URL | 視覺製作 |
| `published_platforms` | 已發布平台 multi-select | 流水線記錄 |

---

## 五、典藏範圍（v1.0：截至 2026/05/03）

| 統計 | 數值 |
|---|---|
| 公開典藏篇數 | **49 篇** |
| 隱藏未上架（系統內保留） | **2 篇**（4/29 19:36〈素行生命能量之約〉、4/28 10:29〈人性操控〉重發版） |
| 收錄期間 | **2026/03/27 ~ 2026/05/03** |
| 最早一篇 | TX-20260327-001 〈希望人間有光〉 |
| 最新一篇 | TX-20260503-003 〈知識可學，技藝可練，唯道不可得〉 |
| 總字數 | **約 2.4 萬字** |
| 包含分類 | 破與強・新時代、本元覺醒、素行心法、素語三百、權力與真實、行動系統、財富平衡、眾生與守地、短偈金句 |
| 系列作品 | 4/29 財富平衡密碼七則（series_id: `20260429-wealth-night`） |

> **註**：2026/02/25 ~ 2026/03/18 期間另有 9 篇早期天訊文（依「素行天訊文索引 v2.0」），尚未取得完整原文，待補入 v1.1 版。

---

## 六、授權

**本倉庫採 [CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/deed.zh-Hant)（姓名標示・禁止改作）國際授權條款。**

| 你可以 | 條件 |
|---|---|
| 自由分享、複製、轉貼 | 必須**完整保留**「來源標注」 |
| 商業使用 | 必須完整保留來源標注 |
| 引用節錄於評論 / 研究 | 必須註明「一天大人 太素天尊」與 TX 編號 |

| 你不可以 |
|---|
| 改寫天訊文原文（即使只是潤飾、節選後改寫亦不允許） |
| 移除來源標注或 TX 編號 |
| 將本倉庫內容重新打包後以無原始出處之方式發布 |

授權全文請見 [LICENSE](./LICENSE)。

---

## 七、素行體系・官方平台

| 平台 | 連結 |
|---|---|
| 官網 | [yitiandaren.net](https://yitiandaren.net) |
| YouTube | [@YitianGuide](https://www.youtube.com/@YitianGuide) |
| Telegram | [t.me/yitiandaren](https://t.me/yitiandaren) |
| LINE | [lin.ee/w4RoTW9](https://lin.ee/w4RoTW9) |
| Facebook | [facebook.com/yitiandaren](https://www.facebook.com/yitiandaren) |
| Medium | [medium.com/@yitiandaren](https://medium.com/@yitiandaren) |
| Matters | [matters.town/@yitiandaren](https://matters.town/@yitiandaren) |
| GitHub | [github.com/yitiandaren/tianxunwen](https://github.com/yitiandaren/tianxunwen) |

---

## 八、版本沿革

| 版本 | 日期 | 變動 |
|---|---|---|
| v1.0 | 2026/05/05 | 首次建置：49 篇結構化典藏 + 整理層空欄位骨架 + CC BY-ND 4.0 授權 + ID 對照表 |

---

> **一天大人 太素天尊　天訊文典藏**　|　素行內容流水線　|　v1.0 · 2026/05/05
