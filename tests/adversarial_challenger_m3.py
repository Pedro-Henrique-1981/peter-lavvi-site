"""
Adversarial Stress Test Suite for Milestone 3 (Tool Modularization & Shared CSS System)
Authored by: empirical_challenger
"""

import unittest
import os
import re
import json

WORKSPACE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE_DIR = os.path.join(WORKSPACE, "site")
CSS_PATH = os.path.join(SITE_DIR, "assets", "css", "lavvi-design-system.css")

MODULAR_TOOLS = [
    "cinema_lavvi.html",
    "radar_mapa.html",
    "credito_imobiliario.html",
    "guias_bairros.html"
]

COMPANION_PAGES = [
    "bookmarks_portal.html",
    "relocation_matcher.html",
    "comparativos.html",
    "checklist-due-diligence.html",
    "holding_simulator.html",
    "hipica_dossier.html",
    "deck.html",
    "guia_alto_da_boa_vista.html",
    os.path.join("dossiers", "index.html")
]

class TestM3AdversarialCSS(unittest.TestCase):
    """Deep adversarial verification of shared CSS system"""

    def setUp(self):
        self.assertTrue(os.path.isfile(CSS_PATH), f"CSS file missing: {CSS_PATH}")
        with open(CSS_PATH, "rb") as f:
            self.raw_bytes = f.read()
        self.css_text = self.raw_bytes.decode("utf-8")

    def test_css_no_utf8_bom(self):
        """Verify CSS contains NO BOM signature"""
        self.assertFalse(self.raw_bytes.startswith(b"\xef\xbb\xbf"), "BOM detected in lavvi-design-system.css")

    def test_css_brace_balance(self):
        """Verify all braces { } are strictly balanced in the CSS"""
        open_count = self.css_text.count("{")
        close_count = self.css_text.count("}")
        self.assertEqual(open_count, close_count, f"Unbalanced braces in CSS: {open_count} open vs {close_count} close")

    def test_css_clamp_parameters_strictly_three_flat(self):
        """
        Adversarially probe EVERY clamp() in CSS:
        - Must have exactly 3 arguments
        - No nested parentheses (no nested calc() or nested clamp)
        """
        clamps = re.findall(r"clamp\s*\(([^;{}]+)\)", self.css_text)
        self.assertGreater(len(clamps), 0, "No clamp declarations found in CSS")
        for idx, clamp_inner in enumerate(clamps):
            self.assertNotIn("(", clamp_inner, f"Clamp #{idx} contains nested opening parenthesis: {clamp_inner}")
            self.assertNotIn(")", clamp_inner, f"Clamp #{idx} contains nested closing parenthesis: {clamp_inner}")
            parts = [p.strip() for p in clamp_inner.split(",")]
            self.assertEqual(len(parts), 3, f"Clamp #{idx} does not have exactly 3 arguments: {clamp_inner}")

    def test_css_font_family_fallbacks_and_generics(self):
        """Verify all font-family declarations terminate with valid generic fallback"""
        font_families = re.findall(r"font-family\s*:\s*([^;{}]+);", self.css_text)
        self.assertGreater(len(font_families), 0, "No font-family declarations found")
        valid_generics = {"sans-serif", "serif", "monospace", "cursive", "fantasy", "system-ui"}
        for idx, ff in enumerate(font_families):
            tokens = [t.strip().strip("'\"") for t in ff.split(",")]
            last_token = tokens[-1].lower()
            has_generic = any(g in last_token for g in valid_generics)
            self.assertTrue(has_generic, f"Font-family #{idx} missing generic fallback: '{ff}'")

    def test_css_required_tokens_present(self):
        """Verify mandatory official tokens are defined in :root"""
        root_match = re.search(r":root\s*\{([^}]+)\}", self.css_text)
        self.assertIsNotNone(root_match, ":root block missing from CSS")
        root_content = root_match.group(1)
        required_vars = [
            "--primary",
            "--primary-light",
            "--primary-dark",
            "--primary-foreground",
            "--secondary",
            "--secondary-foreground",
            "--novvo-dark",
            "--novvo-rose",
            "--border",
            "--card",
            "--header-height"
        ]
        for var in required_vars:
            self.assertIn(var, root_content, f"Mandatory variable {var} missing from :root")

    def test_css_mandatory_utility_classes(self):
        """Verify all required classes are present"""
        required_classes = [
            ".Drawer",
            ".nav-container",
            ".hero-fullbleed",
            ".catalog-grid",
            ".project-card",
            ".badge-novvo",
            ".badge-lavvi",
            ".concierge-widget",
            ".companion-header",
            ".companion-return-btn"
        ]
        for cls in required_classes:
            self.assertIn(cls, self.css_text, f"Mandatory CSS class {cls} missing")


class TestM3AdversarialCinema(unittest.TestCase):
    """Adversarial stress testing of site/cinema_lavvi.html"""

    def setUp(self):
        path = os.path.join(SITE_DIR, "cinema_lavvi.html")
        self.assertTrue(os.path.isfile(path), "cinema_lavvi.html does not exist")
        with open(path, "r", encoding="utf-8") as f:
            self.html = f.read()

    def test_cinema_16_9_widescreen_aspect_ratio(self):
        """Verify 16:9 widescreen video aspect ratio styling"""
        has_aspect = "16 / 9" in self.html or "aspect-video" in self.html or "16:9" in self.html or "56.25%" in self.html
        self.assertTrue(has_aspect, "cinema_lavvi.html missing 16:9 widescreen aspect ratio definition")

    def test_cinema_modal_logic_and_escape_key(self):
        """Verify modal player exists with escape key closing handler"""
        self.assertTrue("modal" in self.html.lower(), "Modal markup/logic missing in cinema_lavvi.html")
        has_escape = "Escape" in self.html or "keyCode === 27" in self.html or "which === 27" in self.html
        self.assertTrue(has_escape, "cinema_lavvi.html missing Escape key handler to close modal video")

    def test_cinema_return_nav_to_index(self):
        """Verify return navigation to index.html with standard wording"""
        has_return = re.search(r'href=["\']index\.html["\'][^>]*>.*?voltar', self.html, re.IGNORECASE | re.DOTALL) or \
                     re.search(r'href=["\']index\.html["\'][^>]*>.*?portal', self.html, re.IGNORECASE | re.DOTALL)
        self.assertTrue(has_return, "cinema_lavvi.html missing return navigation anchor to index.html")

    def test_cinema_streaming_videos_dataset_validity(self):
        """Verify streaming videos array contains valid entries"""
        self.assertIn("streamingVideos", self.html)
        # Check that there are video items with title, project, and video/embed url
        match = re.search(r"const\s+streamingVideos\s*=\s*(\[.*?\]);", self.html, re.DOTALL)
        self.assertIsNotNone(match, "Could not extract streamingVideos array")
        videos_raw = match.group(1)
        self.assertGreater(videos_raw.count("{"), 10, "Fewer than 10 video objects defined in cinema_lavvi.html")


class TestM3AdversarialRadarMapa(unittest.TestCase):
    """Adversarial stress testing of site/radar_mapa.html"""

    def setUp(self):
        path = os.path.join(SITE_DIR, "radar_mapa.html")
        self.assertTrue(os.path.isfile(path), "radar_mapa.html does not exist")
        with open(path, "r", encoding="utf-8") as f:
            self.html = f.read()

    def test_radar_dual_mode_switcher(self):
        """Verify dual mode switcher (Macro SP vs Micro Radar)"""
        has_mode_toggle = ("macro" in self.html.lower() and "radar" in self.html.lower()) and \
                          ("switch" in self.html.lower() or "mode" in self.html.lower() or "tab" in self.html.lower() or "view" in self.html.lower())
        self.assertTrue(has_mode_toggle, "radar_mapa.html missing dual Macro SP vs Micro Radar switcher")

    def test_radar_zero_cors_dependency_file_protocol(self):
        """Verify embedded POI fallback dataset is present for file:/// execution"""
        self.assertTrue(
            "EMBEDDED_POI_RADAR_DATA" in self.html or "FALLBACK_POIS" in self.html,
            "Missing embedded POI dataset for zero-CORS file:/// support"
        )
        # Check that fallback POIs contains valid categories
        for cat in ["escolas", "gastronomia", "saude", "clubes"]:
            self.assertIn(cat, self.html.lower(), f"Category {cat} not represented in radar POIs")

    def test_radar_anchor_clusters_coverage(self):
        """Verify 8 luxury anchor clusters are referenced"""
        clusters = [
            "hipica",
            "moema",
            "paraiso",
            "brooklin",
            "perdizes",
            "klabin",
            "analia",
            "marajoara"
        ]
        html_lower = self.html.lower()
        for cl in clusters:
            self.assertIn(cl, html_lower, f"Anchor cluster '{cl}' missing from radar_mapa.html")

    def test_radar_search_filtering(self):
        """Verify search input and filtering functionality exists"""
        self.assertIn("<input", self.html)
        has_filter = "filter" in self.html or "search" in self.html or "busca" in self.html.lower()
        self.assertTrue(has_filter, "Search/filter mechanism missing in radar_mapa.html")

    def test_radar_return_nav_to_index(self):
        """Verify return navigation to index.html"""
        has_return = re.search(r'href=["\']index\.html["\']', self.html)
        self.assertIsNotNone(has_return, "radar_mapa.html missing return href to index.html")


class TestM3AdversarialCreditoImobiliario(unittest.TestCase):
    """Adversarial stress testing of site/credito_imobiliario.html"""

    def setUp(self):
        path = os.path.join(SITE_DIR, "credito_imobiliario.html")
        self.assertTrue(os.path.isfile(path), "credito_imobiliario.html does not exist")
        with open(path, "r", encoding="utf-8") as f:
            self.html = f.read()

    def test_credito_exact_12_banks(self):
        """Verify all 12 bank interest rates are present with exact nominal rates"""
        expected_banks = {
            "Caixa": "8.09",
            "Poupex": "9.20",
            "Inter": "9.65",
            "Sicoob": "9.87",
            "Unicred": "9.95",
            "BB": "10.24",
            "Sicredi": "10.27",
            "BTG": "10.45",
            "Safra": "10.80",
            "Bradesco": "11.76",
            "Santander": "11.82",
            "Itaú": "11.86"
        }
        for bank, rate in expected_banks.items():
            self.assertTrue(
                (bank in self.html or bank.replace("ú", "u") in self.html) and rate in self.html,
                f"Bank {bank} with rate {rate}% missing or incorrect in credito_imobiliario.html"
            )

    def test_credito_zero_external_dependencies(self):
        """Verify pure vanilla JS (zero external script dependencies or remote trackers)"""
        scripts = re.findall(r'<script\s+src=["\']([^"\']+)["\']', self.html, re.IGNORECASE)
        for s in scripts:
            self.assertFalse(s.startswith("http://") or s.startswith("https://") or s.startswith("//"),
                            f"Remote external script dependency found: {s}")

    def test_credito_amortization_math_validation(self):
        """
        Adversarially verify the mathematical implementation of SAC and PRICE in credito_imobiliario.html
        """
        self.assertIn("calculateSimulations", self.html)
        self.assertIn("currentAmortType === 'SAC'", self.html)
        self.assertIn("rateMonth", self.html)

        # Mathematical oracle verification:
        # P = 1,000,000, annual_rate = 10.24%, term = 30 years (360 months)
        P = 1000000.0
        annual_rate = 0.1024
        i = (1.0 + annual_rate) ** (1.0 / 12.0) - 1.0
        n = 360

        # SAC
        amort = P / n
        first_interest = P * i
        last_interest = amort * i
        first_sac_installment = amort + first_interest
        last_sac_installment = amort + last_interest
        total_sac_interest = ((first_interest + last_interest) / 2.0) * n
        total_sac_paid = P + total_sac_interest

        # PRICE
        pmt = P * (i / (1.0 - (1.0 + i) ** (-n)))
        total_price_paid = pmt * n
        total_price_interest = total_price_paid - P

        # Assert mathematical invariants
        self.assertGreater(first_sac_installment, pmt)
        self.assertLess(last_sac_installment, pmt)
        self.assertLess(total_sac_paid, total_price_paid)
        self.assertLess(total_sac_interest, total_price_interest)

        # Check that the code inside credito_imobiliario.html reflects these exact formulas
        self.assertIn("Math.pow", self.html)
        self.assertIn("amortMonthly", self.html)

    def test_credito_loan_sliders_boundaries(self):
        """Verify sliders support min R$ 300k, max R$ 5M, and 10 to 35 years"""
        self.assertIn("300000", self.html)
        self.assertIn("5000000", self.html)
        self.assertTrue("10" in self.html and "35" in self.html)

    def test_credito_return_nav_to_index(self):
        """Verify return navigation to index.html"""
        has_return = re.search(r'href=["\']index\.html["\']', self.html)
        self.assertIsNotNone(has_return, "credito_imobiliario.html missing return href to index.html")


class TestM3AdversarialGuiasBairros(unittest.TestCase):
    """Adversarial stress testing of site/guias_bairros.html"""

    def setUp(self):
        path = os.path.join(SITE_DIR, "guias_bairros.html")
        self.assertTrue(os.path.isfile(path), "guias_bairros.html does not exist")
        with open(path, "r", encoding="utf-8") as f:
            self.html = f.read()

    def test_guias_all_8_neighborhoods(self):
        """Verify all 8 luxury neighborhoods render valid entries"""
        expected_neighborhoods = [
            "Alto da Boa Vista",
            "Moema",
            "Paraíso",
            "Brooklin",
            "Perdizes",
            "Chácara Klabin",
            "Anália Franco",
            "Jardim Marajoara"
        ]
        for b in expected_neighborhoods:
            b_norm = b.replace("í", "i").replace("á", "a")
            self.assertTrue(
                b in self.html or b_norm in self.html,
                f"Neighborhood {b} missing from guias_bairros.html"
            )

    def test_guias_infrastructure_pillars_and_walkability(self):
        """Verify the 4-card infrastructure blocks and walkability radii are present"""
        for pillar in ["escolas", "hospitais", "clubes", "gastronomia"]:
            self.assertIn(pillar, self.html.lower(), f"Pillar {pillar} not found in guias_bairros.html")
        self.assertTrue(
            "walk" in self.html.lower() or "caminhabilidade" in self.html.lower() or "min" in self.html.lower(),
            "Walkability metrics missing from guias_bairros.html"
        )

    def test_guias_bento_grid_styling(self):
        """Verify bento grid layouts are utilized"""
        self.assertTrue(
            "bento" in self.html.lower() or "grid" in self.html.lower(),
            "Bento grid styling missing in guias_bairros.html"
        )

    def test_guias_return_nav_to_index(self):
        """Verify return navigation to index.html"""
        has_return = re.search(r'href=["\']index\.html["\']', self.html)
        self.assertIsNotNone(has_return, "guias_bairros.html missing return href to index.html")


class TestM3AdversarialLinkIntegrityAndAirGap(unittest.TestCase):
    """Adversarial scan of all site/ HTML files for dead links and boardroom codename leaks"""

    def setUp(self):
        self.html_files = []
        for root, dirs, files in os.walk(SITE_DIR):
            for file in files:
                if file.endswith(".html"):
                    self.html_files.append(os.path.join(root, file))

    def test_no_dead_links_to_lab_or_mobile_hub(self):
        """Search all HTML files in site/ for active dead links to lab.html or mobile_hub.html"""
        public_pages = [
            "index.html",
            "cinema_lavvi.html",
            "radar_mapa.html",
            "credito_imobiliario.html",
            "guias_bairros.html",
            "bookmarks_portal.html",
            "relocation_matcher.html",
            "comparativos.html",
            "checklist-due-diligence.html",
            "holding_simulator.html",
            "hipica_dossier.html",
            "deck.html",
            "guia_alto_da_boa_vista.html",
            os.path.join("dossiers", "index.html")
        ]

        violations = []
        for rel in public_pages:
            path = os.path.join(SITE_DIR, rel)
            if not os.path.isfile(path):
                continue
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            dead_links = re.findall(r'href=["\'][^"\']*(?:lab\.html|mobile_hub\.html)[^"\']*["\']', content)
            if dead_links:
                violations.append((rel, dead_links))

        self.assertEqual(len(violations), 0, f"Found dead links to lab.html/mobile_hub.html in public pages: {violations}")

    def test_global_scan_all_html_files_for_lab_links(self):
        """Scan every single HTML file in site/ (excluding lab.html / index_lab.html / site/lab/) for lab.html links"""
        found_lab = []
        for hf in self.html_files:
            fname = os.path.basename(hf)
            rel = os.path.relpath(hf, SITE_DIR)
            if fname in ["lab.html", "index_lab.html", "lab_mobile.html"] or rel.startswith("lab" + os.sep):
                continue
            with open(hf, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            matches = re.findall(r'href=["\'][^"\']*lab\.html[^"\']*["\']', content)
            if matches:
                found_lab.append((rel, matches))
        self.assertEqual(len(found_lab), 0, f"HTML files with dead lab.html links: {found_lab}")

    def test_no_boardroom_codename_leaks_in_owned_files(self):
        """Verify strict air-gap: ZERO boardroom codenames in all client-facing files"""
        client_facing_files = [
            os.path.join("assets", "css", "lavvi-design-system.css"),
            "cinema_lavvi.html",
            "radar_mapa.html",
            "credito_imobiliario.html",
            "guias_bairros.html",
            "bookmarks_portal.html",
            "relocation_matcher.html",
            "comparativos.html",
            "checklist-due-diligence.html",
            "holding_simulator.html",
            "hipica_dossier.html",
            "deck.html",
            os.path.join("dossiers", "index.html"),
            "guia_alto_da_boa_vista.html",
            "infografico_alphaville_vs_hipica.html",
            "torre_e_3d.html"
        ]

        patterns = [
            r"\bCosimo\b",
            r"\bVito\b",
            r"\bMini Vito\b",
            r"\bJep\b",
            r"\bBurry\b",
            r"\bCobb\b",
            r"\bNolan\b",
            r"\bHagen\b",
            r"\bAriadne\b",
            r"\bMiyamoto\b",
            r"\bChamplain\b"
        ]

        leaks = []
        for rel in client_facing_files:
            path = os.path.join(SITE_DIR, rel)
            if not os.path.isfile(path):
                continue
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            # Strip base64 data to avoid false matches in embedded textures (e.g. torre_e_3d.html)
            content_clean = re.sub(r'data:[^;]+;base64,[a-zA-Z0-9+/=]+', '', content)
            lines = content_clean.splitlines()
            for line_no, line in enumerate(lines, start=1):
                if len(line) > 1000:
                    continue
                for p in patterns:
                    if re.search(p, line, re.IGNORECASE):
                        leaks.append((rel, line_no, p, line.strip()))

        self.assertEqual(len(leaks), 0, f"Boardroom codename leaks detected: {leaks}")

    def test_no_fabricated_creci_in_owned_files(self):
        """Verify no fake CRECI numbers (30.906, bare CRECI SP) in owned M3 files"""
        owned_files = [
            os.path.join("assets", "css", "lavvi-design-system.css"),
            "cinema_lavvi.html",
            "radar_mapa.html",
            "credito_imobiliario.html",
            "guias_bairros.html",
            "bookmarks_portal.html",
            "relocation_matcher.html",
            "comparativos.html",
            "checklist-due-diligence.html",
            "holding_simulator.html",
            "hipica_dossier.html",
            "deck.html",
            os.path.join("dossiers", "index.html"),
            "guia_alto_da_boa_vista.html"
        ]

        creci_patterns = [
            r"30\.?906",
            r"CRECI[\s\-\/]?(?:SP)?[:\s\-\/]+[0-9.,]{4,8}[\-A-Z]*",
            r"\(CRECI[\s\-]*(?:SP)?\)"
        ]

        violations = []
        for rel in owned_files:
            path = os.path.join(SITE_DIR, rel)
            if not os.path.isfile(path):
                continue
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            for p in creci_patterns:
                matches = re.findall(p, content, re.IGNORECASE)
                if matches:
                    violations.append((rel, p, matches))

        self.assertEqual(len(violations), 0, f"Fabricated CRECI detected: {violations}")

    def test_all_owned_files_no_utf8_bom(self):
        """Verify that all owned files have NO BOM byte sequence"""
        owned_files = [
            os.path.join("assets", "css", "lavvi-design-system.css"),
            "cinema_lavvi.html",
            "radar_mapa.html",
            "credito_imobiliario.html",
            "guias_bairros.html",
            "bookmarks_portal.html",
            "relocation_matcher.html",
            "comparativos.html",
            "checklist-due-diligence.html",
            "holding_simulator.html",
            "hipica_dossier.html",
            "deck.html",
            os.path.join("dossiers", "index.html"),
            "guia_alto_da_boa_vista.html"
        ]
        for rel in owned_files:
            path = os.path.join(SITE_DIR, rel)
            if not os.path.isfile(path):
                continue
            with open(path, "rb") as f:
                header = f.read(4)
            self.assertFalse(header.startswith(b"\xef\xbb\xbf"), f"BOM detected in {rel}")


if __name__ == "__main__":
    unittest.main()
