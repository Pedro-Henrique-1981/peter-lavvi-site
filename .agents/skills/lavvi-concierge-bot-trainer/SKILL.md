---
name: lavvi-concierge-bot-trainer
description: >-
  Trains, grounds, audits, and tests Pedro Soares' Concierge chatbot and
  broker knowledge bases from official Lavvi Learning courses (41 modules across
  5 spaces), Lior Associados, lavvi.com.br, meunovvo.com.br, ABNT engineering
  rules, and sales vaults. Use whenever updating Concierge bot intelligence,
  ingesting new Lavvi Learning SCORM/LTI courses, or fixing stale/bloated bot
  answers.
---

# Lavvi Concierge & Sales Bot Training Pipeline

Follow this strict 5-step pipeline to train the on-site Concierge bot and internal broker assistant without hallucinations, walls of text, or internal data leaks.

## Step 1: Audit Existing Bot & Identify Stale Logic
1. Inspect the active Concierge handler (`site/assets/js/` or `site/index.html`) for hardcoded `if/else` facts, missing NOVVO/Lavvi products, verbose (>3 sentence) replies, or stale copy.
2. Cross-check against canonical project data (`site/lavvi_45_projects_clean.json` and `site/assets/js/lavvi_catalog_bundle.js`).

## Step 2: Harvest & Verify Official Sources (Raw JSON Only)
Use authenticated browser inspection (`Model: "flash"`) or official local PDFs to extract missing modules from the 5 `lavvi.learning.rocks` spaces:
- `spaces/191356` (**Trilha do Corretor de Sucesso** — e.g., `1769836 Descomplicando as vendas com IA`, Disney Way, Digital Consumer)
- `spaces/189758` (**Lançamento Lior** — Jardim da Hípica & T.O.M. Paraíso modules)
- `spaces/188982` (**Estoque Lior** — 11 active Lavvi projects + map)
- `spaces/189000` (**Produtos Nvendas** — Well Perdizes, Anália Franco, Vila Prudente, Novvo Santa Marina)
- `spaces/191640` (**Ferramentas** — MOBOX & Manual Corretor Lior)

**Mandatory Verification Gate:** Read raw `outputs/step_*.json` or `transcript_full.jsonl` verbatim before ingesting any spec, table, or URL. Never trust prose paraphrases.

## Step 3: Compile Air-Gapped Knowledge Packs
Split extracted intelligence into two clean tiers:
1. **Internal Broker Training KB (`briefings/` / `site/data/`):** Preserves granular SCORM objection handling, commission/MOBOX flows, Lior unit tables, RSM (`vaults/33_*`), UGREEN (`vaults/34_*`), and `jordan_engine_architecture.json`.
2. **Client-Safe Concierge Runtime (`site/assets/js/`):**
   - Strictly queries the 46-project canonical catalog dynamically.
   - Enforces **2–3 surgical sentences** per reply across all 6 languages (`PT/EN/FR/IT/ES/DE`).
   - Enforces zero internal URLs (`liorassociados`, `learning.rocks`, `skore.io`, `player.sapiencia.com.br`), zero internal agent codenames, zero fake CRECI, and exact Jardim da Hípica tennis specs (`02 Quadras de Tênis Oficiais (18x36m)`).

## Step 4: Adversarial Bot & Sentinel Verification
Run automated validation after every training update:
- `python scripts/cosimo_sentinel.py` (must exit 0)
- `python scripts/verify_bot_execution.py` (update target path if modularized; verify concise outputs, zero stale strings, accurate pricing & Airbnb HIS/HMP rules across all test prompts)
- `python tests/test_e2e_portal.py` (verify zero console errors and desktop/mobile chat UI parity)

## Step 5: Sync & Mirror
Update `AGENCY_SHARED_STATE.md` and run `python scripts/sync_hardware_state.py` to mirror updated training packs and skill changes to Google Drive (`G:\Meine Ablage\LAVVI\...`).
