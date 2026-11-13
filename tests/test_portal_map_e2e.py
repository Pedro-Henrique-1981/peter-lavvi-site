#!/usr/bin/env python3
"""
tests/test_portal_map_e2e.py
================================================================================
LAVVI PRIVATE WEALTH & MEDIA AGENCY — PORTAL MAP E2E VERIFICATION SUITE
Empirical 4-Tier Opaque-Box Test Suite for Interactive SP Portfolio Radar Map
Integration in site/index.html and site/assets/js/portal_map_engine.js.
Pedro Soares • Lavvi Private Wealth (WhatsApp: +55 11 96610-5952)

Architecture:
  - Tier 1: Feature Coverage (All 6 toggles, Modal DOM, Schema.org SEO, Anti-Scroll-Trap, Navigation)
  - Tier 2: Boundary & Corner Cases (SP Coordinates Bounding Box, WCAG 2.5.5 Touch Targets, Payload Size, Unique IDs, Zero Saibro)
  - Tier 3: Cross-Feature Combinations (Catalog + Map Cross-Nav, Focus Trap Tab/Shift+Tab, ESC & Focus Restoration, Background Inertness, Concurrency Transitions)
  - Tier 4: Real-World Scenarios (UHNW Investor Jardim da Hípica, Novvo HIS/HMP Notice, T.O.M. Paraíso Airbnb Cartorial Minute, Competitor Asymmetry, Identity & Air-Gap)

Usage:
  python tests/test_portal_map_e2e.py
  python tests/test_portal_map_e2e.py --tier 1
  python tests/test_portal_map_e2e.py --tier 2
  python tests/test_portal_map_e2e.py --tier 3
  python tests/test_portal_map_e2e.py --tier 4
  python tests/test_portal_map_e2e.py --verbose
================================================================================
"""

import os
import sys
import io
import re
import json
import subprocess
import unittest
from pathlib import Path
from html.parser import HTMLParser
from typing import Dict, List, Optional, Tuple, Any

# Force UTF-8 stdout on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_HTML = BASE_DIR / "site" / "index.html"
ENGINE_JS = BASE_DIR / "site" / "assets" / "js" / "portal_map_engine.js"
CATALOG_JS = BASE_DIR / "site" / "assets" / "js" / "lavvi_catalog_bundle.js"
POI_JSON = BASE_DIR / "site" / "poi_radar_data.json"
CSS_FILE = BASE_DIR / "site" / "assets" / "css" / "lavvi-design-system.css"


# ==============================================================================
# LIGHTWEIGHT DOM & CSS INSPECTORS (STANDARD LIBRARY)
# ==============================================================================

class DOMParserHelper(HTMLParser):
    """Resilient HTML parser for attribute extraction, ID tracking, and structure."""
    def __init__(self):
        super().__init__()
        self.tags: List[Dict[str, Any]] = []
        self.ids_count: Dict[str, int] = {}
        self.elements_by_id: Dict[str, Dict[str, Any]] = {}
        self.all_ids: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]):
        attr_dict = {k.lower(): (v or "") for k, v in attrs}
        node = {
            "tag": tag.lower(),
            "attrs": attr_dict,
        }
        self.tags.append(node)
        node_id = attr_dict.get("id")
        if node_id:
            self.all_ids.append(node_id)
            self.ids_count[node_id] = self.ids_count.get(node_id, 0) + 1
            if node_id not in self.elements_by_id:
                self.elements_by_id[node_id] = node


def parse_index_dom() -> DOMParserHelper:
    parser = DOMParserHelper()
    content = INDEX_HTML.read_text(encoding="utf-8", errors="ignore")
    parser.feed(content)
    return parser


# ==============================================================================
# TIER 1: FEATURE COVERAGE (ALL 6 TOGGLES, MODAL DOM, SCHEMA.ORG, SCROLL TRAP, NAV)
# ==============================================================================

class TestPortalMapTier1_FeatureCoverage(unittest.TestCase):
    """
    Tier 1 tests verify all direct functional specifications of the portal map:
    - 6 segmented filter pills and exact marker counts (Todos: 46, Lançamentos: 17,
      Novvo: 7, Entregues: 22, Lifestyle: 348, Concorrência: 12)
    - Modal DOM landmarks, 2x2 KPI grid, and Pedro Soares WhatsApp CTA
    - Schema.org JSON-LD local SEO generation
    - Anti-scroll-trap configuration and visual hint
    - Navigation anchors in header, mobile drawer, and standalone GIS tool
    """

    @classmethod
    def setUpClass(cls):
        cls.index_content = INDEX_HTML.read_text(encoding="utf-8")
        cls.engine_content = ENGINE_JS.read_text(encoding="utf-8")
        cls.css_content = CSS_FILE.read_text(encoding="utf-8")
        cls.dom = parse_index_dom()

    def test_t1_f01_toggle_todos_46_projects(self):
        """Toggle 'todos' must render all 46 unified projects with valid coordinates."""
        # 1. HTML pill presence and metadata
        self.assertIn('id="portal-filter-todos"', self.index_content)
        self.assertIn('data-filter="todos"', self.index_content)
        pill_match = re.search(r'id="portal-filter-todos"[^>]*>[\s\S]*?<span class="ll-pill-count">(\d+)</span>', self.index_content)
        self.assertIsNotNone(pill_match, "Pill count badge missing for todos")
        self.assertEqual(pill_match.group(1), "46", "Filter todos must display count 46")

        # 2. Headless engine execution via Node
        node_script = """
        const fs = require('fs');
        const vm = require('vm');
        const sandbox = { window: {}, self: {}, global: {} };
        sandbox.window = sandbox;
        sandbox.self = sandbox;
        vm.createContext(sandbox);
        const code = fs.readFileSync('site/assets/js/lavvi_catalog_bundle.js', 'utf8');
        vm.runInContext(code, sandbox);
        const list = sandbox.allProjects || [];
        const validCoords = list.filter(p => p.ll && p.ll.length === 2 && p.ll[0] !== 0);
        console.log(JSON.stringify({ total: list.length, valid: validCoords.length }));
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=str(BASE_DIR), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Node script failed: {proc.stderr}")
        data = json.loads(proc.stdout.strip())
        self.assertEqual(data["total"], 46, f"Expected 46 total projects in bundle, got {data['total']}")
        self.assertEqual(data["valid"], 46, f"Expected 46 projects with valid coordinates, got {data['valid']}")

    def test_t1_f02_toggle_lancamentos_17_active(self):
        """Toggle 'lancamentos' must filter exactly 17 active Lavvi developments."""
        self.assertIn('id="portal-filter-lancamentos"', self.index_content)
        pill_match = re.search(r'id="portal-filter-lancamentos"[^>]*>[\s\S]*?<span class="ll-pill-count">(\d+)</span>', self.index_content)
        self.assertIsNotNone(pill_match, "Pill count badge missing for lancamentos")
        self.assertEqual(pill_match.group(1), "17", "Filter lancamentos must display count 17")

        node_script = """
        const fs = require('fs');
        const vm = require('vm');
        const sandbox = { window: {}, self: {}, global: {} };
        sandbox.window = sandbox;
        sandbox.self = sandbox;
        vm.createContext(sandbox);
        const code = fs.readFileSync('site/assets/js/lavvi_catalog_bundle.js', 'utf8');
        vm.runInContext(code, sandbox);
        const list = sandbox.allProjects || [];
        const lanc = list.filter(p => ((p.brand_line === 'lavvi' || !p.brand_line) && p.cat !== 'vendido' && (!p.status || !p.status.toLowerCase().includes('100% vendido'))) && p.ll && p.ll.length === 2 && p.ll[0] !== 0);
        console.log(JSON.stringify({ count: lanc.length }));
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=str(BASE_DIR), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Node script failed: {proc.stderr}")
        data = json.loads(proc.stdout.strip())
        self.assertEqual(data["count"], 17, f"Expected 17 active Lavvi projects, got {data['count']}")

    def test_t1_f03_toggle_novvo_7_smart_living(self):
        """Toggle 'novvo' must filter exactly 7 Meu Novvo smart living developments."""
        self.assertIn('id="portal-filter-novvo"', self.index_content)
        pill_match = re.search(r'id="portal-filter-novvo"[^>]*>[\s\S]*?<span class="ll-pill-count">(\d+)</span>', self.index_content)
        self.assertIsNotNone(pill_match, "Pill count badge missing for novvo")
        self.assertEqual(pill_match.group(1), "7", "Filter novvo must display count 7")

        node_script = """
        const fs = require('fs');
        const vm = require('vm');
        const sandbox = { window: {}, self: {}, global: {} };
        sandbox.window = sandbox;
        sandbox.self = sandbox;
        vm.createContext(sandbox);
        const code = fs.readFileSync('site/assets/js/lavvi_catalog_bundle.js', 'utf8');
        vm.runInContext(code, sandbox);
        const list = sandbox.allProjects || [];
        const novvo = list.filter(p => (p.brand_line === 'novvo' || p.cat === 'novvo') && p.ll && p.ll.length === 2 && p.ll[0] !== 0);
        console.log(JSON.stringify({ count: novvo.length }));
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=str(BASE_DIR), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Node script failed: {proc.stderr}")
        data = json.loads(proc.stdout.strip())
        self.assertEqual(data["count"], 7, f"Expected 7 Novvo projects, got {data['count']}")

    def test_t1_f04_toggle_entregues_22_selo_historico(self):
        """Toggle 'entregues' must filter 22 completed projects with Selo Histórico and 0 category overlap."""
        self.assertIn('id="portal-filter-entregues"', self.index_content)
        self.assertIn('Selo Histórico', self.index_content)
        pill_match = re.search(r'id="portal-filter-entregues"[^>]*>[\s\S]*?<span class="ll-pill-count">(\d+)</span>', self.index_content)
        self.assertIsNotNone(pill_match, "Pill count badge missing for entregues")
        self.assertEqual(pill_match.group(1), "22", "Filter entregues must display count 22")

        node_script = """
        const fs = require('fs');
        const vm = require('vm');
        const sandbox = { window: {}, self: {}, global: {} };
        sandbox.window = sandbox;
        sandbox.self = sandbox;
        vm.createContext(sandbox);
        const code = fs.readFileSync('site/assets/js/lavvi_catalog_bundle.js', 'utf8');
        vm.runInContext(code, sandbox);
        const list = sandbox.allProjects || [];
        const lanc = list.filter(p => ((p.brand_line === 'lavvi' || !p.brand_line) && p.cat !== 'vendido' && (!p.status || !p.status.toLowerCase().includes('100% vendido'))) && p.ll && p.ll.length === 2 && p.ll[0] !== 0);
        const novvo = list.filter(p => (p.brand_line === 'novvo' || p.cat === 'novvo') && p.ll && p.ll.length === 2 && p.ll[0] !== 0);
        const ent = list.filter(p => (p.cat === 'vendido' || (p.status && p.status.toLowerCase().includes('100% vendido'))) && p.ll && p.ll.length === 2 && p.ll[0] !== 0);

        console.log(JSON.stringify({
            entCount: ent.length,
            sum: lanc.length + novvo.length + ent.length,
            overlapLancNovvo: lanc.filter(p => novvo.includes(p)).length,
            overlapLancEnt: lanc.filter(p => ent.includes(p)).length,
            overlapNovvoEnt: novvo.filter(p => ent.includes(p)).length
        }));
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=str(BASE_DIR), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Node script failed: {proc.stderr}")
        data = json.loads(proc.stdout.strip())
        self.assertEqual(data["entCount"], 22, f"Expected 22 entregues projects, got {data['entCount']}")
        self.assertEqual(data["sum"], 46, f"Disjoint sum of categories must be 46, got {data['sum']}")
        self.assertEqual(data["overlapLancNovvo"], 0, "Overlapping projects between Lançamentos and Novvo!")
        self.assertEqual(data["overlapLancEnt"], 0, "Overlapping projects between Lançamentos and Entregues!")
        self.assertEqual(data["overlapNovvoEnt"], 0, "Overlapping projects between Novvo and Entregues!")

    def test_t1_f05_toggle_lifestyle_348_pois(self):
        """Toggle 'lifestyle' must load 348 verified POIs across 8 luxury clusters."""
        self.assertIn('id="portal-filter-lifestyle"', self.index_content)
        pill_match = re.search(r'id="portal-filter-lifestyle"[^>]*>[\s\S]*?<span class="ll-pill-count">(\d+)</span>', self.index_content)
        self.assertIsNotNone(pill_match, "Pill count badge missing for lifestyle")
        self.assertEqual(pill_match.group(1), "348", "Filter lifestyle must display count 348")

        self.assertTrue(POI_JSON.exists(), f"Missing {POI_JSON}")
        poi_data = json.loads(POI_JSON.read_text(encoding="utf-8"))
        clusters = poi_data.get("projects", {})
        self.assertEqual(len(clusters), 8, f"Expected 8 anchor clusters, got {len(clusters)}")

        total_pois = 0
        valid_pois = 0
        for ck, cl in clusters.items():
            self.assertIn("lat", cl, f"Cluster {ck} missing lat")
            self.assertIn("lon", cl, f"Cluster {ck} missing lon")
            pois = cl.get("pois", [])
            total_pois += len(pois)
            valid_pois += sum(1 for p in pois if p.get("lat") and p.get("lon"))

        self.assertEqual(total_pois, 348, f"Expected 348 POIs in poi_radar_data.json, got {total_pois}")
        self.assertEqual(valid_pois, 348, f"Expected 348 POIs with valid coordinates, got {valid_pois}")

    def test_t1_f06_toggle_concorrencia_12_benchmarks(self):
        """Toggle 'concorrencia' must provide exactly 12 market competitor benchmarks."""
        self.assertIn('id="portal-filter-concorrencia"', self.index_content)
        pill_match = re.search(r'id="portal-filter-concorrencia"[^>]*>[\s\S]*?<span class="ll-pill-count">(\d+)</span>', self.index_content)
        self.assertIsNotNone(pill_match, "Pill count badge missing for concorrencia")
        self.assertEqual(pill_match.group(1), "12", "Filter concorrencia must display count 12")

        comp_match = re.search(r'const MARKET_COMPETITORS = (\[[\s\S]*?\]);\s*//', self.engine_content)
        self.assertIsNotNone(comp_match, "MARKET_COMPETITORS array not found in portal_map_engine.js")

        node_script = f"const comps = {comp_match.group(1)}; console.log(JSON.stringify({{ count: comps.length, valid: comps.filter(c => c.ll && c.ll.length === 2 && c.ll[0] !== 0).length }}));"
        proc = subprocess.run(["node", "-e", node_script], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Node parsing of MARKET_COMPETITORS failed: {proc.stderr}")
        data = json.loads(proc.stdout.strip())
        self.assertEqual(data["count"], 12, f"Expected 12 competitors, got {data['count']}")
        self.assertEqual(data["valid"], 12, f"Expected 12 valid competitor coordinates, got {data['valid']}")

    def test_t1_f07_rich_modal_dom_landmarks(self):
        """Rich modal dialog must contain all required landmarks, 2x2 KPI grid, and Pedro Soares CTA."""
        # Dialog overlay
        overlay = self.dom.elements_by_id.get("map-pin-modal-overlay")
        self.assertIsNotNone(overlay, "map-pin-modal-overlay element missing")
        self.assertEqual(overlay["attrs"].get("role"), "dialog")
        self.assertEqual(overlay["attrs"].get("aria-modal"), "true")
        self.assertEqual(overlay["attrs"].get("aria-labelledby"), "pin-modal-title")

        # Modal card
        card = self.dom.elements_by_id.get("pin-modal-card")
        self.assertIsNotNone(card, "pin-modal-card element missing")
        self.assertEqual(card["attrs"].get("tabindex"), "-1")

        # 2x2 KPI grid cells
        self.assertIn('id="pin-modal-kpi-grid"', self.index_content)
        self.assertIn('id="pin-kpi-m2"', self.index_content)
        self.assertIn('id="pin-kpi-tipo"', self.index_content)
        self.assertIn('id="pin-kpi-preco"', self.index_content)
        self.assertIn('id="pin-kpi-entrega"', self.index_content)

        # Dynamic content containers
        self.assertIn('id="pin-modal-differentials-wrap"', self.index_content)
        self.assertIn('id="pin-modal-diff-list"', self.index_content)
        self.assertIn('id="pin-modal-legal-box"', self.index_content)
        self.assertIn('id="pin-modal-comp-box"', self.index_content)

        # Actions and WhatsApp CTA
        self.assertIn('id="pin-modal-secondary-btn"', self.index_content)
        wa_btn = self.dom.elements_by_id.get("pin-modal-wa-btn")
        self.assertIsNotNone(wa_btn, "pin-modal-wa-btn element missing")
        self.assertIn("https://wa.me/5511966105952", wa_btn["attrs"].get("href", ""))

        # Close button
        close_btn_match = re.search(r'class="[^"]*pin-card-close-btn[^"]*"[^>]*onclick="closePropertyModal\(\)"', self.index_content)
        self.assertIsNotNone(close_btn_match, "pin-card-close-btn with onclick closePropertyModal() missing")

    def test_t1_f08_schema_org_json_ld_generation(self):
        """updateSchemaOrgStructuredData must inject valid Schema.org JSON-LD structured data."""
        self.assertIn("function updateSchemaOrgStructuredData", self.engine_content)
        self.assertIn('"@context": "https://schema.org"', self.engine_content)
        self.assertIn('"@type": "RealEstateAgent"', self.engine_content)
        self.assertIn('"Pedro Soares | Lavvi Private Wealth"', self.engine_content)
        self.assertIn('"+55-11-96610-5952"', self.engine_content)
        self.assertIn('"ApartmentComplex"', self.engine_content)
        self.assertIn('"RealEstateListing"', self.engine_content)
        self.assertIn('"GeoCoordinates"', self.engine_content)

        # Test Schema generation in Node sandbox
        node_script = r"""
        const fs = require('fs');
        const vm = require('vm');
        let schemaText = '';
        const scriptStub = {
            set textContent(v) { schemaText = v; },
            get textContent() { return schemaText; }
        };
        const docStub = {
            getElementById: (id) => id === 'schema-ld-json' ? scriptStub : null,
            createElement: () => scriptStub,
            head: { appendChild: () => {} }
        };
        const sandbox = { window: {}, document: docStub, console: console };
        sandbox.window = sandbox;
        const code = fs.readFileSync('site/assets/js/portal_map_engine.js', 'utf8');
        const fnMatch = code.match(/function updateSchemaOrgStructuredData\([\s\S]*?\n  \}/);
        vm.createContext(sandbox);
        vm.runInContext(fnMatch[0], sandbox);

        const sample = {
            nome: "Jardim da Hípica Residences",
            bairro: "Alto da Boa Vista",
            endereco: "Rua Antônio Bandeira, 305",
            brand_line: "lavvi",
            status: "Lançamento",
            ll: [-23.6402, -46.7025]
        };
        sandbox.updateSchemaOrgStructuredData(sample, 'projeto');
        const parsed = JSON.parse(schemaText);
        console.log(JSON.stringify({
            context: parsed['@context'],
            agentName: parsed['@graph'][0].name,
            agentPhone: parsed['@graph'][0].telephone,
            propertyName: parsed['@graph'][1].name,
            propertyTypes: parsed['@graph'][1]['@type'],
            geo: parsed['@graph'][1].geo
        }));
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=str(BASE_DIR), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Schema Node script failed: {proc.stderr}")
        res = json.loads(proc.stdout.strip())
        self.assertEqual(res["context"], "https://schema.org")
        self.assertIn("Pedro Soares", res["agentName"])
        self.assertIn("96610-5952", res["agentPhone"])
        self.assertIn("Jardim da Hípica", res["propertyName"])
        self.assertIn("RealEstateListing", res["propertyTypes"])
        self.assertIn("ApartmentComplex", res["propertyTypes"])
        self.assertEqual(res["geo"]["latitude"], -23.6402)
        self.assertEqual(res["geo"]["longitude"], -46.7025)

    def test_t1_f09_anti_scroll_trap_configuration(self):
        """Map must initialize with scrollWheelZoom: false and toggle dynamically on focus/mouseleave."""
        self.assertIn("scrollWheelZoom: false", self.engine_content, "scrollWheelZoom must be false by default in Leaflet init")
        self.assertIn("portalMapInstance.scrollWheelZoom.enable()", self.engine_content, "scrollWheelZoom.enable() missing on focus/click")
        self.assertIn("portalMapInstance.scrollWheelZoom.disable()", self.engine_content, "scrollWheelZoom.disable() missing on mouseleave")
        self.assertIn('id="portal-scroll-hint"', self.index_content, "Visual hint #portal-scroll-hint missing in index.html")
        self.assertIn("💡 Clique no mapa para habilitar o zoom por scroll", self.index_content, "Scroll hint text missing")

        # CSS rules
        self.assertIn(".portal-scroll-hint", self.css_content)
        self.assertRegex(self.css_content, r'\.portal-scroll-hint\s*\{[^}]*pointer-events:\s*none', "Hint must have pointer-events: none")
        self.assertRegex(self.css_content, r'\.portal-scroll-hint\s*\{[^}]*z-index:\s*500', "Hint must have z-index: 500")

    def test_t1_f10_navigation_anchors_and_links(self):
        """Navigation links in desktop header, mobile drawer, and standalone tools must target #mapa and radar_mapa.html."""
        # Desktop navigation
        self.assertRegex(self.index_content, r'<a[^>]*href="#mapa"[^>]*>[\s\S]*?Mapa', "Desktop nav link to #mapa missing")

        # Mobile drawer navigation
        self.assertRegex(self.index_content, r'<a[^>]*href="#mapa"[^>]*onclick="toggleMobileDrawer\(false\)"', "Mobile drawer link to #mapa missing")

        # Standalone GIS fullscreen CTA
        self.assertIn('href="radar_mapa.html"', self.index_content, "Link to radar_mapa.html missing")
        self.assertIn('class="btn-gis-fullscreen"', self.index_content, "btn-gis-fullscreen button class missing")


# ==============================================================================
# TIER 2: BOUNDARY & CORNER CASES (SP BOUNDS, TOUCH TARGETS, SIZE, ZERO SAIBRO)
# ==============================================================================

class TestPortalMapTier2_BoundaryCornerCases(unittest.TestCase):
    """
    Tier 2 tests verify safety bounds, precision limits, and non-regression guarantees:
    - Coordinate bounding box within Greater São Paulo: Lat [-24.1, -23.3], Lon [-47.2, -46.3]
    - WCAG 2.5.5 Touch Targets >= 44x44px for buttons and pills
    - Lean payload size budget (< 150 KB for site/index.html)
    - Zero duplicate element IDs across site/index.html
    - Zero mention of saibro in Jardim da Hípica specs
    - Mobile media queries for map and bottom-sheet modal
    """

    @classmethod
    def setUpClass(cls):
        cls.index_content = INDEX_HTML.read_text(encoding="utf-8")
        cls.engine_content = ENGINE_JS.read_text(encoding="utf-8")
        cls.css_content = CSS_FILE.read_text(encoding="utf-8")
        cls.dom = parse_index_dom()

    def test_t2_b01_geographic_coordinates_sp_bounds(self):
        """All geographic coordinates across 46 projects, 12 competitors, and 348 POIs must stay within SP bounds."""
        node_script = r"""
        const fs = require('fs');
        const vm = require('vm');
        const sandbox = { window: {}, self: {}, global: {} };
        sandbox.window = sandbox;
        sandbox.self = sandbox;
        vm.createContext(sandbox);
        const bundleCode = fs.readFileSync('site/assets/js/lavvi_catalog_bundle.js', 'utf8');
        vm.runInContext(bundleCode, sandbox);

        const projects = sandbox.allProjects;
        const poiData = JSON.parse(fs.readFileSync('site/poi_radar_data.json', 'utf8'));
        const engineCode = fs.readFileSync('site/assets/js/portal_map_engine.js', 'utf8');
        const compMatch = engineCode.match(/const MARKET_COMPETITORS = (\[[\s\S]*?\]);\s*\/\//);
        const comps = eval(compMatch[1]);

        function checkCoords(name, list) {
            let outOfBounds = [];
            list.forEach((item, idx) => {
                const lat = item.lat || (item.ll && item.ll[0]);
                const lon = item.lon || (item.ll && item.ll[1]);
                if (lat < -24.1 || lat > -23.3 || lon < -47.2 || lon > -46.3) {
                    outOfBounds.push({ name: item.nome || idx, lat, lon });
                }
            });
            return { count: list.length, errors: outOfBounds };
        }

        const poiList = [];
        for (const k in poiData.projects) {
            const cl = poiData.projects[k];
            poiList.push({ nome: cl.nome, lat: cl.lat, lon: cl.lon });
            (cl.pois || []).forEach(p => poiList.push({ nome: p.nome, lat: p.lat, lon: p.lon }));
        }

        console.log(JSON.stringify({
            projects: checkCoords('projects', projects),
            competitors: checkCoords('competitors', comps),
            pois: checkCoords('pois', poiList)
        }));
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=str(BASE_DIR), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Coordinates Node script failed: {proc.stderr}")
        data = json.loads(proc.stdout.strip())

        self.assertEqual(data["projects"]["count"], 46)
        self.assertEqual(len(data["projects"]["errors"]), 0, f"Projects outside SP bounds: {data['projects']['errors']}")

        self.assertEqual(data["competitors"]["count"], 12)
        self.assertEqual(len(data["competitors"]["errors"]), 0, f"Competitors outside SP bounds: {data['competitors']['errors']}")

        self.assertEqual(data["pois"]["count"], 356) # 8 anchors + 348 POIs
        self.assertEqual(len(data["pois"]["errors"]), 0, f"POIs outside SP bounds: {data['pois']['errors']}")

    def test_t2_b02_touch_targets_wcag_255(self):
        """All interactive elements must guarantee >= 44x44px touch targets in CSS (WCAG 2.5.5)."""
        # Close button: width 44px, height 44px, min-width 44px, min-height 44px
        close_css = re.search(r'\.pin-card-close-btn\s*\{([^}]+)\}', self.css_content)
        self.assertIsNotNone(close_css, ".pin-card-close-btn rule missing in CSS")
        c_body = close_css.group(1)
        self.assertIn("width: 44px", c_body)
        self.assertIn("height: 44px", c_body)
        self.assertIn("min-width: 44px", c_body)
        self.assertIn("min-height: 44px", c_body)

        # Filter pills: min-height 44px
        pill_css = re.search(r'\.ll-filter-pill\s*\{([^}]+)\}', self.css_content)
        self.assertIsNotNone(pill_css, ".ll-filter-pill rule missing in CSS")
        self.assertIn("min-height: 44px", pill_css.group(1))

        # Action buttons: min-height 44px
        for sel in [r'\.btn-gis-fullscreen', r'\.btn-open-full-hub', r'\.btn-pin-wa']:
            m = re.search(sel + r'\s*\{([^}]+)\}', self.css_content)
            self.assertIsNotNone(m, f"{sel} rule missing in CSS")
            self.assertIn("min-height: 44px", m.group(1), f"{sel} must define min-height: 44px")

    def test_t2_b03_lean_file_size_budget(self):
        """site/index.html must strictly stay below the 150 KB (153,600 bytes) performance budget."""
        file_size = INDEX_HTML.stat().st_size
        max_size = 150 * 1024 # 153,600 bytes
        headroom = max_size - file_size
        self.assertLess(file_size, max_size, f"site/index.html ({file_size} bytes) exceeds 150 KB budget!")
        self.assertGreater(headroom, 10 * 1024, f"Headroom ({headroom} bytes) is uncomfortably small (< 10 KB)!")

    def test_t2_b04_zero_duplicate_element_ids(self):
        """site/index.html must have ZERO duplicate element IDs across the entire document."""
        duplicates = {k: v for k, v in self.dom.ids_count.items() if v > 1}
        self.assertEqual(len(duplicates), 0, f"Found duplicate element IDs in site/index.html: {duplicates}")

        # Specifically assert key map IDs exist exactly once
        expected_unique_ids = [
            "mapa",
            "portal-map",
            "portal-scroll-hint",
            "portal-map-status",
            "portal-filter-todos",
            "portal-filter-lancamentos",
            "portal-filter-novvo",
            "portal-filter-entregues",
            "portal-filter-lifestyle",
            "portal-filter-concorrencia",
            "map-pin-modal-overlay",
            "pin-modal-card",
            "pin-modal-kpi-grid",
            "pin-kpi-m2",
            "pin-kpi-tipo",
            "pin-kpi-preco",
            "pin-kpi-entrega",
            "pin-modal-wa-btn",
            "pin-modal-secondary-btn"
        ]
        for eid in expected_unique_ids:
            self.assertEqual(self.dom.ids_count.get(eid), 1, f"Expected ID '{eid}' to appear exactly once, got {self.dom.ids_count.get(eid)}")

    def test_t2_b05_zero_saibro_hallucination_hipica(self):
        """Zero tolerance for 'saibro' hallucination in any Jardim da Hípica context."""
        # 1. Engine JS differentials
        hipica_match = re.search(r"if \(n\.includes\('jardim da h[ií]pica'\)[\s\S]*?return\s*\[([\s\S]*?)\];", self.engine_content)
        self.assertIsNotNone(hipica_match, "Jardim da Hípica differential block not found in portal_map_engine.js")
        self.assertNotIn("saibro", hipica_match.group(1).lower(), "FATAL DEFECT: 'saibro' found in Jardim da Hípica differentials!")

        # 2. Complete engine JS file
        engine_saibro_hits = [m.start() for m in re.finditer(r'saibro', self.engine_content, re.IGNORECASE)]
        self.assertEqual(len(engine_saibro_hits), 0, f"Found 'saibro' in portal_map_engine.js at indices: {engine_saibro_hits}")

        # 3. Complete index.html
        index_saibro_hits = [m.start() for m in re.finditer(r'saibro', self.index_content, re.IGNORECASE)]
        self.assertEqual(len(index_saibro_hits), 0, f"Found 'saibro' in site/index.html at indices: {index_saibro_hits}")

    def test_t2_b06_mobile_viewport_responsiveness_rules(self):
        """CSS must provide mobile media queries with 440px map height and bottom-sheet flex-end modal."""
        self.assertIn("scroll-margin-top: 76px", self.css_content, "#mapa must have scroll-margin-top for sticky header")
        self.assertIn("height: 580px", self.css_content, "Desktop map height must be 580px")

        mobile_match = re.search(r'@media\s*\(\s*max-width:\s*76[78]px\s*\)\s*\{([\s\S]*?\}\s*\})', self.css_content)
        self.assertIsNotNone(mobile_match, "Mobile media query block (@media max-width: 767px or 768px) missing")
        m_css = mobile_match.group(1)
        self.assertIn("height: 440px", m_css, "Mobile map height must be 440px")
        self.assertIn("align-items: flex-end", m_css, "Mobile modal must align to flex-end (bottom sheet)")
        self.assertIn("border-radius: 20px 20px 0 0", m_css, "Mobile modal must round top corners")
        self.assertIn("pinCardMobileSlideUp", m_css, "Mobile modal must animate via pinCardMobileSlideUp")


# ==============================================================================
# TIER 3: CROSS-FEATURE COMBINATIONS (CROSS-NAV, FOCUS TRAP, ESC, INERT, TRANSITIONS)
# ==============================================================================

class TestPortalMapTier3_CrossFeatureCombinations(unittest.TestCase):
    """
    Tier 3 tests verify pairwise interactions and state management across components:
    - DOM landmark sequence: #catalogo < #mapa < #ferramentas
    - Keyboard focus trap cycling (Tab forwards, Shift+Tab backwards)
    - ESC key dismissal and previousActiveElement focus restoration
    - Background inertness and ARIA isolation controller
    - Rapid 100-cycle filter transition stress test
    """

    @classmethod
    def setUpClass(cls):
        cls.index_content = INDEX_HTML.read_text(encoding="utf-8")
        cls.engine_content = ENGINE_JS.read_text(encoding="utf-8")

    def test_t3_c01_catalog_and_map_cross_navigation(self):
        """Section ordering and cross-navigation between catalog and map must be seamless."""
        cat_pos = self.index_content.find('id="catalogo"')
        mapa_pos = self.index_content.find('id="mapa"')
        ferr_pos = self.index_content.find('id="ferramentas"')

        self.assertNotEqual(cat_pos, -1, "#catalogo section missing")
        self.assertNotEqual(mapa_pos, -1, "#mapa section missing")
        self.assertNotEqual(ferr_pos, -1, "#ferramentas section missing")

        self.assertLess(cat_pos, mapa_pos, "#catalogo must precede #mapa in document order")
        self.assertLess(mapa_pos, ferr_pos, "#mapa must precede #ferramentas in document order")

        # Secondary button in map modal targets #catalogo and invokes closePropertyModal
        self.assertIn('id="pin-modal-secondary-btn"', self.index_content)
        self.assertIn('window.closePropertyModal()', self.engine_content)

    def test_t3_c02_keyboard_focus_trap_cycling(self):
        """Modal must trap keyboard focus: Tab wraps from last to first, Shift+Tab from first to last."""
        node_script = """
        const fs = require('fs');
        const listeners = {};
        const elements = {};

        function mockEl(id, tag = 'div') {
            return {
                id, tagName: tag.toUpperCase(), style: {}, attributes: {},
                classList: { add: () => {}, remove: () => {}, contains: () => false },
                setAttribute: function(k, v) { this.attributes[k] = v; },
                getAttribute: function(k) { return this.attributes[k]; },
                removeAttribute: function(k) { delete this.attributes[k]; },
                addEventListener: () => {},
                focus: function() { global.activeElement = this; },
                querySelectorAll: function() {
                    return [elements['btn-close'], elements['btn-sec'], elements['btn-wa']];
                }
            };
        }

        elements['map-pin-modal-overlay'] = mockEl('map-pin-modal-overlay');
        elements['pin-modal-card'] = mockEl('pin-modal-card');
        elements['btn-close'] = mockEl('btn-close', 'button');
        elements['btn-sec'] = mockEl('btn-sec', 'a');
        elements['btn-wa'] = mockEl('btn-wa', 'a');

        global.document = {
            getElementById: (id) => elements[id] || mockEl(id),
            querySelectorAll: () => [],
            addEventListener: (ev, fn) => { if (!listeners[ev]) listeners[ev] = []; listeners[ev].push(fn); },
            createElement: (t) => mockEl('', t),
            head: { appendChild: () => {} },
            get activeElement() { return global.activeElement; }
        };
        global.window = global;
        global.allProjects = [];

        require('./site/assets/js/lavvi_catalog_bundle.js');
        const code = fs.readFileSync('./site/assets/js/portal_map_engine.js', 'utf8');
        eval(code);

        // Open modal
        global.openPropertyModal('Jardim da Hípica');

        // Test Forward Tab from last element
        global.activeElement = elements['btn-wa'];
        let tabPreventDefault = false;
        listeners['keydown'].forEach(fn => fn({
            key: 'Tab', shiftKey: false, preventDefault: () => { tabPreventDefault = true; }
        }));
        const tabResult = tabPreventDefault && global.activeElement.id === 'btn-close';

        // Test Reverse Shift+Tab from first element
        global.activeElement = elements['btn-close'];
        let shiftTabPreventDefault = false;
        listeners['keydown'].forEach(fn => fn({
            key: 'Tab', shiftKey: true, preventDefault: () => { shiftTabPreventDefault = true; }
        }));
        const shiftTabResult = shiftTabPreventDefault && global.activeElement.id === 'btn-wa';

        console.log(JSON.stringify({ tabWrap: tabResult, shiftTabWrap: shiftTabResult }));
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=str(BASE_DIR), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Focus trap Node script failed: {proc.stderr}")
        res = json.loads(proc.stdout.strip())
        self.assertTrue(res["tabWrap"], "Tab on last focusable element did not cycle to first element with preventDefault")
        self.assertTrue(res["shiftTabWrap"], "Shift+Tab on first element did not cycle to last element with preventDefault")

    def test_t3_c03_esc_dismissal_and_focus_restoration(self):
        """Pressing Escape must close the modal and restore focus to previousActiveElement."""
        node_script = """
        const fs = require('fs');
        const listeners = {};
        const elements = {};

        function mockEl(id, tag = 'div') {
            return {
                id, tagName: tag.toUpperCase(), style: { display: 'none' }, attributes: {},
                classList: { add: () => {}, remove: () => {}, contains: () => false },
                setAttribute: function(k, v) { this.attributes[k] = v; },
                getAttribute: function(k) { return this.attributes[k]; },
                removeAttribute: function(k) { delete this.attributes[k]; },
                addEventListener: () => {},
                focus: function() { global.activeElement = this; },
                querySelectorAll: () => []
            };
        }

        elements['map-pin-modal-overlay'] = mockEl('map-pin-modal-overlay');
        elements['pin-modal-card'] = mockEl('pin-modal-card');
        const trigger = mockEl('map-trigger-btn', 'button');

        global.document = {
            getElementById: (id) => elements[id] || mockEl(id),
            querySelectorAll: () => [],
            addEventListener: (ev, fn) => { if (!listeners[ev]) listeners[ev] = []; listeners[ev].push(fn); },
            createElement: (t) => mockEl('', t),
            head: { appendChild: () => {} },
            get activeElement() { return global.activeElement; }
        };
        global.window = global;
        global.allProjects = [];

        require('./site/assets/js/lavvi_catalog_bundle.js');
        const code = fs.readFileSync('./site/assets/js/portal_map_engine.js', 'utf8');
        eval(code);

        // Focus trigger element before opening modal
        trigger.focus();

        // Open modal
        global.openPropertyModal('Jardim da Hípica');
        const opened = elements['map-pin-modal-overlay'].style.display === 'flex';

        // Press Escape
        listeners['keydown'].forEach(fn => fn({ key: 'Escape' }));
        const closed = elements['map-pin-modal-overlay'].style.display === 'none';
        const focusRestored = global.activeElement.id === 'map-trigger-btn';

        console.log(JSON.stringify({ opened, closed, focusRestored }));
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=str(BASE_DIR), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"ESC restoration script failed: {proc.stderr}")
        res = json.loads(proc.stdout.strip())
        self.assertTrue(res["opened"], "Modal failed to open with display: flex")
        self.assertTrue(res["closed"], "Modal failed to close on ESC key")
        self.assertTrue(res["focusRestored"], "Focus failed to restore to trigger element after ESC")

    def test_t3_c04_background_inertness_and_aria_isolation(self):
        """setBackgroundInert must toggle aria-hidden and inert attributes on background landmarks."""
        node_script = """
        const fs = require('fs');
        const elements = {};
        const bgNodes = [];

        function mockEl(id, tag = 'div') {
            return {
                id, tagName: tag.toUpperCase(), style: { display: 'none' }, attributes: {},
                classList: { add: () => {}, remove: () => {}, contains: () => false },
                setAttribute: function(k, v) { this.attributes[k] = v; },
                getAttribute: function(k) { return this.attributes[k]; },
                removeAttribute: function(k) { delete this.attributes[k]; },
                addEventListener: () => {},
                focus: () => {},
                querySelectorAll: () => []
            };
        }

        elements['map-pin-modal-overlay'] = mockEl('map-pin-modal-overlay');
        elements['pin-modal-card'] = mockEl('pin-modal-card');
        const bg1 = mockEl('site-header', 'header');
        const bg2 = mockEl('catalog-section', 'section');
        bgNodes.push(bg1, bg2);

        global.document = {
            getElementById: (id) => elements[id] || mockEl(id),
            querySelectorAll: (sel) => bgNodes,
            addEventListener: () => {},
            createElement: (t) => mockEl('', t),
            head: { appendChild: () => {} },
            get activeElement() { return null; }
        };
        global.window = global;
        global.allProjects = [];

        require('./site/assets/js/lavvi_catalog_bundle.js');
        const code = fs.readFileSync('./site/assets/js/portal_map_engine.js', 'utf8');
        eval(code);

        global.openPropertyModal('Jardim da Hípica');
        const inertApplied = bgNodes.every(n => n.getAttribute('aria-hidden') === 'true' && n.getAttribute('inert') === '');

        global.closePropertyModal();
        const inertRemoved = bgNodes.every(n => n.getAttribute('aria-hidden') === undefined && n.getAttribute('inert') === undefined);

        console.log(JSON.stringify({ inertApplied, inertRemoved }));
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=str(BASE_DIR), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Inertness script failed: {proc.stderr}")
        res = json.loads(proc.stdout.strip())
        self.assertTrue(res["inertApplied"], "Background landmarks failed to receive aria-hidden and inert on open")
        self.assertTrue(res["inertRemoved"], "Background landmarks failed to clear aria-hidden and inert on close")

    def test_t3_c05_rapid_filter_transition_stress(self):
        """Rapid 100-cycle filter transition stress test must complete with 0 exceptions and clean layer state."""
        node_script = """
        const fs = require('fs');
        const vm = require('vm');

        class MockEl {
            constructor(id) {
                this.id = id;
                this.style = {};
                this.classList = { add: () => {}, remove: () => {} };
                this.attributes = {};
            }
            setAttribute(k, v) { this.attributes[k] = v; }
            getAttribute(k) { return this.attributes[k]; }
            removeAttribute(k) { delete this.attributes[k]; }
            addEventListener() {}
            focus() {}
        }

        const elements = {
            'portal-map': new MockEl('portal-map'),
            'portal-scroll-hint': new MockEl('portal-scroll-hint'),
            'portal-map-status': new MockEl('portal-map-status'),
            'portal-filter-todos': new MockEl('portal-filter-todos'),
            'portal-filter-lancamentos': new MockEl('portal-filter-lancamentos'),
            'portal-filter-novvo': new MockEl('portal-filter-novvo'),
            'portal-filter-entregues': new MockEl('portal-filter-entregues'),
            'portal-filter-lifestyle': new MockEl('portal-filter-lifestyle'),
            'portal-filter-concorrencia': new MockEl('portal-filter-concorrencia')
        };

        let markers = [];
        const L = {
            map: () => ({
                scrollWheelZoom: { enable: () => {}, disable: () => {} },
                on: () => {},
                fitBounds: () => {}
            }),
            tileLayer: () => ({ addTo: function() { return this; } }),
            layerGroup: () => ({
                addTo: function() { return this; },
                clearLayers: () => { markers = []; },
                getLayers: () => markers,
                addLayer: (m) => markers.push(m)
            }),
            divIcon: (o) => o,
            marker: function(ll, o) {
                const m = {
                    ll: ll,
                    opts: o,
                    on: function() {},
                    addTo: function(lg) { lg.addLayer(this); return this; }
                };
                return m;
            },
            circle: () => ({ addTo: () => {} }),
            latLngBounds: () => ({ extend: () => {} })
        };

        const sandbox = {
            window: {},
            document: {
                getElementById: (id) => elements[id] || new MockEl(id),
                querySelectorAll: () => Object.values(elements),
                addEventListener: () => {},
                createElement: (t) => new MockEl(t),
                head: { appendChild: () => {} }
            },
            L: L,
            fetch: () => Promise.resolve({ ok: true, json: () => Promise.resolve(JSON.parse(fs.readFileSync('site/poi_radar_data.json', 'utf8'))) }),
            setTimeout: setTimeout,
            clearTimeout: clearTimeout,
            console: console
        };
        sandbox.window = sandbox;

        vm.createContext(sandbox);
        vm.runInContext(fs.readFileSync('site/assets/js/lavvi_catalog_bundle.js', 'utf8'), sandbox);
        vm.runInContext(fs.readFileSync('site/assets/js/portal_map_engine.js', 'utf8'), sandbox);

        const keys = ['todos', 'lancamentos', 'novvo', 'entregues', 'concorrencia'];
        let errors = 0;
        for (let i = 0; i < 100; i++) {
            const k = keys[Math.floor(Math.random() * keys.length)];
            try {
                sandbox.applyPortalMapFilter(k);
            } catch (err) {
                errors++;
            }
        }

        // Final Novvo render
        sandbox.applyPortalMapFilter('novvo');
        const novvoMarkerCount = markers.length;

        console.log(JSON.stringify({ errors, novvoMarkerCount }));
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=str(BASE_DIR), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Rapid transition stress script failed: {proc.stderr}")
        res = json.loads(proc.stdout.strip())
        self.assertEqual(res["errors"], 0, f"Encountered {res['errors']} errors during rapid transitions")
        self.assertEqual(res["novvoMarkerCount"], 7, f"Layer accumulation detected! Expected 7 Novvo markers, got {res['novvoMarkerCount']}")


# ==============================================================================
# TIER 4: REAL-WORLD APPLICATION SCENARIOS (INVESTOR, NOVVO, AIRBNB, ASYMMETRY, IDENTITY)
# ==============================================================================

class TestPortalMapTier4_RealWorldScenarios(unittest.TestCase):
    """
    Tier 4 tests verify end-to-end real-world user journeys and compliance guarantees:
    - Scenario 1: UHNW Investor inspecting Jardim da Hípica specs (40.000 m², 18x36m tennis, 60m pool, CBRE, zero saibro)
    - Scenario 2: First-time Novvo buyer verifying statutory short-stay prohibition on HIS/HMP units
    - Scenario 3: Short-stay investor auditing T.O.M. Paraíso cartorial condominium minute approving Airbnb in R2V
    - Scenario 4: Competitor benchmark and asymmetry arbitrage analysis vs Lavvi
    - Scenario 5: Pedro Soares canonical identity enforcement and client-facing air-gap
    """

    @classmethod
    def setUpClass(cls):
        cls.engine_content = ENGINE_JS.read_text(encoding="utf-8")
        cls.index_content = INDEX_HTML.read_text(encoding="utf-8")

    def test_t4_s01_uhnw_investor_jardim_da_hipica(self):
        """Scenario 1: UHNW investor due diligence on Jardim da Hípica specifications."""
        # 1. Exact verified numbers in differentials
        self.assertIn("39.553 m² (~40.000 m²)", self.engine_content)
        self.assertIn("Praça Verde de 10.000 m²", self.engine_content)
        self.assertIn("02 Quadras de Tênis Oficiais (18x36m)", self.engine_content)
        self.assertIn("02 Beach Tennis", self.engine_content)
        self.assertIn("raia de 60m", self.engine_content)
        self.assertIn("CBRE", self.engine_content)
        self.assertIn("Body Care", self.engine_content)
        self.assertIn("04 Private Houses", self.engine_content)

        # 2. Scrutinize that NO mention of saibro exists in Jardim da Hípica
        hipica_block = re.search(r"if \(n\.includes\('jardim da h[ií]pica'\)[\s\S]*?return\s*\[([\s\S]*?)\];", self.engine_content)
        self.assertIsNotNone(hipica_block)
        self.assertNotIn("saibro", hipica_block.group(1).lower())

        # 3. WhatsApp CTA linking to Pedro Soares
        self.assertIn("https://wa.me/5511966105952", self.engine_content)

    def test_t4_s02_novvo_buyer_his_hmp_regulatory_notice(self):
        """Scenario 2: Novvo first-time buyer journey and legal short-stay ban notice on HIS/HMP units."""
        # Regulatory legal warning box in modal
        self.assertIn("Aviso Legal &amp; Política Habitacional", self.engine_content)
        self.assertIn("legislação urbanística e habitacional de São Paulo", self.engine_content)
        self.assertIn("unidades enquadradas em HIS (Habitação de Interesse Social) e HMP (Habitação de Mercado Popular)", self.engine_content)
        self.assertIn("vedação legal e estatutária à exploração por Airbnb ou short-stay", self.engine_content)

        # Slate and Rose visual badge tokens in CSS
        css_text = CSS_FILE.read_text(encoding="utf-8")
        self.assertIn("#22343E", css_text, "Novvo slate navy #22343E missing in CSS")
        self.assertIn("#A06F71", css_text, "Novvo rose accent #A06F71 missing in CSS")

    def test_t4_s03_tenant_auditing_tom_paraiso_airbnb_minute(self):
        """Scenario 3: Short-stay investor auditing T.O.M. Paraíso cartorial condominium minute approving Airbnb in R2V."""
        self.assertIn("5.600 m²", self.engine_content)
        self.assertIn("240m do Metrô Paraíso", self.engine_content)
        self.assertIn("Triplex Arquitetura", self.engine_content)
        self.assertIn("Convenção Auditada em Cartório", self.engine_content)
        self.assertIn("Minuta de Convenção arquivada em cartório", self.engine_content)
        self.assertIn("blindando o investidor contra assembleias restritivas", self.engine_content)

    def test_t4_s04_competitor_asymmetry_analysis(self):
        """Scenario 4: Competitor benchmark and asymmetry arbitrage analysis vs Lavvi."""
        self.assertIn("Análise de Assimetria vs. Lavvi", self.engine_content)
        self.assertIn("Parque Global Residences", self.engine_content)
        self.assertIn("On The Sky Cyrela", self.engine_content)
        self.assertIn("Haus Mitre Chácara Santo Antônio", self.engine_content)
        self.assertIn("fração ideal", self.engine_content.lower())

    def test_t4_s05_pedro_soares_identity_and_airgap(self):
        """Scenario 5: Pedro Soares canonical identity enforcement and client-facing air-gap."""
        # Canonical phone and WhatsApp
        self.assertIn("96610-5952", self.engine_content)
        self.assertIn("https://wa.me/5511966105952", self.engine_content)
        self.assertIn("Pedro Soares | Lavvi Private Wealth", self.engine_content)

        # Zero fake CRECI numbers (30.906 or bare CRECI SP)
        self.assertNotRegex(self.engine_content, r'30\.?906', "Fake CRECI 30.906 found in engine JS!")
        self.assertNotRegex(self.engine_content, r'creci\s*[-:]?\s*\d+', "Invented CRECI pattern found in engine JS!")
        self.assertNotRegex(self.index_content, r'30\.?906', "Fake CRECI 30.906 found in index.html!")

        # Air-gap: Zero internal agent codenames leaked in client-facing engine JS
        forbidden_codenames = ['vito', 'burry', 'cosimo', 'ariadne', 'miyamoto', 'jep', 'cobb', 'nolan', 'hagen']
        for codename in forbidden_codenames:
            matches = list(re.finditer(rf'\b{codename}\b', self.engine_content, re.IGNORECASE))
            self.assertEqual(len(matches), 0, f"Client-facing leakage: codename '{codename}' found in portal_map_engine.js!")


# ==============================================================================
# MAIN TEST RUNNER WITH DETAILED REPORTING
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Lavvi Portal Map E2E Test Suite Runner")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3, 4], help="Run only tests from a specific tier (1, 2, 3, or 4)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose test execution")
    args, unknown = parser.parse_known_args()

    print("=" * 80)
    print("🏛️  LAVVI PRIVATE WEALTH & MEDIA AGENCY — PORTAL MAP E2E TEST SUITE")
    print("   Empirical 4-Tier Opaque-Box Verification of SP Portfolio Radar Map")
    print("   Pedro Soares • Lavvi Private Wealth (WhatsApp: +55 11 96610-5952)")
    print("=" * 80)

    suite = unittest.TestSuite()
    tier_map = {
        1: TestPortalMapTier1_FeatureCoverage,
        2: TestPortalMapTier2_BoundaryCornerCases,
        3: TestPortalMapTier3_CrossFeatureCombinations,
        4: TestPortalMapTier4_RealWorldScenarios,
    }

    if args.tier:
        print(f"🔬 Running Tier {args.tier} only...")
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(tier_map[args.tier]))
    else:
        for t_cls in tier_map.values():
            suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(t_cls))

    verbosity = 2 if args.verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    print("\n" + "=" * 80)
    print("📊 PORTAL MAP E2E TEST EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 80)

    if result.wasSuccessful():
        print("🎉 ALL PORTAL MAP E2E TESTS PASSED (100% SPEC COMPLIANCE)!")
        sys.exit(0)
    else:
        print(f"❌ TEST FAILURES DETECTED ({len(result.failures)} failures, {len(result.errors)} errors)!")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    main()
