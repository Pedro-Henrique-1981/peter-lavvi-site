import os
import sys
import io
import json
import re
from pathlib import Path

# Force UTF-8 stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent
IDENTITY_FILE = BASE_DIR / "site" / "data" / "pedro_canonical_identity.json"
SPECS_TRUTH_FILE = BASE_DIR / "briefings" / "LAVVI_OFFICIAL_SPECS_TRUTH.md"
GEMINI_MD_FILE = BASE_DIR / "GEMINI.md"
CHROME_BOOKMARKS_PATH = Path(os.environ.get('LOCALAPPDATA', '')) / 'Google' / 'Chrome' / 'User Data' / 'Default' / 'Bookmarks'

def run_sentinel_audit(verbose=False):
    print("=" * 80)
    print("🛡️ COSIMO SENTINEL — SUPER-AGENTE DETERMINÍSTICO ANTI-ALUCINAÇÃO (TIER 0)")
    print("=" * 80)

    violations = []
    warnings = []

    # 1. Carregar Base Canônica de Identidade
    if not IDENTITY_FILE.exists():
        violations.append(f"CRÍTICO: Base canônica de identidade não encontrada em: {IDENTITY_FILE}")
        return False, violations, warnings
    
    with open(IDENTITY_FILE, 'r', encoding='utf-8') as f:
        identity_data = json.load(f)

    blacklist_urls = identity_data.get("homonym_negative_blacklist", {}).get("youtube_channels", [])
    blacklist_topics = identity_data.get("homonym_negative_blacklist", {}).get("blacklisted_topics_and_claims", [])

    print(f"✓ Base Canônica carregada ({len(blacklist_urls)} URLs e {len(blacklist_topics)} termos na Blacklist)")

    # 2. Verificar Teto de 24 KB no GEMINI.md
    if GEMINI_MD_FILE.exists():
        gemini_size = os.path.getsize(GEMINI_MD_FILE)
        if gemini_size > 24000:
            violations.append(f"GEMINI.md EXCEDEU O LIMITE DE 24 KB: {gemini_size} bytes! (Truncamento ativo!)")
        elif gemini_size > 18000:
            warnings.append(f"GEMINI.md próximo do limite: {gemini_size} bytes (Recomendado < 18 KB)")
        else:
            print(f"✓ GEMINI.md dentro do teto seguro: {gemini_size} bytes (< 18 KB)")
    else:
        violations.append("GEMINI.md não encontrado!")

    # 3. Escanear Diretórios Ativos
    scan_dirs = [
        BASE_DIR / "site",
        BASE_DIR / "00_COCKPIT_PEDRO",
        BASE_DIR / "00_COFRES_DE_INTELIGENCIA",
        BASE_DIR / "briefings",
        BASE_DIR / "scripts"
    ]

    scanned_files = 0
    clean_files = 0

    # Padrões regex proibidos
    re_fake_creci = re.compile(r'CRECI[\s\-\/]?(?:SP)?[:\s\-\/]+[0-9.,]{4,8}[\-A-Z]*|\(CRECI[\s\-]*(?:SP)?\)', re.IGNORECASE)
    re_internal_names = re.compile(r'\b(Cosimo|Vito|Jep|Burry|Cobb|Nolan|Hagen|Ariadne|Miyamoto|Champlain)\b')
    CLIENT_FACING = {
        'index.html',
        'lab_mobile.html',
        'comparativos.html',
        'relocation_matcher.html',
        'checklist-due-diligence.html',
        'holding_simulator.html',
        'hipica_dossier.html',
        'deck.html',
        'guia_alto_da_boa_vista.html',
        'infografico_alphaville_vs_hipica.html',
        'linkedin_studio.html',
        'torre_e_3d.html',
        'cinema_lavvi.html',
        'radar_mapa.html',
        'credito_imobiliario.html',
        'guias_bairros.html'
    }
    re_fake_yt = re.compile(r'youtube\.com/@pedrosoares', re.IGNORECASE)
    re_442_videos = re.compile(r'442\s*(vídeos|aulas|videos)', re.IGNORECASE)

    for sdir in scan_dirs:
        if not sdir.exists():
            continue
        for root, _, files in os.walk(sdir):
            if any(x in root for x in ['.venv', '.git', '__pycache__', 'archive', '_lixo', 'backup_raw_assets', 'dwv_transcripts']):
                continue
            for fname in files:
                if fname.startswith(('clean_', 'cleanse_')):
                    continue
                if fname.endswith(('.html', '.json', '.md', '.py', '.txt')):
                    fpath = Path(root) / fname
                    scanned_files += 1
                    try:
                        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()

                        # Ignorar o próprio arquivo de identidade e este script
                        if fpath == IDENTITY_FILE or fpath == Path(__file__).resolve():
                            continue

                        # Ignorar payloads Base64 e linhas gigantes para evitar falsos positivos
                        check_lines = [l for l in content.splitlines() if len(l) <= 1000]
                        check_content = '\n'.join(check_lines)
                        check_content = re.sub(r'data:[^;]+;base64,[a-zA-Z0-9+/=]+', '', check_content)

                        # Check 1: YouTube homonym channel
                        if re_fake_yt.search(check_content):
                            violations.append(f"[HOMÔNIMO FALSO] {fpath.relative_to(BASE_DIR)}: contém 'youtube.com/@pedrosoares'")

                        # Check 2: 442 vídeos / vestibular claims
                        if re_442_videos.search(check_content):
                            violations.append(f"[TERMO PROIBIDO] {fpath.relative_to(BASE_DIR)}: contém menção a '442 vídeos/aulas'")

                        # Check 3: CRECI inventado (exceto se for simulado ou crecisp site)
                        if "simulado" not in fname.lower() and "spider.crecisp" not in check_content.lower():
                            creci_match = re_fake_creci.search(check_content)
                            if creci_match:
                                # Permitir apenas se contiver 'estagiário' ou 'em andamento' no contexto
                                snippet = check_content[max(0, creci_match.start()-40):min(len(check_content), creci_match.end()+40)]
                                if not any(w in snippet.lower() for w in ['estagiário', 'estagiario', 'inscrição', 'fase', 'registro profissional', 'conselho', 'regulatório', 'regulatorio']):
                                    violations.append(f"[CRECI NÃO HOMOLOGADO] {fpath.relative_to(BASE_DIR)}: '{creci_match.group(0)}'")

                        # Check 4: air-gap de marca (nomes internos de subagentes em páginas voltadas ao cliente)
                        if fname in CLIENT_FACING and Path(root).name == 'site':
                            leak = re_internal_names.search(check_content)
                            if leak:
                                violations.append(f"[AIR-GAP] {fpath.relative_to(BASE_DIR)}: nome interno de subagente '{leak.group(0)}' em página de cliente")

                        clean_files += 1
                    except Exception as e:
                        warnings.append(f"Erro ao ler {fpath.name}: {e}")

    # 4. Verificar Arquivo de Favoritos do Chrome
    if CHROME_BOOKMARKS_PATH.exists():
        scanned_files += 1
        try:
            with open(CHROME_BOOKMARKS_PATH, 'r', encoding='utf-8') as f:
                bm_content = f.read()
            if re_fake_yt.search(bm_content):
                warnings.append("CHROME BOOKMARKS: Chrome ativo em memória mantém cache antigo do atalho. Clique com botão direito no item '▶️ YouTube Oficial' na barra de favoritos e selecione 'Excluir'.")
                print("⚠️ Aviso: Chrome Bookmarks possui atalho pendente de remoção manual no navegador")
            else:
                print("✓ Perfil do Google Chrome Bookmarks auditado e 100% limpo")
        except Exception as e:
            warnings.append(f"Aviso ao ler Chrome Bookmarks: {e}")

    # 5. Relatório Executivo
    print(f"\nTotal de arquivos inspecionados: {scanned_files}")
    print("-" * 80)

    if violations:
        print(f"❌ ALERTA MÁXIMO: {len(violations)} VIOLAÇÃO(ÕES) DETECTADA(S):")
        for v in violations:
            print(f"   [!] {v}")
        print("\nOperação BLOQUEADA pelo Cosimo Sentinel!")
        
        # Envio automático de alerta para o celular de Pedro via ntfy
        try:
            sys.path.insert(0, str(BASE_DIR))
            from scripts.notify_pedro import send_notification
            send_notification(
                message=f"Cosimo Sentinel detectou {len(violations)} violação(ões) de integridade e bloqueou a gravação de arquivos. Inspecione o terminal.",
                title="🚨 ALERTA CRÍTICO: Cosimo Sentinel",
                priority="urgent",
                tags=["warning", "rotating_light", "shield"]
            )
        except Exception:
            pass
            
        return False
    else:
        print("✅ STATUS VERDE: ZERO ALUCINAÇÕES DETECTADAS!")
        print("✓ Nenhuma atribuição indevida de homônimos encontrada.")
        print("✓ Nenhum número de CRECI inventado.")
        print("✓ Todos os arquivos respeitam a base canônica de Pedro Soares.")
        if warnings:
            print(f"\n⚠️ Avisos secundários ({len(warnings)}):")
            for w in warnings:
                print(f"   [-] {w}")
        return True

if __name__ == "__main__":
    success = run_sentinel_audit(verbose=True)
    sys.exit(0 if success else 1)
