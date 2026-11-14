# AGÊNCIA LAVVI — MEMÓRIA UNIFICADA MULTI-COMPUTADOR (VITO & BOARDROOM)
> **Última Atualização:** 13/11/2026 - 21:49 (Horário de Brasília)
> **Último Hardware Ativo:** `PedroRadeon6700` (PC 1 • Home Master GPU)
> **Sincronização Ativa:** PC 1 Master (GPU Casa) <---> Google Drive (`G:\Meine Ablage\LAVVI`) <---> PC 2 Portátil (ARM) <---> Celular Samsung

---

## 0. REGRA 0.0 — PROTOCOLO DE HANDOFF MULTI-HARDWARE AUTOMÁTICO:
1. **Ao abrir o agente em um PC diferente (Boot):**
   - Pela Regra `0.0` do `GEMINI.md`, o agente lê automaticamente `G:\Meine Ablage\LAVVI\AGENCY_SHARED_STATE.md` e roda `python scripts\sync_hardware_state.py` antes de responder à primeira mensagem.
   - Se Pedro quiser forçar no terminal com 1 palavra, basta digitar: **`sync`** (ou dizer no chat: *"Vito, sync"*).
2. **Ao terminar qualquer tarefa em um PC (Fechamento):**
   - O agente atualiza este arquivo (`AGENCY_SHARED_STATE.md`) e roda `python scripts\sync_hardware_state.py --push` para deixar o Google Drive e o GitHub Pages 100% prontos para o outro PC.

---

## 1. PROTOCOLO AUTOMÁTICO "SUBI NO DRIVE" (GRUPO DO MICHEL -> BASE OFICIAL):
Sempre que Pedro disser **"subi no Drive"** (ou *"atualizei o grupo do Michel"*), o agente DEVE executar imediatamente sem fazer perguntas:
1. **Pasta de Origem no Google Drive:** `G:\Meine Ablage\WhatsApp` (pacotes ZIP exportados do WhatsApp, mesmo quando sem extensão `.zip`).
2. **Comando Único de Execução:**
   ```powershell
   python scripts\sync_michel_drive_pipeline.py
   ```
3. **O que esse pipeline faz sozinho:**
   - Copia apenas os arquivos novos/modificados de `G:\Meine Ablage\WhatsApp` para `scratch_audit\whatsapp_michel_dump\`.
   - Roda `scripts/scan_michel_whatsapp_by_project.py` e `scripts/extract_november_2026_michel_tables.py`.
   - Atualiza a Arena do Bot (`lab/lab_bot_arena.html`) e o Auditor por Produto (`lab/lab_michel_auditor.html`), passa pelo `scripts/cosimo_sentinel.py` e faz push para `https://pedro-henrique-1981.github.io/lavvi-mobile/`.

---

## 2. O QUE ESTÁ NO AR HOJE (12/11/2026 • Overhaul 46 Projetos + Bot Trainer):
1. **Portal Oficial Lavvi & Meu Novvo Unificado (Paridade Visual `lavvi.com.br` + `meunovvo.com.br`):**
   - **Catálogo 46 Empreendimentos (`site/index.html` + `site/lavvi_45_projects_clean.json` + `site/assets/js/lavvi_catalog_bundle.js`):** 17 Lavvi Ativos + 22 Lavvi 100% Vendidos + 7 Meu Novvo Ativos (incluindo *Novvo Largo Treze*), 100% de fotos hero verificadas, 9 vídeos YouTube oficiais, 8 Tours 360° (`tour.lavvi.com.br`) e 14 plantas S3.
   - **Ferramentas Dedicadas Modulares:** `site/cinema_lavvi.html` (48 vídeos), `site/radar_mapa.html` (46 projetos + 56 POIs), `site/credito_imobiliario.html` (12 bancos SAC/PRICE + 35/65 vs CDI), `site/guias_bairros.html` (8 bairros nobres).
   - **Concierge Bot Treinado (`site/data/lavvi_learning_41_courses_kb.json` + `.agents/skills/lavvi-concierge-bot-trainer/SKILL.md`):** Respostas cirúrgicas de 2 a 3 frases em 6 idiomas sobre todos os 46 projetos, ABNT NBR 15.575, alvenaria estrutural vs concreto armado e Airbnb R2V vs vedação HIS/HMP (`133/133` testes E2E + `verify_bot_execution.py` + `cosimo_sentinel.py` 100% PASS).
2. **Peter Mobile Cockpit (24/7 na Nuvem):**
   - **Hub Principal:** `https://pedro-henrique-1981.github.io/lavvi-mobile/mobile_hub.html` (corrigido espaçamento `tools-grid` no bloco Sandbox).
   - **Comparador de Bairros 2D Instantâneo:** `https://pedro-henrique-1981.github.io/lavvi-mobile/relocation_matcher.html` (substituiu o antigo 3D pesado, arquivado em `lab/lab_relocation_3d_legacy.html`).
   - **Copilot WhatsApp (46 Projetos + Tabelas Nov `26.11` + FAQ R01):** `https://pedro-henrique-1981.github.io/lavvi-mobile/copilot_whatsapp.html`.
   - **Máquina de Follow-up & Vitrine 90 Dias (Airton Lavirri In-House):** `https://pedro-henrique-1981.github.io/lavvi-mobile/lab/lab_followup_machine.html`.
   - **Dia A — Painel Grupo do Michel por Produto (15.587 msgs + 270 PDFs + 27 Tabelas `26.11` Nov/2026):** `https://pedro-henrique-1981.github.io/lavvi-mobile/lab/lab_michel_auditor.html`.
   - **Dia B — Arena Omnichannel do Bot (30 Perguntas Difíceis em WhatsApp/Telegram/E-mail):** `https://pedro-henrique-1981.github.io/lavvi-mobile/lab/lab_bot_arena.html`.

2. **Canal Push de Comunicação Móvel (`ntfy`):**
   - **Tópico Ativo:** `https://ntfy.sh/lavvi-3be8151a106beace199f`
   - **Ritual Diário Agendado:** Todo dia às **18h30** cai um push cobrando 15 minutos de calibração (alternando Dia A e Dia B).

3. **Quarentena Solarium:**
   - Todos os arquivos do Solarium permanecem isolados (sem apagar) em `_LIXEIRA_SOLARIUM` (local e no Drive) com manifesto CSV reversível.

4. **Regra Anti-Sobrecarga:**
   - Sempre responder indicando: **ONDE OLHAR**, **O QUE PROCURAR (em negrito)** e **O QUE FAZER (1 ação)**.

---

## 3. ATUALIZAÇÃO RECENTE (13/11/2026 • Correção de Imagens no Mapa Interativo & Catálogo):
- **Modais de Mapa & Hub (`site/index.html`, `site/assets/js/portal_map_engine.js`, `site/radar_mapa.html`):** Overlay (`#map-pin-modal-overlay`) passa a abrir antes da atribuição de `imgEl.src`, com `loading="lazy"` removido dinamicamente e fallback automático `onerror` para `assets/hipica_piscina60m.jpg`.
- **Pinos de Mercado & Clusters (`MARKET_COMPETITORS` & `CLUSTER_HERO_IMAGES`):** Todos os 12 concorrentes e 8 clusters/POIs nos mapas interativos atualizados para renders locais verificados sob `site/assets/`.
- **Catálogo 46 Projetos (`site/lavvi_45_projects_clean.json`, `site/assets/js/lavvi_catalog_bundle.js` e `FALLBACK_GEO_PROJECTS` em `site/radar_mapa.html`):** Removidas 100% das URLs antigas `s3.us-east-1.amazonaws.com` e atualizados 19 empreendimentos (incluindo *Well Perdizes*, *Palace*, *Jardim da Hípica*, *T.O.M. Paraíso*, *Villa Residence/Studios*, *Petra*, *Alive*, *Heaven*, *Grand Square*, *Green View*, *Studios Elie Saab* e *High Wonder*) para renders locais autenticados em disco (`49/49` presentes).
- **Validação Executada:** `test_portal_map_e2e.py` (`26/26 PASS`), `test_e2e_portal.py` (`133/133 PASS`) e `cosimo_sentinel.py` (exit `0`).
