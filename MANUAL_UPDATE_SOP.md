# 天訊文人工更新SOP v2.1

## 一、目的

以最少人工操作，完成可追溯、可驗證、可由AI理解的天訊文典藏更新。  
本SOP只處理核定資料與Metadata，不允許改寫一天大人原文。

## 二、角色

- **行**：提供原始內容、確認公開權限、核准最終版本。
- **智**：建立ID、整理Metadata、執行驗證、建立PR、更新索引。

## 三、準備資料

```yaml
原始內容:
現示時間:
來源平台:
發送者:
上下文:
公開權限:
行的核准:
```

缺少現示秒數、原始內容或公開權限時，不建立正式公開物件。

## 四、建立ID

假設現示時間是2026-04-04 12:44:30：

```text
yts_id: YTS-TX-20260404124430-001
tx_id: TX-20260404124430
檔名: archive/TX-20260404124430.md
publish_code: 20260404124430
```

若存在遷移前ID，另存：

```text
legacy_id: TX-20260404-003
```

若存在網站舊ID，另存於`old_id`。

## 五、更新流程

1. 從`main`建立`agent/<任務名稱>`分支。
2. 複製`templates/TEMPLATE_20260514_TX_TianXun_天訊文_v1_0.md`。
3. 填入ID、現示時間、來源、分類、權限及審核欄位。
4. 將一天大人原文逐字放入`## 天訊文原文`。
5. 不在原文內加入摘要、解說、翻譯或AI內容。
6. 執行：
   ```bash
   python -m pip install pyyaml
   python scripts/validate_tx.py
   ```
7. 建立Draft Pull Request。
8. 行核准後才合併`main`。
9. GitHub Actions自動重建索引及Metadata稽核。

## 六、現有資料修正

### 允許直接修正

- 分類、標籤、關鍵詞
- `editor_intro`
- `open_question`
- `related_ids`
- `meta_description`
- 發布平台、權限及審核欄位

### 必須有證據及審核

- `show_time`
- `tx_id`
- `yts_id`
- `legacy_id`
- 原文任何字元

### 不得執行

- 刪除原始證據
- 為了SEO改寫原文
- 把AI推論當成一天大人原意
- 直接Commit到`main`
- 以Notion或社群版本覆蓋GitHub正式版本

## 七、網站與平台發布

發布內容必須回指GitHub正式版本。網站、Facebook、YouTube、Medium及其他平台只能：

- 完整轉載原文
- 明確標示節錄
- 建立與原文分離的解說或應用內容

不得把衍生文案寫成一天大人原文。

## 八、異常處理

| 異常 | 處理 |
|---|---|
| 同一秒有多筆來源 | 暫停建檔，人工確認SEQ及上下文 |
| 缺少現示秒數 | 保留RAW，不建立正式TX |
| 新舊ID衝突 | 查`data/id_mapping.json`，不得自行重編 |
| 驗證失敗 | 不得合併，先修正Metadata或Schema |
| 原文有疑義 | 標記`REVIEW_REQUIRED`並查原始來源 |
| 權限不明 | 預設不公開 |

## 九、完成標準

- 原始來源存在
- ID可追溯且唯一
- 原文逐字一致
- 權限明確
- 驗證通過
- 行已核准
- PR及Commit歷史完整
