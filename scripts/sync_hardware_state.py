# -*- coding: utf-8 -*-
r"""
Sincronizador Multi-Hardware Automatico (PC 1 Master <---> Google Drive <---> PC 2 Portatil ARM)
Uso:
  python scripts\sync_hardware_state.py          (Sincroniza bidirecionalmente pelo arquivo mais recente)
  python scripts\sync_hardware_state.py --push   (Forca envio do estado deste PC para o Google Drive)
  python scripts\sync_hardware_state.py --pull   (Forca puxada do Google Drive para este PC)
"""
import os
import sys
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
DRIVE_ROOT = Path(r"G:\Meine Ablage\LAVVI")
PC_NAME = os.environ.get("COMPUTERNAME", "PC-LAVVI")

CORE_FILES = [
    ("AGENCY_SHARED_STATE.md", "AGENCY_SHARED_STATE.md"),
    ("GEMINI.md", "GEMINI.md"),
    ("briefings/LAVVI_OFFICIAL_SPECS_TRUTH.md", "LAVVI_OFFICIAL_SPECS_TRUTH.md"),
    ("site/index.html", "site/index.html"),
    ("site/lavvi_45_projects_clean.json", "site/lavvi_45_projects_clean.json"),
    ("site/assets/js/lavvi_catalog_bundle.js", "site/assets/js/lavvi_catalog_bundle.js"),
    ("site/data/lavvi_learning_41_courses_kb.json", "site/data/lavvi_learning_41_courses_kb.json"),
    (".agents/skills/lavvi-concierge-bot-trainer/SKILL.md", ".agents/skills/lavvi-concierge-bot-trainer/SKILL.md"),
    ("site/mobile_hub.html", "site/mobile_hub.html"),
    ("site/relocation_matcher.html", "site/relocation_matcher.html"),
    ("site/copilot_whatsapp.html", "site/copilot_whatsapp.html"),
    ("scripts/sync_hardware_state.py", "scripts/sync_hardware_state.py"),
]


def sync_file(local_rel: str, drive_rel: str, mode: str = "auto"):
    local_p = BASE_DIR / local_rel
    drive_p = DRIVE_ROOT / drive_rel
    drive_p.parent.mkdir(parents=True, exist_ok=True)
    local_p.parent.mkdir(parents=True, exist_ok=True)

    if mode == "push" or (local_p.exists() and not drive_p.exists()):
        if local_p.exists():
            shutil.copy2(local_p, drive_p)
            print(f"  [PUSH -> DRIVE] {local_rel}")
        return

    if mode == "pull" or (drive_p.exists() and not local_p.exists()):
        if drive_p.exists():
            shutil.copy2(drive_p, local_p)
            print(f"  [PULL <- DRIVE] {local_rel}")
        return

    if local_p.exists() and drive_p.exists():
        l_mtime = local_p.stat().st_mtime
        d_mtime = drive_p.stat().st_mtime
        if abs(l_mtime - d_mtime) < 2.0:
            print(f"  [EM DIA]        {local_rel}")
        elif l_mtime > d_mtime:
            shutil.copy2(local_p, drive_p)
            print(f"  [PUSH -> DRIVE] {local_rel} (local mais recente)")
        else:
            shutil.copy2(drive_p, local_p)
            print(f"  [PULL <- DRIVE] {local_rel} (Drive mais recente)")


def main():
    mode = "auto"
    if "--push" in sys.argv:
        mode = "push"
    elif "--pull" in sys.argv:
        mode = "pull"

    print("=" * 72)
    print(f"[SYNC] LAVVI MULTI-HARDWARE SYNC | Maquina: {PC_NAME} | Modo: {mode.upper()}")
    print("=" * 72)

    if not DRIVE_ROOT.exists():
        print("[AVISO] Google Drive (G:\\Meine Ablage\\LAVVI) nao montado ou bloqueado pelo Sandbox.")
        sys.exit(1)

    for local_rel, drive_rel in CORE_FILES:
        sync_file(local_rel, drive_rel, mode)

    # Git pull no repositorio mobile se existir
    mobile_repo = BASE_DIR / "scratch_audit" / "lavvi-mobile"
    if (mobile_repo / ".git").exists():
        try:
            subprocess.run(["git", "-C", str(mobile_repo), "pull", "--rebase", "origin", "main"], check=False)
        except Exception as e:
            print(f"  [GIT INFO] {e}")

    print("-" * 72)
    print(f"[OK] Sincronizacao concluida em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ({PC_NAME})")


if __name__ == "__main__":
    main()
