import re

with open('site/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update CSS for Header, Brand, 3 dots top left, WhatsApp green, and discreet Bairro Trigger
css_refinement = '''    /* Apple-Clean Luxury Header with Left-Aligned 3-Dots & Emerald WhatsApp */
    .site-header {
      position: fixed;
      top: 0; left: 0; right: 0;
      height: 66px;
      background: rgba(15, 23, 42, 0.55);
      backdrop-filter: blur(24px) saturate(180%);
      -webkit-backdrop-filter: blur(24px) saturate(180%);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      z-index: 1000;
      display: flex;
      align-items: center;
      transition: background 0.3s ease, border-color 0.3s ease;
    }
    .site-header.scrolled {
      background: rgba(15, 23, 42, 0.94);
      border-bottom-color: rgba(212, 175, 55, 0.25);
    }
    .nav-container {
      width: 100%;
      max-width: 1440px;
      margin: 0 auto;
      padding: 0 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }
    .nav-left-group {
      display: flex;
      align-items: center;
      gap: 12px;
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
      font-size: 0.74rem;
      font-weight: 600;
      letter-spacing: 0.04em;
      color: #F3DC8A;
      text-transform: none;
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
      color: rgba(255, 255, 255, 0.82);
      text-decoration: none;
      font-size: 0.8rem;
      font-weight: 500;
      letter-spacing: 0.01em;
      text-transform: none;
      white-space: nowrap;
      transition: color 0.2s ease;
    }
    .nav-links-desktop a:hover {
      color: #FFFFFF;
    }
    .nav-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    /* Official WhatsApp Green Button */
    .btn-header-wa {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #25D366;
      border: 1px solid rgba(255, 255, 255, 0.35);
      color: #FFFFFF;
      text-decoration: none;
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.02em;
      padding: 8px 18px;
      border-radius: 24px;
      box-shadow: 0 4px 14px rgba(37, 211, 102, 0.35);
      transition: all 0.24s cubic-bezier(0.16, 1, 0.3, 1);
      white-space: nowrap;
    }
    .btn-header-wa:hover {
      background: #20BA5A;
      box-shadow: 0 6px 20px rgba(37, 211, 102, 0.5);
      transform: translateY(-1px);
    }
    .wa-icon-svg {
      width: 16px;
      height: 16px;
      fill: #FFFFFF;
      flex-shrink: 0;
    }
    /* Three Dots Dropdown Menu on Top Left */
    .more-options-wrap {
      position: relative;
      display: inline-block;
    }
    .btn-more-dots {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.18);
      color: #FFFFFF;
      width: 34px;
      height: 34px;
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
      background: rgba(255, 255, 255, 0.22);
      color: #F3DC8A;
      transform: scale(1.05);
    }
    .more-options-menu {
      display: none;
      position: absolute;
      top: calc(100% + 8px);
      left: 0;
      right: auto;
      width: 250px;
      background: rgba(15, 23, 42, 0.96);
      backdrop-filter: blur(20px);
      border: 1px solid rgba(212, 175, 55, 0.35);
      border-radius: 12px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5);
      padding: 8px 0;
      z-index: 1100;
      flex-direction: column;
    }
    .more-options-menu.open {
      display: flex;
    }
    .more-options-menu a {
      padding: 10px 18px;
      color: rgba(255, 255, 255, 0.9);
      text-decoration: none;
      font-size: 0.82rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: background 0.18s ease, color 0.18s ease;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .more-options-menu a:last-child {
      border-bottom: none;
    }
    .more-options-menu a:hover {
      background: rgba(212, 175, 55, 0.15);
      color: #F3DC8A;
    }
    /* Compact Minimal Language Selector */
    .lang-pill-group {
      display: flex;
      align-items: center;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 20px;
      padding: 2px 4px;
    }
    .lang-btn {
      background: transparent;
      border: none;
      color: rgba(255, 255, 255, 0.65);
      font-size: 0.68rem;
      font-weight: 600;
      padding: 3px 6px;
      border-radius: 12px;
      cursor: pointer;
      text-transform: uppercase;
      transition: all 0.15s ease;
    }
    .lang-btn:hover {
      color: #FFFFFF;
    }
    .lang-btn.active {
      background: rgba(255, 255, 255, 0.2);
      color: #F3DC8A;
      font-weight: 700;
    }
    /* Discreet Apple Bairro Trigger */
    .bairro-selector-wrapper {
      position: relative;
      width: 100%;
      max-width: 440px;
      margin: 0 auto;
    }
    .btn-bairro-trigger {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(15, 23, 42, 0.45);
      border: 1px solid rgba(255, 255, 255, 0.2);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      color: rgba(255, 255, 255, 0.92);
      padding: 9px 18px;
      border-radius: 24px;
      font-family: 'Archivo', sans-serif;
      font-size: 0.82rem;
      font-weight: 500;
      letter-spacing: 0.02em;
      cursor: pointer;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
      transition: all 0.24s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .btn-bairro-trigger:hover {
      background: rgba(15, 23, 42, 0.7);
      border-color: rgba(255, 255, 255, 0.35);
      transform: translateY(-1px);
    }
    .btn-bairro-trigger .trigger-icon {
      font-size: 0.95rem;
      color: #F3DC8A;
      margin-right: 6px;
    }
    .btn-bairro-trigger .trigger-chevron {
      font-size: 0.68rem;
      color: rgba(255, 255, 255, 0.6);
      transition: transform 0.24s ease;
    }
    .bairro-selector-wrapper.open .trigger-chevron {
      transform: rotate(180deg);
    }
    .bairro-popover-menu {
      display: none;
      position: absolute;
      bottom: calc(100% + 10px);
      left: 50%;
      transform: translateX(-50%);
      width: 100%;
      max-width: 580px;
      max-height: 340px;
      overflow-y: auto;
      background: rgba(15, 23, 42, 0.97);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-radius: 16px;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.7);
      padding: 12px;
      z-index: 100;
      grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
      gap: 6px;
    }
    .bairro-selector-wrapper.open .bairro-popover-menu {
      display: grid;
    }
    .bairro-popover-item {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: #FFFFFF;
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 0.78rem;
      font-weight: 500;
      text-align: left;
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .bairro-popover-item:hover,
    .bairro-popover-item.active {
      background: #957B2B;
      border-color: #957B2B;
      color: #FFFFFF;
    }'''

# Replace header and bairro CSS
old_header_css = re.search(r'/\* Apple-Clean Luxury Header & Hero Layout \*/.*?\.bairro-popover-item\.active\s*\{[^}]*\}', text, re.DOTALL)
if old_header_css:
    text = text[:old_header_css.start()] + css_refinement + text[old_header_css.end():]
    print('CSS refinement replaced!')
else:
    print('Could not find old_header_css, appending to head')

# 2. Update Header HTML:
# Top left: 3 dots button + LAVVI + "Peter Corretor direto da Lavvi grupo Cyrela"
# Middle: Clean nav links without "Peter AI" next to simulador
# Top right: Language selector + WhatsApp Peter in green with SVG logo
new_header_html = '''  <!-- 1. FIXED 66PX OFFICIAL LAVVI HEADER -->
  <header class="site-header">
    <nav class="nav-container" aria-label="Navegação Principal">
      <div class="nav-left-group">
        <!-- 3 Dots More Options Menu on Top Left -->
        <div class="more-options-wrap">
          <button type="button" class="btn-more-dots" id="moreOptionsBtn" onclick="toggleMoreOptionsMenu()" aria-label="Mais opções e ferramentas" aria-expanded="false">
            &#8942;
          </button>
          <div class="more-options-menu" id="moreOptionsMenu">
            <a href="radar_mapa.html">🗺️ Mapa 46 Projetos &amp; 3km</a>
            <a href="cinema_lavvi.html">🎬 Cinema Lavvi 4K</a>
            <a href="guias_bairros.html">📍 Guias de Bairros &amp; NBR</a>
            <a href="credito_imobiliario.html">📈 Simulador 35/65 vs CDI</a>
            <a href="comparativos.html">⚖️ Comparativos Técnicos</a>
            <a href="dossiers/index.html">📑 Private Banking Dossiers</a>
            <a href="crm_cockpit.html" style="color:#F3DC8A;">🔒 Cockpit do Corretor</a>
          </div>
        </div>

        <a href="#topo" class="brand-logo-link">
          <svg class="brand-lion-icon" width="26" height="26" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path d="M16 3C14.2 3 12.8 3.8 11.8 5.2C10.5 4.8 9.1 5.2 8.2 6.3C7.4 7.2 7.1 8.6 7.5 9.8C6.3 10.8 5.6 12.3 5.8 14C6 15.5 6.9 16.8 8.2 17.5C8 18.8 8.5 20.2 9.6 21.1C10.5 21.8 11.7 22.1 12.8 21.9C13.5 23.2 14.8 24.1 16.3 24.3L16.5 27.5C16.5 28.3 17.2 29 18 29C18.8 29 19.5 28.3 19.5 27.5L19.2 23.8C22.2 23.2 24.5 20.8 25 17.8C25.5 14.8 24.1 11.8 21.6 10.2C21.4 8.2 20.2 6.5 18.5 5.5C17.7 3.9 16.9 3 16 3Z" fill="#D4AF37"/>
            <path d="M17.5 9.5C17.5 10.3 16.8 11 16 11C15.2 11 14.5 10.3 14.5 9.5C14.5 8.7 15.2 8 16 8C16.8 8 17.5 8.7 17.5 9.5Z" fill="#182842"/>
            <path d="M19 14.5C18.2 14.5 17.5 13.8 17.5 13C17.5 12.2 18.2 11.5 19 11.5C19.8 11.5 20.5 12.2 20.5 13C20.5 13.8 19.8 14.5 19 14.5Z" fill="#D4AF37"/>
          </svg>
          <span class="brand-wordmark">LAVVI</span>
          <span class="brand-divider"></span>
          <span class="brand-advisor">Peter Corretor direto da Lavvi grupo Cyrela</span>
        </a>
      </div>

      <ul class="nav-links-desktop">
        <li><a href="#catalogo">Empreendimentos (46)</a></li>
        <li><a href="#catalogo" onclick="setCategoryTab('novvo', document.getElementById('tab-novvo'))">Linha Novvo</a></li>
        <li><a href="cinema_lavvi.html">Cinema 4K</a></li>
        <li><a href="#mapa">Mapa &amp; Radar</a></li>
        <li><a href="guias_bairros.html">Bairros</a></li>
        <li><a href="credito_imobiliario.html">Simulador</a></li>
      </ul>

      <div class="nav-actions">
        <div class="lang-pill-group" id="lang-selector" role="group" aria-label="Idioma">
          <button type="button" class="lang-btn active" onclick="setLanguage('pt')">PT</button>
          <button type="button" class="lang-btn" onclick="setLanguage('en')">EN</button>
          <button type="button" class="lang-btn" onclick="setLanguage('fr')">FR</button>
          <button type="button" class="lang-btn" onclick="setLanguage('it')">IT</button>
          <button type="button" class="lang-btn" onclick="setLanguage('es')">ES</button>
          <button type="button" class="lang-btn" onclick="setLanguage('de')">DE</button>
        </div>

        <a href="https://wa.me/5511966105952?text=Ol%C3%A1%20Peter%2C%20estou%20no%20portal%20Lavvi%20e%20gostaria%20de%20atendimento%20direto." target="_blank" rel="noopener" class="btn-header-wa" id="nav-wa-btn">
          <svg class="wa-icon-svg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M12.031 0C5.393 0 0 5.393 0 12.031c0 2.12.553 4.184 1.605 6.007L.062 24l6.143-1.611A11.96 11.96 0 0012.031 24c6.638 0 12.031-5.393 12.031-12.031C24.062 5.393 18.669 0 12.031 0zm0 22.016c-1.848 0-3.644-.497-5.215-1.442l-.374-.225-3.87 1.015 1.033-3.771-.247-.393a9.987 9.987 0 01-1.531-5.169c0-5.526 4.496-10.022 10.022-10.022 5.526 0 10.022 4.496 10.022 10.022 0 5.526-4.496 10.022-10.022 10.022zm5.495-7.51c-.301-.151-1.782-.88-2.058-.981-.277-.1-.478-.151-.679.151-.2.301-.778.981-.954 1.182-.176.2-.352.226-.653.075s-1.27-.468-2.42-1.494c-.895-.798-1.499-1.784-1.675-2.086-.176-.301-.019-.464.132-.614.136-.135.301-.352.452-.528.151-.176.201-.301.301-.502.1-.2.05-.377-.025-.528-.075-.151-.679-1.635-.93-2.239-.244-.588-.493-.508-.679-.517l-.578-.01c-.2 0-.527.075-.803.377s-1.055 1.031-1.055 2.514c0 1.483 1.08 2.917 1.231 3.118.151.201 2.125 3.245 5.148 4.552.719.311 1.28.497 1.718.636.722.23 1.379.197 1.898.12.579-.086 1.782-.728 2.033-1.432.251-.703.251-1.306.176-1.432-.075-.126-.276-.201-.577-.352z"/>
          </svg>
          WhatsApp Peter
        </a>

        <button type="button" class="btn-drawer-toggle" id="mobile-menu-open-btn" aria-controls="mobile-nav-dialog" aria-expanded="false" onclick="toggleMobileDrawer(true)">
          Menu
        </button>
      </div>
    </nav>
  </header>'''

header_pattern = re.compile(r'<!-- 1\. FIXED 66PX OFFICIAL LAVVI HEADER -->.*?<!-- NATIVE DIALOG DRAWER FOR MOBILE NAVIGATION -->', re.DOTALL)
if header_pattern.search(text):
    text = header_pattern.sub(new_header_html + '\n\n  <!-- NATIVE DIALOG DRAWER FOR MOBILE NAVIGATION -->', text, count=1)
    print('Header HTML replaced successfully!')
else:
    print('Could not find header_pattern')

# 3. Update Bairro Popover Menu with Complete Bairros List (including Brás, Vila Prudente, Anália Franco, Barra Funda, etc.)
complete_bairros_popover = '''            <!-- Popover Menu with Complete SP Bairros (Lavvi & Linha Meu Novvo) -->
            <div class="bairro-popover-menu" id="bairroPopoverMenu" role="listbox" aria-label="Opções de Bairros de São Paulo">
              <button type="button" class="bairro-popover-item active" onclick="selectBairroOption('todos', 'Todos os Bairros')" role="option">🏙️ Todos os Bairros (46)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Alto da Boa Vista', 'Alto da Boa Vista')" role="option">🐎 Alto da Boa Vista (2)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Moema', 'Moema Nobre')" role="option">✈️ Moema Nobre (8)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Paraíso', 'Paraíso / Ibirapuera')" role="option">🌳 Paraíso / Ibirapuera (5)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Chácara Klabin', 'Chácara Klabin')" role="option">🏛️ Chácara Klabin (5)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Brás', 'Brás / Complexo Wonder')" role="option">🏢 Brás / Wonder (4)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Brooklin', 'Brooklin')" role="option">💼 Brooklin (2)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Perdizes', 'Perdizes / PUC-SP')" role="option">🎓 Perdizes (2)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Vila Prudente', 'Vila Prudente')" role="option">🚇 Vila Prudente (2)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Ipiranga', 'Ipiranga')" role="option">🌿 Ipiranga (2)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Água Branca', 'Água Branca / Santa Marina')" role="option">🚉 Água Branca (1)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Barra Funda', 'Barra Funda')" role="option">🎨 Barra Funda (1)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Anália Franco', 'Anália Franco')" role="option">💎 Anália Franco (1)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Jardim Marajoara', 'Jardim Marajoara')" role="option">🏡 Jardim Marajoara (1)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Santo Amaro', 'Santo Amaro / Largo Treze')" role="option">🛍️ Santo Amaro (1)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Vila Mariana', 'Vila Mariana')" role="option">🏫 Vila Mariana (1)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Butantã', 'Butantã')" role="option">📚 Butantã (1)</button>
            </div>'''

popover_pattern = re.compile(r'<!-- Popover Menu with SP Bairros -->.*?</div>\s*<!-- Semantic <search>', re.DOTALL)
if popover_pattern.search(text):
    text = popover_pattern.sub(complete_bairros_popover + '\n\n            <!-- Semantic <search>', text, count=1)
    print('Popover menu replaced successfully!')
else:
    print('Could not find popover_pattern')

# Also update the Bairro Quick Filter Pills row in #catalogo to include Brás and all key active hubs
complete_pills_row = '''      <!-- Neighborhood Quick Filter Pills (All Canonical Lavvi & Novvo Hubs) -->
      <div class="bairro-pills-row" aria-label="Filtrar por bairro">
        <button type="button" class="bairro-pill active" onclick="setBairroPill('todos', this)">Todos os Bairros</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Alto da Boa Vista', this)">Alto da Boa Vista</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Paraíso', this)">Paraíso</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Moema', this)">Moema</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Chácara Klabin', this)">Chácara Klabin</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Brás', this)">Brás / Wonder</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Brooklin', this)">Brooklin</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Perdizes', this)">Perdizes</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Vila Prudente', this)">Vila Prudente</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Água Branca', this)">Água Branca</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Barra Funda', this)">Barra Funda</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Anália Franco', this)">Anália Franco</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Jardim Marajoara', this)">Jardim Marajoara</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Santo Amaro', this)">Santo Amaro</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Butantã', this)">Butantã</button>
      </div>'''

pills_pattern = re.compile(r'<!-- Neighborhood Quick Filter Pills.*?</div>\s*<!-- 1:1 Square Cards', re.DOTALL)
if pills_pattern.search(text):
    text = pills_pattern.sub(complete_pills_row + '\n\n      <!-- 1:1 Square Cards', text, count=1)
    print('Bairro pills row updated!')
else:
    print('Could not find pills_pattern')

# 4. Bottom right Concierge Widget:
# User said: "top right. just say peter ai" (referring to the widget launcher button in bottom right)
# Let's simplify the widget launcher text to just say "Peter AI":
new_concierge_launcher = '''      <div style="text-align:left;">
        <div style="font-size:0.85rem;font-weight:700;line-height:1.2;display:flex;align-items:center;gap:5px;">
          <span>Peter AI</span>
          <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#22C55E;"></span>
        </div>
      </div>'''

old_launcher_text = re.search(r'<div style="text-align:left;">\s*<div style="font-size:0\.82rem.*?</div>\s*<div style="font-size:0\.68rem.*?</div>\s*</div>', text, re.DOTALL)
if old_launcher_text:
    text = text[:old_launcher_text.start()] + new_concierge_launcher + text[old_launcher_text.end():]
    print('Concierge launcher text simplified to just Peter AI!')
else:
    print('Could not find old_launcher_text')

with open('site/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated site/index.html successfully!')
