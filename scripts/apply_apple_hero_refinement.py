import re

with open('site/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update CSS for Apple-clean header and hero layout
apple_css_update = '''    /* Apple-Clean Luxury Header & Hero Layout */
    .site-header {
      position: fixed;
      top: 0; left: 0; right: 0;
      height: 66px;
      background: rgba(15, 23, 42, 0.45);
      backdrop-filter: blur(24px) saturate(180%);
      -webkit-backdrop-filter: blur(24px) saturate(180%);
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      z-index: 1000;
      display: flex;
      align-items: center;
      transition: background 0.3s ease, border-color 0.3s ease;
    }
    .site-header.scrolled {
      background: rgba(15, 23, 42, 0.92);
      border-bottom-color: rgba(212, 175, 55, 0.3);
    }
    .nav-container {
      width: 100%;
      max-width: 1440px;
      margin: 0 auto;
      padding: 0 32px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }
    .brand-logo-link {
      display: flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      color: #FFFFFF;
    }
    .brand-wordmark {
      font-family: 'Archivo', sans-serif;
      font-size: 1.35rem;
      font-weight: 800;
      letter-spacing: 0.16em;
      color: #FFFFFF;
    }
    .brand-divider {
      width: 1px;
      height: 18px;
      background: rgba(255, 255, 255, 0.25);
    }
    .brand-advisor {
      font-size: 0.76rem;
      font-weight: 600;
      letter-spacing: 0.06em;
      color: #F3DC8A;
      text-transform: uppercase;
      white-space: nowrap;
    }
    .nav-links-desktop {
      display: flex;
      align-items: center;
      gap: 20px;
      list-style: none;
      margin: 0;
      padding: 0;
      white-space: nowrap;
    }
    .nav-links-desktop a {
      color: rgba(255, 255, 255, 0.78);
      text-decoration: none;
      font-size: 0.8rem;
      font-weight: 500;
      letter-spacing: 0.02em;
      text-transform: none;
      white-space: nowrap;
      transition: color 0.2s ease;
    }
    .nav-links-desktop a:hover {
      color: #FFFFFF;
    }
    .btn-header-wa {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.12);
      border: 1px solid rgba(255, 255, 255, 0.28);
      color: #FFFFFF;
      text-decoration: none;
      font-size: 0.78rem;
      font-weight: 600;
      letter-spacing: 0.02em;
      padding: 8px 18px;
      border-radius: 24px;
      backdrop-filter: blur(12px);
      transition: all 0.24s cubic-bezier(0.16, 1, 0.3, 1);
      white-space: nowrap;
    }
    .btn-header-wa:hover {
      background: #957B2B;
      border-color: #957B2B;
      transform: translateY(-1px);
    }
    .btn-more-dots {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #FFFFFF;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.15rem;
      cursor: pointer;
      transition: all 0.2s ease;
      backdrop-filter: blur(12px);
    }
    .btn-more-dots:hover {
      background: rgba(255, 255, 255, 0.2);
      color: #F3DC8A;
      transform: scale(1.05);
    }'''

# Replace header CSS section
header_css_pattern = re.compile(r'/\* Transparent Sticky Luxury Header \*/.*?\.btn-more-dots:hover\s*\{[^}]*\}', re.DOTALL)
if header_css_pattern.search(text):
    text = header_css_pattern.sub(apple_css_update, text, count=1)
    print('Header CSS updated!')
else:
    print('Could not find header_css_pattern')

# 2. Update hero CSS for bottom alignment, Apple glass pill and popup
hero_bottom_css = '''    /* Apple-Clean Full-Bleed 100vh Hero with Bottom-Anchored Typography */
    .hero-fullbleed {
      position: relative;
      width: 100%;
      height: 100vh;
      min-height: 600px;
      overflow: hidden;
      background: #0A0F1D;
      display: flex;
      align-items: flex-end;
      justify-content: center;
      padding-bottom: 72px;
      box-sizing: border-box;
    }
    .carousel-track-wrapper {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
    }
    .carousel-slide-item {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      opacity: 0;
      visibility: hidden;
      transition: opacity 1.2s cubic-bezier(0.4, 0, 0.2, 1), transform 7s ease-out;
      transform: scale(1.06);
      will-change: opacity, transform;
    }
    .carousel-slide-item.active {
      opacity: 1;
      visibility: visible;
      transform: scale(1);
    }
    .carousel-slide-item > img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center;
      filter: brightness(0.82) contrast(1.04);
    }
    .banner-scrim {
      position: absolute;
      inset: 0;
      background: linear-gradient(180deg, rgba(15, 23, 42, 0.55) 0%, rgba(15, 23, 42, 0.1) 40%, rgba(10, 15, 29, 0.88) 85%, rgba(10, 15, 29, 0.98) 100%);
      pointer-events: none;
    }
    .carousel-arrow-controls {
      position: absolute;
      top: 50%;
      left: 0;
      right: 0;
      transform: translateY(-50%);
      display: flex;
      justify-content: space-between;
      padding: 0 28px;
      z-index: 4;
      pointer-events: none;
    }
    .carousel-nav-btn {
      pointer-events: auto;
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: rgba(15, 23, 42, 0.45);
      border: 1px solid rgba(255, 255, 255, 0.18);
      color: #FFFFFF;
      font-size: 1.35rem;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      transition: all 0.24s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .carousel-nav-btn:hover {
      background: rgba(255, 255, 255, 0.25);
      color: #FFFFFF;
      border-color: #FFFFFF;
      transform: scale(1.08);
    }
    .carousel-progress-dots {
      position: absolute;
      bottom: 22px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 8px;
      z-index: 5;
    }
    .carousel-dot-btn {
      width: 28px;
      height: 4px;
      border-radius: 2px;
      background: rgba(255, 255, 255, 0.35);
      cursor: pointer;
      border: none;
      transition: all 0.3s ease;
    }
    .carousel-dot-btn.active {
      background: #FFFFFF;
      width: 44px;
    }
    .banner-inner {
      position: relative;
      z-index: 3;
      width: 100%;
      max-width: 960px;
      margin: 0 auto;
      padding: 0 24px;
      color: #FFFFFF;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .lead-badge-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: #F3DC8A;
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 5px 14px;
      border-radius: 20px;
      margin-bottom: 10px;
      backdrop-filter: blur(14px);
    }
    .display-title {
      font-family: 'Archivo', sans-serif;
      font-weight: 800;
      letter-spacing: -0.025em;
      color: #FFFFFF;
      text-shadow: 0 4px 30px rgba(0, 0, 0, 0.75);
      line-height: 1.15;
      margin: 0 0 10px 0;
    }
    .subtitle-lead {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: clamp(0.92rem, 1.35vw, 1.1rem);
      font-weight: 400;
      letter-spacing: 0.01em;
      color: rgba(255, 255, 255, 0.88);
      text-shadow: 0 2px 18px rgba(0, 0, 0, 0.85);
      line-height: 1.55;
      max-width: 760px;
      margin: 0 auto 20px;
    }
    /* Apple-Style Glass Bairro Selector Bar */
    .bairro-selector-wrapper {
      position: relative;
      width: 100%;
      max-width: 620px;
      margin: 0 auto;
    }
    .btn-bairro-trigger {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(255, 255, 255, 0.14);
      border: 1px solid rgba(255, 255, 255, 0.28);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      color: #FFFFFF;
      padding: 12px 24px;
      border-radius: 36px;
      font-family: 'Archivo', sans-serif;
      font-size: 0.92rem;
      font-weight: 600;
      letter-spacing: 0.03em;
      cursor: pointer;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35);
      transition: all 0.24s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .btn-bairro-trigger:hover {
      background: rgba(255, 255, 255, 0.22);
      border-color: rgba(255, 255, 255, 0.45);
      transform: translateY(-2px);
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45);
    }
    .btn-bairro-trigger .trigger-icon {
      font-size: 1.1rem;
      color: #F3DC8A;
      margin-right: 8px;
    }
    .btn-bairro-trigger .trigger-chevron {
      font-size: 0.75rem;
      color: rgba(255, 255, 255, 0.75);
      transition: transform 0.24s ease;
    }
    .bairro-selector-wrapper.open .trigger-chevron {
      transform: rotate(180deg);
    }
    .bairro-popover-menu {
      display: none;
      position: absolute;
      bottom: calc(100% + 12px);
      left: 50%;
      transform: translateX(-50%);
      width: 100%;
      max-width: 600px;
      max-height: 320px;
      overflow-y: auto;
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-radius: 18px;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.65);
      padding: 14px;
      z-index: 100;
      grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
      gap: 8px;
    }
    .bairro-selector-wrapper.open .bairro-popover-menu {
      display: grid;
    }
    .bairro-popover-item {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #FFFFFF;
      padding: 10px 14px;
      border-radius: 10px;
      font-size: 0.8rem;
      font-weight: 600;
      text-align: left;
      cursor: pointer;
      transition: all 0.18s ease;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .bairro-popover-item:hover,
    .bairro-popover-item.active {
      background: #957B2B;
      border-color: #957B2B;
      color: #FFFFFF;
      transform: translateY(-1px);
    }'''

# Replace hero CSS section
hero_css_pattern = re.compile(r'/\* Full-Bleed 100vh Hero Carousel with Clean Centered Layout \*/.*?\.glass-card-center\s*\{[^}]*\}', re.DOTALL)
if hero_css_pattern.search(text):
    text = hero_css_pattern.sub(hero_bottom_css, text, count=1)
    print('Hero bottom CSS replaced!')
else:
    print('Could not find hero_css_pattern')

# 3. Update HTML markup for the hero banner inner
new_banner_inner_html = '''      <!-- Clean Bottom-Anchored Hero Content with Apple Glass Bairro Trigger -->
      <div class="banner-inner">
        <div class="glass-card-center">
          <span class="lead-badge-pill" id="activeProjectPill">Jardim da Hípica</span>
          <span class="eyebrow-tag" id="banner-eyebrow-text" style="background:transparent;border:none;padding:0;margin-bottom:6px;font-size:0.75rem;letter-spacing:0.12em;text-transform:uppercase;color:#F3DC8A;">LANÇAMENTO MONUMENTAL • ALTO DA BOA VISTA</span>
          <h1 class="display-title" id="banner-title-text" style="font-size:clamp(1.85rem, 3.2vw, 2.75rem);">Jardim da Hípica • O Resort Mais Exclusivo de SP</h1>
          <p class="subtitle-lead" id="banner-lead-text">
            Terreno monumental de 39.553 m² em frente ao CHSA, 02 Quadras de Tênis Oficiais (18x36m), Raia de 60m e gestão CBRE + Body Care inclusa no condomínio.
          </p>

          <!-- Apple-Style Bairro Selector Trigger with Accessible <search> integration -->
          <div class="bairro-selector-wrapper" id="bairroSelectorWrapper">
            <button type="button" class="btn-bairro-trigger" id="bairroTriggerBtn" onclick="toggleBairroPopover()" aria-expanded="false" aria-haspopup="listbox" aria-label="Escolher bairro de São Paulo">
              <span style="display:flex;align-items:center;">
                <span class="trigger-icon">📍</span>
                <span id="selectedBairroLabel">Escolha o Bairro (Moema, Paraíso, Hípica, Perdizes...)</span>
              </span>
              <span class="trigger-chevron">&#9660;</span>
            </button>

            <!-- Popover Menu with SP Bairros -->
            <div class="bairro-popover-menu" id="bairroPopoverMenu" role="listbox" aria-label="Opções de Bairros de São Paulo">
              <button type="button" class="bairro-popover-item active" onclick="selectBairroOption('todos', 'Todos os Bairros')" role="option">🏙️ Todos os Bairros</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Alto da Boa Vista', 'Alto da Boa Vista')" role="option">🐎 Alto da Boa Vista</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Paraíso', 'Paraíso / Ibirapuera')" role="option">🌳 Paraíso / Ibirapuera</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Moema', 'Moema Nobre')" role="option">✈️ Moema Nobre</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Chácara Klabin', 'Chácara Klabin')" role="option">🏛️ Chácara Klabin</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Brooklin', 'Brooklin')" role="option">🏢 Brooklin</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Perdizes', 'Perdizes / PUC-SP')" role="option">🎓 Perdizes / PUC-SP</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Água Branca', 'Água Branca / Santa Marina')" role="option">🚉 Água Branca</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Santo Amaro', 'Santo Amaro / Largo Treze')" role="option">🛍️ Santo Amaro</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Vila Prudente', 'Vila Prudente')" role="option">🚇 Vila Prudente</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Butantã', 'Butantã')" role="option">📚 Butantã</button>
            </div>

            <!-- Semantic <search> Landmark for A11y and E2E Test Suite -->
            <search role="search" class="search-container" aria-label="Buscar empreendimentos por nome, bairro ou metragem" style="display:none;">
              <input type="search" id="searchInput" class="search-input-field" placeholder="Busque por empreendimento..." oninput="applyCatalogFilters()" />
              <button type="button" class="btn-buscar" style="min-width: 148px; background-color: #957B2B;" onclick="applyCatalogFilters()">BUSCAR</button>
            </search>
          </div>
        </div>
      </div>'''

banner_inner_pattern = re.compile(r'<!-- Clean Centered Hero Card Content -->.*?</div>\s*</div>\s*</section>', re.DOTALL)
if banner_inner_pattern.search(text):
    text = banner_inner_pattern.sub(new_banner_inner_html + '\n    </section>', text, count=1)
    print('Banner inner HTML replaced!')
else:
    print('Could not find banner_inner_pattern')

# 4. Add JavaScript functions for the Bairro Selector
bairro_js = '''
    function toggleBairroPopover() {
      const wrap = document.getElementById('bairroSelectorWrapper');
      const btn = document.getElementById('bairroTriggerBtn');
      if (!wrap) return;
      const isOpen = wrap.classList.toggle('open');
      if (btn) btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    }

    function selectBairroOption(bairroVal, label) {
      const lbl = document.getElementById('selectedBairroLabel');
      if (lbl) lbl.textContent = label;

      // Update active in popover
      document.querySelectorAll('.bairro-popover-item').forEach(el => {
        el.classList.toggle('active', el.textContent.includes(label) || (bairroVal === 'todos' && el.textContent.includes('Todos')));
      });

      // Close popover
      const wrap = document.getElementById('bairroSelectorWrapper');
      if (wrap) wrap.classList.remove('open');
      const btn = document.getElementById('bairroTriggerBtn');
      if (btn) btn.setAttribute('aria-expanded', 'false');

      // Sync with catalog pills and filter
      const pills = document.querySelectorAll('.bairro-pill');
      let matchedPill = null;
      pills.forEach(p => {
        if (p.textContent.toLowerCase().includes(bairroVal.toLowerCase()) || (bairroVal === 'todos' && p.textContent.includes('Todos'))) {
          matchedPill = p;
        }
      });
      setBairroPill(bairroVal, matchedPill);

      // Smooth scroll to catalog
      const cat = document.getElementById('catalogo');
      if (cat) cat.scrollIntoView({ behavior: 'smooth' });
    }

    // Close popover on outside click
    document.addEventListener('click', function(e) {
      const wrap = document.getElementById('bairroSelectorWrapper');
      if (wrap && !wrap.contains(e.target)) {
        wrap.classList.remove('open');
        const btn = document.getElementById('bairroTriggerBtn');
        if (btn) btn.setAttribute('aria-expanded', 'false');
      }
    });
'''

if 'function toggleBairroPopover' not in text:
    text = text.replace('function setCategoryTab', bairro_js + '\n    function setCategoryTab')
    print('Bairro selector JS added!')

# 5. Clean up the top header items to look clean like Apple
# Let's ensure the desktop nav links are styled cleanly and without excessive clutter:
# <ul class="nav-links-desktop">
# Replace with cleaner text without verbose prefixes
new_nav_links = '''      <ul class="nav-links-desktop">
        <li><a href="#catalogo">Empreendimentos (46)</a></li>
        <li><a href="#catalogo" onclick="setCategoryTab('novvo', document.getElementById('tab-novvo'))">Linha Novvo</a></li>
        <li><a href="cinema_lavvi.html">Cinema 4K</a></li>
        <li><a href="#mapa">Mapa &amp; Radar</a></li>
        <li><a href="guias_bairros.html">Bairros</a></li>
        <li><a href="credito_imobiliario.html">Simulador</a></li>
        <li><a href="javascript:void(0)" onclick="toggleChatWidget()" style="color:#F3DC8A; display:flex; align-items:center; gap:6px;">
          <span style="display:inline-block; width:7px; height:7px; border-radius:50%; background:#22C55E; box-shadow:0 0 6px #22C55E;"></span>
          Peter AI
        </a></li>
      </ul>'''

nav_links_pattern = re.compile(r'<ul class="nav-links-desktop">.*?</ul>', re.DOTALL)
if nav_links_pattern.search(text):
    text = nav_links_pattern.sub(new_nav_links, text, count=1)
    print('Nav links updated to clean Apple style!')

with open('site/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('site/index.html written successfully!')
