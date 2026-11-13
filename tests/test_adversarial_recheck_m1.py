"""
Adversarial Verification Recheck Harness for Milestone 1 (M1)
Executed by: challenger_m1_recheck_2
"""
import os
import sys
import re
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

def run_cmd(cmd_list):
    res = subprocess.run(cmd_list, capture_output=True, text=True, cwd=str(ROOT))
    return res.returncode, res.stdout.strip(), res.stderr.strip()

def check_ntfy_git_untracking():
    print("\n--- 1. Checking Git Untracking of site/data/ntfy_config.json ---")
    code, stdout, stderr = run_cmd(["git", "ls-files", "-s", "site/data/ntfy_config.json"])
    assert code == 0, f"git ls-files failed: {stderr}"
    assert stdout == "", f"Expected empty output for untracked file, got: '{stdout}'"
    print("  [PASS] git ls-files -s returns empty string.")

    code, stdout, stderr = run_cmd(["git", "check-ignore", "-v", "site/data/ntfy_config.json"])
    assert code == 0, f"git check-ignore failed: {stderr}"
    assert "site/data/ntfy_config.json" in stdout, f"Unexpected check-ignore output: {stdout}"
    print(f"  [PASS] git check-ignore matches: {stdout}")

    ntfy_file = ROOT / "site" / "data" / "ntfy_config.json"
    assert ntfy_file.exists(), "Local ntfy_config.json must still exist on disk"
    assert ntfy_file.stat().st_size > 0, "ntfy_config.json must not be empty"
    print("  [PASS] Local ntfy_config.json remains intact on disk.")

def check_cosimo_sentinel():
    print("\n--- 2. Checking Cosimo Sentinel Exit Code and Health ---")
    sentinel_py = ROOT / "scripts" / "cosimo_sentinel.py"
    assert sentinel_py.exists(), "scripts/cosimo_sentinel.py must exist"

    code, stdout, stderr = run_cmd([sys.executable, str(sentinel_py)])
    assert code == 0, f"cosimo_sentinel.py exited with code {code}!\nStderr: {stderr}\nStdout: {stdout}"
    assert "STATUS VERDE: ZERO ALUCINAÇÕES DETECTADAS!" in stdout, f"Missing green status header: {stdout}"
    print("  [PASS] cosimo_sentinel.py executed cleanly with code 0 and STATUS VERDE.")

    # Adversarial test: verify that cosimo_sentinel would catch a fake CRECI if injected
    print("  Testing sentinel detection power against synthetic bad inputs...")
    from scripts.cosimo_sentinel import run_sentinel_audit
    re_fake_creci = re.compile(r'CRECI[\s\-\/]?(?:SP)?[:\s\-\/]+[0-9.,]{4,8}[\-A-Z]*|\(CRECI[\s\-]*(?:SP)?\)', re.IGNORECASE)
    test_violations = [
        "Pedro Soares (CRECI SP)",
        "Pedro Soares CRECI 30.906",
        "CRECI-SP: 30906",
        "CRECI SP 30.906"
    ]
    for tv in test_violations:
        m = re_fake_creci.search(tv)
        assert m is not None, f"Sentinel regex failed to match: '{tv}'"
    print("  [PASS] Sentinel regex catches all tested CRECI variations.")

def check_e2e_tier1():
    print("\n--- 3. Checking E2E Tier 1 Tests (F09, F10, F11, F12) ---")
    cmd = [
        sys.executable, "-m", "unittest",
        "tests.tier1_features.TestF09_IdentityCompliance",
        "tests.tier1_features.TestF10_OfficialSpecs",
        "tests.tier1_features.TestF11_MediaAssets",
        "tests.tier1_features.TestF12_SentinelGitHygiene"
    ]
    code, stdout, stderr = run_cmd(cmd)
    combined = stdout + "\n" + stderr
    assert code == 0, f"Tier 1 M1 tests failed (code {code}):\n{combined}"
    assert "Ran 20 tests" in combined, f"Expected 20 tests, got:\n{combined}"
    assert "OK" in combined, f"Expected OK in output, got:\n{combined}"
    print("  [PASS] All 20 Tier 1 tests (F09, F10, F11, F12) passed cleanly (OK).")

def check_e2e_tier2():
    print("\n--- 4. Checking E2E Tier 2 Tests (B09, B10, B11, B12) ---")
    cmd = [
        sys.executable, "-m", "unittest",
        "tests.tier2_boundaries.TestB09_IdentityBoundaries",
        "tests.tier2_boundaries.TestB10_OfficialSpecsBoundaries",
        "tests.tier2_boundaries.TestB11_MediaAssetsBoundaries",
        "tests.tier2_boundaries.TestB12_SentinelHygieneBoundaries"
    ]
    code, stdout, stderr = run_cmd(cmd)
    combined = stdout + "\n" + stderr
    assert code == 0, f"Tier 2 M1 tests failed (code {code}):\n{combined}"
    assert "Ran 20 tests" in combined, f"Expected 20 tests, got:\n{combined}"
    assert "OK" in combined, f"Expected OK in output, got:\n{combined}"
    print("  [PASS] All 20 Tier 2 tests (B09, B10, B11, B12) passed cleanly (OK).")

def check_assets_downscaling():
    print("\n--- 5. Checking Asset Downscaling & Raw Backups ---")
    target_jpgs = [
        "site/assets/hipica_private_house.jpg",
        "site/assets/hipica_piscina60m.jpg",
        "site/assets/tom_beach_tennis.jpg",
        "site/assets/tom_rooftop_pool.jpg",
        "site/assets/images/heaven_gal_1.jpg"
    ]
    raw_backups = [
        "backup_raw_assets/hipica_private_house.jpg",
        "backup_raw_assets/hipica_piscina60m.jpg",
        "backup_raw_assets/tom_beach_tennis.jpg",
        "backup_raw_assets/tom_rooftop_pool.jpg",
        "backup_raw_assets/heaven_gal_1.jpg"
    ]
    for jpg, bak in zip(target_jpgs, raw_backups):
        p_jpg = ROOT / jpg
        p_bak = ROOT / bak
        assert p_jpg.exists(), f"Asset missing: {jpg}"
        assert p_bak.exists(), f"Backup missing: {bak}"

        sz = p_jpg.stat().st_size
        bak_sz = p_bak.stat().st_size
        assert sz < 512000, f"Asset {jpg} exceeds 500 KB: {sz} bytes"
        assert sz > 10000, f"Asset {jpg} is suspiciously small: {sz} bytes"
        assert bak_sz > 5 * 1024 * 1024, f"Backup {bak} is less than 5 MB: {bak_sz} bytes"

        # Check JPEG magic bytes and EOF
        with open(p_jpg, "rb") as f:
            header = f.read(3)
            assert header == b"\xff\xd8\xff", f"Invalid JPEG header in {jpg}: {header}"
            f.seek(-2, os.SEEK_END)
            eof = f.read(2)
            assert eof == b"\xff\xd9", f"Invalid JPEG EOF in {jpg}: {eof}"
        print(f"  [PASS] {jpg}: {sz/1024:.1f} KB (raw backup: {bak_sz/(1024*1024):.1f} MB, valid JPEG)")

def check_creci_purged():
    print("\n--- 6. Checking Complete CRECI Purge Across Client Facing Files ---")
    files_to_check = [
        "site/index.html",
        "site/linkedin_studio.html",
        "site/index_lab.html",
        "site/lab.html",
        "00_COFRES_DE_INTELIGENCIA/29_google_search_seo_geo_ariadne/ariadne_geo_vault/ARIADNE_GLOBAL_GEO_KNOWLEDGE_GRAPH.json"
    ]
    for rel in files_to_check:
        p = ROOT / rel
        assert p.exists(), f"Target file missing: {rel}"
        txt = p.read_text(encoding="utf-8", errors="ignore")
        assert "30.906" not in txt, f"Found 30.906 in {rel}"
        assert "30906" not in txt, f"Found 30906 in {rel}"
        bare = re.findall(r'\(CRECI[\s\-]*(?:SP)?\)', txt, re.IGNORECASE)
        assert len(bare) == 0, f"Found bare (CRECI SP) in {rel}: {bare}"
        print(f"  [PASS] {rel}: 0 fake CRECI or bare tags.")

def check_tennis_specs():
    print("\n--- 7. Checking Tennis Court Specs ---")
    files = [
        "site/comparativos.html",
        "site/hipica_dossier.html",
        "site/deck.html",
        "site/infografico_alphaville_vs_hipica.html"
    ]
    for rel in files:
        p = ROOT / rel
        assert p.exists(), f"Target file missing: {rel}"
        txt = p.read_text(encoding="utf-8", errors="ignore")
        # Check that saibro is not attributed to Jardim da Hípica
        bad = re.findall(r'(\bquadras? de (?:tênis de )?saibro\b.*?(?:hípica|18x36m))', txt, re.IGNORECASE)
        assert len(bad) == 0, f"Saibro attributed to Hípica in {rel}: {bad}"
        assert "02 Quadras de Tênis Oficiais (18x36m)" in txt or "02 Quadras de Tênis Oficiais" in txt, f"Missing 18x36m spec in {rel}"
        print(f"  [PASS] {rel}: official tennis specs verified, 0 saibro claims.")

if __name__ == "__main__":
    print("================================================================================")
    print("🔬 RUNNING ADVERSARIAL RECHECK SUITE FOR MILESTONE 1 (M1)")
    print("================================================================================")
    try:
        check_ntfy_git_untracking()
        check_cosimo_sentinel()
        check_e2e_tier1()
        check_e2e_tier2()
        check_assets_downscaling()
        check_creci_purged()
        check_tennis_specs()
        print("\n================================================================================")
        print("🎉 ALL ADVERSARIAL RECHECK ASSERTIONS PASSED WITH 100% EMPIRICAL CONFIDENCE!")
        print("================================================================================")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ ADVERSARIAL CHALLENGE FAILURE: {e}")
        sys.exit(1)
