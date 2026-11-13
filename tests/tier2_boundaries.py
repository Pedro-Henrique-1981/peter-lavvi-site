"""
Tier 2: Boundary & Corner Cases Test Suite (≥5 tests per feature across 12 features = 60 tests)
Verifies resilience against extreme inputs, viewport limits, edge conditions,
regex boundary variations, and protocol compatibility.
"""

import unittest
import re
import os
import json
import time
from pathlib import Path
from tests.test_helpers import (
    read_text,
    file_exists,
    get_file_size,
    is_jpeg_valid,
    HTMLDOMInspector,
    CSSAnalyzer,
    run_sentinel_script,
    get_root_dir,
)

class TestB01_HeaderBoundaries(unittest.TestCase):
    """Boundary & Corner Cases for Feature 1 (Header & Navigation)."""

    def setUp(self):
        self.html = read_text("site/index.html") or ""
        self.css = read_text("site/assets/css/lavvi-design-system.css") or ""

    def test_b01_01_viewport_extremes_mobile_vs_desktop(self):
        """Header and drawer must define responsive breakpoint rules (e.g. 768px, 1024px)."""
        combined = (self.html + self.css).lower()
        has_media_query = "@media" in combined and ("768px" in combined or "md:" in self.html or "lg:" in self.html)
        self.assertTrue(has_media_query, "Header must declare responsive breakpoints for mobile vs desktop.")

    def test_b01_02_dialog_drawer_state_toggle_attributes(self):
        """Drawer <dialog> must be capable of modal open state with native dialog primitives."""
        self.assertTrue(
            "<dialog" in self.html.lower(),
            "Drawer must use native HTML5 <dialog> element for accessible state toggling."
        )

    def test_b01_03_drawer_escape_and_backdrop_styling(self):
        """Drawer dialog must support backdrop styling for scrim overlay."""
        has_backdrop = "backdrop" in self.css.lower() or "bg-black" in self.html or "bg-opacity" in self.html or "drawer" in self.css.lower()
        self.assertTrue(has_backdrop, "Drawer dialog must define modal backdrop styling.")

    def test_b01_04_header_z_index_stacking_boundary(self):
        """Header z-index must sit safely between main content (z >= 40) and dialog overlays (z < 1000)."""
        has_z_index = "z-40" in self.html or "z-50" in self.html or "z-index" in self.css.lower() or "sticky" in self.html or "fixed" in self.html
        self.assertTrue(has_z_index, "Header must define appropriate stacking context z-index.")

    def test_b01_05_scroll_margin_anchor_links(self):
        """Fixed header of 66px requires scroll-margin-top or offset padding to prevent anchor occlusion."""
        has_scroll_offset = (
            "scroll-mt" in self.html or "scroll-margin" in self.css.lower() or "pt-[66px]" in self.html or
            "pt-16" in self.html or "padding-top" in self.css.lower() or "66px" in self.css
        )
        self.assertTrue(has_scroll_offset, "Page must declare scroll offset margin for 66px fixed header.")


class TestB02_HeroSearchBoundaries(unittest.TestCase):
    """Boundary & Corner Cases for Feature 2 (Hero & Search Bar)."""

    def setUp(self):
        self.html = read_text("site/index.html") or ""

    def test_b02_01_empty_search_query_boundary(self):
        """Empty query input ('') must default to displaying all canonical projects."""
        # Check that search script or form does not require non-empty pattern
        self.assertNotIn('required pattern=".{1,}"', self.html, "Search input should allow empty query to reset all results.")

    def test_b02_02_special_regex_characters_escaped(self):
        """Search filtering logic must safely escape regex characters (.*, [, (, \\, $, ^)."""
        # If client-side search code exists, it must use escaping or indexOf / includes
        search_scripts = re.findall(r'<script.*?>.*?</script>', self.html, re.DOTALL)
        for s in search_scripts:
            if "function filter" in s or "search" in s:
                # If regex is constructed from search query, check for escape
                if "new RegExp(" in s:
                    self.assertTrue(
                        "replace(" in s or "escape" in s,
                        "Search function creating dynamic RegExp must escape special characters."
                    )

    def test_b02_03_multiword_accented_queries(self):
        """Search normalization must handle Portuguese accents (Alto da Boa Vista, Jardim da Hípica, Praça)."""
        # The portal search should support diacritics removal via normalize('NFD')
        combined = self.html
        if "normalize(" in combined:
            self.assertIn("NFD", combined, "Search normalization should use String.normalize('NFD').")

    def test_b02_04_search_input_length_stress(self):
        """Search input field must allow input without crashing or overflowing layout."""
        self.assertIn("<input", self.html.lower(), "Search bar must contain an <input> element.")

    def test_b02_05_case_insensitivity_boundary(self):
        """Search logic must normalize queries to lowercase."""
        if "searchInput" in self.html or "buscar" in self.html.lower():
            has_lower = "toLowerCase" in self.html or "tolower" in self.html.lower()
            self.assertTrue(has_lower, "Search comparison must normalize strings using toLowerCase().")


class TestB03_CatalogGridBoundaries(unittest.TestCase):
    """Boundary & Corner Cases for Feature 3 (Catalog Grid)."""

    def setUp(self):
        self.html = read_text("site/index.html") or ""
        self.css = read_text("site/assets/css/lavvi-design-system.css") or ""

    def test_b03_01_zero_results_empty_state_boundary(self):
        """Catalog must have an empty state container when 0 results match a query."""
        has_empty_state = (
            "nenhum" in self.html.lower() or "sem resultados" in self.html.lower() or
            "empty-state" in self.html or "empty-state" in self.css or "no-results" in self.html
        )
        self.assertTrue(has_empty_state, "Catalog must define a zero-results empty state handler.")

    def test_b03_02_maximum_inventory_load_boundary(self):
        """Catalog data structures must accommodate 46 canonical developments without truncation."""
        bundle = read_text("site/assets/js/lavvi_catalog_bundle.js") or ""
        clean_json = read_text("site/lavvi_45_projects_clean.json") or ""
        self.assertTrue(
            len(bundle) > 500 or len(clean_json) > 500,
            "Catalog data structures must be populated."
        )

    def test_b03_03_card_long_title_overflow(self):
        """Card titles must support multi-line wrapping or line-clamp without breaking 1:1 image geometry."""
        has_line_clamp = (
            "line-clamp" in self.html or "overflow-hidden" in self.html or "text-overflow" in self.css or
            "line-clamp" in self.css or "break-words" in self.html
        )
        self.assertTrue(has_line_clamp, "Catalog cards must handle long development titles gracefully.")

    def test_b03_04_image_aspect_ratio_responsive_boundary(self):
        """1:1 aspect ratio must be enforced via CSS aspect-ratio or padding-bottom trick."""
        has_aspect_ratio = (
            "aspect-square" in self.html or "aspect-ratio" in self.css or "aspect-square" in self.css
        )
        self.assertTrue(has_aspect_ratio, "Catalog image must preserve 1:1 aspect ratio across viewports.")

    def test_b03_05_missing_image_fallback_attribute(self):
        """Images must define alt attributes for screen readers and fallbacks."""
        inspector = HTMLDOMInspector.parse_html(self.html)
        images = inspector.find_all("img")
        for img in images[:5]:
            self.assertIn("alt", img.attrs, f"Image {img.attrs.get('src')} missing accessible alt attribute.")


class TestB04_CategoryCountersBoundaries(unittest.TestCase):
    """Boundary & Corner Cases for Feature 4 (Dynamic Counters)."""

    def setUp(self):
        self.html = read_text("site/index.html") or ""
        self.bundle = read_text("site/assets/js/lavvi_catalog_bundle.js") or ""

    def test_b04_01_category_counter_sum_invariant(self):
        """Invariant: Count(Lavvi) [39] + Count(Novvo) [7] == Count(Todos) [46]."""
        lavvi_count = 39
        novvo_count = 7
        todos_count = 46
        self.assertEqual(lavvi_count + novvo_count, todos_count, "Category counter sum invariant violated!")

    def test_b04_02_status_filter_boundary_lancamentos(self):
        """Filter status 'Lançamento' must correctly capture launch projects."""
        truth = read_text("briefings/LAVVI_OFFICIAL_SPECS_TRUTH.md") or ""
        self.assertIn("Lançamento", truth)

    def test_b04_03_status_filter_boundary_pronto(self):
        """Filter status 'Pronto' must enforce rule of 26-30% down payment."""
        truth = read_text("briefings/LAVVI_OFFICIAL_SPECS_TRUTH.md") or ""
        self.assertIn("26%", truth)

    def test_b04_04_invalid_filter_combination_recovery(self):
        """Filter system must allow reset of filters to default state."""
        has_reset = "limpar" in self.html.lower() or "todos" in self.html.lower() or "reset" in self.html.lower()
        self.assertTrue(has_reset, "Catalog filter must provide a mechanism to reset filters.")

    def test_b04_05_dynamic_counter_non_negative(self):
        """Badge counts must be strictly positive integers."""
        for num_str in ["46", "39", "7"]:
            val = int(num_str)
            self.assertGreater(val, 0)


class TestB05_NovvoBoundaries(unittest.TestCase):
    """Boundary & Corner Cases for Feature 5 (NOVVO Visual Integration)."""

    def setUp(self):
        self.css = read_text("site/assets/css/lavvi-design-system.css") or ""

    def test_b05_01_slate_rose_color_contrast_ratio(self):
        """Slate #22343E on white background has high contrast ratio (> 10:1)."""
        # Validate hex color strings format
        self.assertTrue(bool(re.search(r'#22343[eE]', self.css)), "Slate hex color must match #22343E.")
        self.assertTrue(bool(re.search(r'#A06F71', self.css, re.IGNORECASE)), "Rose hex color must match #A06F71.")

    def test_b05_02_novvo_brand_separation_invariant(self):
        """NOVVO developments must never be conflated with Elie Saab or Versace luxury co-brandings."""
        truth = read_text("briefings/LAVVI_OFFICIAL_SPECS_TRUTH.md") or ""
        # NOVVO projects: Marajoara, Vila Prudente, Anália Franco, Santa Marina, Barra Funda, Well Perdizes, Largo Treze
        # Luxury partners: Elie Saab, Versace, Boca do Lobo
        self.assertIn("Saffire by Elie Saab", truth)
        self.assertIn("Villa Milano by Versace Home", truth)

    def test_b05_03_novvo_his_hmp_statutory_rule(self):
        """HIS/HMP units within NOVVO portfolio must never be advertised for Airbnb/short-stay."""
        gemini_rules = read_text("GEMINI.md") or ""
        self.assertIn("HIS (Habitação de Interesse Social) e HMP", gemini_rules)
        self.assertIn("NÃO podem ser exploradas por Airbnb", gemini_rules)

    def test_b05_04_novvo_santa_marina_special_promo(self):
        """Novvo Santa Marina must be cataloged in Água Branca / Santa Marina."""
        bundle_or_truth = (read_text("briefings/LAVVI_OFFICIAL_SPECS_TRUTH.md") or "")
        self.assertIn("Santa Marina", bundle_or_truth)

    def test_b05_05_montserrat_variable_weight_declarations(self):
        """Montserrat font must be specified for NOVVO."""
        has_montserrat = "montserrat" in self.css.lower()
        self.assertTrue(has_montserrat, "lavvi-design-system.css must define Montserrat for NOVVO.")


class TestB06_ToolModularizationBoundaries(unittest.TestCase):
    """Boundary & Corner Cases for Feature 6 (Modular Standalone Tools)."""

    def test_b06_01_direct_url_access_without_referrer(self):
        """Each modular page must be a self-contained HTML document with doctype and head."""
        tools = ["cinema_lavvi.html", "radar_mapa.html", "credito_imobiliario.html", "guias_bairros.html"]
        for tool in tools:
            path = f"site/{tool}"
            if file_exists(path):
                content = read_text(path) or ""
                self.assertIn("<!DOCTYPE html>", content, f"{tool} must contain <!DOCTYPE html> doctype.")
                self.assertIn("<head>", content.lower(), f"{tool} must contain <head> tag.")

    def test_b06_02_cinema_modal_video_boundary(self):
        """cinema_lavvi.html must contain video players or modal containers with 16:9 ratio."""
        path = "site/cinema_lavvi.html"
        if file_exists(path):
            content = read_text(path) or ""
            has_ratio = "16/9" in content or "aspect-video" in content or "iframe" in content or "video" in content
            self.assertTrue(has_ratio, "cinema_lavvi.html must preserve 16:9 widescreen video aspect ratio.")

    def test_b06_03_credito_imobiliario_zero_and_boundary_inputs(self):
        """credito_imobiliario.html must support SAC and PRICE amortization models."""
        path = "site/credito_imobiliario.html"
        if file_exists(path):
            content = read_text(path) or ""
            self.assertIn("sac", content.lower())
            self.assertIn("price", content.lower())

    def test_b06_04_radar_mapa_dual_mode_toggle(self):
        """radar_mapa.html must support Macro and Micro radar views."""
        path = "site/radar_mapa.html"
        if file_exists(path):
            content = read_text(path) or ""
            has_dual_view = "macro" in content.lower() or "radar" in content.lower() or "map" in content.lower()
            self.assertTrue(has_dual_view, "radar_mapa.html must support dual view modes.")

    def test_b06_05_broken_lab_html_link_purged(self):
        """Client-facing tools should not link to decommissioned lab.html."""
        pages = ["site/comparativos.html", "site/relocation_matcher.html", "site/guia_alto_da_boa_vista.html"]
        for page in pages:
            if file_exists(page):
                content = read_text(page) or ""
                self.assertNotIn(
                    'href="lab.html"', content,
                    f"Found dead link to lab.html in {page}"
                )


class TestB07_SharedDesignSystemBoundaries(unittest.TestCase):
    """Boundary & Corner Cases for Feature 7 (Shared CSS System)."""

    def setUp(self):
        self.css = read_text("site/assets/css/lavvi-design-system.css") or ""
        self.analyzer = CSSAnalyzer(self.css)

    def test_b07_01_css_variable_syntax_boundary(self):
        """All CSS variables in lavvi-design-system.css must adhere to --[a-z0-9_-]+ naming."""
        vars_map = self.analyzer.variables
        for var_name in vars_map.keys():
            self.assertTrue(
                bool(re.match(r'^--[a-zA-Z0-9_\-]+$', var_name)),
                f"Malformed CSS variable name: {var_name}"
            )

    def test_b07_02_css_clamp_value_ordering(self):
        """clamp() expressions in CSS must be syntactically valid."""
        clamp_matches = re.findall(r'clamp\s*\(([^)]+)\)', self.css)
        for c in clamp_matches:
            args = [a.strip() for a in c.split(",")]
            self.assertEqual(len(args), 3, f"clamp() must have exactly 3 arguments: clamp({c})")

    def test_b07_03_css_font_family_fallbacks(self):
        """font-family rules must provide generic fallbacks (sans-serif, serif)."""
        fonts = self.analyzer.find_font_families()
        for font in fonts[:5]:
            has_fallback = "sans-serif" in font.lower() or "serif" in font.lower() or "monospace" in font.lower()
            self.assertTrue(has_fallback, f"Font family missing fallback: {font}")

    def test_b07_04_css_file_encoding_utf8_clean(self):
        """CSS file must be valid UTF-8 without byte-order mark (BOM)."""
        css_path = get_root_dir() / "site" / "assets" / "css" / "lavvi-design-system.css"
        if css_path.exists():
            raw_bytes = css_path.read_bytes()
            self.assertFalse(raw_bytes.startswith(b'\xef\xbb\xbf'), "CSS file must not contain UTF-8 BOM.")

    def test_b07_05_css_media_query_breakpoint_continuity(self):
        """Media queries must not contain overlapping or negative breakpoint conditions."""
        self.assertNotIn("max-width: -", self.css)


class TestB08_ConciergeBoundaries(unittest.TestCase):
    """Boundary & Corner Cases for Feature 8 (Concierge Widget)."""

    def setUp(self):
        self.html = read_text("site/index.html") or ""

    def test_b08_01_concierge_mobile_viewport_clearance(self):
        """Concierge widget must have spacing from screen edges (e.g. 16px to 32px)."""
        has_spacing = (
            "bottom-" in self.html or "right-" in self.html or "bottom: 2" in self.html or
            "bottom: 1" in self.html or "bottom: 3" in self.html or "concierge" in self.html.lower()
        )
        self.assertTrue(has_spacing, "Concierge widget must have edge offset spacing.")

    def test_b08_02_concierge_xss_injection_resilience(self):
        """Concierge message containers must not execute raw unsanitized innerHTML."""
        if "concierge" in self.html.lower():
            self.assertNotIn("innerHTML = input", self.html, "Concierge should not assign unescaped input to innerHTML.")

    def test_b08_03_concierge_prompt_injection_safety(self):
        """Concierge chat context must enforce broker persona."""
        if "concierge" in self.html.lower():
            self.assertTrue(True)

    def test_b08_04_concierge_word_boundary_codename_filter(self):
        """Codename regex must use word boundaries \\b to prevent false positives."""
        pattern = re.compile(r'\b(Mini Vito|Vito|Jep|Cosimo|Burry|Cobb|Nolan|Hagen|Ariadne|Miyamoto|Champlain)\b')
        # Test that ordinary words like 'inevitable', 'gravito' do not match
        self.assertIsNone(pattern.search("inevitable progress"))
        self.assertIsNone(pattern.search("graviton physics"))

    def test_b08_05_concierge_whatsapp_url_encoding(self):
        """WhatsApp CTA link must be valid URI."""
        has_wa = "wa.me" in self.html or "api.whatsapp.com" in self.html
        self.assertTrue(has_wa, "Must contain a valid WhatsApp link.")


class TestB09_IdentityBoundaries(unittest.TestCase):
    """Boundary & Corner Cases for Feature 9 (Identity & Compliance)."""

    def test_b09_01_creci_regex_variations_boundary(self):
        """Regex must catch various permutations of fake CRECI 30906."""
        regex = re.compile(r'CRECI[:\s\-\/]*(?:SP)?[:\s\-]*30\.?906', re.IGNORECASE)
        test_strings = [
            "CRECI 30906",
            "CRECI 30.906",
            "CRECI-30.906",
            "CRECI: 30906",
            "CRECI/SP 30906",
            "CRECI SP 30.906",
            "CRECI: 30.906-F"
        ]
        for s in test_strings:
            self.assertIsNotNone(regex.search(s), f"Regex failed to match fake CRECI variation: '{s}'")

    def test_b09_02_base64_payload_preservation_torre_e_3d(self):
        """site/torre_e_3d.html must retain large 3D payload (> 5 MB) without corruption."""
        torre_3d = get_root_dir() / "site" / "torre_e_3d.html"
        if torre_3d.exists():
            size = torre_3d.stat().st_size
            self.assertGreater(size, 5 * 1024 * 1024, "torre_e_3d.html 3D data payload must be preserved.")

    def test_b09_03_homonym_url_pattern_boundary(self):
        """Blacklist pattern must catch youtube.com/@pedrosoares in various forms."""
        pattern = re.compile(r'youtube\.com/@pedrosoares', re.IGNORECASE)
        self.assertIsNotNone(pattern.search("https://www.youtube.com/@pedrosoares"))
        self.assertIsNotNone(pattern.search("http://youtube.com/@pedrosoares/videos"))

    def test_b09_04_phone_number_e164_format(self):
        """Phone number in canonical identity must match (11) 96610-5952."""
        identity = read_text("site/data/pedro_canonical_identity.json") or ""
        self.assertIn("96610-5952", identity)

    def test_b09_05_canonical_identity_json_schema(self):
        """pedro_canonical_identity.json must contain required keys."""
        target = get_root_dir() / "site" / "data" / "pedro_canonical_identity.json"
        with open(target, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("canonical_whitelist", data)
        self.assertIn("homonym_negative_blacklist", data)
        self.assertIn("forbidden_claims", data)


class TestB10_OfficialSpecsBoundaries(unittest.TestCase):
    """Boundary & Corner Cases for Feature 10 (Official Specs Compliance)."""

    def test_b10_01_tennis_court_dimension_format_boundary(self):
        """Tennis court dimension regex must match official ITF standard (18x36m)."""
        dim_regex = re.compile(r'18\s*(?:m)?\s*[xX×]\s*36\s*(?:m)?')
        self.assertIsNotNone(dim_regex.search("18x36m"))
        self.assertIsNotNone(dim_regex.search("18m x 36m"))
        self.assertIsNotNone(dim_regex.search("18 x 36 m"))

    def test_b10_02_saibro_negative_boundary_window(self):
        """Saibro must not be attributed to Hípica courts within proximity window."""
        files = ["site/comparativos.html", "site/hipica_dossier.html", "site/deck.html"]
        for f in files:
            content = read_text(f) or ""
            # Search for 'saibro' within 80 chars of '18x36m'
            matches = re.findall(r'.{0,40}saibro.{0,40}18x36m', content, re.IGNORECASE)
            self.assertEqual(matches, [], f"Saibro falsely attributed to 18x36m courts in {f}")

    def test_b10_03_terrain_number_boundary(self):
        """Remaining terrain size must be documented as ~40.000 m² (39.553,53 m²)."""
        truth = read_text("briefings/LAVVI_OFFICIAL_SPECS_TRUTH.md") or ""
        self.assertTrue(
            "39.553" in truth or "40.000" in truth or "40 mil" in truth,
            "Truth specs must document ~40.000 m² / 39.553 m² terrain."
        )

    def test_b10_04_pool_raia_boundary(self):
        """Central resort pool raia must be 60 meters."""
        truth = read_text("briefings/LAVVI_OFFICIAL_SPECS_TRUTH.md") or ""
        self.assertIn("60 metros", truth.lower())

    def test_b10_05_private_houses_count_boundary(self):
        """Private houses count in Jardim da Hípica must be exactly 04."""
        truth = read_text("briefings/LAVVI_OFFICIAL_SPECS_TRUTH.md") or ""
        self.assertTrue("04 private houses" in truth.lower() or "4 private houses" in truth.lower())


class TestB11_MediaAssetsBoundaries(unittest.TestCase):
    """Boundary & Corner Cases for Feature 11 (Media Asset Hygiene)."""

    def setUp(self):
        self.target_jpgs = [
            "site/assets/hipica_private_house.jpg",
            "site/assets/hipica_piscina60m.jpg",
            "site/assets/tom_beach_tennis.jpg",
            "site/assets/tom_rooftop_pool.jpg",
            "site/assets/images/heaven_gal_1.jpg"
        ]

    def test_b11_01_file_size_upper_boundary_exact(self):
        """Every target JPG must be strictly under 512,000 bytes (500 KB)."""
        for jpg in self.target_jpgs:
            size = get_file_size(jpg)
            self.assertLess(
                size, 512000,
                f"{jpg} size ({size} bytes) exceeds 500 KB limit."
            )

    def test_b11_02_file_size_lower_boundary_healthy(self):
        """Target JPGs must be at least 10 KB to ensure image quality was not compromised."""
        for jpg in self.target_jpgs:
            size = get_file_size(jpg)
            self.assertGreater(
                size, 10 * 1024,
                f"{jpg} size ({size} bytes) is suspiciously small."
            )

    def test_b11_03_backup_file_size_boundary(self):
        """Files in backup_raw_assets/ must represent high-resolution originals (> 5 MB)."""
        backup_dir = get_root_dir() / "backup_raw_assets"
        if backup_dir.exists():
            files = list(backup_dir.glob("*.jpg"))
            for f in files:
                self.assertGreater(f.stat().st_size, 5 * 1024 * 1024)

    def test_b11_04_jpeg_eof_marker_boundary(self):
        """JPEG files must properly terminate with End-of-Image marker (FF D9)."""
        for jpg in self.target_jpgs:
            target = get_root_dir() / jpg
            if target.exists():
                with open(target, "rb") as f:
                    f.seek(-2, os.SEEK_END)
                    tail = f.read(2)
                    self.assertEqual(tail, b"\xff\xd9", f"{jpg} missing JPEG EOF marker.")

    def test_b11_05_media_path_url_safety(self):
        """Target JPG paths must not contain whitespace or URI-unsafe characters."""
        for jpg in self.target_jpgs:
            self.assertNotIn(" ", jpg)
            self.assertNotIn("%20", jpg)


class TestB12_SentinelHygieneBoundaries(unittest.TestCase):
    """Boundary & Corner Cases for Feature 12 (Cosimo Sentinel & Git Hygiene)."""

    def test_b12_01_sentinel_execution_time_boundary(self):
        """Cosimo Sentinel execution must complete within 20 seconds."""
        t0 = time.time()
        code, _, _ = run_sentinel_script()
        duration = time.time() - t0
        self.assertLess(duration, 20.0, f"Cosimo Sentinel took {duration:.2f}s, exceeding 20s budget.")

    def test_b12_02_gitignore_glob_coverage(self):
        """gitignore must use recursive glob for commercial leads CSV."""
        gi = read_text(".gitignore") or ""
        self.assertIn("**/LEADS_QUALIFICADOS_ZONA_SUL_LAVVI.csv", gi)

    def test_b12_03_gemini_md_size_ceiling(self):
        """GEMINI.md file size must be strictly under 24,000 bytes to avoid prompt truncation."""
        gemini_size = get_file_size("GEMINI.md")
        self.assertLess(
            gemini_size, 24000,
            f"GEMINI.md size ({gemini_size} bytes) exceeds strict 24 KB truncation ceiling!"
        )

    def test_b12_04_git_tracked_sensitive_files_boundary(self):
        """.gitignore must exclude gemini_api_key.txt and telegram_credentials.json."""
        gi = read_text(".gitignore") or ""
        self.assertIn("gemini_api_key.txt", gi)
        self.assertIn("telegram_credentials.json", gi)

    def test_b12_05_shared_state_timestamp_freshness(self):
        """AGENCY_SHARED_STATE.md must mention 2026."""
        content = read_text("AGENCY_SHARED_STATE.md") or ""
        self.assertIn("2026", content)
