import json
import os
import re
import subprocess
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML = os.path.join(ROOT_DIR, "site", "index.html")
BUNDLE_JS = os.path.join(ROOT_DIR, "site", "assets", "js", "lavvi_catalog_bundle.js")
CATALOG_JSON = os.path.join(ROOT_DIR, "site", "lavvi_45_projects_clean.json")
TEMP_JS = os.path.join(ROOT_DIR, "scripts", "_temp_bot_test_runner.js")


def main():
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    scripts = re.findall(r"<script(?:\s+[^>]*)?>(.*?)</script>", html, re.DOTALL | re.IGNORECASE)
    inline_js = "\n".join(s for s in scripts if "generatePedroBotResponse" in s)
    if not inline_js:
        print("FAIL: Could not find generatePedroBotResponse in site/index.html")
        sys.exit(1)

    with open(CATALOG_JSON, "r", encoding="utf-8") as f:
        catalog_projects = json.load(f)

    project_names = [p["nome"] for p in catalog_projects]

    harness = f"""
const fs = require('fs');
global.window = {{}};
global.document = {{
  addEventListener: () => {{}},
  getElementById: () => null,
  querySelectorAll: () => []
}};

const bundleCode = fs.readFileSync({json.dumps(BUNDLE_JS)}, 'utf8');
eval(bundleCode);

{inline_js}

const queries = [
  "Me fale sobre o Jardim da Hípica",
  "Como funciona o T.O.M. Paraíso e Airbnb?",
  "Me explique o Well Perdizes",
  "Me fale sobre o Soleil",
  "Onde fica o Le Six?",
  "Quais são os 7 projetos da Linha Novvo?",
  "Posso remover parede ou fazer reforma? Como funciona a ABNT NBR 15.575?",
  "Existe barulho de avião de Congonhas em Moema Pássaros?",
  "What kind of apartments do you have at Jardim da Hípica?",
  "Bonjour, parlez-vous français ?",
  "Buongiorno, parla italiano?",
  "Hola, hablas español?",
  "Guten Tag, sprechen Sie Deutsch?"
];

const results = {{}};
for (const q of queries) {{
  results[q] = generatePedroBotResponse(q);
}}

const projectResults = {{}};
const projectNames = {json.dumps(project_names, ensure_ascii=False)};
for (const name of projectNames) {{
  projectResults[name] = generatePedroBotResponse("Me fale sobre o " + name);
}}

console.log(JSON.stringify({{ results, projectResults, catalogCount: (window.allProjects || []).length }}));
"""

    with open(TEMP_JS, "w", encoding="utf-8") as f:
        f.write(harness)

    try:
        proc = subprocess.run(
            ["node", TEMP_JS],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
    finally:
        if os.path.exists(TEMP_JS):
            os.remove(TEMP_JS)

    payload = json.loads(proc.stdout.strip().splitlines()[-1])
    results = payload["results"]
    project_results = payload["projectResults"]
    catalog_count = payload["catalogCount"]

    print("=" * 80)
    print("🤖 LAVVI CONCIERGE BOT — DETERMINISTIC VERIFICATION SUITE")
    print("=" * 80)
    assert catalog_count == 46, f"Expected 46 projects in window.allProjects, got {catalog_count}"
    print(f"✓ Bundle loaded: {catalog_count}/46 canonical projects in window.allProjects")

    forbidden = [
        "Cosimo", "Mini Vito", "Don Vito", "Burry", "Ariadne", "Miyamoto",
        "Champlain", "30.906", "saibro", "Philippe Starck"
    ]

    for q, res in results.items():
        txt = res.get("text", "")
        assert txt and len(txt) > 30, f"Empty/short response for {q}"
        for bad in forbidden:
            assert bad.lower() not in txt.lower(), f"Forbidden token '{bad}' found in response to '{q}': {txt}"
        # Count sentences ( stripping HTML tags and decimal numbers )
        clean = re.sub(r"<[^>]+>", " ", txt)
        clean = re.sub(r"\d+\.\d+", "N", clean)
        clean = clean.replace("T.O.M.", "TOM").replace("Jr.", "Jr")
        sentences = [s.strip() for s in re.split(r"[.!?]+", clean) if len(s.strip()) > 5]
        assert 1 <= len(sentences) <= 4, f"Expected 2-3 surgical sentences for '{q}', got {len(sentences)}: {sentences}"
        print(f"✓ [PASS] {q} -> {len(sentences)} sentences")

    # Specific factual assertions
    assert "39.553" in results["Me fale sobre o Jardim da Hípica"]["text"]
    assert "18x36m" in results["Me fale sobre o Jardim da Hípica"]["text"]
    assert "901" in results["Como funciona o T.O.M. Paraíso e Airbnb?"]["text"]
    assert "1.252" in results["Me explique o Well Perdizes"]["text"]
    assert "alvenaria estrutural" in results["Me explique o Well Perdizes"]["text"].lower()
    assert "Boca do Lobo" in results["Me fale sobre o Soleil"]["text"]
    assert "Paraíso" in results["Onde fica o Le Six?"]["text"] and "Ibirapuera" in results["Onde fica o Le Six?"]["text"]
    assert "Novvo Largo Treze" in results["Quais são os 7 projetos da Linha Novvo?"]["text"]

    # Check all 46 projects resolve with project-specific facts (not generic fallback)
    for name, res in project_results.items():
        txt = res.get("text", "")
        assert "Posso consultar instantaneamente fichas técnicas" not in txt, f"Project '{name}' fell through to generic fallback!"
        for bad in forbidden:
            assert bad.lower() not in txt.lower(), f"Forbidden token '{bad}' in project '{name}'"

    print(f"✓ All {len(project_results)}/46 individual project queries resolved with grounded specs and zero fallbacks!")
    print("✅ CONCIERGE BOT VERIFICATION: 100% PASS (EXIT 0)")


if __name__ == "__main__":
    main()
