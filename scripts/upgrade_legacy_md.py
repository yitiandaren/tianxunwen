"""Deprecated legacy migration entry point.

The repository completed the TX ID migration on 2026-06-02. Running the former
script would recreate the retired TX-YYYYMMDD-NNN convention and can break
filename, metadata, URL, and index consistency.

Use data/id_mapping.json for historical lookup. New records must be created from
templates/TEMPLATE_20260514_TX_TianXun_天訊文_v1_0.md and validated with
scripts/validate_tx.py.
"""

import sys

MESSAGE = """
此遷移腳本已停用。

原因：177份天訊文已完成 TX-YYYYMMDD-NNN → TX-YYYYMMDDHHMMSS 遷移。

請改用：
1. data/id_mapping.json：查詢新舊ID對照
2. templates/TEMPLATE_20260514_TX_TianXun_天訊文_v1_0.md：建立新物件
3. python scripts/validate_tx.py：驗證一致性

若需再次執行批次遷移，必須另建專案腳本、分支、備份與人工審核，
不得直接恢復本歷史腳本。
""".strip()

print(MESSAGE, file=sys.stderr)
sys.exit(2)
