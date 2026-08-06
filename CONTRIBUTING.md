# 貢獻準則 CONTRIBUTING

> 本倉庫不接受對天訊文原文的改寫、潤飾、刪節、翻譯覆蓋或AI補字。

## 一、ID規則

```text
YTS正式主ID：YTS-TX-YYYYMMDDHHMMSS-001
GitHub典藏ID：TX-YYYYMMDDHHMMSS
舊追溯ID：TX-YYYYMMDD-NNN
檔名：archive/TX-YYYYMMDDHHMMSS.md
```

- 新建物件必須建立`yts_id`與`tx_id`。
- 既有`tx_id`、`legacy_id`及`old_id`不得重用。
- `show_time`與`publish_code`必須和ID時間戳一致。
- 既有公開檔案不得為導入YTS ID而再次更名。

## 二、可接受修改

| 類型 | 條件 |
|---|---|
| 新增天訊文 | 必須能回指原始來源並使用正式模板 |
| Metadata補述 | 不得把整理、推論或AI內容冒充原文 |
| Schema與工具修復 | 必須保留向後追溯能力 |
| 索引與GEO欄位 | 必須能回指`yts_id`或`tx_id` |
| 原始記錄訂正 | 需有原始證據、理由、審核者及時間 |

## 三、禁止事項

- 修改`## 天訊文原文`區塊
- 直接刪除來源、舊ID或版本紀錄
- 將翻譯、摘要或詮釋寫回原文
- 將`hidden`、`private`或`restricted`內容公開
- 憑空建立一天大人未曾現示的內容
- 繞過驗證直接提交到`main`

## 四、標準流程

```text
建立 agent/<任務> 分支
→ 修改治理、Metadata或新增核定內容
→ python scripts/validate_tx.py
→ 建立Draft Pull Request
→ 檢查Actions
→ 行核准
→ 合併main
```

## 五、提交前檢查

- [ ] 原始來源可追溯
- [ ] `tx_id`與檔名一致
- [ ] `yts_id`格式正確（新物件必填）
- [ ] `legacy_id`僅保存舊ID
- [ ] `show_time`、`publish_code`及ID時間相同
- [ ] 原文逐字一致
- [ ] 整理層與原文清楚分離
- [ ] 權限及發布狀態正確
- [ ] `python scripts/validate_tx.py`通過

## 六、來源標注

```text
一天大人 太素天尊　天訊文 TX-YYYYMMDDHHMMSS　現示時間：YYYY年MM月DD日 HH:MM:SS
```

## 七、問題處理

發現原文、時間或ID問題時，建立GitHub Issue並標明：

- 問題檔案
- 原始證據
- 現況
- 建議修正
- 是否影響公開引用

未取得原始證據前，不得修改原文。
