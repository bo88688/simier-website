import os

base = '/Users/nibaba/furniture-website'
assets = f'{base}/assets'
pages_dir = f'{base}/pages/gallery'
os.makedirs(pages_dir, exist_ok=True)

def get_images(cat):
    path = f'{assets}/{cat}'
    if not os.path.exists(path): return []
    return sorted([f'../../assets/{cat}/{f}' for f in os.listdir(path)
                   if f.lower().endswith(('.jpg','.jpeg','.png')) and not f.startswith('.')])

HEAD = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Product Gallery | SIMIER</title>
  <meta name="description" content="{desc}">
  <link rel="preload" as="image" href="{hero}" fetchpriority="high">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@300;400;500;600&family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;700&family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=ZCOOL+XiaoWei&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../css/style.css">
  <style>
    .gallery-masonry {{ columns:4; column-gap:1rem; }}
    .gallery-item {{ break-inside:avoid; margin-bottom:1rem; border-radius:4px; overflow:hidden; transition:transform 0.3s var(--ease-out-expo); cursor:pointer; background:var(--color-stone); }}
    .gallery-item:hover {{ transform:scale(1.02); }}
    .gallery-item img {{ width:100%; display:block; }}
    .gallery-cta {{ text-align:center; padding:clamp(3rem,6vw,5rem) 0; background:var(--color-cream); }}
    .gallery-cta__text {{ font-size:1rem; color:#777; max-width:560px; margin:0 auto 1.5rem; line-height:1.8; }}
    @media(max-width:900px){{ .gallery-masonry{{columns:3}} }}
    @media(max-width:600px){{ .gallery-masonry{{columns:2}} }}
    @media(max-width:400px){{ .gallery-masonry{{columns:1}} }}
  </style>
</head>
<body>
  <header class="header header--scrolled" id="header">
    <div class="header__inner">
      <a href="../../index.html" class="header__logo">SIMIER</a>
      <nav class="header__nav" id="mainNav">
        <ul class="header__links">
          <li><a href="../seating.html" class="header__link" data-i18n="nav.products">Products</a></li>
          <li><a href="../about.html" class="header__link" data-i18n="nav.about">About</a></li>
          <li><a href="../sendayi.html" class="header__link" data-i18n="nav.sendayi">森怡大时</a></li>
          <li><a href="../gallery.html" class="header__link header__link--active" data-i18n="nav.gallery">Gallery</a></li>
          <li><a href="../factory.html" class="header__link" data-i18n="nav.factory">Factory</a></li>
          <li><a href="mailto:hello@simier.top" class="header__link" data-i18n="nav.contact" onclick="openChat();">Contact</a></li>
          <li><a href="../cart.html" class="header__link">Cart</a></li>
        </ul>
      </nav>
      <div class="header__actions">
        <button class="header__icon-btn" aria-label="Search"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg></button>
        <button class="header__icon-btn header__icon-btn--cart" aria-label="Cart" onclick="location.href='../cart.html'"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg></button>
        <button class="header__menu-toggle" id="menuToggle" aria-label="Menu"><span></span><span></span></button>
      </div>
    </div>
  </header>
  <main>
    <nav class="sendayi-breadcrumb">
      <a href="../../index.html">SIMIER</a> &rsaquo; <a href="../gallery.html">Gallery</a> &rsaquo; <span>{title}</span>
    </nav>
    <section class="sendayi-page-hero">
      <div class="sendayi-page-hero__bg" style="background-image: url('{hero}')"></div>
      <div class="sendayi-page-hero__overlay"></div>
      <div class="sendayi-page-hero__content">
        <p class="sendayi-page-hero__eyebrow">{hero_eyebrow}</p>
        <h1 class="sendayi-page-hero__title">{hero_title}</h1>
        <p class="sendayi-page-hero__subtitle" style="max-width:600px;margin:0.8rem auto 0;font-size:0.9rem;color:rgba(255,255,255,0.65);line-height:1.8;">{hero_sub}</p>
      </div>
    </section>
    <section class="sendayi-page-section">
      <div class="container">
        <div class="reveal">
          <h2 class="sendayi-page-section__title">{intro_title}</h2>
          <div class="sendayi-page-section__text">
            <p>{intro_p1}</p>
            <p>{intro_p2}</p>
          </div>
        </div>
      </div>
    </section>
    <section class="sendayi-page-section sendayi-page-section--alt">
      <div class="container">
        <div class="gallery-masonry reveal" id="galleryGrid">
'''

FOOT = '''        </div>
      </div>
    </section>
    <section class="gallery-cta">
      <div class="container">
        <p class="gallery-cta__text">{cta_text}</p>
        <a href="{cta_link}" class="btn btn--primary">{cta_label}</a>
      </div>
    </section>
    <div class="sendayi-back">
      <a href="../gallery.html">← Back to Gallery</a>
    </div>
  </main>
  <footer class="footer"><div class="container"><div class="footer__grid">
    <div class="footer__brand"><a href="../../index.html" class="footer__logo">SIMIER</a><p class="footer__tagline" data-i18n="footer.tagline">Made with intention.<br>Crafted in our Guangdong workshop.</p><div class="footer__social"><a href="#">IG</a><a href="#">PI</a><a href="#">RED</a></div></div>
    <div class="footer__col"><h4 class="footer__heading">Products</h4><ul class="footer__links"><li><a href="../seating.html">Sofas & Armchairs</a></li><li><a href="../dining.html">Dining</a></li><li><a href="../bedroom.html">Beds</a></li><li><a href="../storage.html">Storage & Tables</a></li><li><a href="../sendayi.html">森怡大时</a></li><li><a href="../gallery.html">Gallery</a></li></ul></div>
    <div class="footer__col"><h4 class="footer__heading">Company</h4><ul class="footer__links"><li><a href="../about.html">About</a></li><li><a href="../factory.html">Factory Tour</a></li><li><a href="../partners.html">Partners</a></li><li><a href="mailto:hello@simier.top">Contact</a></li></ul></div>
    <div class="footer__col"><h4 class="footer__heading">Support</h4><ul class="footer__links"><li><a href="mailto:hello@simier.top">Shipping & Returns</a></li><li><a href="mailto:hello@simier.top">Care Guide</a></li><li><a href="mailto:hello@simier.top">Trade Program</a></li><li><a href="mailto:hello@simier.top">Custom Orders</a></li></ul></div>
  </div><div class="footer__bottom"><p>&copy; 2026 Guangdong SIMIER Home Furnishing Co., Ltd.</p><p class="footer__location">Foshan, Guangdong, China — Sud de la France — California — Istanbul</p></div></div></footer>
  <div class="chat-widget" id="chatWidget"><button class="chat-widget__bubble" id="chatBubble"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg></button><div class="chat-widget__panel" id="chatPanel"><div class="chat-widget__header"><span>SIMIER Assistant</span><button class="chat-widget__close" id="chatClose">×</button></div><div class="chat-widget__messages" id="chatMessages"><div class="chat-widget__msg chat-widget__msg--bot">Hello! Ask me about our furniture, materials, or custom orders.</div></div><form class="chat-widget__input" id="chatInputForm"><input type="text" id="chatInput" placeholder="Ask me anything..."><button type="submit"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg></button></form></div></div>
  <script src="../../js/main.js"></script><script src="../../js/cart.js"></script><script src="../../js/i18n.js"></script><script src="../../js/chat.js"></script>
</body></html>'''

configs = {
    'seating': dict(
        title='Sofas & Armchairs', title_zh='坐具', desc='SIMIER sofas, chairs & armchairs. Crafted in Guangdong.',
        hero='../../assets/坐具/IMG_7724.JPG',
        hero_eyebrow='The Art of Sitting',
        hero_title='Where Comfort<br>Meets Form',
        hero_sub='From the Provencal afternoon to a California morning — a good sofa is the soul of a first home. Each piece shaped by hands that have spent decades learning what comfort truly means.',
        intro_title='Sofas, Chairs & Armchairs',
        intro_p1='Every seat we make begins with a frame built to outlast its owner. Solid hardwood, reinforced joints, and a quiet obsession with the angle of a backrest — the difference between sitting down and settling in.',
        intro_p2='Our upholstery is sourced from Italian mills and cut in-house. Foam densities are specified per cushion, per chair, per use. Because the way you sit in a dining chair is not the way you sink into a sofa.',
        cta_text='Explore the full seating collection — from compact apartment sofas to generous sectional pieces.',
        cta_link='../seating.html', cta_label='Shop Seating',
        asset_cat='坐具'
    ),
    'dining': dict(
        title='Dining Tables & Chairs', title_zh='餐厅', desc='SIMIER dining tables & chairs. Built for the long meal.',
        hero='../../assets/餐厅/IMG_7723.JPG',
        hero_eyebrow='The Gathering Place',
        hero_title='Tables That Bring<br>People Together',
        hero_sub='A dining table is where mornings begin and evenings unwind. It holds coffee cups and laptop screens, celebration dinners and quiet breakfasts for one.',
        intro_title='Tables, Chairs & Dining Sets',
        intro_p1='Our tables are cut from solid wood slabs — oak, walnut, and ash — each selected for grain character and structural integrity. Legs are joined with traditional mortise-and-tenon.',
        intro_p2='Dining chairs are engineered for the long meal — the one that stretches past dessert into another bottle of wine. Proper lumbar support and finishes that age gracefully.',
        cta_text='Browse our dining collection — tables for two to twelve, chairs for every occasion.',
        cta_link='../dining.html', cta_label='Shop Dining',
        asset_cat='餐厅'
    ),
    'bedroom': dict(
        title='Beds & Bedroom', title_zh='卧室', desc='SIMIER beds, headboards & bedroom furniture.',
        hero='../../assets/卧室/IMG_7718.JPG',
        hero_eyebrow='The Private Sanctuary',
        hero_title='Rest Well.<br>Really Well.',
        hero_sub='A third of your life is spent in bed. We think that deserves furniture built with the same care as the pieces in your living room.',
        intro_title='Beds, Headboards & Nightstands',
        intro_p1='Every bed frame starts with kiln-dried hardwood and a center support system engineered to stay silent. No creaks. No compromises.',
        intro_p2='Our bedroom pieces are designed for the way we actually live: soft morning light falling across a surface that feels warm to the touch.',
        cta_text='Discover beds designed for deep rest — from single frames to full bedroom sets.',
        cta_link='../bedroom.html', cta_label='Shop Bedroom',
        asset_cat='卧室'
    ),
    'storage': dict(
        title='Storage & Tables', title_zh='柜类 & 桌几', desc='SIMIER cabinets, sideboards, coffee tables & storage.',
        hero='../../assets/柜类/IMG_7719.JPG',
        hero_eyebrow='Order & Beauty',
        hero_title='Storage That<br>Doesn\'t Hide',
        hero_sub='The pieces that hold everything else. Sideboards that anchor a room. Coffee tables collecting books and mugs. Cabinets that deserve to be seen.',
        intro_title='Cabinets, Sideboards & Side Tables',
        intro_p1='Storage should never be an afterthought. Our cabinets use the same joinery, the same wood selection, the same finishing process as our statement pieces.',
        intro_p2='From solid wood coffee tables to glass-fronted display cabinets, every piece is built to carry the weight of daily use — and look better with every passing year.',
        cta_text='Explore storage solutions and accent tables — organization made beautiful.',
        cta_link='../storage.html', cta_label='Shop Storage',
        asset_cat='柜类+桌几'
    ),
    'sendayi': dict(
        title='Sen Yi Da Shi', title_zh='森怡大时', desc='森怡大时 Chinese heritage furniture collection.',
        hero='../../assets/森怡大时/sendayi-07.jpg',
        hero_eyebrow='Chinese Heritage Collection',
        hero_title='以顺遂之心<br>致生活时光',
        hero_sub='Anchored in the craft traditions of Song and Ming dynasties. Ruanti weaving, wild rattan, mountain palm — natural materials shaped by hands that remember a thousand years of technique.',
        intro_title='The Complete Sendayi Range',
        intro_p1='Every Sendayi piece is a collaboration between past and present. Traditional mortise-and-tenon joinery meets contemporary proportions. Ancient Ruanti weaving techniques applied to furniture designed for modern homes.',
        intro_p2='Browse the full visual catalog below, then visit the Sendayi section for detailed product pages, materials deep-dives, and the stories behind each collection.',
        cta_text='Visit the complete Sen Yi Da Shi section — 13 pages of products, materials, and brand story.',
        cta_link='../sendayi.html', cta_label='Explore 森怡大时',
        asset_cat='森怡大时'
    ),
}

for key, cfg in configs.items():
    if cfg['asset_cat'] == '柜类+桌几':
        imgs = get_images('柜类') + get_images('桌几')
    else:
        imgs = get_images(cfg['asset_cat'])

    # Build HTML
    head_html = HEAD.format(**cfg)
    img_html = '\n'.join(f'          <div class="gallery-item"><img src="{img}" alt="SIMIER {cfg["title"]}" loading="lazy"></div>' for img in imgs)
    foot_html = FOOT.format(**cfg)

    full_html = head_html + img_html + '\n' + foot_html

    fpath = os.path.join(pages_dir, f'{key}.html')
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f'✓ gallery/{key}.html — {len(imgs)} images, {full_html.count(chr(10))} lines')

print(f'\nDone! 5 sub-pages in {pages_dir}/')
