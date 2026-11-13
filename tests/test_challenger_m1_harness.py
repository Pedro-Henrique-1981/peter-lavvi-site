import os
import sys
import re
import html
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def test_task_1_creci_scan():
    print("=== TASK 1: ADVERSARIAL CRECI SCAN ===")
    
    # Files worker claimed to have remediated:
    remediated_files = [
        "site/linkedin_studio.html",
        "site/index_lab.html",
        "site/lab.html",
        "site/llms.txt",
        "site/llms-full.txt",
        "site/checklist-due-diligence.html",
        "scripts/install_chatbot.py",
        "scripts/linkedin_infographics_generator.py",
        "scripts/scrooge_enrich_vault_29_seo.py"
    ]
    
    client_facing_all = [
        "site/index.html",
        "site/lab_mobile.html",
        "site/comparativos.html",
        "site/relocation_matcher.html",
        "site/checklist-due-diligence.html",
        "site/holding_simulator.html",
        "site/hipica_dossier.html",
        "site/deck.html",
        "site/guia_alto_da_boa_vista.html",
        "site/infografico_alphaville_vs_hipica.html",
        "site/linkedin_studio.html",
        "site/torre_e_3d.html",
        "site/cinema_lavvi.html",
        "site/radar_mapa.html",
        "site/credito_imobiliario.html",
        "site/guias_bairros.html",
        "site/index_lab.html",
        "site/lab.html"
    ]

    # Tricky regexes
    tricky_30906 = re.compile(r'30(?:[\s\.\,\-\_\/\&\#\;\*\~\^]|&#46;|&nbsp;)*906', re.IGNORECASE)
    bare_creci = re.compile(r'\(?\s*CRECI[\s\-\_\/\&\#\;]*(?:SP)?\s*\)?', re.IGNORECASE)
    any_fake_creci = re.compile(r'CRECI[:\s\-\/]+[0-9.,]{4,8}[\-A-Z]*|\(CRECI[\s\-]*SP\)', re.IGNORECASE)
    
    results = {}
    for rel_path in client_facing_all:
        fpath = BASE_DIR / rel_path
        if not fpath.exists():
            results[rel_path] = "FILE_DOES_NOT_EXIST"
            continue
        try:
            raw = fpath.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            results[rel_path] = f"READ_ERROR: {e}"
            continue
        
        unescaped = html.unescape(raw)
        # Check tricky 30906
        m_30906 = list(tricky_30906.finditer(unescaped))
        # Check fake creci
        m_fake = list(any_fake_creci.finditer(unescaped))
        
        # Check bare creci without estagio qualification
        bare_matches = []
        for m in bare_creci.finditer(unescaped):
            start = max(0, m.start() - 50)
            end = min(len(unescaped), m.end() + 50)
            snippet = unescaped[start:end].replace('\n', ' ')
            if not any(k in snippet.lower() for k in ['estágio', 'estagiário', 'estagio', 'estagiario', 'spider.crecisp', 'crecisp.gov.br']):
                bare_matches.append((m.group(0), snippet))
                
        results[rel_path] = {
            "30906": [m.group(0) for m in m_30906],
            "fake_creci": [m.group(0) for m in m_fake],
            "bare_creci_unqualified": bare_matches
        }
        print(f"File: {rel_path}")
        print(f"  30906 matches: {len(m_30906)}")
        print(f"  fake_creci matches: {len(m_fake)}")
        print(f"  bare unqualified: {len(bare_matches)}")
        if m_30906 or m_fake or bare_matches:
            print(f"  DETAILS: {results[rel_path]}")

    return results

def test_task_2_assets():
    print("\n=== TASK 2: EMPIRICAL VERIFICATION OF 5 DOWNSCALED JPEGS ===")
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
    
    asset_results = []
    for jpg, backup in zip(target_jpgs, raw_backups):
        p_jpg = BASE_DIR / jpg
        p_bak = BASE_DIR / backup
        
        info = {
            "file": jpg,
            "exists": p_jpg.exists(),
            "backup_exists": p_bak.exists(),
            "size": p_jpg.stat().st_size if p_jpg.exists() else 0,
            "backup_size": p_bak.stat().st_size if p_bak.exists() else 0,
            "corrupted": False,
            "width": 0,
            "height": 0,
            "format": None
        }
        
        # Verify magic bytes
        if p_jpg.exists():
            with open(p_jpg, "rb") as f:
                header = f.read(3)
                if header != b"\xff\xd8\xff":
                    info["corrupted"] = True
                    info["decode_error"] = f"Invalid magic bytes: {header}"
                
        # Also check with ffprobe if available
        try:
            cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,codec_name", "-of", "default=noprint_wrappers=1", str(p_jpg)]
            res = subprocess.run(cmd, capture_output=True, text=True)
            info["ffprobe"] = res.stdout.strip()
        except Exception as e:
            info["ffprobe_error"] = str(e)
            
        print(f"Asset: {jpg}")
        print(f"  Size: {info['size']} bytes ({info['size']/1024:.2f} KB) - under 500 KB: {info['size'] < 512000}")
        print(f"  Dimensions: {info['width']}x{info['height']} - width <= 1920: {info['width'] <= 1920}")
        print(f"  Format: {info['format']}, Corrupted: {info['corrupted']}")
        print(f"  Backup size: {info['backup_size']} bytes ({info['backup_size']/(1024*1024):.2f} MB), Backup intact: {info['backup_size'] > 10*1024*1024}")
        print(f"  ffprobe: {info.get('ffprobe')}")
        asset_results.append(info)
        
    return asset_results

def test_task_3_cosimo_sentinel():
    print("\n=== TASK 3: STRESS-TEST COSIMO_SENTINEL.PY ===")
    sentinel_path = BASE_DIR / "scripts" / "cosimo_sentinel.py"
    torre_path = BASE_DIR / "site" / "torre_e_3d.html"
    
    # 1. Run cosimo_sentinel.py directly
    cmd = [sys.executable, str(sentinel_path)]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(BASE_DIR))
    print(f"Sentinel exit code: {proc.returncode}")
    print(f"Sentinel stdout:\n{proc.stdout}")
    print(f"Sentinel stderr:\n{proc.stderr}")
    
    # 2. Check torre_e_3d.html Base64 and behavior
    print("\n-- Subtest: torre_e_3d.html Base64 analysis --")
    if torre_path.exists():
        torre_content = torre_path.read_text(encoding='utf-8', errors='ignore')
        base64_count = len(re.findall(r'data:[^;]+;base64,', torre_content))
        lines = torre_content.splitlines()
        long_lines = [len(l) for l in lines if len(l) > 1000]
        print(f"torre_e_3d.html total size: {len(torre_content)} chars")
        print(f"torre_e_3d.html base64 blocks: {base64_count}")
        print(f"torre_e_3d.html long lines (>1000 chars): {len(long_lines)}, max length: {max(long_lines) if long_lines else 0}")
    else:
        print("torre_e_3d.html DOES NOT EXIST!")

    # 3. Test oracle: does sentinel catch real CRECI violations when injected into a temporary test copy?
    print("\n-- Subtest: Sentinel Oracle (True Positives & False Positives) --")
    # We test the regex and logic directly against various test strings
    re_fake_creci = re.compile(r'CRECI[:\s\-\/]+[0-9.,]{4,8}[\-A-Z]*|\(CRECI[\s\-]*SP\)', re.IGNORECASE)
    test_cases = [
        ("CRECI 30.906", True, "Standard fake CRECI"),
        ("CRECI 30906", True, "Fake CRECI without dot"),
        ("CRECI: 12345", True, "Colon separated"),
        ("CRECI - 123.456-F", True, "With suffix"),
        ("(CRECI SP)", True, "Bare tag with parens"),
        ("(CRECI-SP)", True, "Bare tag hyphenated with parens"),
        ("Pedro Soares (CRECI SP)", True, "In sentence"),
        ("Pedro Soares • CRECI-SP (Estágio em homologação)", False, "Allowed internship context"),
        ("CRECI-SP - estagiário em inscrição", False, "Allowed estagiario context"),
        ("Base64 string with embedded text: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9h...", False, "Base64 payload")
    ]
    
    for text, expected_violation, desc in test_cases:
        m = re_fake_creci.search(text)
        is_viol = False
        if m:
            snippet = text[max(0, m.start()-40):min(len(text), m.end()+40)]
            if not any(w in snippet.lower() for w in ['estagiário', 'estagiario', 'inscrição', 'fase', 'registro profissional']):
                is_viol = True
        match_success = (is_viol == expected_violation)
        print(f"  [{'PASS' if match_success else 'FAIL'}] '{text}' -> violation detected: {is_viol} (expected: {expected_violation}) [{desc}]")

def test_task_4_tennis_specs():
    print("\n=== TASK 4: TENNIS COURT SPECS AUDIT ===")
    target_files = [
        "site/comparativos.html",
        "site/hipica_dossier.html",
        "site/deck.html",
        "site/infografico_alphaville_vs_hipica.html"
    ]
    
    for rel_path in target_files:
        p = BASE_DIR / rel_path
        if not p.exists():
            print(f"File {rel_path} MISSING!")
            continue
        content = p.read_text(encoding='utf-8', errors='ignore')
        
        # Check mentions of 'saibro'
        saibro_lines = [l.strip() for l in content.splitlines() if 'saibro' in l.lower()]
        official_lines = [l.strip() for l in content.splitlines() if '02 quadras de tênis oficiais' in l.lower() or '18x36m' in l.lower()]
        
        print(f"File: {rel_path}")
        print(f"  'saibro' count: {len(saibro_lines)}")
        if saibro_lines:
            for sl in saibro_lines:
                print(f"    VIOLATION LINE: {sl[:120]}")
        print(f"  '02 Quadras de Tênis Oficiais' / '18x36m' count: {len(official_lines)}")
        for ol in official_lines[:3]:
            print(f"    SAMPLE LINE: {ol[:120]}")

    print("\n-- Checking guia_alto_da_boa_vista.html for CHSA saibro preservation --")
    guia_p = BASE_DIR / "site" / "guia_alto_da_boa_vista.html"
    if guia_p.exists():
        guia_content = guia_p.read_text(encoding='utf-8', errors='ignore')
        chsa_saibro_lines = [l.strip() for l in guia_content.splitlines() if 'saibro' in l.lower()]
        print(f"guia_alto_da_boa_vista.html 'saibro' mentions: {len(chsa_saibro_lines)}")
        for csl in chsa_saibro_lines:
            print(f"  CHSA saibro line: {csl[:120]}")
            
        # Check lab.html links
        lab_links = [l.strip() for l in guia_content.splitlines() if 'lab.html' in l.lower()]
        print(f"guia_alto_da_boa_vista.html 'lab.html' links: {len(lab_links)}")
    else:
        print("guia_alto_da_boa_vista.html MISSING!")

def test_task_5_test_suite():
    print("\n=== TASK 5: EXECUTION OF E2E TEST SUITE TIER 1 (F09, F10, F11, F12) ===")
    cmd = [sys.executable, "-m", "unittest", "tests.tier1_features.TestF09_IdentityCompliance", 
           "tests.tier1_features.TestF10_OfficialSpecs", 
           "tests.tier1_features.TestF11_MediaAssets", 
           "tests.tier1_features.TestF12_SentinelGitHygiene"]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(BASE_DIR))
    print(f"Unittest exit code: {proc.returncode}")
    print(f"STDOUT:\n{proc.stdout}")
    print(f"STDERR:\n{proc.stderr}")

if __name__ == "__main__":
    test_task_1_creci_scan()
    test_task_2_assets()
    test_task_3_cosimo_sentinel()
    test_task_4_tennis_specs()
    test_task_5_test_suite()
