with open('site/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Top left brand text:
# Replace "Peter AI" in brand-advisor with "Peter Corretor direto da Lavvi grupo Cyrela"
text = text.replace(
    '<span class="brand-advisor">Peter AI</span>',
    '<span class="brand-advisor" style="text-transform:none;letter-spacing:0.02em;">Peter Corretor direto da Lavvi grupo Cyrela</span>'
)

# 2. Top left 3-dots button:
# Move the 3 dots button from nav-actions to the left side of brand-logo-link
old_3dots_html = '''        <!-- 3 Dots More Options Menu -->
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
        </div>'''

# Remove from original position
text = text.replace(old_3dots_html, '')

# Place 3 dots on the left of the header brand logo
left_3dots_html = '''        <!-- 3 Dots More Options Menu on Top Left -->
        <div class="more-options-wrap" style="margin-right:8px;">
          <button type="button" class="btn-more-dots" id="moreOptionsBtn" onclick="toggleMoreOptionsMenu()" aria-label="Mais opções e ferramentas" aria-expanded="false">
            &#8942;
          </button>
          <div class="more-options-menu" id="moreOptionsMenu" style="left:0;right:auto;">
            <a href="radar_mapa.html">🗺️ Mapa 46 Projetos &amp; 3km</a>
            <a href="cinema_lavvi.html">🎬 Cinema Lavvi 4K</a>
            <a href="guias_bairros.html">📍 Guias de Bairros &amp; NBR</a>
            <a href="credito_imobiliario.html">📈 Simulador 35/65 vs CDI</a>
            <a href="comparativos.html">⚖️ Comparativos Técnicos</a>
            <a href="dossiers/index.html">📑 Private Banking Dossiers</a>
            <a href="crm_cockpit.html" style="color:#F3DC8A;">🔒 Cockpit do Corretor</a>
          </div>
        </div>'''

text = text.replace(
    '<nav class="nav-container" aria-label="Navegação Principal">\n      <a href="#topo" class="brand-logo-link">',
    '<nav class="nav-container" aria-label="Navegação Principal">\n      <div style="display:flex;align-items:center;gap:10px;">\n' + left_3dots_html + '\n      <a href="#topo" class="brand-logo-link">'
)
# Close that div before ul
text = text.replace(
    '</a>\n\n            <ul class="nav-links-desktop">',
    '</a>\n      </div>\n\n      <ul class="nav-links-desktop">'
)

# 3. WhatsApp button green with SVG logo:
old_wa_btn = '''<a href="https://wa.me/5511966105952?text=Ol%C3%A1%20Pedro%2C%20estou%20no%20seu%20portal%20Lavvi%20e%20gostaria%20de%20atendimento%20direto." target="_blank" rel="noopener" class="btn-header-wa" id="nav-wa-btn">
          WhatsApp Peter
        </a>'''

new_wa_btn = '''<a href="https://wa.me/5511966105952?text=Ol%C3%A1%20Peter%2C%20estou%20no%20portal%20Lavvi%20e%20gostaria%20de%20atendimento%20direto." target="_blank" rel="noopener" class="btn-header-wa" id="nav-wa-btn" style="background:#25D366;border-color:rgba(255,255,255,0.3);box-shadow:0 4px 14px rgba(37,211,102,0.35);">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="#FFFFFF" style="flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
            <path d="M12.031 0C5.393 0 0 5.393 0 12.031c0 2.12.553 4.184 1.605 6.007L.062 24l6.143-1.611A11.96 11.96 0 0012.031 24c6.638 0 12.031-5.393 12.031-12.031C24.062 5.393 18.669 0 12.031 0zm0 22.016c-1.848 0-3.644-.497-5.215-1.442l-.374-.225-3.87 1.015 1.033-3.771-.247-.393a9.987 9.987 0 01-1.531-5.169c0-5.526 4.496-10.022 10.022-10.022 5.526 0 10.022 4.496 10.022 10.022 0 5.526-4.496 10.022-10.022 10.022zm5.495-7.51c-.301-.151-1.782-.88-2.058-.981-.277-.1-.478-.151-.679.151-.2.301-.778.981-.954 1.182-.176.2-.352.226-.653.075s-1.27-.468-2.42-1.494c-.895-.798-1.499-1.784-1.675-2.086-.176-.301-.019-.464.132-.614.136-.135.301-.352.452-.528.151-.176.201-.301.301-.502.1-.2.05-.377-.025-.528-.075-.151-.679-1.635-.93-2.239-.244-.588-.493-.508-.679-.517l-.578-.01c-.2 0-.527.075-.803.377s-1.055 1.031-1.055 2.514c0 1.483 1.08 2.917 1.231 3.118.151.201 2.125 3.245 5.148 4.552.719.311 1.28.497 1.718.636.722.23 1.379.197 1.898.12.579-.086 1.782-.728 2.033-1.432.251-.703.251-1.306.176-1.432-.075-.126-.276-.201-.577-.352z"/>
          </svg>
          WhatsApp Peter
        </a>'''

text = text.replace(old_wa_btn, new_wa_btn)

# 4. Make language selector compact and discreet:
old_lang_selector = '''        <div class="lang-pill-group" id="lang-selector" role="group" aria-label="Idioma">
          <button type="button" class="lang-btn active" onclick="setLanguage('pt')">PT</button>
          <button type="button" class="lang-btn" onclick="setLanguage('en')">EN</button>
          <button type="button" class="lang-btn" onclick="setLanguage('fr')">FR</button>
          <button type="button" class="lang-btn" onclick="setLanguage('it')">IT</button>
          <button type="button" class="lang-btn" onclick="setLanguage('es')">ES</button>
          <button type="button" class="lang-btn" onclick="setLanguage('de')">DE</button>
        </div>'''

new_lang_selector = '''        <div class="lang-pill-group" id="lang-selector" role="group" aria-label="Idioma" style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);border-radius:20px;padding:2px 4px;">
          <button type="button" class="lang-btn active" onclick="setLanguage('pt')" style="font-size:0.65rem;padding:2px 5px;border-radius:10px;">PT</button>
          <button type="button" class="lang-btn" onclick="setLanguage('en')" style="font-size:0.65rem;padding:2px 5px;border-radius:10px;">EN</button>
          <button type="button" class="lang-btn" onclick="setLanguage('fr')" style="font-size:0.65rem;padding:2px 5px;border-radius:10px;">FR</button>
          <button type="button" class="lang-btn" onclick="setLanguage('it')" style="font-size:0.65rem;padding:2px 5px;border-radius:10px;">IT</button>
          <button type="button" class="lang-btn" onclick="setLanguage('es')" style="font-size:0.65rem;padding:2px 5px;border-radius:10px;">ES</button>
          <button type="button" class="lang-btn" onclick="setLanguage('de')" style="font-size:0.65rem;padding:2px 5px;border-radius:10px;">DE</button>
        </div>'''

text = text.replace(old_lang_selector, new_lang_selector)

# 5. Make the "Escolha o Bairro" trigger more discreet (smaller width, compact padding, darker glass background):
text = text.replace(
    '.bairro-selector-wrapper {\n      position: relative;\n      width: 100%;\n      max-width: 620px;\n      margin: 0 auto;\n    }',
    '.bairro-selector-wrapper {\n      position: relative;\n      width: 100%;\n      max-width: 420px;\n      margin: 0 auto;\n    }'
)
text = text.replace(
    'padding: 12px 24px;\n      border-radius: 36px;\n      font-family: \'Archivo\', sans-serif;\n      font-size: 0.92rem;',
    'padding: 8px 18px;\n      border-radius: 24px;\n      font-family: \'Archivo\', sans-serif;\n      font-size: 0.8rem;'
)

# 6. Complete list of bairros in Popover menu (including Brás, Vila Prudente, Anália Franco, Barra Funda, etc.):
old_popover_content = '''            <!-- Popover Menu with SP Bairros -->
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
            </div>'''

new_popover_content = '''            <!-- Popover Menu with SP Bairros (Complete Lavvi & Novvo Portfolio) -->
            <div class="bairro-popover-menu" id="bairroPopoverMenu" role="listbox" aria-label="Opções de Bairros de São Paulo">
              <button type="button" class="bairro-popover-item active" onclick="selectBairroOption('todos', 'Todos os Bairros')" role="option">🏙️ Todos os Bairros (46)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Alto da Boa Vista', 'Alto da Boa Vista')" role="option">🐎 Alto da Boa Vista (2)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Moema', 'Moema Nobre')" role="option">✈️ Moema Nobre (8)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Paraíso', 'Paraíso / Ibirapuera')" role="option">🌳 Paraíso / Ibirapuera (5)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Chácara Klabin', 'Chácara Klabin')" role="option">🏛️ Chácara Klabin (5)</button>
              <button type="button" class="bairro-popover-item" onclick="selectBairroOption('Brás', 'Brás / Wonder')" role="option">🏢 Brás / Wonder (4)</button>
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

text = text.replace(old_popover_content, new_popover_content)

# 7. Complete list of Bairro Pills row in Catalog section (#catalogo):
old_bairro_pills = '''      <!-- Neighborhood Quick Filter Pills -->
      <div class="bairro-pills-row" aria-label="Filtrar por bairro">
        <button type="button" class="bairro-pill active" onclick="setBairroPill('todos', this)">Todos os Bairros</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Alto da Boa Vista', this)">Alto da Boa Vista</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Paraíso', this)">Paraíso</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Moema', this)">Moema</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Chácara Klabin', this)">Chácara Klabin</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Brooklin', this)">Brooklin</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Perdizes', this)">Perdizes</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Água Branca', this)">Água Branca / Santa Marina</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Santo Amaro', this)">Santo Amaro / Largo Treze</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Vila Prudente', this)">Vila Prudente</button>
        <button type="button" class="bairro-pill" onclick="setBairroPill('Butantã', this)">Butantã</button>
      </div>'''

new_bairro_pills = '''      <!-- Neighborhood Quick Filter Pills (All Canonical Lavvi & Novvo Hubs) -->
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

text = text.replace(old_bairro_pills, new_bairro_pills)

# 8. Concierge launcher widget: simplify text to just "Peter AI"
old_concierge_launcher = '''      <div style="text-align:left;">
        <div style="font-size:0.82rem;font-weight:700;line-height:1.2;display:flex;align-items:center;gap:4px;">
          <span>Peter AI</span>
          <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#22C55E;"></span>
        </div>
        <div style="font-size:0.68rem;color:#F3DC8A;">Consultor Lavvi • 6 Idiomas</div>
      </div>'''

new_concierge_launcher = '''      <div style="text-align:left;">
        <div style="font-size:0.85rem;font-weight:700;line-height:1.2;display:flex;align-items:center;gap:5px;">
          <span>Peter AI</span>
          <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#22C55E;"></span>
        </div>
      </div>'''

text = text.replace(old_concierge_launcher, new_concierge_launcher)

with open('site/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Surgical edits applied successfully!')
