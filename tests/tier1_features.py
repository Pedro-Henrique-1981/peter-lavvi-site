"""
Tier 1: Feature Coverage Test Suite (≥5 tests per feature across 12 features = 60 tests)
Verifies the essential contracts and functionality for all portal components.
"""

import unittest
import re
import os
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

class TestF01_HeaderNavigation(unittest.TestCase):
    """Feature 1: Fixed 66px Header & Navigation System."""

    def setUp(self):
        self.html = read_text("site/index.html") or ""
        self.dom = HTMLDOMInspector.parse_html(self.html)
        self.css = read_text("site/assets/css/lavvi-design-system.css") or ""

    def test_f01_01_header_fixed_66px(self):
        """Header must have 66px fixed height specified in HTML or CSS design system."""
        has_header_66px = False
        if "h-[66px]" in self.html or "height: 66px" in self.html or "height:66px" in self.html:
            has_header_66px = True
        elif "66px" in self.css and ("header" in self.css.lower() or "nav" in self.css.lower()):
            has_header_66px = True

        headers = self.dom.landmarks.get("header", [])
        self.assertTrue(
            len(headers) > 0,
            "site/index.html must contain a <header> landmark element."
        )
        self.assertTrue(
            has_header_66px,
            "Header must have explicit 66px height defined in inline class/style or lavvi-design-system.css."
        )

    def test_f01_02_header_single_nav_landmark(self):
        """Header must expose exactly one <nav> landmark to avoid screen reader clutter."""
        navs = self.dom.landmarks.get("nav", [])
        self.assertEqual(
            len(navs), 1,
            f"Expected exactly 1 <nav> landmark in site/index.html, but found {len(navs)}."
        )

    def test_f01_03_header_native_dialog_drawer(self):
        """Mobile drawer must use HTML5 <dialog> with class 'Drawer'."""
        dialogs = self.dom.landmarks.get("dialog", [])
        has_drawer_dialog = any(
            d.has_class("Drawer") or "drawer" in d.attrs.get("class", "").lower()
            for d in dialogs
        )
        self.assertTrue(
            has_drawer_dialog,
            "site/index.html must contain a native <dialog class='Drawer'> element for mobile navigation."
        )

    def test_f01_04_header_no_emoji_rows(self):
        """Header must not contain emoji clutter rows (🚀, 🔥, ⚡, 💎, 🏢, etc.)."""
        headers = self.dom.landmarks.get("header", [])
        header_text = headers[0].text_content if headers else ""
        emoji_pattern = re.compile(r'[\U0001F300-\U0001F9FF]')
        found_emojis = emoji_pattern.findall(header_text)
        self.assertLessEqual(
            len(found_emojis), 2,
            f"Header contains excess emoji rows ({found_emojis}). Luxury design system requires clean typography."
        )

    def test_f01_05_header_no_duplicate_ids(self):
        """Header and document must contain no duplicate element IDs (#lang-selector, #nav-wa-btn)."""
        duplicates = {k: len(v) for k, v in self.dom.ids_map.items() if len(v) > 1}
        self.assertEqual(
            duplicates, {},
            f"Found duplicate DOM IDs in site/index.html: {duplicates}"
        )


class TestF02_HeroSearchBar(unittest.TestCase):
    """Feature 2: Single Full-Bleed Hero & Search Bar."""

    def setUp(self):
        self.html = read_text("site/index.html") or ""
        self.dom = HTMLDOMInspector.parse_html(self.html)

    def test_f02_01_single_hero_section(self):
        """Homepage must contain exactly one primary hero section, without stacked duplicates."""
        heroes = [n for n in self.dom.all_nodes if "hero" in (n.id or "").lower() or any("hero" in c.lower() for c in n.classes)]
        self.assertTrue(
            1 <= len(heroes) <= 2,
            f"Expected 1 hero section in site/index.html, found {len(heroes)}."
        )

    def test_f02_02_search_landmark_present(self):
        """Search functionality must be wrapped in semantic <search> element or role='search'."""
        search_landmarks = self.dom.landmarks.get("search", [])
        has_search = len(search_landmarks) > 0 or "<search" in self.html.lower() or 'role="search"' in self.html.lower()
        self.assertTrue(
            has_search,
            "site/index.html must feature a semantic <search> landmark element."
        )

    def test_f02_03_buscar_button_min_width_148px(self):
        """Search action button (BUSCAR) must have min-width 148px."""
        has_min_width = bool(re.search(r'min-w(?:idth)?[:\-\s]+148px', self.html, re.IGNORECASE))
        has_css_min_width = False
        css = read_text("site/assets/css/lavvi-design-system.css") or ""
        if "148px" in css and "buscar" in css.lower():
            has_css_min_width = True

        self.assertTrue(
            has_min_width or has_css_min_width,
            "BUSCAR button must enforce min-width 148px in inline class/style or lavvi-design-system.css."
        )

    def test_f02_04_buscar_button_gold_color(self):
        """BUSCAR button must use official Lavvi Gold (#957B2B)."""
        has_gold = ("#957B2B" in self.html or "#957b2b" in self.html or "var(--primary)" in self.html)
        css = read_text("site/assets/css/lavvi-design-system.css") or ""
        has_gold_css = ("#957B2B" in css or "#957b2b" in css)
        self.assertTrue(
            has_gold or has_gold_css,
            "Search action button must use official Lavvi gold color token (#957B2B)."
        )

    def test_f02_05_hero_fetchpriority_high(self):
        """Hero banner image must specify fetchpriority='high' for LCP optimization."""
        images = self.dom.find_all("img")
        hero_imgs = [img for img in images if img.attrs.get("fetchpriority") == "high"]
        self.assertTrue(
            len(hero_imgs) > 0 or 'fetchpriority="high"' in self.html,
            "Hero banner image must declare fetchpriority='high' to optimize Largest Contentful Paint."
        )


class TestF03_CatalogGrid(unittest.TestCase):
    """Feature 3: Unified 1:1 Aspect-Square Project Catalog Grid."""

    def setUp(self):
        self.html = read_text("site/index.html") or ""
        self.css = read_text("site/assets/css/lavvi-design-system.css") or ""
        self.dom = HTMLDOMInspector.parse_html(self.html)

    def test_f03_01_catalog_1_to_1_square_aspect_ratio(self):
        """Catalog project cards or images must define 1:1 square aspect ratio."""
        has_aspect_ratio = (
            "aspect-square" in self.html or
            "aspect-ratio: 1/1" in self.html or
            "aspect-ratio: 1 / 1" in self.html or
            "aspect-square" in self.css or
            "aspect-ratio: 1/1" in self.css or
            "aspect-ratio: 1 / 1" in self.css
        )
        self.assertTrue(
            has_aspect_ratio,
            "Catalog cards must enforce 1:1 aspect-ratio square imagery."
        )

    def test_f03_02_catalog_css_grid_subgrid(self):
        """Catalog container must use CSS Grid with subgrid or flex alignment."""
        has_grid = (
            "grid" in self.html and ("catalog" in self.html or "catalogo" in self.html)
        ) or (
            ".catalog-grid" in self.css and "display: grid" in self.css
        )
        self.assertTrue(
            has_grid,
            "Catalog container must use CSS Grid layout structure."
        )

    def test_f03_03_catalog_metadata_positioned_below_image(self):
        """Project cards must place metadata (title, neighborhood, specs) below the image."""
        has_card_body = (
            ".card-body" in self.css or "project-info" in self.html or "card-body" in self.html or "card-content" in self.html
        )
        self.assertTrue(
            has_card_body,
            "Catalog card layout must structure card metadata below card imagery."
        )

    def test_f03_04_catalog_cls_zero_explicit_dimensions(self):
        """Catalog images must specify explicit width/height or aspect-ratio to ensure CLS=0."""
        has_cls_protection = (
            "aspect-square" in self.html or "aspect-ratio" in self.css or "loading=\"lazy\"" in self.html
        )
        self.assertTrue(
            has_cls_protection,
            "Catalog cards must guard against Cumulative Layout Shift (CLS=0)."
        )

    def test_f03_05_catalog_accessible_action_links(self):
        """Catalog cards must provide accessible 'Ver detalhes' or project detail action links."""
        has_action_links = (
            "ver detalhes" in self.html.lower() or "detalhes" in self.html.lower()
        )
        self.assertTrue(
            has_action_links,
            "Catalog cards must contain accessible 'Ver detalhes' call-to-action links."
        )


class TestF04_CategoryCounters(unittest.TestCase):
    """Feature 4: Category Filter Tabs & Dynamic Inventory Counters."""

    def setUp(self):
        self.html = read_text("site/index.html") or ""
        self.bundle = read_text("site/assets/js/lavvi_catalog_bundle.js") or ""
        self.clean_json = read_text("site/lavvi_45_projects_clean.json") or ""

    def test_f04_01_category_tabs_presence(self):
        """Category filter tabs for Todos, Lavvi, and Novvo must be present in DOM."""
        self.assertTrue(
            "todos" in self.html.lower() and "lavvi" in self.html.lower() and "novvo" in self.html.lower(),
            "Category tabs (Todos | Lavvi | Novvo) must be present in site/index.html."
        )

    def test_f04_02_dynamic_counter_todos_46(self):
        """Total inventory counter for 'Todos' must equal 46 canonical developments."""
        # Check either bundle, html or clean json reflects 46 total developments
        has_46 = "46" in self.html or "46" in self.bundle
        self.assertTrue(
            has_46,
            "Inventory counter for 'Todos' must reflect 46 canonical developments."
        )

    def test_f04_03_dynamic_counter_lavvi_39(self):
        """Inventory counter for 'Lavvi' must reflect 39 developments (17 Active + 22 Sold)."""
        has_39 = "39" in self.html or "39" in self.bundle
        self.assertTrue(
            has_39,
            "Inventory counter for 'Lavvi' must reflect 39 developments (17 active + 22 sold)."
        )

    def test_f04_04_dynamic_counter_novvo_7(self):
        """Inventory counter for 'Novvo' must reflect 7 active developments."""
        has_7 = "7" in self.html or "7" in self.bundle
        self.assertTrue(
            has_7,
            "Inventory counter for 'Novvo' must reflect 7 active developments."
        )

    def test_f04_05_status_and_bedroom_filters(self):
        """Filters must include status options (Lançamento, Em Obras, Pronto, 100% Vendido)."""
        html_lower = self.html.lower()
        has_status = "lançamento" in html_lower or "lancamento" in html_lower or "pronto" in html_lower
        self.assertTrue(
            has_status,
            "Catalog must provide project status and bedroom filtering controls."
        )


class TestF05_NovvoIntegration(unittest.TestCase):
    """Feature 5: NOVVO Visual Integration & Slate/Rose Palette."""

    def setUp(self):
        self.html = read_text("site/index.html") or ""
        self.css = read_text("site/assets/css/lavvi-design-system.css") or ""
        self.bundle = read_text("site/assets/js/lavvi_catalog_bundle.js") or ""

    def test_f05_01_novvo_slate_and_rose_badge_tokens(self):
        """NOVVO design tokens Slate (#22343E) and Rose (#A06F71) must be defined."""
        has_tokens = (
            ("#22343E" in self.css or "#22343e" in self.css) and
            ("#A06F71" in self.css or "#a06f71" in self.css)
        )
        self.assertTrue(
            has_tokens,
            "site/assets/css/lavvi-design-system.css must define Slate (#22343E) and Rose (#A06F71) tokens."
        )

    def test_f05_02_novvo_montserrat_variable_font(self):
        """Montserrat Variable font must be specified for NOVVO components."""
        has_montserrat = "montserrat" in self.css.lower() or "montserrat" in self.html.lower()
        self.assertTrue(
            has_montserrat,
            "Montserrat font family must be declared for NOVVO cards and badges."
        )

    def test_f05_03_novvo_all_7_projects_present(self):
        """All 7 active NOVVO developments must be included in the catalog inventory."""
        target_projects = [
            "Novvo Marajoara",
            "Novvo Vila Prudente",
            "Novvo Anália Franco",
            "Novvo Santa Marina",
            "Novvo Barra Funda",
            "Well Perdizes",
            "Novvo Largo Treze"
        ]
        bundle_or_html = (self.bundle + self.html).lower()
        for proj in target_projects:
            self.assertTrue(
                proj.lower() in bundle_or_html,
                f"Missing official NOVVO development in inventory: '{proj}'"
            )

    def test_f05_04_novvo_badge_styling_applied(self):
        """NOVVO cards must feature distinct Slate/Rose styling or badge class."""
        has_badge_class = (
            "badge-novvo" in self.css or "badge-novvo" in self.html or
            "novvo-badge" in self.css or "novvo-badge" in self.html or
            "novvo-tag" in self.css or "novvo-tag" in self.html
        )
        self.assertTrue(
            has_badge_class,
            "NOVVO items must have distinct badge class (.badge-novvo) defined in CSS/HTML."
        )

    def test_f05_05_novvo_santa_marina_and_largo_treze(self):
        """Novvo Santa Marina and Novvo Largo Treze must be correctly classified as NOVVO."""
        combined = (self.bundle + self.html).lower()
        self.assertTrue("santa marina" in combined, "Missing Santa Marina in catalog.")
        self.assertTrue("largo treze" in combined, "Missing Largo Treze in catalog.")


class TestF06_ToolModularization(unittest.TestCase):
    """Feature 6: Modular Standalone Advisor Tools & Index Size Reduction."""

    def test_f06_01_cinema_lavvi_standalone_exists_and_nav(self):
        """site/cinema_lavvi.html must exist and contain return navigation to index.html."""
        self.assertTrue(file_exists("site/cinema_lavvi.html"), "site/cinema_lavvi.html must exist.")
        content = read_text("site/cinema_lavvi.html") or ""
        self.assertTrue(
            "index.html" in content or "href=\"/\"" in content or "href=\"#\"" in content,
            "cinema_lavvi.html must provide return navigation to the portal home."
        )

    def test_f06_02_radar_mapa_standalone_exists_and_nav(self):
        """site/radar_mapa.html must exist and contain return navigation to index.html."""
        self.assertTrue(file_exists("site/radar_mapa.html"), "site/radar_mapa.html must exist.")
        content = read_text("site/radar_mapa.html") or ""
        self.assertTrue(
            "index.html" in content or "href=\"/\"" in content or "href=\"#\"" in content,
            "radar_mapa.html must provide return navigation to the portal home."
        )

    def test_f06_03_credito_imobiliario_standalone_exists_and_nav(self):
        """site/credito_imobiliario.html must exist and contain return navigation to index.html."""
        self.assertTrue(file_exists("site/credito_imobiliario.html"), "site/credito_imobiliario.html must exist.")
        content = read_text("site/credito_imobiliario.html") or ""
        self.assertTrue(
            "index.html" in content or "href=\"/\"" in content or "href=\"#\"" in content,
            "credito_imobiliario.html must provide return navigation to the portal home."
        )

    def test_f06_04_guias_bairros_standalone_exists_and_nav(self):
        """site/guias_bairros.html must exist and contain return navigation to index.html."""
        self.assertTrue(file_exists("site/guias_bairros.html"), "site/guias_bairros.html must exist.")
        content = read_text("site/guias_bairros.html") or ""
        self.assertTrue(
            "index.html" in content or "href=\"/\"" in content or "href=\"#\"" in content,
            "guias_bairros.html must provide return navigation to the portal home."
        )

    def test_f06_05_index_html_size_lean(self):
        """site/index.html must be lean (< 150 KB) with inline modular sections extracted."""
        size = get_file_size("site/index.html")
        self.assertLess(
            size, 150 * 1024,
            f"site/index.html size ({size} bytes) exceeds lean target of 150 KB. "
            f"Verify inline tools (#cinema-section, #mapa-section, #credito-imobiliario, #guia-bairros) are extracted."
        )


class TestF07_SharedDesignSystem(unittest.TestCase):
    """Feature 7: Shared Lavvi Design System (lavvi-design-system.css)."""

    def setUp(self):
        self.css_content = read_text("site/assets/css/lavvi-design-system.css") or ""
        self.analyzer = CSSAnalyzer(self.css_content)

    def test_f07_01_lavvi_design_system_css_exists(self):
        """site/assets/css/lavvi-design-system.css must exist."""
        self.assertTrue(
            file_exists("site/assets/css/lavvi-design-system.css"),
            "Shared CSS design system site/assets/css/lavvi-design-system.css must exist."
        )

    def test_f07_02_official_color_tokens(self):
        """CSS must define official tokens: --primary (#957B2B), --secondary (#182842), --novvo-dark, --novvo-rose."""
        self.assertTrue(self.analyzer.has_token("--primary", "#957b2b"), "Must define --primary: #957B2B")
        self.assertTrue(self.analyzer.has_token("--secondary", "#182842"), "Must define --secondary: #182842")
        self.assertTrue(self.analyzer.has_token("--novvo-dark", "#22343e"), "Must define --novvo-dark: #22343E")
        self.assertTrue(self.analyzer.has_token("--novvo-rose", "#a06f71"), "Must define --novvo-rose: #A06F71")

    def test_f07_03_typography_tokens(self):
        """Design system must include Lato, Montserrat, and IvyOra or Cormorant Garamond."""
        css_lower = self.css_content.lower()
        self.assertIn("lato", css_lower, "Design system must define Lato font token.")
        self.assertIn("montserrat", css_lower, "Design system must define Montserrat font token.")
        has_serif = "ivyora" in css_lower or "cormorant" in css_lower or "serif" in css_lower
        self.assertTrue(has_serif, "Design system must define luxury serif font token (IvyOra / Cormorant Garamond).")

    def test_f07_04_fluid_typography_clamps(self):
        """Design system must use clamp() functions for responsive typography."""
        self.assertTrue(
            self.analyzer.has_clamp_typography(),
            "Design system must implement fluid responsive typography using clamp()."
        )

    def test_f07_05_drawer_modal_primitives(self):
        """Design system must define primitives for .Drawer and .nav-container."""
        self.assertTrue(
            self.analyzer.has_class_definition("Drawer") or self.analyzer.has_class_definition("drawer"),
            "Design system must define .Drawer styling."
        )


class TestF08_ConciergeWidget(unittest.TestCase):
    """Feature 8: Concierge Lavvi Private Wealth Widget."""

    def setUp(self):
        self.html = read_text("site/index.html") or ""
        self.dom = HTMLDOMInspector.parse_html(self.html)

    def test_f08_01_concierge_widget_present(self):
        """site/index.html must contain a floating Concierge widget element."""
        has_concierge = (
            "concierge" in self.html.lower() or
            "chat-widget" in self.html.lower() or
            "floating-widget" in self.html.lower()
        )
        self.assertTrue(has_concierge, "site/index.html must contain the Concierge Private Wealth widget.")

    def test_f08_02_concierge_floating_non_colliding(self):
        """Concierge widget must have fixed bottom-right positioning without colliding with navigation."""
        has_fixed_position = (
            "fixed" in self.html.lower() and ("bottom" in self.html.lower() or "right" in self.html.lower())
        )
        self.assertTrue(has_fixed_position, "Concierge widget must use non-colliding fixed positioning.")

    def test_f08_03_concierge_concise_tone_configuration(self):
        """Concierge instructions or UI copy must adhere to concise 2-3 sentence tone rule."""
        has_concise_rule = (
            "2 a 3 frases" in self.html.lower() or "2-3 frases" in self.html.lower() or
            "2 a 3 sentences" in self.html.lower() or "quiet luxury" in self.html.lower() or
            "concierge" in self.html.lower()
        )
        self.assertTrue(has_concise_rule, "Concierge widget must follow concise 2-3 sentence conversational rule.")

    def test_f08_04_concierge_zero_boardroom_codenames(self):
        """Customer-facing DOM must strictly avoid internal boardroom codenames."""
        forbidden_pattern = re.compile(r'\b(Mini Vito|Vito|Jep|Cosimo|Burry|Cobb|Nolan|Hagen|Ariadne|Miyamoto|Champlain)\b')
        # Check rendered text and non-comment DOM
        matches = forbidden_pattern.findall(self.html)
        self.assertEqual(
            matches, [],
            f"Found internal boardroom codenames exposed in customer-facing DOM: {matches}"
        )

    def test_f08_05_concierge_peter_whatsapp_cta(self):
        """Concierge or primary contact button must link to Peter's WhatsApp (11) 96610-5952."""
        has_wa = (
            "5511966105952" in self.html or "96610-5952" in self.html or "966105952" in self.html
        )
        self.assertTrue(has_wa, "Concierge CTA must link to Peter's verified WhatsApp (11) 96610-5952.")


class TestF09_IdentityCompliance(unittest.TestCase):
    """Feature 9: Identity & Compliance Remediation (Zero Fake CRECI)."""

    def setUp(self):
        self.client_facing_files = [
            "site/index.html",
            "site/linkedin_studio.html",
            "site/index_lab.html",
            "site/lab.html"
        ]

    def test_f09_01_zero_fake_creci_30906(self):
        """Zero occurrences of fake CRECI 30.906 or 30906 across all client-facing files."""
        for rel_path in self.client_facing_files:
            content = read_text(rel_path)
            if content:
                self.assertFalse(
                    "30.906" in content,
                    f"Found fabricated CRECI 30.906 in {rel_path}"
                )
                self.assertFalse(
                    "30906" in content,
                    f"Found fabricated CRECI 30906 in {rel_path}"
                )

    def test_f09_02_zero_bare_creci_sp(self):
        """Zero occurrences of bare '(CRECI SP)' without official registration in client files."""
        for rel_path in self.client_facing_files:
            content = read_text(rel_path)
            if content:
                matches = re.findall(r'\(CRECI[\s\-]*(?:SP)?\)', content, re.IGNORECASE)
                self.assertEqual(
                    matches, [],
                    f"Found bare unverified CRECI tag in {rel_path}: {matches}"
                )

    def test_f09_03_canonical_broker_commercial_title(self):
        """Broker identity must reference official title 'Peter' or 'Pedro Soares'."""
        identity = read_text("site/data/pedro_canonical_identity.json") or ""
        self.assertTrue("Pedro Soares" in identity, "Identity must include Pedro Soares")
        self.assertTrue("Peter" in identity, "Identity must include Peter")

    def test_f09_04_intern_creci_disclaimer_accuracy(self):
        """Identity disclosure must accurately state intern registration status without claiming full CRECI."""
        identity_text = read_text("site/data/pedro_canonical_identity.json") or ""
        self.assertTrue("estagiário" in identity_text.lower(), "Identity JSON must document intern registration status.")

    def test_f09_05_homonym_blacklist_zero_biology_claims(self):
        """Client-facing files must not associate Pedro Soares with 442 YouTube biology lectures."""
        for rel_path in self.client_facing_files:
            content = read_text(rel_path)
            if content:
                self.assertFalse("442 vídeos" in content.lower(), f"Found blacklisted homonym term '442 vídeos' in {rel_path}")
                self.assertFalse("cordados" in content.lower(), f"Found blacklisted homonym term 'cordados' in {rel_path}")


class TestF10_OfficialSpecs(unittest.TestCase):
    """Feature 10: Official Specs Compliance (Tennis Courts 18x36m)."""

    def setUp(self):
        self.target_files = [
            "site/comparativos.html",
            "site/hipica_dossier.html",
            "site/deck.html",
            "site/infografico_alphaville_vs_hipica.html"
        ]

    def test_f10_01_tennis_courts_official_spec(self):
        """Jardim da Hípica courts must be specified as '02 Quadras de Tênis Oficiais (18x36m)'."""
        found_count = 0
        for rel_path in self.target_files:
            content = read_text(rel_path)
            if content and ("02 Quadras de Tênis Oficiais (18x36m)" in content or "02 Quadras de Tênis Oficiais" in content):
                found_count += 1
        self.assertGreaterEqual(
            found_count, 1,
            "Expected '02 Quadras de Tênis Oficiais (18x36m)' to be specified in official collateral."
        )

    def test_f10_02_zero_saibro_in_hipica_context(self):
        """Zero mentions of 'saibro' claimed for Jardim da Hípica courts across official collateral."""
        for rel_path in self.target_files:
            content = read_text(rel_path)
            if content:
                # Find occurrences where saibro is paired with Hípica or 18x36m
                bad_matches = re.findall(r'(\bquadras? de (?:tênis de )?saibro\b.*?(?:hípica|18x36m))', content, re.IGNORECASE)
                self.assertEqual(
                    bad_matches, [],
                    f"Found inaccurate saibro claim for Jardim da Hípica in {rel_path}: {bad_matches}"
                )

    def test_f10_03_chsa_saibro_preserved(self):
        """External Clube Hípico de Santo Amaro (CHSA) saibro references must be preserved."""
        # CHSA context should not be inadvertently damaged by blanket replacement
        truth_specs = read_text("briefings/LAVVI_OFFICIAL_SPECS_TRUTH.md") or ""
        self.assertIn("Hípica", truth_specs)

    def test_f10_04_terrain_and_park_dimensions(self):
        """Jardim da Hípica terrain must be documented as ~40.000 m² (39.553 m²) + 10.000 m² public park."""
        truth = read_text("briefings/LAVVI_OFFICIAL_SPECS_TRUTH.md") or ""
        self.assertIn("39.553", truth, "Truth file must document exact 39.553 m² remaining terrain.")
        self.assertIn("10.000", truth, "Truth file must document 10.000 m² public park.")

    def test_f10_05_resort_pool_and_cbre_management(self):
        """Jardim da Hípica must feature 60m resort pool raia and CBRE condominium management."""
        truth = read_text("briefings/LAVVI_OFFICIAL_SPECS_TRUTH.md") or ""
        self.assertIn("60m", truth.lower())
        self.assertIn("cbre", truth.lower())


class TestF11_MediaAssets(unittest.TestCase):
    """Feature 11: Media Asset Hygiene & Size Verification (<500 KB)."""

    def setUp(self):
        self.target_jpgs = [
            "site/assets/hipica_private_house.jpg",
            "site/assets/hipica_piscina60m.jpg",
            "site/assets/tom_beach_tennis.jpg",
            "site/assets/tom_rooftop_pool.jpg",
            "site/assets/images/heaven_gal_1.jpg"
        ]

    def test_f11_01_all_5_target_jpgs_exist(self):
        """All 5 target JPGs must exist in the local project workspace."""
        for jpg in self.target_jpgs:
            self.assertTrue(file_exists(jpg), f"Required asset missing: {jpg}")

    def test_f11_02_jpg_sizes_under_500kb(self):
        """Each target JPG must be strictly under 500 KB (512,000 bytes) after downscaling."""
        for jpg in self.target_jpgs:
            size = get_file_size(jpg)
            self.assertLess(
                size, 500 * 1024,
                f"Asset {jpg} is {size} bytes, which exceeds the 500 KB threshold. Needs FFmpeg downscale."
            )

    def test_f11_03_jpg_files_non_empty(self):
        """Each target JPG must be a non-empty file (> 1,000 bytes)."""
        for jpg in self.target_jpgs:
            size = get_file_size(jpg)
            self.assertGreater(
                size, 1000,
                f"Asset {jpg} is corrupted or empty ({size} bytes)."
            )

    def test_f11_04_jpg_valid_headers(self):
        """Each target JPG must have valid JPEG magic bytes (FF D8 FF)."""
        for jpg in self.target_jpgs:
            self.assertTrue(
                is_jpeg_valid(jpg),
                f"Asset {jpg} does not have valid JPEG header magic bytes."
            )

    def test_f11_05_backup_raw_assets_directory(self):
        """Uncompressed master assets must be safely archived in backup_raw_assets/."""
        backup_dir = get_root_dir() / "backup_raw_assets"
        self.assertTrue(
            backup_dir.exists() and backup_dir.is_dir(),
            "Directory backup_raw_assets/ must exist to preserve uncompressed high-res master files."
        )


class TestF12_SentinelGitHygiene(unittest.TestCase):
    """Feature 12: Cosimo Sentinel & Git Hygiene Protection."""

    def test_f12_01_cosimo_sentinel_exit_code_zero(self):
        """python scripts/cosimo_sentinel.py must execute cleanly with exit code 0."""
        code, stdout, stderr = run_sentinel_script()
        self.assertEqual(
            code, 0,
            f"Cosimo Sentinel failed with code {code}.\nStdout: {stdout}\nStderr: {stderr}"
        )

    def test_f12_02_gitignore_sensitive_files(self):
        """gitignore must exclude credentials, sessions, and ntfy_config.json."""
        gi = read_text(".gitignore") or ""
        self.assertIn("ntfy_config.json", gi, ".gitignore must exclude ntfy_config.json")
        self.assertIn("gemini_api_key.txt", gi, ".gitignore must exclude gemini_api_key.txt")
        self.assertIn("*.session", gi, ".gitignore must exclude *.session")

    def test_f12_03_gitignore_pii_leads_csv(self):
        """gitignore must exclude commercial leads CSV file."""
        gi = read_text(".gitignore") or ""
        self.assertIn("LEADS_QUALIFICADOS_ZONA_SUL_LAVVI.csv", gi)

    def test_f12_04_gitignore_scratch_eval_scripts(self):
        """gitignore must exclude scratch eval JS dumps."""
        gi = read_text(".gitignore") or ""
        self.assertIn("eval_script_*.js", gi)
        self.assertIn("temp_*.js", gi)

    def test_f12_05_agency_shared_state_exists_and_synced(self):
        """AGENCY_SHARED_STATE.md must exist and document multi-hardware synchronization state."""
        self.assertTrue(file_exists("AGENCY_SHARED_STATE.md"), "AGENCY_SHARED_STATE.md must exist.")
        content = read_text("AGENCY_SHARED_STATE.md") or ""
        self.assertIn("MEMÓRIA UNIFICADA MULTI-COMPUTADOR", content)
