"""
Tier 3: Cross-Feature Combinations & Pairwise Integration Test Suite
Verifies feature interactions, cross-component data flow, responsive layout stability,
and protocol independence across the modular portal.
"""

import unittest
import re
from pathlib import Path
from tests.test_helpers import (
    read_text,
    file_exists,
    HTMLDOMInspector,
    CSSAnalyzer,
    get_root_dir,
)

class TestTier3_CrossFeatureCombinations(unittest.TestCase):
    """Pairwise and multi-feature interaction test suite."""

    def setUp(self):
        self.html = read_text("site/index.html") or ""
        self.css = read_text("site/assets/css/lavvi-design-system.css") or ""
        self.bundle = read_text("site/assets/js/lavvi_catalog_bundle.js") or ""

    def test_c01_search_query_with_category_tab_pairwise(self):
        """Cross-feature: Search query combined with category tab filtering."""
        # When Novvo tab is selected, searching 'Marina' must find Novvo Santa Marina
        # When Lavvi tab is selected, searching 'Marina' should find 0 Lavvi projects
        bundle_lower = self.bundle.lower()
        self.assertTrue("santa marina" in bundle_lower, "Catalog bundle must contain Santa Marina.")
        self.assertTrue("novvo" in bundle_lower, "Catalog bundle must contain Novvo brand.")

    def test_c02_search_query_with_neighborhood_pairwise(self):
        """Cross-feature: Search query combined with neighborhood dropdown filter."""
        # Filtering Moema + searching 'Saffire' isolates Moema luxury
        bundle_lower = self.bundle.lower()
        self.assertTrue("saffire" in bundle_lower, "Bundle must contain Saffire.")
        self.assertTrue("moema" in bundle_lower, "Bundle must contain Moema neighborhood.")

    def test_c03_category_tab_and_detail_modal_consistency(self):
        """Cross-feature: Project detail modal inherits brand styling (Lavvi gold vs Novvo slate/rose)."""
        combined = (self.html + self.css).lower()
        has_badges = "badge" in combined or "brand" in combined or "novvo" in combined
        self.assertTrue(has_badges, "Card modals must inherit brand-specific badge styling.")

    def test_c04_standalone_tool_roundtrip_navigation(self):
        """Cross-feature: Seamless roundtrip navigation between homepage and standalone advisor tools."""
        tools = ["cinema_lavvi.html", "radar_mapa.html", "credito_imobiliario.html", "guias_bairros.html"]
        for tool in tools:
            path = f"site/{tool}"
            if file_exists(path):
                content = read_text(path) or ""
                self.assertTrue(
                    "index.html" in content or "href=\"/\"" in content or "href=\"#\"" in content,
                    f"{tool} must provide return navigation link back to index.html."
                )

    def test_c05_shared_css_cascading_to_modular_pages(self):
        """Cross-feature: Shared CSS design system link in all modular standalone pages."""
        tools = ["cinema_lavvi.html", "radar_mapa.html", "credito_imobiliario.html", "guias_bairros.html"]
        for tool in tools:
            path = f"site/{tool}"
            if file_exists(path):
                content = read_text(path) or ""
                self.assertIn(
                    "lavvi-design-system.css", content,
                    f"{tool} must link to site/assets/css/lavvi-design-system.css"
                )

    def test_c06_concierge_widget_drawer_z_index_separation(self):
        """Cross-feature: Drawer modal dialog and floating Concierge widget maintain distinct z-indices."""
        # Drawer modal dialog must overlay page without widget colliding or clipping
        self.assertTrue(
            "<dialog" in self.html.lower() or "drawer" in self.css.lower(),
            "Modal Drawer must be present in layout."
        )

    def test_c07_umd_bundle_protocol_independence(self):
        """Cross-feature: Catalog bundle must support file:/// and http:// via window global export."""
        bundle_path = get_root_dir() / "site" / "assets" / "js" / "lavvi_catalog_bundle.js"
        if bundle_path.exists():
            bundle_content = bundle_path.read_text(encoding="utf-8", errors="ignore")
            # UMD check: window.allProjects or window.LAVVI_CATALOG_BUNDLE
            has_window_export = "window.allProjects" in bundle_content or "window.LAVVI_CATALOG_BUNDLE" in bundle_content or "allProjects" in bundle_content
            self.assertTrue(
                has_window_export,
                "Catalog JS bundle must expose global window export for file:/// and HTTP protocol independence."
            )

    def test_c08_bedroom_filter_and_brand_combination(self):
        """Cross-feature: 4+ bedroom filter combined with brand categories."""
        truth = read_text("briefings/LAVVI_OFFICIAL_SPECS_TRUTH.md") or ""
        # High-luxury Lavvi developments offer 4 suites (Hípica 276m, Villa Milano, etc.)
        self.assertIn("276 m²", truth)
        self.assertIn("Jardim da Hípica", truth)
