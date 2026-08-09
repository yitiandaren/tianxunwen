# 一天大人 太素天尊・天訊文典藏

> 本倉庫保存一天大人太素天尊之天訊文核定版本，作為可追溯、可驗證、可由AI檢索的長期知識層。  
> 天訊文原文不得改寫；原始訊息、影音及證據檔由Google Drive保存，本倉庫保存結構化典藏版本。

## 一、權威定位

| 層級 | 工具 | 職責 |
|---|---|---|
| 原始證據 | Google Drive | WhatsApp、LINE、音訊、影片、原始檔 |
| 正式知識 | GitHub | 核定Markdown、Schema、索引、版本歷史 |
| 作業管理 | Notion | 任務、審核、決策、發布與成效 |

## 二、ID政策 v2.1

| 欄位 | 格式 | 用途 |
|---|---|---|
| `yts_id` | `YTS-TX-YYYYMMDDHHMMSS-001` | YTS正式主ID；新物件必建，既有資料分階段補入 |
| `tx_id` | `TX-YYYYMMDDHHMMSS` | 本倉庫穩定典藏ID、檔名及公開URL錨點 |
| `legacy_id` | `TX-YYYYMMDD-NNN` | 2026年6月遷移前ID，僅供追溯 |
| `old_id` | 依舊系統格式 | 網站或其他舊資料來源ID |

既有公開檔名不因導入YTS主ID而再次更名，避免破壞Git歷史、外部連結及引用。

## 三、目錄

```text
tianxunwen/
├── archive/                 # 天訊文結構化典藏
├── core/                    # 母Schema、分類、語意與工作流規格
├── schema/                  # 執行期Metadata規格
├── templates/               # 新物件模板
├── scripts/                 # 驗證、索引、稽核與同步
├── data/                    # 自動生成索引及報告
├── governance/              # 原典與協作治理
├── .github/workflows/       # 持續驗證與衍生資料重建
├── SCHEMA.md
└── CONTRIBUTING.md
```

天訊文檔名：

```text
archive/TX-YYYYMMDDHHMMSS.md
```

例如：

```text
archive/TX-20260404124430.md
```

## 四、現況

- ID遷移完成：177份典藏檔由舊流水號格式轉為14碼現示時間格式。
- 遷移對照：`data/id_mapping.json`。
- 正式驗證入口：`python scripts/validate_tx.py`。
- `data/tx_index.json`、`data/metadata_audit.json`及`id_mapping.csv`為自動生成資料，不得手動視為新的權威來源。
- YTS正式主ID為後續Metadata遷移欄位；原文內容不因ID治理而變動。

## 五、新增與修改流程

```text
原始來源確認
→ 建立分支
→ 使用TX模板
→ 只新增或修正Metadata
→ 執行驗證
→ 建立Pull Request
→ 行核准
→ 合併main
→ Actions重建索引與稽核報告
```

禁止直接改動`archive/`內的「天訊文原文」區塊。

## 六、驗證

```bash
python -m pip install pyyaml
python scripts/validate_tx.py
```

驗證項目包括：

- `tx_id`與檔名一致
- `tx_id`、`yts_id`、`legacy_id`格式
- `show_time`、`publish_code`與ID時間戳一致
- ID唯一性
- 必填欄位、陣列欄位、狀態與權限值

## 七、授權

本倉庫採CC BY-ND 4.0。可分享及引用，但必須保留來源，且不得改作天訊文原文。

## 八、版本

| 版本 | 日期 | 內容 |
|---|---|---|
| v1.0 | 2026-05-05 | 建立初版結構化典藏 |
| v2.0 | 2026-06-02 | 177份檔案遷移為14碼現示時間ID |
| v2.1 | 2026-08-06 | 對齊文件、Schema、模板、驗證器與CI；導入YTS主ID政策 |
