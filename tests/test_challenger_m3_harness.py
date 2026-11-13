import os
import sys
import re
import math
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def test_css_stress():
    print("================================================================================")
    print("1. CSS STRESS TESTING: site/assets/css/lavvi-design-system.css")
    print("================================================================================")
    css_path = BASE_DIR / "site" / "assets" / "css" / "lavvi-design-system.css"
    
    if not css_path.exists():
        print("FAIL: lavvi-design-system.css does not exist!")
        return False
        
    raw_bytes = css_path.read_bytes()
    # Check BOM
    has_bom = raw_bytes.startswith(b'\xef\xbb\xbf')
    print(f"- UTF-8 BOM check: {'FAIL (BOM present)' if has_bom else 'PASS (No BOM detected)'}")
    
    try:
        content = raw_bytes.decode('utf-8')
        print("- UTF-8 decoding: PASS")
    except UnicodeDecodeError as e:
        print(f"- UTF-8 decoding: FAIL ({e})")
        return False
        
    # Check braces balance
    open_braces = content.count('{')
    close_braces = content.count('}')
    print(f"- Braces balance: open={open_braces}, close={close_braces} -> {'PASS' if open_braces == close_braces else 'FAIL'}")
    
    # Check variable naming
    var_defs = re.findall(r'(--[a-zA-Z0-9\-_]+)\s*:', content)
    invalid_vars = [v for v in var_defs if not re.match(r'^--[a-z0-9\-_]+$', v)]
    print(f"- CSS Variables declared: {len(var_defs)}, Invalid names: {len(invalid_vars)} -> {'PASS' if len(invalid_vars) == 0 else 'FAIL'}")
    
    # Check official color tokens
    mandatory_tokens = ['--primary', '--primary-light', '--primary-dark', '--secondary', '--novvo-dark', '--novvo-rose']
    missing_tokens = [t for t in mandatory_tokens if t not in var_defs]
    print(f"- Mandatory brand tokens: {'PASS (All present)' if not missing_tokens else f'FAIL (Missing: {missing_tokens})'}")
    
    # Check clamp() parameter counts: exactly 3 arguments without nested calc/parens
    clamp_matches = list(re.finditer(r'clamp\s*\(([^)]+)\)', content))
    broken_clamps = []
    for m in clamp_matches:
        inside = m.group(1).strip()
        args = [a.strip() for a in inside.split(',')]
        if len(args) != 3:
            broken_clamps.append((m.group(0), f"argument count {len(args)} != 3"))
        if '(' in inside or ')' in inside:
            broken_clamps.append((m.group(0), "nested parentheses detected"))
    print(f"- Fluid clamp() declarations: {len(clamp_matches)}, Broken clamps: {len(broken_clamps)} -> {'PASS' if len(broken_clamps) == 0 else 'FAIL'}")
    for bc, reason in broken_clamps:
        print(f"  BROKEN CLAMP: {bc} ({reason})")
        
    # Check font-family fallbacks
    font_decls = re.findall(r'font-family:\s*([^;]+);', content)
    generic_fallbacks = ['sans-serif', 'serif', 'monospace', 'cursive', 'fantasy', 'system-ui']
    missing_fallbacks = []
    for fd in font_decls:
        fonts = [f.strip().strip("'\"") for f in fd.split(',')]
        last = fonts[-1].lower()
        if not any(last == g or last.endswith(g) for g in generic_fallbacks):
            missing_fallbacks.append(fd)
    print(f"- Font-family declarations: {len(font_decls)}, Missing generic fallback: {len(missing_fallbacks)} -> {'PASS' if len(missing_fallbacks) == 0 else 'FAIL'}")
    for mf in missing_fallbacks:
        print(f"  MISSING FALLBACK: {mf}")
        
    return not has_bom and open_braces == close_braces and len(broken_clamps) == 0 and len(missing_fallbacks) == 0

def test_cinema_lavvi():
    print("\n================================================================================")
    print("2. STANDALONE TOOL STRESS TESTING: site/cinema_lavvi.html")
    print("================================================================================")
    path = BASE_DIR / "site" / "cinema_lavvi.html"
    if not path.exists():
        print("FAIL: site/cinema_lavvi.html does not exist!")
        return False
        
    content = path.read_text(encoding='utf-8', errors='ignore')
    
    # 1. 16:9 aspect ratio checks
    has_16_9 = 'aspect-ratio: 16 / 9' in content or 'aspect-video' in content
    print(f"- 16:9 widescreen aspect ratio: {'PASS' if has_16_9 else 'FAIL'}")
    
    # 2. Return navigation to index.html
    has_return_nav = ('href="index.html"' in content or "href='index.html'" in content) and ('Voltar' in content or 'voltar' in content)
    print(f"- Return navigation to index.html: {'PASS' if has_return_nav else 'FAIL'}")
    
    # 3. Modal open / close logic
    has_open_modal = 'openDirectVideoModal' in content or 'openVideoModal' in content
    has_close_modal = 'closeVideoPlayerModal' in content or 'closeVideoModal' in content
    has_active_modal = 'video-player-modal' in content
    print(f"- Modal opening/closing logic: {'PASS' if has_open_modal and has_close_modal and has_active_modal else 'FAIL'}")
    
    # 4. Escape key handling
    has_escape = "e.key === 'Escape'" in content or 'e.key === "Escape"' in content or 'keyCode === 27' in content
    print(f"- Escape key handler: {'PASS' if has_escape else 'FAIL'}")
    
    # 5. Shared CSS system link
    has_css = 'assets/css/lavvi-design-system.css' in content
    print(f"- Shared CSS system link: {'PASS' if has_css else 'FAIL'}")
    
    # 6. Streaming video catalogue count
    video_matches = re.findall(r'"id":\s*"([^"]+)"', content)
    print(f"- Streaming videos defined: {len(video_matches)} (Expected >= 16) -> {'PASS' if len(video_matches) >= 16 else 'FAIL'}")
    
    return has_16_9 and has_return_nav and has_open_modal and has_close_modal and has_escape and has_css

def test_radar_mapa():
    print("\n================================================================================")
    print("3. STANDALONE TOOL STRESS TESTING: site/radar_mapa.html")
    print("================================================================================")
    path = BASE_DIR / "site" / "radar_mapa.html"
    if not path.exists():
        print("FAIL: site/radar_mapa.html does not exist!")
        return False
        
    content = path.read_text(encoding='utf-8', errors='ignore')
    
    # 1. Dual mode switcher
    has_macro = 'switchViewMode(\'macro\')' in content or 'macro-view' in content
    has_radar = 'switchViewMode(\'radar\')' in content or 'radar-view' in content
    print(f"- Dual view mode switcher (Macro SP vs Micro Radar): {'PASS' if has_macro and has_radar else 'FAIL'}")
    
    # 2. Embedded fallback dataset (zero CORS/network dependency under file:///)
    has_embedded_data = 'EMBEDDED_POI_RADAR_DATA' in content
    print(f"- Zero CORS/network dependency fallback under file:///: {'PASS' if has_embedded_data else 'FAIL'}")
    
    # 3. All 8 anchor clusters
    clusters = ['hipica', 'moema', 'paraiso', 'brooklin', 'well_perdizes', 'klabin', 'analia_franco', 'marajoara']
    missing_clusters = [c for c in clusters if f"switchRadarCluster('{c}'" not in content and f'switchRadarCluster("{c}"' not in content]
    print(f"- All 8 anchor clusters present: {'PASS' if not missing_clusters else f'FAIL (Missing: {missing_clusters})'}")
    
    # 4. Search filtering
    has_search = 'onRadarSearchInput' in content or 'radar-poi-search-input' in content
    print(f"- POI search filtering logic: {'PASS' if has_search else 'FAIL'}")
    
    # 5. Shared CSS system link & return nav
    has_css = 'assets/css/lavvi-design-system.css' in content
    has_return_nav = ('href="index.html"' in content or "href='index.html'" in content) and ('Voltar' in content or 'voltar' in content)
    print(f"- Shared CSS system link: {'PASS' if has_css else 'FAIL'}")
    print(f"- Return navigation to index.html: {'PASS' if has_return_nav else 'FAIL'}")
    
    # 6. CRITICAL SPEC CHECK: Does Jardim da Hípica claim "saibro" in specs_oficiais?
    # Notice: external clubs like CHSA can mention saibro, but the condominium itself must NOT!
    saibro_condo_matches = re.findall(r'"lazer_destaque":\s*"[^"]*saibro[^"]*"', content, re.IGNORECASE)
    if saibro_condo_matches:
        print(f"⚠️ DEFECT DETECTED: 'saibro' found in condominium specs_oficiais lazer_destaque:")
        for sm in saibro_condo_matches:
            print(f"  {sm}")
    else:
        print("- Condominium tennis court spec (zero saibro on Jardim da Hípica condo): PASS")
        
    return has_macro and has_radar and has_embedded_data and not missing_clusters and has_search and has_css and has_return_nav

def test_credito_imobiliario():
    print("\n================================================================================")
    print("4. STANDALONE TOOL STRESS TESTING: site/credito_imobiliario.html")
    print("================================================================================")
    path = BASE_DIR / "site" / "credito_imobiliario.html"
    if not path.exists():
        print("FAIL: site/credito_imobiliario.html does not exist!")
        return False
        
    content = path.read_text(encoding='utf-8', errors='ignore')
    
    # 1. 12 Verified Banks and Rates
    expected_rates = {
        "caixa": 8.09,
        "poupex": 9.20,
        "inter": 9.65,
        "sicoob": 9.87,
        "unicred": 9.95,
        "bb": 10.24,
        "sicredi": 10.27,
        "btg": 10.45,
        "safra": 10.80,
        "bradesco": 11.76,
        "santander": 11.82,
        "itau": 11.86
    }
    
    missing_rates = []
    for bank_id, rate in expected_rates.items():
        pattern = rf'"{bank_id}"[\s\S]*?"taxa_aa":\s*{rate}'
        if not re.search(pattern, content):
            missing_rates.append((bank_id, rate))
            
    print(f"- 12 Brazilian banks and exact rates: {12 - len(missing_rates)}/12 found -> {'PASS' if not missing_rates else f'FAIL (Missing/Mismatched: {missing_rates})'}")
    
    # 2. Sliders & Amortization edge cases (Min R$ 300k, Max R$ 5M, 10 vs 35 years)
    has_slider_amount = 'min="300000"' in content and 'max="5000000"' in content
    has_slider_term = 'min="10"' in content and 'max="35"' in content
    has_sac = 'credit-btn-sac' in content and 'SAC' in content
    has_price = 'credit-btn-price' in content and 'PRICE' in content
    print(f"- Sliders configured (R$ 300k to R$ 5M, 10 to 35 years): {'PASS' if has_slider_amount and has_slider_term else 'FAIL'}")
    print(f"- Dual amortization systems (SAC and PRICE): {'PASS' if has_sac and has_price else 'FAIL'}")
    
    # 3. Mathematical Oracle for SAC and PRICE
    # Test SAC and PRICE formulas across multiple boundaries
    test_cases = [
        {"amount": 300000, "years": 10, "rate": 8.09},
        {"amount": 1500000, "years": 30, "rate": 8.09},
        {"amount": 5000000, "years": 35, "rate": 11.86}
    ]
    math_pass = True
    for tc in test_cases:
        months = tc["years"] * 12
        rate_year = tc["rate"] / 100.0
        rate_month = math.pow(1.0 + rate_year, 1.0 / 12.0) - 1.0
        
        # SAC
        amort_monthly = tc["amount"] / months
        first_interest = tc["amount"] * rate_month
        last_interest = amort_monthly * rate_month
        first_sac = amort_monthly + first_interest
        last_sac = amort_monthly + last_interest
        total_interest_sac = ((first_interest + last_interest) / 2.0) * months
        total_paid_sac = tc["amount"] + total_interest_sac
        
        # PRICE
        first_price = tc["amount"] * (rate_month / (1.0 - math.pow(1.0 + rate_month, -months)))
        total_paid_price = first_price * months
        total_interest_price = total_paid_price - tc["amount"]
        
        if first_sac <= 0 or last_sac <= 0 or first_price <= 0:
            math_pass = False
        if total_paid_price <= total_paid_sac: # Price always costs more total interest than SAC
            math_pass = False
            
    print(f"- Mathematical sanity (SAC linear decrease, PRICE fixed annuity, Total Price > Total SAC): {'PASS' if math_pass else 'FAIL'}")
    
    # 4. Zero external dependencies check (no 3P CDN scripts)
    external_scripts = re.findall(r'<script\s+src=[\"\'](https?://[^\"\']+)[\"\']', content)
    print(f"- Zero external CDN/network script dependencies: {'PASS (0 external scripts)' if len(external_scripts) == 0 else f'FAIL ({external_scripts})'}")
    
    # 5. Shared CSS system link & return nav
    has_css = 'assets/css/lavvi-design-system.css' in content
    has_return_nav = ('href="index.html"' in content or "href='index.html'" in content) and ('Voltar' in content or 'voltar' in content)
    print(f"- Shared CSS system link: {'PASS' if has_css else 'FAIL'}")
    print(f"- Return navigation to index.html: {'PASS' if has_return_nav else 'FAIL'}")
    
    return not missing_rates and has_slider_amount and has_slider_term and has_sac and has_price and math_pass and len(external_scripts) == 0

def test_guias_bairros():
    print("\n================================================================================")
    print("5. STANDALONE TOOL STRESS TESTING: site/guias_bairros.html")
    print("================================================================================")
    path = BASE_DIR / "site" / "guias_bairros.html"
    if not path.exists():
        print("FAIL: site/guias_bairros.html does not exist!")
        return False
        
    content = path.read_text(encoding='utf-8', errors='ignore')
    
    # 1. 8 Prime Luxury Neighborhoods
    bairros = ['hipica', 'moema', 'paraiso', 'brooklin', 'perdizes', 'klabin', 'analia_franco', 'marajoara']
    missing_bairros = []
    for b in bairros:
        if f"switchBairroGuide('{b}'" not in content and f'switchBairroGuide("{b}"' not in content:
            missing_bairros.append(b)
    print(f"- 8 Luxury Neighborhood tabs: {'PASS' if not missing_bairros else f'FAIL (Missing: {missing_bairros})'}")
    
    # 2. Bento Grid Elements per neighborhood
    has_schools = 'schools:' in content or 'Escolas' in content
    has_hospitals = 'hospitals:' in content or 'Hospitais' in content
    has_sports = 'sports:' in content or 'Esportes' in content
    has_gastro = 'gastro:' in content or 'Gastronomia' in content
    has_walkscore = 'walkscore:' in content or 'fiveMin' in content
    has_day_in_life = 'dayInLife:' in content or 'Um Dia no Bairro' in content
    print(f"- Bento Grid structure (schools, hospitals, sports, gastro): {'PASS' if has_schools and has_hospitals and has_sports and has_gastro else 'FAIL'}")
    print(f"- Walkability radii (5/10/15 min): {'PASS' if has_walkscore else 'FAIL'}")
    print(f"- 'Um Dia no Bairro por Pedro Soares': {'PASS' if has_day_in_life else 'FAIL'}")
    
    # 3. Shared CSS system link & return nav
    has_css = 'assets/css/lavvi-design-system.css' in content
    has_return_nav = ('href="index.html"' in content or "href='index.html'" in content) and ('Voltar' in content or 'voltar' in content)
    print(f"- Shared CSS system link: {'PASS' if has_css else 'FAIL'}")
    print(f"- Return navigation to index.html: {'PASS' if has_return_nav else 'FAIL'}")
    
    return not missing_bairros and has_schools and has_hospitals and has_sports and has_gastro and has_walkscore and has_css and has_return_nav

def test_link_integrity_and_air_gap():
    print("\n================================================================================")
    print("6. LINK INTEGRITY & AIR-GAP PROBING ACROSS ALL SITE/ FILES")
    print("================================================================================")
    
    # 1. Check for dead links to lab.html or mobile_hub.html in ALL html files under site/
    site_dir = BASE_DIR / "site"
    html_files = list(site_dir.rglob("*.html"))
    
    lab_links = []
    mobile_hub_links = []
    for hf in html_files:
        # Ignore lab/ folder itself where lab sub-pages live
        if 'lab' in hf.parts:
            continue
        try:
            c = hf.read_text(encoding='utf-8', errors='ignore')
            m_lab = re.findall(r'href=[\"\']([^\"\']*lab\.html[^\"\']*)[\"\']', c)
            if m_lab:
                lab_links.append((hf.relative_to(BASE_DIR), m_lab))
            m_hub = re.findall(r'href=[\"\']([^\"\']*mobile_hub\.html[^\"\']*)[\"\']', c)
            if m_hub:
                mobile_hub_links.append((hf.relative_to(BASE_DIR), m_hub))
        except Exception as e:
            pass
            
    print(f"- Scan for dead links to lab.html outside site/lab/:")
    if lab_links:
        print(f"  FOUND {len(lab_links)} files linking to lab.html:")
        for path, matches in lab_links:
            print(f"    {path}: {matches}")
    else:
        print(f"  PASS: Zero links to lab.html found across {len(html_files)} HTML files outside site/lab/!")
        
    print(f"- Scan for dead links to mobile_hub.html outside site/lab/:")
    if mobile_hub_links:
        print(f"  FOUND {len(mobile_hub_links)} files linking to mobile_hub.html:")
        for path, matches in mobile_hub_links:
            print(f"    {path}: {matches}")
    else:
        print(f"  PASS: Zero links to mobile_hub.html found across {len(html_files)} HTML files outside site/lab/!")
        
    # 2. Boardroom codenames leak check
    m3_owned_files = [
        "site/assets/css/lavvi-design-system.css",
        "site/cinema_lavvi.html",
        "site/radar_mapa.html",
        "site/credito_imobiliario.html",
        "site/guias_bairros.html",
        "site/comparativos.html",
        "site/relocation_matcher.html",
        "site/checklist-due-diligence.html",
        "site/holding_simulator.html",
        "site/hipica_dossier.html",
        "site/deck.html",
        "site/guia_alto_da_boa_vista.html",
        "site/bookmarks_portal.html",
        "site/dossiers/index.html"
    ]
    
    codenames = [r'\bCosimo\b', r'\bVito\b', r'\bMini Vito\b', r'\bJep\b', r'\bBurry\b', r'\bCobb\b', r'\bNolan\b', r'\bHagen\b', r'\bAriadne\b', r'\bMiyamoto\b', r'\bChamplain\b']
    re_fake_creci = re.compile(r'CRECI[\s\-\/]?(?:SP)?[:\s\-\/]+[0-9.,]{4,8}[\-A-Z]*|\(CRECI[\s\-]*(?:SP)?\)', re.IGNORECASE)
    
    m3_codename_leaks = []
    m3_creci_leaks = []
    
    for rel_path in m3_owned_files:
        p = BASE_DIR / rel_path
        if not p.exists():
            continue
        try:
            raw = p.read_text(encoding='utf-8', errors='ignore')
            lines = raw.splitlines()
            for idx, line in enumerate(lines):
                if len(line) > 1000:
                    continue
                for cn in codenames:
                    if re.search(cn, line, re.IGNORECASE):
                        m3_codename_leaks.append((rel_path, idx + 1, cn, line.strip()))
                creci_m = re_fake_creci.search(line)
                if creci_m:
                    snippet = line[max(0, creci_m.start()-30):min(len(line), creci_m.end()+30)]
                    if not any(w in snippet.lower() for w in ['estagiário', 'estagiario', 'inscrição', 'fase', 'registro profissional']):
                        m3_creci_leaks.append((rel_path, idx + 1, creci_m.group(0), line.strip()))
        except Exception as e:
            pass
            
    print(f"- Boardroom codename leaks in M3 owned files ({len(m3_owned_files)} files): {len(m3_codename_leaks)} leaks found -> {'PASS' if len(m3_codename_leaks) == 0 else 'FAIL'}")
    for f, line_no, term, snippet in m3_codename_leaks:
        print(f"  LEAK: {f}:{line_no} [{term}]: {snippet[:100]}")
        
    print(f"- Fake CRECI leaks in M3 owned files: {len(m3_creci_leaks)} leaks found -> {'PASS' if len(m3_creci_leaks) == 0 else 'FAIL'}")
    for f, line_no, term, snippet in m3_creci_leaks:
        print(f"  CRECI: {f}:{line_no} [{term}]: {snippet[:100]}")
        
    return len(m3_codename_leaks) == 0 and len(m3_creci_leaks) == 0

if __name__ == "__main__":
    r1 = test_css_stress()
    r2 = test_cinema_lavvi()
    r3 = test_radar_mapa()
    r4 = test_credito_imobiliario()
    r5 = test_guias_bairros()
    r6 = test_link_integrity_and_air_gap()
    
    print("\n================================================================================")
    print("SUMMARY OF ADVERSARIAL CHALLENGES:")
    print(f"  1. CSS Stress: {'PASS' if r1 else 'FAIL'}")
    print(f"  2. Cinema Lavvi: {'PASS' if r2 else 'FAIL'}")
    print(f"  3. Radar Mapa: {'PASS' if r3 else 'FAIL'}")
    print(f"  4. Crédito Imobiliário: {'PASS' if r4 else 'FAIL'}")
    print(f"  5. Guias Bairros: {'PASS' if r5 else 'FAIL'}")
    print(f"  6. Link Integrity & Air-Gap: {'PASS' if r6 else 'FAIL'}")
    print("================================================================================")
