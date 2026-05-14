# Templates v1.0 YAML Validation Report

| File | YAML | source_type | canonical | domain | use | citation_allowed | reference_allowed |
|---|---|---|---|---|---|---|---|
| LS_template.md | OK | LS | True | T1 | A1 | False | True |
| TS_template.md | OK | TS | False | T1 | A1 | False | True |
| TX_template.md | OK | TX | True | T1 | A1 | True | True |
| EK_template.md | OK | EK | True | T1 | A1 | True | True |
| MN_template.md | OK | MN | True | T3 | A1 | True | True |
| PB_template.md | OK | PB | False | T1 | A4 | False | True |
| MA_template.md | OK | MA | False | T3 | A4 | False | True |

## Governance Checks

- Domain 欄位均使用 T1 或 T3 預設值，符合 T1-T10 規則。
- Use 欄位均使用 A1 或 A4 預設值，符合 A1-A7 規則。
- canonical 欄位：LS/TX/EK/MN=true；TS/PB/MA=false。
- TX/EK/MN 均包含 citation_allowed: true 與 reference_allowed: true。
- LS/TS/PB/MA 均採 citation_allowed: false 與 reference_allowed: true。
- PB 包含 citation_mode: hybrid。
- TS 包含 semantic_complete: true。
- MA 包含 derivative_type: music_adaptation。
- 七份模板均包含 created_by / created_at / updated_at。
