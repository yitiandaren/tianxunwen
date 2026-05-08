name: Migrate Governance v2

on:
  workflow_dispatch:

permissions:
  contents: write

jobs:
  migrate-governance-v2:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install pyyaml

      - name: Migrate governance v2
        run: python scripts/migrate_governance_v2.py

      - name: Build tx_index.json
        run: python scripts/build_index.py

      - name: Audit metadata
        run: python scripts/audit_metadata.py

      - name: Commit governance migration
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: auto migrate TX governance v2
          file_pattern: |
            archive/**/*.md
            data/tx_index.json
            data/metadata_audit.json
