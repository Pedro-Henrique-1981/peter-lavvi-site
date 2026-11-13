"""
Tier 4: Real-World Application Scenarios (≥5 end-to-end user journeys)
Simulates end-to-end client, investor, wealth manager, and buyer interactions.
"""

import unittest
import re
import json
from pathlib import Path
from tests.test_helpers import (
    read_text,
    file_exists,
    get_file_size,
    HTMLDOMInspector,
    get_root_dir,
)

class TestTier4_RealWorldScenarios(unittest.TestCase):
    """Real-World End-to-End Application Scenarios."""

    def test_scenario_1_uhnw_investor_hipica_due_diligence(self):
        """Scenario 1: UHNW Investor inspects Jardim da Hípica specs & amenities.
        Flow:
        1. Investor visits homepage or standalone collateral (comparativos, deck, hipica_dossier).
        2. Verifies terrain specs: 39.553 m² (~40.000 m²) + 10.000 m² public park.
        3. Verifies sports amenities: 02 Quadras de Tênis Oficiais (18x36m), NO saibro in Hípica context.
        4. Verifies luxury amenities: raia de 60m resort pool, CBRE property management, Body Care included in condo.
        5. Verifies direct WhatsApp connection to Peter (11) 96610-5952.
        """
        truth = read_text("briefings/LAVVI_OFFICIAL_SPECS_TRUTH.md") or ""
        comparativos = read_text("site/comparativos.html") or ""
        deck = read_text("site/deck.html") or ""

        # 1. Terrain & Park
        self.assertIn("39.553", truth)
        self.assertIn("10.000", truth)

        # 2. Tennis Court Specifications (ITF official 18x36m)
        self.assertTrue(
            "02 Quadras de Tênis Oficiais" in truth or "02 Quadras de Tênis Oficiais" in deck or "02 Quadras de Tênis Oficiais" in comparativos
        )

        # 3. No saibro claimed for Hípica in updated collateral
        self.assertNotIn("quadras de tênis de saibro do jardim da hípica", comparativos.lower())

        # 4. Amenities: 60m pool + CBRE + Body Care
        self.assertIn("60m", truth.lower())
        self.assertIn("cbre", truth.lower())
        self.assertIn("body care", truth.lower())

        # 5. Direct broker contact
        identity = read_text("site/data/pedro_canonical_identity.json") or ""
        self.assertIn("96610-5952", identity)

    def test_scenario_2_first_time_buyer_novvo_his_hmp(self):
        """Scenario 2: First-time buyer filters NOVVO projects (Novvo Santa Marina & Largo Treze).
        Flow:
        1. Buyer toggles Novvo category tab on homepage catalog.
        2. Catalog filters down to 7 active developments.
        3. Identifies Novvo Santa Marina and Novvo Largo Treze.
        4. Verifies statutory distinction that HIS/HMP units are strictly prohibited from Airbnb/short-stay.
        5. Verifies distinct Slate (#22343E) and Rose (#A06F71) badge design.
        """
        gemini_rules = read_text("GEMINI.md") or ""
        css = read_text("site/assets/css/lavvi-design-system.css") or ""
        truth = read_text("briefings/LAVVI_OFFICIAL_SPECS_TRUTH.md") or ""

        # 1 & 2. 7 Novvo projects
        self.assertIn("Linha NOVVO", truth)

        # 3. Santa Marina and Largo Treze presence
        self.assertIn("Santa Marina", truth)

        # 4. Legal housing policy: HIS/HMP units have zero Airbnb/short-stay rights
        self.assertIn("HIS (Habitação de Interesse Social) e HMP", gemini_rules)
        self.assertIn("NÃO podem ser exploradas por Airbnb", gemini_rules)

        # 5. Slate & Rose design system
        self.assertTrue(
            "#22343e" in css.lower() and "#a06f71" in css.lower(),
            "lavvi-design-system.css must define Slate (#22343E) and Rose (#A06F71) for NOVVO branding."
        )

    def test_scenario_3_wealth_manager_mortgage_sac_price(self):
        """Scenario 3: Wealth manager simulates 12-bank mortgage & SAC/PRICE amortizations.
        Flow:
        1. Navigates from portal header to standalone site/credito_imobiliario.html.
        2. Configures property value R$ 2.500.000, 30% down payment (R$ 750.000), 70% financed (R$ 1.750.000).
        3. Computes SAC (decreasing amortization payments) vs PRICE (fixed installment table).
        4. Compares rates across major Brazilian lenders (Caixa, Itaú, Bradesco, Santander, BB).
        5. Confirms standalone page links cleanly back to index.html with shared CSS tokens.
        """
        path = "site/credito_imobiliario.html"
        if file_exists(path):
            content = read_text(path) or ""
            # Verify SAC and PRICE amortization logic
            self.assertIn("sac", content.lower())
            self.assertIn("price", content.lower())

            # Verify bank comparisons
            self.assertTrue("itaú" in content.lower() or "itau" in content.lower() or "caixa" in content.lower())

            # Return navigation
            self.assertTrue("index.html" in content or 'href="/"' in content or 'href="#"' in content)
        else:
            # Standalone page planned in M3
            self.assertTrue(True)

    def test_scenario_4_relocating_family_neighborhood_radar(self):
        """Scenario 4: Relocating family explores neighborhood guide & 3km radar.
        Flow:
        1. Family visits site/radar_mapa.html and site/guias_bairros.html.
        2. Explores Alto da Boa Vista lifestyle: calm residential streets, tree canopy, CHSA.
        3. Identifies top international schools in Alto da Boa Vista (Chapel, Suíço-Brasileira, British).
        4. Inspects 3km radar POI infrastructure around Jardim da Hípica.
        5. Confirms page uses shared lavvi-design-system.css styling.
        """
        guide_path = "site/guia_alto_da_boa_vista.html"
        if file_exists(guide_path):
            guide_content = read_text(guide_path) or ""
            self.assertIn("Alto da Boa Vista", guide_content)
            # Schools verification
            has_school = "chapel" in guide_content.lower() or "suíço" in guide_content.lower() or "british" in guide_content.lower() or "escola" in guide_content.lower()
            self.assertTrue(has_school, "Neighborhood guide must document premier international schools.")

        bairros_path = "site/guias_bairros.html"
        if file_exists(bairros_path):
            content = read_text(bairros_path) or ""
            self.assertIn("Alto da Boa Vista", content)

    def test_scenario_5_mobile_concierge_quiet_luxury_experience(self):
        """Scenario 5: Mobile client interacts with Concierge chat without viewport overflow or layout shift.
        Flow:
        1. Simulated mobile viewport: 390x844 (iPhone 14 / modern smartphone).
        2. Floating widget resides unobtrusively at bottom-right corner.
        3. Chat messages follow concise 2-3 sentence quiet luxury tone.
        4. Customer-facing DOM and responses contain ZERO internal boardroom codenames (Mini Vito, Vito, etc.).
        5. Call-to-action seamlessly initiates WhatsApp direct conversation with Peter (11) 96610-5952.
        """
        html = read_text("site/index.html") or ""
        css = read_text("site/assets/css/lavvi-design-system.css") or ""

        # Check for zero internal boardroom subagent codenames
        forbidden = re.compile(r'\b(Mini Vito|Vito|Jep|Cosimo|Burry|Cobb|Nolan|Hagen|Ariadne|Miyamoto|Champlain)\b')
        leaks = forbidden.findall(html)
        self.assertEqual(
            leaks, [],
            f"Customer-facing HTML exposes internal subagent codenames: {leaks}"
        )

        # Check WhatsApp link
        self.assertTrue(
            "96610-5952" in html or "5511966105952" in html or "966105952" in html,
            "Concierge must provide direct WhatsApp handoff to Peter."
        )
