#!/usr/bin/env python3
"""
Comprehensive E2E Opaque-Box Test Suite for Lavvi Media Agency Web Portal.
Executes systematic 4-Tier verification across 12 portal features, boundaries,
cross-feature combinations, and real-world application scenarios.

Usage:
    python tests/test_e2e_portal.py
    python tests/test_e2e_portal.py --tier 1
    python tests/test_e2e_portal.py --tier 2
    python tests/test_e2e_portal.py --tier 3
    python tests/test_e2e_portal.py --tier 4
    python tests/test_e2e_portal.py --verbose
"""

import sys
import os
import io
import time
import argparse
import unittest
from pathlib import Path
from typing import List, Dict, Tuple, Any

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Force UTF-8 stdout on Windows
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Import Tier test modules
import tests.tier1_features as tier1
import tests.tier2_boundaries as tier2
import tests.tier3_cross_feature as tier3
import tests.tier4_scenarios as tier4

# Re-export all test classes so standard unittest discovery finds them
from tests.tier1_features import (
    TestF01_HeaderNavigation,
    TestF02_HeroSearchBar,
    TestF03_CatalogGrid,
    TestF04_CategoryCounters,
    TestF05_NovvoIntegration,
    TestF06_ToolModularization,
    TestF07_SharedDesignSystem,
    TestF08_ConciergeWidget,
    TestF09_IdentityCompliance,
    TestF10_OfficialSpecs,
    TestF11_MediaAssets,
    TestF12_SentinelGitHygiene,
)

from tests.tier2_boundaries import (
    TestB01_HeaderBoundaries,
    TestB02_HeroSearchBoundaries,
    TestB03_CatalogGridBoundaries,
    TestB04_CategoryCountersBoundaries,
    TestB05_NovvoBoundaries,
    TestB06_ToolModularizationBoundaries,
    TestB07_SharedDesignSystemBoundaries,
    TestB08_ConciergeBoundaries,
    TestB09_IdentityBoundaries,
    TestB10_OfficialSpecsBoundaries,
    TestB11_MediaAssetsBoundaries,
    TestB12_SentinelHygieneBoundaries,
)

from tests.tier3_cross_feature import (
    TestTier3_CrossFeatureCombinations,
)

from tests.tier4_scenarios import (
    TestTier4_RealWorldScenarios,
)

TIER_CLASSES = {
    1: [
        TestF01_HeaderNavigation,
        TestF02_HeroSearchBar,
        TestF03_CatalogGrid,
        TestF04_CategoryCounters,
        TestF05_NovvoIntegration,
        TestF06_ToolModularization,
        TestF07_SharedDesignSystem,
        TestF08_ConciergeWidget,
        TestF09_IdentityCompliance,
        TestF10_OfficialSpecs,
        TestF11_MediaAssets,
        TestF12_SentinelGitHygiene,
    ],
    2: [
        TestB01_HeaderBoundaries,
        TestB02_HeroSearchBoundaries,
        TestB03_CatalogGridBoundaries,
        TestB04_CategoryCountersBoundaries,
        TestB05_NovvoBoundaries,
        TestB06_ToolModularizationBoundaries,
        TestB07_SharedDesignSystemBoundaries,
        TestB08_ConciergeBoundaries,
        TestB09_IdentityBoundaries,
        TestB10_OfficialSpecsBoundaries,
        TestB11_MediaAssetsBoundaries,
        TestB12_SentinelHygieneBoundaries,
    ],
    3: [
        TestTier3_CrossFeatureCombinations,
    ],
    4: [
        TestTier4_RealWorldScenarios,
    ]
}

FEATURE_MAP = {
    "F01": "Header & Navigation (66px, single row, <dialog> drawer)",
    "F02": "Hero & Search Bar (single hero, #957B2B button)",
    "F03": "1:1 Aspect-Square Catalog Grid (subgrid, CLS=0)",
    "F04": "Category Tabs & Counters (Todos 46, Lavvi 39, Novvo 7)",
    "F05": "NOVVO Integration (Slate #22343E, Rose #A06F71, Montserrat)",
    "F06": "Tool Modularization (cinema, radar, credito, guias)",
    "F07": "Shared CSS System (lavvi-design-system.css)",
    "F08": "Concierge Chatbot (2-3 sentences, zero codename leaks)",
    "F09": "Identity Compliance (Zero fake CRECI 30.906 or bare CRECI SP)",
    "F10": "Official Specs (Tennis 18x36m, zero saibro in Hípica context)",
    "F11": "Media Assets (<500 KB, 5 JPGs, backup_raw_assets/)",
    "F12": "Cosimo Sentinel & Git Hygiene (Exit Code 0, .gitignore)",
}

class ColoredTestResult(unittest.TextTestResult):
    """Custom TestResult collecting detailed per-tier and per-feature metrics."""
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.successes: List[unittest.TestCase] = []
        self.tier_stats = {1: {"pass": 0, "fail": 0}, 2: {"pass": 0, "fail": 0}, 3: {"pass": 0, "fail": 0}, 4: {"pass": 0, "fail": 0}}
        self.feature_stats = {f"F{i:02d}": {"pass": 0, "fail": 0} for i in range(1, 13)}

    def _classify_test(self, test: unittest.TestCase) -> Tuple[int, str]:
        cls_name = test.__class__.__name__
        # Tier detection
        if "TestF" in cls_name:
            tier_num = 1
            feat_match = cls_name.replace("Test", "").split("_")[0]
        elif "TestB" in cls_name:
            tier_num = 2
            feat_match = cls_name.replace("TestB", "F").split("_")[0]
        elif "Tier3" in cls_name:
            tier_num = 3
            feat_match = "Cross"
        elif "Tier4" in cls_name:
            tier_num = 4
            feat_match = "Scenario"
        else:
            tier_num = 1
            feat_match = "F01"
        return tier_num, feat_match

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successes.append(test)
        tier_num, feat = self._classify_test(test)
        self.tier_stats[tier_num]["pass"] += 1
        if feat in self.feature_stats:
            self.feature_stats[feat]["pass"] += 1

    def addFailure(self, test, err):
        super().addFailure(test, err)
        tier_num, feat = self._classify_test(test)
        self.tier_stats[tier_num]["fail"] += 1
        if feat in self.feature_stats:
            self.feature_stats[feat]["fail"] += 1

    def addError(self, test, err):
        super().addError(test, err)
        tier_num, feat = self._classify_test(test)
        self.tier_stats[tier_num]["fail"] += 1
        if feat in self.feature_stats:
            self.feature_stats[feat]["fail"] += 1

def build_suite(selected_tiers: List[int]) -> unittest.TestSuite:
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for t in selected_tiers:
        for cls in TIER_CLASSES.get(t, []):
            suite.addTests(loader.loadTestsFromTestCase(cls))
    return suite

def print_banner():
    print("=" * 80)
    print("🏛️  LAVVI PRIVATE WEALTH & MEDIA AGENCY — E2E TEST SUITE")
    print("   Comprehensive Opaque-Box Test Runner (Tiers 1-4)")
    print("=" * 80)

def print_summary_report(result: ColoredTestResult, duration: float):
    total_tests = result.testsRun
    total_passes = len(result.successes)
    total_fails = len(result.failures) + len(result.errors)

    print("\n" + "=" * 80)
    print("📊 TEST EXECUTION SUMMARY REPORT")
    print("=" * 80)
    print(f"Total Tests Run: {total_tests} | Passed: {total_passes} | Failed: {total_fails} | Duration: {duration:.2f}s\n")

    print("┌" + "─" * 10 + "┬" + "─" * 30 + "┬" + "─" * 10 + "┬" + "─" * 10 + "┬" + "─" * 12 + "┐")
    print(f"│ {'Tier':^8} │ {'Description':<28} │ {'Passed':^8} │ {'Failed':^8} │ {'Pass Rate':^10} │")
    print("├" + "─" * 10 + "┼" + "─" * 30 + "┼" + "─" * 10 + "┼" + "─" * 10 + "┼" + "─" * 12 + "┤")

    tier_names = {
        1: "Tier 1: Feature Coverage",
        2: "Tier 2: Boundary & Corner Cases",
        3: "Tier 3: Cross-Feature (Pairwise)",
        4: "Tier 4: Real-World Scenarios"
    }

    for t in sorted(result.tier_stats.keys()):
        p = result.tier_stats[t]["pass"]
        f = result.tier_stats[t]["fail"]
        tot = p + f
        rate = f"{(p / tot * 100):.1f}%" if tot > 0 else "N/A"
        print(f"│ {f'Tier {t}':^8} │ {tier_names[t]:<28} │ {p:^8} │ {f:^8} │ {rate:^10} │")

    print("└" + "─" * 10 + "┴" + "─" * 30 + "┴" + "─" * 10 + "┴" + "─" * 10 + "┴" + "─" * 12 + "┘")

    # Feature breakdown table
    print("\n📋 FEATURE-BY-FEATURE READINESS CHECKLIST:")
    print("┌" + "─" * 6 + "┬" + "─" * 50 + "┬" + "─" * 10 + "┬" + "─" * 8 + "┐")
    print(f"│ {'Feat':^4} │ {'Feature Name':<48} │ {'Pass/Total':^8} │ {'Status':^6} │")
    print("├" + "─" * 6 + "┼" + "─" * 50 + "┼" + "─" * 10 + "┼" + "─" * 8 + "┤")

    for feat_id, feat_name in FEATURE_MAP.items():
        p = result.feature_stats[feat_id]["pass"]
        f = result.feature_stats[feat_id]["fail"]
        tot = p + f
        status = "✅ PASS" if tot > 0 and f == 0 else ("⏳ PEND" if tot > 0 and p > 0 else "❌ FAIL")
        print(f"│ {feat_id:^4} │ {feat_name:<48} │ {f'{p}/{tot}':^8} │ {status:^6} │")

    print("└" + "─" * 6 + "┴" + "─" * 50 + "┴" + "─" * 10 + "┴" + "─" * 8 + "┘")

    if result.failures or result.errors:
        print("\n🔍 FAILED TESTS DETAIL (PENDING IMPLEMENTATION MILESTONES):")
        print("-" * 80)
        all_issues = result.failures + result.errors
        for idx, (test, traceback_text) in enumerate(all_issues[:15], 1):
            test_name = test._testMethodName
            test_cls = test.__class__.__name__
            # Extract first line of failure message and truncate
            lines = [l for l in traceback_text.strip().split("\n") if l.strip()]
            first_err = lines[-1] if lines else "Failed"
            if len(first_err) > 120:
                first_err = first_err[:120] + "... [truncated]"
            print(f"[{idx:02d}] {test_cls}.{test_name}")
            print(f"     Reason: {first_err}")
        if len(all_issues) > 15:
            print(f"\n... and {len(all_issues) - 15} more pending tests.")
        print("-" * 80)
    else:
        print("\n🎉 ALL TESTS PASSED! Portal implementation meets 100% of specifications.")

def run_e2e_suite(tiers: List[int] = [1, 2, 3, 4], verbose: bool = False) -> bool:
    print_banner()
    suite = build_suite(tiers)
    runner = unittest.TextTestRunner(
        resultclass=ColoredTestResult,
        verbosity=2 if verbose else 1,
        stream=sys.stdout
    )

    t0 = time.time()
    result = runner.run(suite)
    duration = time.time() - t0

    print_summary_report(result, duration)
    return result.wasSuccessful()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lavvi Media Agency E2E Test Suite")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3, 4], help="Run specific test tier only (1, 2, 3, or 4)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose test execution output")
    args = parser.parse_args()

    selected_tiers = [args.tier] if args.tier else [1, 2, 3, 4]
    success = run_e2e_suite(tiers=selected_tiers, verbose=args.verbose)
    sys.exit(0 if success else 1)
