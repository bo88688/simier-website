import os, random

base = '/Users/nibaba/furniture-website'
assets = f'{base}/assets'
pages_dir = f'{base}/pages/gallery'
os.makedirs(pages_dir, exist_ok=True)

def get_images(cat):
    path = f'{assets}/{cat}'
    if not os.path.exists(path): return []
    return sorted([f'../../assets/{cat}/{f}' for f in os.listdir(path)
                   if f.lower().endswith(('.jpg','.jpeg','.png')) and not f.startswith('.')])

def pick(img_list, n=4):
    """Pick n evenly-spaced images from list"""
    if len(img_list) <= n: return img_list
    step = max(1, len(img_list) // n)
    return [img_list[i] for i in range(0, len(img_list), step)][:n]

# ===== DTC-STYLE HTML TEMPLATES =====

HEAD_OPEN = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — SIMIER</title>
  <meta name="description" content="{desc}">
  <link rel="preload" as="image" href="{hero}" fetchpriority="high">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@300;400;500;600&family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;700&family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=ZCOOL+XiaoWei&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../css/style.css">
  <style>
    /* === DTC Editorial Styles === */
    .dtc-hero {{ position:relative; height:85vh; min-height:520px; display:flex; align-items:center; overflow:hidden; background:#1a1a1a; }}
    .dtc-hero__bg {{ position:absolute; inset:0; background-size:cover; background-position:center; }}
    .dtc-hero__overlay {{ position:absolute; inset:0; background:linear-gradient(180deg,rgba(0,0,0,0.25) 0%,rgba(0,0,0,0.15) 50%,rgba(0,0,0,0.5) 100%); z-index:1; }}
    .dtc-hero__content {{ position:relative; z-index:2; color:#fff; max-width:720px; padding:0 clamp(2rem,5vw,4rem); }}
    .dtc-hero__eyebrow {{ font-family:var(--font-body); font-size:0.6rem; letter-spacing:0.32em; text-transform:uppercase; color:var(--color-brass); margin-bottom:1.5rem; }}
    .dtc-hero__title {{ font-family:var(--font-hero); font-size:clamp(2.6rem,5.5vw,4.8rem); font-weight:400; line-height:1.08; letter-spacing:-0.015em; margin-bottom:1.5rem; }}
    .dtc-hero__sub {{ font-family:var(--font-body); font-size:clamp(0.95rem,1.3vw,1.1rem); font-weight:300; line-height:1.8; color:rgba(255,255,255,0.7); max-width:500px; }}

    .dtc-section {{ padding:clamp(5rem,10vw,8rem) 0; }}
    .dtc-section--warm {{ background:var(--color-cream); }}
    .dtc-section--dark {{ background:#1a1a1a; color:#fff; }}
    .dtc-section__header {{ text-align:center; max-width:640px; margin:0 auto clamp(3rem,5vw,5rem); }}
    .dtc-section__eyebrow {{ font-family:var(--font-body); font-size:0.6rem; letter-spacing:0.28em; text-transform:uppercase; color:var(--color-taupe); margin-bottom:1.25rem; }}
    .dtc-section__title {{ font-family:var(--font-display); font-size:clamp(1.6rem,3vw,2.4rem); font-weight:400; line-height:1.25; color:var(--color-charcoal); margin-bottom:1rem; }}
    .dtc-section--dark .dtc-section__title {{ color:#fff; }}
    .dtc-section__body {{ font-family:var(--font-body); font-size:0.95rem; line-height:2; color:#777; max-width:600px; margin:0 auto; }}
    .dtc-section--dark .dtc-section__body {{ color:rgba(255,255,255,0.55); }}

    /* Featured Picks Grid */
    .dtc-featured {{ display:grid; grid-template-columns:repeat(4,1fr); gap:1.5rem; }}
    .dtc-featured__card {{ transition:transform 0.35s var(--ease-out-expo); }}
    .dtc-featured__card:hover {{ transform:translateY(-6px); }}
    .dtc-featured__img {{ width:100%; aspect-ratio:3/4; background-size:cover; background-position:center; background-color:var(--color-stone); border-radius:3px; margin-bottom:1rem; }}
    .dtc-featured__name {{ font-family:var(--font-display); font-size:1.05rem; font-weight:500; color:var(--color-charcoal); margin-bottom:0.25rem; }}
    .dtc-featured__desc {{ font-size:0.8rem; color:var(--color-taupe); line-height:1.6; }}

    /* Material Spotlight */
    .dtc-spotlight {{ display:grid; grid-template-columns:1fr 1fr; gap:clamp(3rem,6vw,6rem); align-items:center; }}
    .dtc-spotlight__image {{ width:100%; aspect-ratio:4/5; background-size:cover; background-position:center; border-radius:4px; box-shadow:0 8px 40px rgba(0,0,0,0.06); }}
    .dtc-spotlight__text h3 {{ font-family:var(--font-display); font-size:1.6rem; font-weight:400; color:var(--color-charcoal); margin-bottom:1rem; }}
    .dtc-spotlight__text p {{ font-size:0.93rem; line-height:2; color:#777; margin-bottom:0.75rem; }}

    /* Full Gallery Masonry */
    .dtc-masonry {{ columns:4; column-gap:1rem; }}
    .dtc-masonry__item {{ break-inside:avoid; margin-bottom:1rem; border-radius:3px; overflow:hidden; transition:transform 0.3s var(--ease-out-expo); cursor:pointer; background:var(--color-stone); }}
    .dtc-masonry__item:hover {{ transform:scale(1.02); }}
    .dtc-masonry__item img {{ width:100%; display:block; }}

    /* CTA Banner */
    .dtc-cta {{ text-align:center; padding:clamp(4rem,8vw,6rem) 0; }}
    .dtc-cta__title {{ font-family:var(--font-display); font-size:clamp(1.5rem,2.8vw,2rem); font-weight:400; color:var(--color-charcoal); margin-bottom:1rem; }}
    .dtc-cta__text {{ font-size:0.93rem; color:#999; max-width:480px; margin:0 auto 2rem; line-height:1.8; }}

    /* Breadcrumb */
    .dtc-breadcrumb {{ padding:1.5rem var(--container-padding); font-size:0.72rem; color:var(--color-taupe); max-width:var(--container-max); margin:0 auto; }}
    .dtc-breadcrumb a {{ color:var(--color-taupe); transition:color 0.2s; }}
    .dtc-breadcrumb a:hover {{ color:var(--color-charcoal); }}
    .dtc-breadcrumb span {{ color:var(--color-charcoal); }}

    @media(max-width:900px){{ .dtc-featured{{grid-template-columns:repeat(2,1fr)}} .dtc-spotlight{{grid-template-columns:1fr}} .dtc-spotlight__image{{order:-1;aspect-ratio:3/2}} .dtc-masonry{{columns:3}} }}
    @media(max-width:600px){{ .dtc-featured{{grid-template-columns:repeat(2,1fr);gap:1rem}} .dtc-masonry{{columns:2}} }}
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
          <li><a href="../sendayi.html" class="header__link" data-i18n="nav.sendayi">Sen Yi Da Shi</a></li>
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
    <nav class="dtc-breadcrumb"><a href="../../index.html">SIMIER</a> &rsaquo; <a href="../gallery.html">Gallery</a> &rsaquo; <span>{title}</span></nav>
'''

HERO = '''    <section class="dtc-hero">
      <div class="dtc-hero__bg" style="background-image:url('{hero}')"></div>
      <div class="dtc-hero__overlay"></div>
      <div class="dtc-hero__content">
        <p class="dtc-hero__eyebrow">{hero_eyebrow}</p>
        <h1 class="dtc-hero__title">{hero_title}</h1>
        <p class="dtc-hero__sub">{hero_sub}</p>
      </div>
    </section>
'''

CLOSE = '''
    <section class="dtc-cta">
      <div class="container">
        <h3 class="dtc-cta__title">{cta_title}</h3>
        <p class="dtc-cta__text">{cta_text}</p>
        <a href="{cta_link}" class="btn btn--primary">{cta_label}</a>
      </div>
    </section>
    <div class="sendayi-back"><a href="../gallery.html">&larr; Back to Gallery</a></div>
  </main>
  <footer class="footer"><div class="container"><div class="footer__grid">
    <div class="footer__brand"><a href="../../index.html" class="footer__logo">SIMIER</a><p class="footer__tagline" data-i18n="footer.tagline">Made with intention.<br>Crafted in our Guangdong workshop.</p><div class="footer__social"><a href="#">IG</a><a href="#">PI</a><a href="#">RED</a></div></div>
    <div class="footer__col"><h4 class="footer__heading">Products</h4><ul class="footer__links"><li><a href="../seating.html">Sofas & Armchairs</a></li><li><a href="../dining.html">Dining</a></li><li><a href="../bedroom.html">Beds</a></li><li><a href="../storage.html">Storage & Tables</a></li><li><a href="../sendayi.html">Sen Yi Da Shi</a></li><li><a href="../gallery.html">Gallery</a></li></ul></div>
    <div class="footer__col"><h4 class="footer__heading">Company</h4><ul class="footer__links"><li><a href="../about.html">About</a></li><li><a href="../factory.html">Factory Tour</a></li><li><a href="../partners.html">Partners</a></li><li><a href="mailto:hello@simier.top">Contact</a></li></ul></div>
    <div class="footer__col"><h4 class="footer__heading">Support</h4><ul class="footer__links"><li><a href="mailto:hello@simier.top">Shipping & Returns</a></li><li><a href="mailto:hello@simier.top">Care Guide</a></li><li><a href="mailto:hello@simier.top">Trade Program</a></li><li><a href="mailto:hello@simier.top">Custom Orders</a></li></ul></div>
  </div><div class="footer__bottom"><p>&copy; 2026 Guangdong SIMIER Home Furnishing Co., Ltd.</p><p class="footer__location">Foshan, Guangdong &mdash; South of France &mdash; California &mdash; Istanbul</p></div></div></footer>
  <div class="chat-widget" id="chatWidget"><button class="chat-widget__bubble" id="chatBubble"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg></button><div class="chat-widget__panel" id="chatPanel"><div class="chat-widget__header"><span>SIMIER Assistant</span><button class="chat-widget__close" id="chatClose">&times;</button></div><div class="chat-widget__messages" id="chatMessages"><div class="chat-widget__msg chat-widget__msg--bot">Hi there. Ask me about materials, lead times, or anything about our furniture.</div></div><form class="chat-widget__input" id="chatInputForm"><input type="text" id="chatInput" placeholder="Type your question&hellip;"><button type="submit"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg></button></form></div></div>
  <script src="../../js/main.js"></script><script src="../../js/cart.js"></script><script src="../../js/i18n.js"></script><script src="../../js/chat.js"></script>
</body></html>'''

# ===== PAGE CONFIGS (DTC Editorial Copy) =====
configs = {
    'seating': dict(
        title='The Seating Collection',
        desc='Sofas, armchairs, and sectionals. Designed in Guangdong for modern homes across the world.',
        hero='../../assets/坐具/IMG_7724.JPG',
        hero_eyebrow='The Seating Collection',
        hero_title='A place to land.<br>A reason to stay.',
        hero_sub='The right sofa does not just fill a room. It defines it. It is where mornings are planned and evenings are surrendered, where conversations stretch past midnight and Sunday afternoons disappear without apology. This is furniture that shapes the rhythm of a home — and we believe that deserves more than a foam block on a pine frame.',
        narrative_eyebrow='Why It Matters',
        narrative_title='We believe a sofa should outlast<br>the device you are reading this on.',
        narrative_p1='Most sofas are built to a price point, not a standard. The average lifespan of a mass-market sofa is seven years — less than a refrigerator, less than a washing machine, less than the phone in your pocket. The frame loosens. The cushions collapse. The fabric pills and fades. And then you do it all over again: the showroom visits, the measuring tape, the four-to-six-week wait, the delivery window that arrives sometime between 8 a.m. and never. We think this cycle is absurd. A sofa is the largest piece of furniture most people will ever buy. It should be the last one they buy for a very long time.',
        narrative_p2='Every SIMIER seat begins with a kiln-dried hardwood frame assembled with reinforced corner blocks and double-doweled joints — construction techniques borrowed from fine cabinetmaking, not mass-production upholstery lines. Our suspension systems use eight-way hand-tied coils or sinuous springs, chosen per design rather than per cost spreadsheet. Foam densities are specified cushion by cushion, because the way you sit in an armchair with a book is not the way you sink into a three-seater after a fourteen-hour day. These distinctions matter. You feel them in your lower back after hour two. You feel them when you stand up and realize you were not thinking about the sofa at all — you were just comfortable, which is the highest compliment furniture can receive.',
        narrative_p3='Then there is the upholstery. We source from Italian mills that have been weaving for generations — family-owned operations where the difference between a twill and a plain weave is not academic but visceral. Performance weaves for households with children and pets, engineered to release stains with nothing more than water and a cloth. Velvets with a pile depth that shifts color as light moves across the room. Linens that soften with every sit, developing a lived-in character that cannot be faked by any factory distressing process. Every fabric is tested for 40,000 to 100,000 double rubs — which, in plain English, means it will still look intentional when your children are old enough to borrow the car. We also believe in transparency: the foam inside every cushion is CertiPUR-US certified, meaning no heavy metals, no formaldehyde, no ozone depleters. The wood in every frame is FSC-sourced. These are not marketing claims. They are the terms of engagement for every piece that leaves our Guangdong workshop.',
        featured_eyebrow='Featured Picks',
        featured_title='Four places to start.',
        mat_title='A closer look at the materials.',
        mat_p1='Italian-milled performance linen. Eight-way hand-tied springs that distribute weight across the entire seat deck rather than concentrating it under the heaviest points. Solid walnut legs, each hand-oiled and burnished to a depth that catches light differently at every hour of the day — cooler in the morning, warmer toward evening, as if the furniture itself is aware of the time. These are the details that separate a SIMIER piece from everything else on the market. They are also the details you will notice every single day: when you run your hand along the armrest, when you rest your coffee on the wide, flat surface of a well-proportioned arm, when you notice — months in — that the seat cushions have not lost their shape, that the fabric has not pilled, that the frame has remained absolutely silent.',
        mat_p2='Our foam is CertiPUR-US certified. Our wood is FSC-sourced. Our finishes are low-VOC and water-based — no off-gassing, no chemical smell, no headaches. We do not make a big deal about this because we believe it should be the baseline, not the exception. But we mention it here because someone has to. The furniture industry has normalized materials that off-gas for months after unboxing, fabrics that pill within a year, frames that creak from day one. We reject all of that. Quietly. Without marketing fanfare. The proof is in the piece.',
        cta_title='Ready to find your seat?',
        cta_text='Browse the full seating collection online, or contact us for a custom consultation — dimensions, fabrics, and fill can all be tailored. Every piece is made to order in our Guangdong workshop.',
        cta_link='../seating.html', cta_label='Shop Seating',
        asset_cat='坐具',
    ),
    'dining': dict(
        title='The Dining Collection',
        desc='Dining tables, chairs, and sets. Built for the long meal and the everyday breakfast.',
        hero='../../assets/餐厅/IMG_7723.JPG',
        hero_eyebrow='The Dining Collection',
        hero_title='Where the day<br>comes together.',
        hero_sub='A dining table is never just a table. It is the stage for Tuesday-night spaghetti and Saturday-night dinner parties. It holds homework and laptops, birthday cakes and condolence cards. It sees your family at their best, their worst, and their most unguarded. No other piece of furniture is asked to do so much — and so we build it to handle everything.',
        narrative_eyebrow='Why It Matters',
        narrative_title='The table is the hardest-working<br>piece of furniture you own.',
        narrative_p1='Think about everything your dining table does in a single week. Breakfast for one, eaten standing up while scrolling through email. Lunch over a video call, the laptop angled to hide the toast crumbs. Afternoon homework spread across every available inch. Evening dinner for four, with candles and wine and the kind of conversation that makes you forget to check your phone. Weekend brunch that stretches into late afternoon, the table accumulating coffee cups and newspaper sections and the pleasant disorder of a day with nowhere to be. Most furniture gets to do one thing well. A dining table has to do everything — and it has to make it look effortless.',
        narrative_p2='Our tables are cut from solid hardwood slabs — American oak, black walnut, and ash — each board selected individually for grain character, color consistency, and structural stability. We do not use veneers. We do not use engineered wood cores with a thin skin of something that looks like the real thing. The tabletop you see is the tabletop you get: a single slab or a bookmatched set of boards, joined with invisible glue lines and hand-sanded through five progressively finer grits until the surface feels almost soft to the touch. The finish is a hand-applied matte lacquer that protects against water rings and heat marks without creating that plastic-looking gloss you see on mass-produced furniture. Run your hand across the surface. That warmth is real wood. It always will be.',
        narrative_p3='And the chairs. A dining chair has a harder job than any seat in the house. It has to support a person through a three-hour meal — through appetizers and mains and dessert and another bottle of wine — without making them shift in their seat, cross and uncross their legs, or glance at the clock. Our chair frames use the same mortise-and-tenon joinery found in heirloom furniture. Seat depths and back angles are calibrated to actual human bodies — not industry averages from a 1970s ergonomics textbook. The result is a chair that disappears. You do not think about it. You think about the food, the company, the conversation. The chair just does its job, quietly, for decades.',
        featured_eyebrow='Featured Picks',
        featured_title='Tables, chairs, and the space between.',
        mat_title='Solid wood. Real joinery. No shortcuts.',
        mat_p1='Every tabletop tells the story of the tree it came from. The grain patterns, the mineral streaks, the subtle color variations — these are not imperfections to be hidden. They are the evidence of a living thing, now given a second life in your home. The legs are attached with traditional mortise-and-tenon joinery — a joint that has held furniture together for three thousand years, since before the written word, and will hold yours for at least a few decades more. No metal brackets. No cam locks. No assembly required beyond setting it in place.',
        mat_p2='We finish with a hand-rubbed matte lacquer that seals against moisture without suffocating the wood. The surface continues to breathe. It responds to humidity. It ages — slowly, gracefully, becoming more itself with every passing year. That is not a flaw to be managed. It is the whole point of owning furniture made from natural materials. In a world of disposable everything, a solid wood table is a quiet act of resistance.',
        cta_title='Bring everyone to the table.',
        cta_text='Explore our dining collection — from intimate two-person sets to tables that extend to seat twelve. Every piece is made to order in Guangdong.',
        cta_link='../dining.html', cta_label='Shop Dining',
        asset_cat='餐厅',
    ),
    'bedroom': dict(
        title='The Bedroom Collection',
        desc='Beds, headboards, and nightstands. A third of your life deserves furniture that means it.',
        hero='../../assets/卧室/IMG_7718.JPG',
        hero_eyebrow='The Bedroom Collection',
        hero_title='You spend 26 years<br>in bed. Make them count.',
        hero_sub='The average person sleeps for twenty-six years. Twenty-six years of eyes closed, breathing slow, the weight of the day lifting. The bed that holds you through all of that — through the restless nights and the rainy Sunday mornings, through illness and recovery, through the quiet intimacy of 3 a.m. conversations — should be more than a metal frame and a box spring. It should be the most carefully considered piece of furniture you own.',
        narrative_eyebrow='Why It Matters',
        narrative_title='Sleep is not a luxury.<br>Neither should be the furniture<br>that supports it.',
        narrative_p1='Walk into any furniture showroom and you will find beds that creak on day one. Frames assembled with cam locks that loosen with every toss and turn, every shift of weight, every quiet moment interrupted by the sound of metal scraping against particle board. Headboards attached with brackets designed for shipping convenience rather than structural integrity — wobbling gently against the wall, a small but constant reminder that something is not quite right. The bed becomes something you tolerate rather than something you look forward to. And because bedrooms are private spaces, we accept this. We would never tolerate a sofa that creaked or a dining table that wobbled. But the bed — the piece of furniture we spend more time in than any other — we have collectively decided is allowed to be mediocre. We reject that premise entirely.',
        narrative_p2='We build beds differently. Every SIMIER bed frame starts with a solid hardwood platform — no plywood, no particle board, no MDF, no engineered shortcuts hidden beneath upholstery. Center support legs run the full length of the mattress area and are screwed directly into the frame structure, not clipped on as an afterthought. The slat system is engineered to distribute weight evenly across the entire mattress surface — which means better support for your mattress, better support for your spine, and absolute silence when you roll over. Get up at 3 a.m. Your partner will not feel a thing. That is not a promise we make lightly. It is the result of engineering decisions made at every stage of design and construction.',
        narrative_p3='Our headboards are upholstered in the same Italian fabrics we use on our sofas — performance weaves and textured linens that invite you to lean back with a book, a cup of tea, or just a few minutes of quiet before the day begins. The nightstands are solid wood with soft-close drawers, English-dovetailed at all four corners, with a felt-lined top drawer for the things you want within reach but out of sight. Every surface that can be touched from the bed has been sanded and finished to the same standard as a dining table. Because your fingertips will find it in the dark, and they should find something warm.',
        featured_eyebrow='Featured Picks',
        featured_title='The foundation of every morning.',
        mat_title='Built silent. Built solid. Built to stay.',
        mat_p1='Kiln-dried hardwood frames. Steel-reinforced center supports. Slat systems with integrated anti-slip pads, spaced precisely to maintain mattress warranty requirements while maximizing airflow. These are not marketing bullet points — they are the engineering decisions that determine whether your bed is a sanctuary or a source of low-grade irritation every single night for years. The hardware is recessed and felt-padded where it meets the floor. The headboard brackets are steel, not plastic. The center leg has an adjustable foot to accommodate uneven floors — because no floor is perfectly level, and a bed should not require shims to sit steady.',
        mat_p2='Our finishes are low-VOC and water-based. No off-gassing. No chemical smell. No waking up with a headache you cannot explain. Just the quiet, steady presence of well-made furniture in the room where you are most vulnerable — where you sleep, dream, recover, and begin again each morning. We think that room deserves the best furniture we know how to make.',
        cta_title='Rest better, starting tonight.',
        cta_text='Discover beds, headboards, and nightstands — every piece made to order in our Guangdong workshop. Custom dimensions available.',
        cta_link='../bedroom.html', cta_label='Shop Bedroom',
        asset_cat='卧室',
    ),
    'storage': dict(
        title='The Storage Collection',
        desc='Cabinets, sideboards, coffee tables, and consoles. Organization has never looked this intentional.',
        hero='../../assets/柜类/IMG_7719.JPG',
        hero_eyebrow='The Storage Collection',
        hero_title='The things you keep<br>deserve a proper home.',
        hero_sub='Storage is not just about hiding clutter. It is about honoring the objects you have chosen to live with — the books that changed the way you think, the glassware your grandmother passed down, the record collection that soundtracks your Saturday mornings, the ceramic bowl you carried home from a trip and still remember buying. These things tell the story of who you are. They deserve furniture that tells the same story.',
        narrative_eyebrow='Why It Matters',
        narrative_title='Storage should never be<br>an afterthought.',
        narrative_p1='Most storage furniture is designed from the outside in — a visually acceptable facade hiding particle-board shelves, stapled back panels, and drawer bottoms so thin they bow under the weight of a few sweaters. The thinking, such as it is, goes like this: storage is utility, utility is invisible, therefore storage furniture can be built to a lower standard than the rest of the room. We think this logic is backward. Storage is the most intimate category of furniture. It holds the things you have decided are worth keeping. The things you reach for every day and the things you save for the right moment. Cabinets, sideboards, and shelves should be built with the same integrity as the objects they contain.',
        narrative_p2='We design from the inside out. Every SIMIER cabinet and sideboard starts with the same solid hardwood, the same joinery techniques, and the same finishing process as our dining tables and bed frames. Drawers are English-dovetailed at all four corners — a joint that actually strengthens as wood expands and contracts with the seasons. Shelves are solid wood, not veneered MDF, and rest on adjustable brass pins rather than fixed plastic clips. Soft-close hardware catches every door before it can slam, because the sound of a closing cabinet should be a quiet click, not a slap that reverberates through the room. Back panels are finished to the same standard as fronts — because someday you might place that cabinet in the middle of a room, or angle it in a corner, and the back will be just as visible as the front.',
        narrative_p3='Our coffee tables, side tables, and consoles follow the same philosophy. Solid wood tops. Mortise-and-tenon leg joints — the same joint used in fine woodworking for millennia. Hand-applied finishes that develop a patina rather than peeling or chipping. A coffee table should not wobble when you put your feet up after a long day. A console table should not sway when you set down a stack of books. These are not unreasonable expectations. They are the baseline. And if the industry has convinced you otherwise, we are here to reset that baseline.',
        featured_eyebrow='Featured Picks',
        featured_title='Storage that stands on its own.',
        mat_title='Inside and out, built to the same standard.',
        mat_p1='Solid wood drawer boxes with English dovetail joinery at every corner. Full-extension drawer glides rated for 100 pounds — open the drawer fully, load it with cast iron cookware or a full set of dinnerware, and it will glide smoothly every time. Adjustable shelf pins in solid brass that will not degrade, rust, or snap. Soft-close door hinges that catch the door in the last inch of travel and bring it gently home. These are the invisible details — the ones you do not see in a photograph, the ones no salesperson will mention, the ones that cost more to produce and take longer to make. They are also the details that determine whether a piece of furniture feels solid or flimsy, intentional or indifferent, built to last or built to be replaced.',
        mat_p2='Every surface — front, back, top, bottom, inside every drawer — is sanded through five grits and finished with the same hand-applied lacquer. Because we do not know which side will face the room. Because the inside of a drawer should feel as considered as the outside of a cabinet. Because the back panel that faces the wall today might face the room tomorrow, and it should be ready for that moment. We do not cut corners that no one will see. We finish every surface as if it will be the first thing you touch every morning.',
        cta_title='Give your things the home they deserve.',
        cta_text='Explore cabinets, sideboards, coffee tables, consoles, and more. Every piece made to order. Custom dimensions and configurations available.',
        cta_link='../storage.html', cta_label='Shop Storage',
        asset_cat='柜类+桌几',
    ),
    'sendayi': dict(
        title='Sen Yi Da Shi',
        desc='Chinese heritage furniture. Ruanti weaving, wild rattan, mountain palm. A thousand years of craft in every piece.',
        hero='../../assets/森怡大时/sendayi-07.jpg',
        hero_eyebrow='Chinese Heritage Collection',
        hero_title='以顺遂之心<br>致生活时光',
        hero_sub='Not a revival. Not a reproduction. A continuation. Sen Yi Da Shi carries forward the craft traditions of Song and Ming dynasty furniture — Ruanti hand-weaving, wild Indonesian rattan, mountain palm fiber, natural wood wax oil — shaped by artisans who inherited techniques that span a thousand years. Each piece is a collaboration between past and present, between the hands that remember and the homes that await.',
        narrative_eyebrow='Why It Matters',
        narrative_title='Some crafts are too important<br>to let disappear.',
        narrative_p1='Ruanti — the art of hand-weaving palm and rattan fibers into a tight, breathable seat surface — was the standard for fine Chinese furniture for centuries. The technique originated in the Ming dynasty, reached its technical peak during the Qing, and was nearly extinguished by the 20th century. Simmons mattresses arrived. Foam cushions replaced woven seats. Mass production rewarded speed over skill. By the 1990s, the number of artisans still practicing Ruanti at a professional level could be counted on two hands. An unbroken chain of craft knowledge stretching back six hundred years had, in the span of three generations, nearly snapped.',
        narrative_p2='Sen Yi Da Shi was born from a simple conviction: that this craft deserves to live, and that the people who practice it deserve to be supported. Our founder, Maggie, spent two years traveling across southern China — through Guizhou, Yunnan, Guangdong, and Fujian — finding the last remaining palm and rattan weavers, documenting their techniques, and adapting their methods to furniture designed for contemporary homes. She learned that wild Indonesian rattan, grown in volcanic soil under equatorial sun, produces vines far superior to cultivated varieties — thicker, stronger, more consistent in diameter. She discovered that mountain palm fiber, mentioned in Li Shizhen\'s Ming Dynasty Compendium of Materia Medica for its medicinal properties, also happens to be one of the most breathable, mite-resistant, and durable natural materials on earth — which is why the World Health Organization designated palm-fiber mattresses as approved medical bedding in the 1970s. None of this knowledge was secret. It had simply been forgotten by an industry that had moved on to faster, cheaper, more disposable methods.',
        narrative_p3='Every piece in the Sen Yi Da Shi collection uses traditional mortise-and-tenon joinery — no metal fasteners, no screws, no nails, just wood interlocking with wood in joints that actually strengthen as humidity and temperature shift through the seasons. The finishes contain zero formaldehyde. The wood is FSC-certified. The artisans who build each piece have an average of fifteen years of experience — and they are paid for their time, not for their output. These are not marketing claims. They are the terms of engagement for every piece that leaves our workshop. We document them here not to impress you, but because you have a right to know how your furniture was made, who made it, and what it is made of.',
        featured_eyebrow='Featured Picks',
        featured_title='Where to begin.',
        mat_title='Natural materials. Ancient techniques. Modern living.',
        mat_p1='Wild Indonesian rattan grows on volcanic soil under equatorial sun and rain — the thickest vines reach six centimeters in diameter, the longest exceed one hundred and eighty meters. It is hand-harvested, hand-stripped of knots and irregularities, and woven into seat surfaces that are simultaneously taut and giving, structured and breathable. Mountain palm fiber — the same material used for waterproof cables on modern naval warships — forms the base layer of our mattresses and seat cushions, providing resilience that foam cannot match and breathability that synthetic materials actively prevent. These are materials that work with the body rather than against it: cool in summer, warm in winter, responsive to pressure without collapsing under it.',
        mat_p2='Solid elm and black walnut form the frames. Natural wood wax oil — a German formulation derived from plant oils and waxes — protects the surface without sealing it in plastic. The wood continues to breathe. It responds to the humidity in your home. It develops a patina. It ages alongside you. That is not a compromise — it is the entire philosophy of the collection. Sen Yi Da Shi is furniture that lives. Furniture with memory. Furniture that becomes more itself with every passing year, carrying the traces of use not as damage but as evidence of a life well lived.',
        cta_title='Step into a thousand years of craft.',
        cta_text='Visit the complete Sen Yi Da Shi section with 13 pages of detailed product specifications, material deep-dives, founder stories, and team profiles.',
        cta_link='../sendayi.html', cta_label='Explore 森怡大时',
        asset_cat='森怡大时',
    ),
}

# ===== GENERATE =====
for key, cfg in configs.items():
    if cfg['asset_cat'] == '柜类+桌几':
        imgs = get_images('柜类') + get_images('桌几')
    else:
        imgs = get_images(cfg['asset_cat'])

    featured_imgs = pick(imgs, 4)
    spotlight_img = imgs[len(imgs)//3] if imgs else cfg['hero']

    # Build page
    html = HEAD_OPEN.format(title=cfg['title'], desc=cfg['desc'], hero=cfg['hero'])
    html += HERO.format(**cfg)

    # Narrative section
    html += f'''    <section class="dtc-section">
      <div class="container">
        <div class="dtc-section__header reveal">
          <p class="dtc-section__eyebrow">{cfg['narrative_eyebrow']}</p>
          <h2 class="dtc-section__title">{cfg['narrative_title']}</h2>
        </div>
        <div class="dtc-section__body reveal">
          <p>{cfg['narrative_p1']}</p>
          <p>{cfg['narrative_p2']}</p>
          <p>{cfg['narrative_p3']}</p>
        </div>
      </div>
    </section>
'''

    # Featured Picks
    html += f'''    <section class="dtc-section dtc-section--warm">
      <div class="container">
        <div class="dtc-section__header reveal">
          <p class="dtc-section__eyebrow">{cfg['featured_eyebrow']}</p>
          <h2 class="dtc-section__title">{cfg['featured_title']}</h2>
        </div>
        <div class="dtc-featured reveal">
'''
    for i, img in enumerate(featured_imgs):
        html += f'''          <div class="dtc-featured__card">
            <div class="dtc-featured__img" style="background-image:url('{img}')"></div>
            <p class="dtc-featured__name">{cfg['title'].replace("The ","").replace(" Collection","")} #{i+1:02d}</p>
            <p class="dtc-featured__desc">Solid hardwood frame. Italian upholstery. Made to order in Guangdong.</p>
          </div>
'''
    html += '''        </div>\n      </div>\n    </section>\n'''

    # Materials Spotlight
    html += f'''    <section class="dtc-section">
      <div class="container">
        <div class="dtc-spotlight reveal">
          <div class="dtc-spotlight__image" style="background-image:url('{spotlight_img}')"></div>
          <div class="dtc-spotlight__text">
            <h3>{cfg['mat_title']}</h3>
            <p>{cfg['mat_p1']}</p>
            <p>{cfg['mat_p2']}</p>
          </div>
        </div>
      </div>
    </section>
'''

    # Full Gallery
    html += '''    <section class="dtc-section dtc-section--warm">
      <div class="container">
        <div class="dtc-section__header reveal">
          <p class="dtc-section__eyebrow">The Complete Range</p>
          <h2 class="dtc-section__title">Every finish. Every angle.<br>Every detail.</h2>
        </div>
        <div class="dtc-masonry reveal">
'''
    for img in imgs:
        html += f'          <div class="dtc-masonry__item"><img src="{img}" alt="{cfg["title"]}" loading="lazy"></div>\n'
    html += '''        </div>\n      </div>\n    </section>\n'''

    # CTA
    html += CLOSE.format(**cfg)

    fpath = os.path.join(pages_dir, f'{key}.html')
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'✓ gallery/{key}.html — {len(imgs)} images, {html.count(chr(10))} lines')

print(f'\nDone! 5 DTC-style pages in {pages_dir}/')
