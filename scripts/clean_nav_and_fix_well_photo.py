with open('site/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove "Peter AI" next to Simulador from nav-links-desktop:
old_peter_ai_li = '''        <li><a href="javascript:void(0)" onclick="toggleChatWidget()" style="color:#F3DC8A; display:flex; align-items:center; gap:6px;">
          <span style="display:inline-block; width:7px; height:7px; border-radius:50%; background:#22C55E; box-shadow:0 0 6px #22C55E;"></span>
          Peter AI
        </a></li>'''

if old_peter_ai_li in text:
    text = text.replace(old_peter_ai_li, '')
    print('Removed Peter AI from nav-links-desktop!')
else:
    print('old_peter_ai_li not found')

# 2. Add .nav-actions CSS so top right is properly spaced and never cramped:
nav_actions_css = '''    .nav-actions {
      display: flex;
      align-items: center;
      gap: 14px;
      flex-shrink: 0;
    }'''

if '.nav-actions {' not in text:
    text = text.replace('.nav-links-desktop {', nav_actions_css + '\n    .nav-links-desktop {')
    print('Added .nav-actions CSS!')

# 3. Ensure more-options-menu is styled to open on the left under the 3-dots button:
if 'left: 0;' not in text or 'right: auto;' not in text:
    text = text.replace(
        '.more-options-menu {\n      display: none;\n      position: absolute;\n      top: calc(100% + 8px);\n      right: 0;',
        '.more-options-menu {\n      display: none;\n      position: absolute;\n      top: calc(100% + 8px);\n      left: 0;\n      right: auto;'
    )

# 4. Check slide 0 for Well Perdizes:
# If well_perdizes_gal_3.jpg is present, switch to well_perdizes_gal_2.jpg (gorgeous high-res facade render)
if 'well_perdizes_gal_3.jpg' in text:
    text = text.replace('assets/images/well_perdizes_gal_3.jpg', 'assets/images/well_perdizes_gal_2.jpg')
    print('Switched Well Perdizes slide image to well_perdizes_gal_2.jpg')

with open('site/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated site/index.html successfully!')
