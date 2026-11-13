import re

with open('site/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add toggleMoreOptionsMenu
toggle_fn = '''
    function toggleMoreOptionsMenu() {
      const menu = document.getElementById('moreOptionsMenu');
      const btn = document.getElementById('moreOptionsBtn');
      if (!menu) return;
      const isOpen = menu.classList.toggle('open');
      if (btn) btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    }

    document.addEventListener('click', function(e) {
      const wrap = document.querySelector('.more-options-wrap');
      const menu = document.getElementById('moreOptionsMenu');
      const btn = document.getElementById('moreOptionsBtn');
      if (wrap && menu && !wrap.contains(e.target)) {
        menu.classList.remove('open');
        if (btn) btn.setAttribute('aria-expanded', 'false');
      }
    });
'''

if 'function toggleMobileDrawer' in text and 'function toggleMoreOptionsMenu' not in text:
    text = text.replace('function toggleMobileDrawer', toggle_fn + '\n    function toggleMobileDrawer')

# 2. Update slides
new_slides_html = '''      <!-- Carousel Slides Container (9 Iconic Projects) -->
      <div class="carousel-track-wrapper" id="carouselTrackWrapper">
        <!-- Slide 0: Well Perdizes -->
        <div class="carousel-slide-item active" data-index="0" data-project="Well Perdizes" data-eyebrow="LANÇAMENTO • PERDIZES / PUC-SP &amp; ALLIANZ" data-title="Well Perdizes • Bem-Estar e Sofisticação na Zona Oeste" data-lead="Plantas inteligentes e lazer contemporâneo em Perdizes nobre. Alta liquidez e conveniência perto de hospitais, faculdades e parques.">
          <img src="assets/images/well_perdizes_gal_2.jpg" alt="Well Perdizes — Perdizes, São Paulo" fetchpriority="high" />
        </div>
        <!-- Slide 1: Jardim da Hípica -->
        <div class="carousel-slide-item" data-index="1" data-project="Jardim da Hípica" data-eyebrow="LANÇAMENTO MONUMENTAL • ALTO DA BOA VISTA" data-title="Jardim da Hípica • O Resort Mais Exclusivo de SP" data-lead="Terreno monumental de 39.553 m² em frente ao CHSA, 02 Quadras de Tênis Oficiais (18x36m), Raia de 60m e gestão CBRE + Body Care.">
          <img src="assets/images/jardim_hipica_facade_4k.jpg" alt="Jardim da Hípica — Rua Antônio Bandeira, 305, Alto da Boa Vista" loading="lazy" />
        </div>
        <!-- Slide 2: T.O.M. Paraíso -->
        <div class="carousel-slide-item" data-index="2" data-project="T.O.M. Paraíso" data-eyebrow="ARQUITETURA DE AUTOR • PARAÍSO / IBIRAPUERA" data-title="T.O.M. Paraíso • Design Assinado a Passos do Parque" data-lead="Apartamentos e Studios R2V com Airbnb liberado na minuta de cartório. Lazer nas alturas e vista panorâmica para o Parque Ibirapuera.">
          <img src="assets/images/tom_gallery_1.jpg" alt="T.O.M. Paraíso — Rua Tomé de Souza, Paraíso" loading="lazy" />
        </div>
        <!-- Slide 3: Alive Club Resort -->
        <div class="carousel-slide-item" data-index="3" data-project="Alive Club Resort" data-eyebrow="RESORT URBANO • CHÁCARA KLABIN" data-title="Alive Club Resort • Oásis Privativo na Chácara Klabin" data-lead="Complexo de lazer resort completo em localização nobre com conectividade privilegiada e plantas generosas para toda a família.">
          <img src="assets/images/alive_gallery_1.jpg" alt="Alive Club Resort — Chácara Klabin, São Paulo" loading="lazy" />
        </div>
        <!-- Slide 4: Green View Residence -->
        <div class="carousel-slide-item" data-index="4" data-project="Green View Residence" data-eyebrow="VISTA VERDE DEFINITIVA • BROOKLIN" data-title="Green View • Sofisticação e Natureza Integrada no Brooklin" data-lead="Arquitetura elegante integrada à paisagem arborizada do Brooklin, unindo tranquilidade residencial e proximidade aos principais polos executivos.">
          <img src="assets/images/greenview_gallery_1.jpg" alt="Green View Residence — Brooklin, São Paulo" loading="lazy" />
        </div>
        <!-- Slide 5: Grand Square -->
        <div class="carousel-slide-item" data-index="5" data-project="Grand Square" data-eyebrow="ALTO PADRÃO • CHÁCARA KLABIN / VILA MARIANA" data-title="Grand Square • Amplitude e Exclusividade em Cada Detalhe" data-lead="Residências de altíssimo padrão com acabamentos refinados, lazer contemporâneo e localização estratégica no eixo sul.">
          <img src="assets/images/grandsquare_gallery_1.jpg" alt="Grand Square — Chácara Klabin, São Paulo" loading="lazy" />
        </div>
        <!-- Slide 6: Saffire by Elie Saab -->
        <div class="carousel-slide-item" data-index="6" data-project="Saffire by Elie Saab" data-eyebrow="HAUTE COUTURE • MOEMA NOBRE" data-title="Saffire by Elie Saab • Primeira Residência do Designer no Brasil" data-lead="O ápice do luxo internacional em Moema nobre com design exclusivo assinado pela Maison Elie Saab e lazer monumental.">
          <img src="assets/images/saffire_elie_saab_facade_4k.jpg" alt="Saffire by Elie Saab — Moema Nobre, São Paulo" loading="lazy" />
        </div>
        <!-- Slide 7: Heaven by YOO -->
        <div class="carousel-slide-item" data-index="7" data-project="Heaven by YOO" data-eyebrow="DESIGN INTERNACIONAL • VILA MARIANA" data-title="Heaven by YOO • Design Global Philippe Starck &amp; John Hitchcox" data-lead="Conceito cosmopolita com interiores assinados pelo renomado estúdio internacional YOO, lazer nas alturas e sofisticação pura.">
          <img src="assets/images/heaven_gallery_1.jpg" alt="Heaven by YOO — Vila Mariana, São Paulo" loading="lazy" />
        </div>
        <!-- Slide 8: High Wonder -->
        <div class="carousel-slide-item" data-index="8" data-project="High Wonder" data-eyebrow="COMPLEXO WONDER • PRAÇA PRIVATIVA" data-title="High Wonder • A Evolução do Bem Viver em Grande Estilo" data-lead="Parte do complexo monumental com praça privativa, infraestrutura esportiva completa e valorização acelerada.">
          <img src="assets/images/high_wonder_praca.webp" alt="High Wonder — São Paulo" loading="lazy" />
        </div>
      </div>'''

track_pattern = re.compile(r'<!-- Carousel Slides Container.*?</div>\s*</div>', re.DOTALL)
if track_pattern.search(text):
    text = track_pattern.sub(new_slides_html, text, count=1)
    print('Track wrapper replaced successfully!')
else:
    print('Could not find track_pattern')

# 3. Update dots
new_dots_html = '''      <!-- Clean Progress Dots on Bottom (9 Slides) -->
      <div class="carousel-progress-dots" id="carouselDotsWrap">
        <button type="button" class="carousel-dot-btn active" onclick="goToHeroSlide(0)" aria-label="Slide 1 Well Perdizes"></button>
        <button type="button" class="carousel-dot-btn" onclick="goToHeroSlide(1)" aria-label="Slide 2 Jardim da Hípica"></button>
        <button type="button" class="carousel-dot-btn" onclick="goToHeroSlide(2)" aria-label="Slide 3 T.O.M. Paraíso"></button>
        <button type="button" class="carousel-dot-btn" onclick="goToHeroSlide(3)" aria-label="Slide 4 Alive Club Resort"></button>
        <button type="button" class="carousel-dot-btn" onclick="goToHeroSlide(4)" aria-label="Slide 5 Green View"></button>
        <button type="button" class="carousel-dot-btn" onclick="goToHeroSlide(5)" aria-label="Slide 6 Grand Square"></button>
        <button type="button" class="carousel-dot-btn" onclick="goToHeroSlide(6)" aria-label="Slide 7 Saffire by Elie Saab"></button>
        <button type="button" class="carousel-dot-btn" onclick="goToHeroSlide(7)" aria-label="Slide 8 Heaven by YOO"></button>
        <button type="button" class="carousel-dot-btn" onclick="goToHeroSlide(8)" aria-label="Slide 9 High Wonder"></button>
      </div>'''

dots_pattern = re.compile(r'<!-- Clean 3 Progress Dots.*?</div>', re.DOTALL)
if dots_pattern.search(text):
    text = dots_pattern.sub(new_dots_html, text, count=1)
    print('Dots replaced successfully!')
else:
    print('Could not find dots_pattern')

# 4. Update JS heroSlides
new_hero_slides_js = '''    const heroSlides = [
      {
        project: "Well Perdizes",
        eyebrow: "LANÇAMENTO • PERDIZES / PUC-SP & ALLIANZ",
        title: "Well Perdizes • Bem-Estar e Sofisticação na Zona Oeste",
        lead: "Plantas inteligentes e lazer contemporâneo em Perdizes nobre. Alta liquidez e conveniência perto de hospitais, faculdades e parques."
      },
      {
        project: "Jardim da Hípica",
        eyebrow: "LANÇAMENTO MONUMENTAL • ALTO DA BOA VISTA",
        title: "Jardim da Hípica • O Resort Mais Exclusivo de SP",
        lead: "Terreno monumental de 39.553 m² em frente ao CHSA, 02 Quadras de Tênis Oficiais (18x36m), Raia de 60m e gestão CBRE + Body Care inclusa no condomínio."
      },
      {
        project: "T.O.M. Paraíso",
        eyebrow: "ARQUITETURA DE AUTOR • PARAÍSO / IBIRAPUERA",
        title: "T.O.M. Paraíso • Design Assinado a Passos do Parque",
        lead: "Apartamentos e Studios R2V com Airbnb liberado na minuta de cartório. Lazer nas alturas e vista panorâmica para o Parque Ibirapuera."
      },
      {
        project: "Alive Club Resort",
        eyebrow: "RESORT URBANO • CHÁCARA KLABIN",
        title: "Alive Club Resort • Oásis Privativo na Chácara Klabin",
        lead: "Complexo de lazer resort completo em localização nobre com conectividade privilegiada e plantas generosas para toda a família."
      },
      {
        project: "Green View Residence",
        eyebrow: "VISTA VERDE DEFINITIVA • BROOKLIN",
        title: "Green View • Sofisticação e Natureza Integrada no Brooklin",
        lead: "Arquitetura elegante integrada à paisagem arborizada do Brooklin, unindo tranquilidade residencial e proximidade aos principais polos executivos."
      },
      {
        project: "Grand Square",
        eyebrow: "ALTO PADRÃO • CHÁCARA KLABIN / VILA MARIANA",
        title: "Grand Square • Amplitude e Exclusividade em Cada Detalhe",
        lead: "Residências de altíssimo padrão com acabamentos refinados, lazer contemporâneo e localização estratégica no eixo sul."
      },
      {
        project: "Saffire by Elie Saab",
        eyebrow: "HAUTE COUTURE • MOEMA NOBRE",
        title: "Saffire by Elie Saab • Primeira Residência do Designer no Brasil",
        lead: "O ápice do luxo internacional em Moema nobre com design exclusivo assinado pela Maison Elie Saab e lazer monumental."
      },
      {
        project: "Heaven by YOO",
        eyebrow: "DESIGN INTERNACIONAL • VILA MARIANA",
        title: "Heaven by YOO • Design Global Philippe Starck & John Hitchcox",
        lead: "Conceito cosmopolita com interiores assinados pelo renomado estúdio internacional YOO, lazer nas alturas e sofisticação pura."
      },
      {
        project: "High Wonder",
        eyebrow: "COMPLEXO WONDER • PRAÇA PRIVATIVA",
        title: "High Wonder • A Evolução do Bem Viver em Grande Estilo",
        lead: "Parte do complexo monumental com praça privativa, infraestrutura esportiva completa e valorização acelerada."
      }
    ];'''

js_pattern = re.compile(r'const heroSlides = \[.*?\];', re.DOTALL)
if js_pattern.search(text):
    text = js_pattern.sub(new_hero_slides_js, text, count=1)
    print('heroSlides JS array replaced successfully!')
else:
    print('Could not find heroSlides js pattern')

with open('site/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated site/index.html successfully!')
