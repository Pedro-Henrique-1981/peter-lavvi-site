with open('site/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_block = '''<span class="lead-badge-pill" id="activeProjectPill">Jardim da Hípica</span>
          <span class="eyebrow-tag" id="banner-eyebrow-text" style="background:transparent;border:none;padding:0;margin-bottom:6px;font-size:0.75rem;letter-spacing:0.12em;text-transform:uppercase;color:#F3DC8A;">LANÇAMENTO MONUMENTAL • ALTO DA BOA VISTA</span>
          <h1 class="display-title" id="banner-title-text" style="font-size:clamp(1.85rem, 3.2vw, 2.75rem);">Jardim da Hípica • O Resort Mais Exclusivo de SP</h1>
          <p class="subtitle-lead" id="banner-lead-text">
            Terreno monumental de 39.553 m² em frente ao CHSA, 02 Quadras de Tênis Oficiais (18x36m), Raia de 60m e gestão CBRE + Body Care inclusa no condomínio.
          </p>'''

new_block = '''<span class="lead-badge-pill" id="activeProjectPill">Well Perdizes</span>
          <span class="eyebrow-tag" id="banner-eyebrow-text" style="background:transparent;border:none;padding:0;margin-bottom:6px;font-size:0.75rem;letter-spacing:0.12em;text-transform:uppercase;color:#F3DC8A;">LANÇAMENTO • PERDIZES / PUC-SP &amp; ALLIANZ</span>
          <h1 class="display-title" id="banner-title-text" style="font-size:clamp(1.85rem, 3.2vw, 2.75rem);">Well Perdizes • Bem-Estar e Sofisticação na Zona Oeste</h1>
          <p class="subtitle-lead" id="banner-lead-text">
            Plantas inteligentes e lazer contemporâneo em Perdizes nobre. Alta liquidez e conveniência perto de hospitais, faculdades e parques.
          </p>'''

if old_block in text:
    text = text.replace(old_block, new_block)
    with open('site/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Synchronized banner text successfully!')
else:
    print('old_block not found')
