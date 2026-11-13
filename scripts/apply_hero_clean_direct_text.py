import re

with open('site/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Substitute carousel pictures for Well, Hípica and T.O.M.
# Slide 0: Well Perdizes -> assets/images/well_perdizes_gal_3.jpg
text = text.replace('assets/images/well_perdizes_gal_2.jpg', 'assets/images/well_perdizes_gal_3.jpg')

# Slide 1: Jardim da Hípica -> assets/hipica_piscina60m.jpg (or assets/hipica_tenis.jpg)
text = text.replace('assets/images/jardim_hipica_facade_4k.jpg', 'assets/hipica_piscina60m.jpg')

# Slide 2: T.O.M. Paraíso -> assets/tom_rooftop_pool.jpg
text = text.replace('assets/images/tom_gallery_1.jpg', 'assets/tom_rooftop_pool.jpg')

# 2. Fix the top white gap: Remove padding-top: 66px from body so the 100vh hero image starts at the very top of the screen (underneath transparent fixed header)
text = text.replace('body {\n      padding-top: 66px;', 'body {\n      padding-top: 0;')
text = text.replace('body {\n  padding-top: 66px;', 'body {\n  padding-top: 0;')

# 3. In the header brand logo: change "Peter AI" to just "Peter AI" without the divider, or keep it ultra clean as requested:
# User said: "just say peter ai"
# In .brand-logo-link:
# <span class="brand-wordmark">LAVVI</span>
# <span class="brand-divider"></span>
# <span class="brand-advisor">Peter AI</span>
# Replace with:
# <span class="brand-wordmark" style="letter-spacing:0.12em;">LAVVI</span>
# <span class="brand-divider"></span>
# <span class="brand-advisor" style="color:#F3DC8A;">Peter AI</span>
# Also ensure no "Private Wealth" or extra words appear next to Peter AI in the brand logo.

# 4. WhatsApp button text:
# User said: "instead of sayinf falar com pedro say whatsapp peter"
text = re.sub(
    r'(<a[^>]*id="nav-wa-btn"[^>]*>)\s*Falar com Pedro\s*(</a>)',
    r'\1\n          WhatsApp Peter\n        \2',
    text
)
# Also check if Falar com Pedro exists anywhere else in drawer or header
text = text.replace('Falar com Pedro', 'WhatsApp Peter')

# 5. Get rid of the middle information box and just use the letters on top of the picture:
# User said: "all the information box in the middle, get rid of it and just use the letters on top of the picture"
# We remove background, border, backdrop-filter, box-shadow from .glass-card-center so it becomes a transparent container with text directly on the picture with luxury text-shadows.

# Replace .glass-card-center styling in CSS:
old_glass_card_css = re.search(r'\.glass-card-center\s*\{[^}]*\}', text)
if old_glass_card_css:
    new_glass_card_css = '''.glass-card-center {
      background: transparent;
      backdrop-filter: none;
      -webkit-backdrop-filter: none;
      border: none;
      border-radius: 0;
      padding: 0;
      box-shadow: none;
      width: 100%;
      max-width: 900px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }'''
    text = text[:old_glass_card_css.start()] + new_glass_card_css + text[old_glass_card_css.end():]

# Enhance typography shadows for direct placement on top of image
old_display_title_css = re.search(r'\.display-title\s*\{[^}]*\}', text)
if old_display_title_css:
    new_display_title_css = '''.display-title {
      font-family: 'Archivo', sans-serif;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: #FFFFFF;
      text-shadow: 0 4px 24px rgba(0, 0, 0, 0.85), 0 1px 4px rgba(0, 0, 0, 0.95);
      line-height: 1.15;
    }'''
    text = text[:old_display_title_css.start()] + new_display_title_css + text[old_display_title_css.end():]

old_subtitle_lead_css = re.search(r'\.subtitle-lead\s*\{[^}]*\}', text)
if old_subtitle_lead_css:
    new_subtitle_lead_css = '''.subtitle-lead {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-weight: 500;
      letter-spacing: 0.01em;
      color: #F8FAFC;
      text-shadow: 0 2px 14px rgba(0, 0, 0, 0.9), 0 1px 3px rgba(0, 0, 0, 0.9);
      line-height: 1.6;
    }'''
    text = text[:old_subtitle_lead_css.start()] + new_subtitle_lead_css + text[old_subtitle_lead_css.end():]

# Also ensure .banner-inner has padding-top to account for the transparent 66px header:
text = text.replace('.banner-inner {\n      position: relative;', '.banner-inner {\n      position: relative;\n      padding-top: 72px;')

with open('site/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated site/index.html successfully!')
