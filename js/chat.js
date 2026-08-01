/* ============================================================
   SIMIER AI Chat Widget
   ============================================================ */

(function () {
  'use strict';

  const bubble = document.getElementById('chatBubble');
  const panel = document.getElementById('chatPanel');
  const closeBtn = document.getElementById('chatClose');
  const messages = document.getElementById('chatMessages');
  const quickBtns = document.getElementById('chatQuick');
  const form = document.getElementById('chatInputForm');
  const input = document.getElementById('chatInput');

  let isOpen = false;

  // Knowledge base
  const knowledge = {
    'sofa': 'Our sofas range from compact 2-seaters to modular sectionals. The "Shanhai Modular Sofa" is perfect for apartments — you can start with an L-shape and expand later. Fabrics include Italian tech-linen, velvet, and premium microfiber. All covers are removable and washable! 🛋️',
    'small': 'Great question! For compact spaces, check out our "Yunying Lounge Chair" (only 75cm wide with 360° swivel) or the "Shanhai Modular Sofa" — it grows with you. Our furniture is designed specifically for urban apartments and student living. 🏠',
    'apartment': 'Our entire collection is designed with small spaces in mind! The "Yunying Lounge Chair", "Cangshan Sideboard" (push-door, no clearance needed), and "Yuexiang Round Table" (60cm diameter) are our top apartment picks. 📐',
    'student': 'YES! We offer a 15% student discount for verified university students worldwide. Just email us from your .edu address or show your student ID. Because your first apartment deserves good furniture! 🎓',
    'discount': 'We have a 15% student discount, and also seasonal promotions. Sign up for our newsletter to get notified about sales. We also offer bundle pricing when you furnish a full room! 💰',
    'shipping': 'We ship worldwide from our atelier in Foshan, Guangdong! Delivery typically takes 7-15 business days depending on your location. Free shipping on orders over $1,390. We ship to France, USA, Turkey, and beyond! 🚚',
    'price': 'Our pieces range from $415 (Yuexiang Round Table) to $4,970 (Shanhai Modular Sofa). The sweet spot for most first-apartment buyers is $695–2,085. Great value for solid wood, Italian fabrics, and real craftsmanship! 💎',
    'material': 'We use solid oak, walnut, and ash wood for frames; Italian-imported tech fabrics and premium microfiber for upholstery; and eco-friendly water-based finishes. Every piece passes 27 quality checks. No shortcuts! 🌿',
    'fabric': 'We offer Italian tech-linen (breathable, casual look), premium velvet (soft, rich texture), and microfiber (durable, easy-clean). All are stain-resistant and removable for washing. Color samples available on request! 🎨',
    'custom': 'Yes! Since we manufacture in our own atelier, we can customize dimensions, fabrics, and wood finishes. Contact us with your requirements and we will provide a quote within 48 hours. Made just for you! ✨',
    'partner': 'We are actively seeking distribution partners worldwide! Visit our Partners page for details on margins, support, and product training. Or leave your email and our B2B team will reach out! 🤝',
    'return': '30-day satisfaction guarantee. If you are not happy, we will arrange return shipping. Our pieces are built to last, but if anything goes wrong, we offer a 2-year warranty on frames and 1 year on upholstery. 💪',
    'hi': 'Hello! 👋 So happy you stopped by. I am your SIMIER design assistant. What can I help you with — finding the right sofa, checking prices, student discounts, or just exploring?',
    'hello': 'Hey there! 👋 Welcome to SIMIER. We make beautiful furniture for first homes around the world. What brings you here today?',
    'email': 'You can reach our team directly at <b>hello@simier.top</b> 📧 We typically respond within 24 hours. Or leave your email here and I will have someone reach out!',
    'contact': 'Absolutely! You can email us anytime at <b>hello@simier.top</b> ✉️ Our team responds within 24 hours. Want to leave a message right now? Just type your email and message below!',
    'human': 'Of course! I will connect you. Please type your email address and message, and a real person from our team will get back to you within 24 hours 💌',
    'real': 'Absolutely! Our team at <b>hello@simier.top</b> would love to help you personally. Leave your email and message here, or email us directly ✉️',
  };

  function getBotReply(text) {
    const lower = text.toLowerCase();
    for (const [key, reply] of Object.entries(knowledge)) {
      if (lower.includes(key)) return reply;
    }
    const fallbacks = [
      'That is a great question! 😊 You can reach our team directly at <b>hello@simier.top</b> — they will get back to you within 24 hours. Or leave your email here and I will pass it along! ✉️',
      'I love talking about furniture! 😄 For detailed questions, email us at <b>hello@simier.top</b> or leave your email below and our team will reach out 💌',
      'Good one! 🎯 Our human team knows everything — reach them at <b>hello@simier.top</b> or drop your email here for a personal reply within 24 hours ✨',
    ];
    return fallbacks[Math.floor(Math.random() * fallbacks.length)];
  }

  function addMessage(text, type) {
    const div = document.createElement('div');
    div.className = 'chat-widget__msg chat-widget__msg--' + type;
    div.innerHTML = '<p>' + text + '</p>';
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  function showTyping() {
    const div = document.createElement('div');
    div.className = 'chat-widget__msg chat-widget__msg--bot chat-widget__msg--typing';
    div.innerHTML = '<p><span></span><span></span><span></span></p>';
    div.id = 'typingIndicator';
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  function hideTyping() {
    const el = document.getElementById('typingIndicator');
    if (el) el.remove();
  }

  function handleSend(text) {
    if (!text.trim()) return;
    addMessage(text, 'user');
    showTyping();
    setTimeout(() => {
      hideTyping();
      addMessage(getBotReply(text), 'bot');
    }, 800 + Math.random() * 1000);
  }

  // Open/close panel
  bubble.addEventListener('click', () => {
    isOpen = !isOpen;
    panel.classList.toggle('chat-widget__panel--open', isOpen);
    bubble.classList.toggle('chat-widget__bubble--active', isOpen);
    if (isOpen) {
      input.focus();
      quickBtns.style.display = 'flex';
    }
  });

  closeBtn.addEventListener('click', () => {
    isOpen = false;
    panel.classList.remove('chat-widget__panel--open');
    bubble.classList.remove('chat-widget__bubble--active');
  });

  // Add Email Us quick button dynamically
  var emailBtn = document.createElement('button');
  emailBtn.className = 'chat-widget__quick-btn';
  emailBtn.setAttribute('data-q', 'I want to contact a real person');
  emailBtn.textContent = '✉️ Email Us';
  if (quickBtns) quickBtns.appendChild(emailBtn);

  // Quick replies
  quickBtns.addEventListener('click', (e) => {
    const btn = e.target.closest('.chat-widget__quick-btn');
    if (!btn) return;
    const q = btn.dataset.q;
    handleSend(q);
    quickBtns.style.display = 'none';
  });

  // Form submit
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    handleSend(text);
    input.value = '';
    quickBtns.style.display = 'none';
  });

  // Show bubble with cute bounce on load
  setTimeout(() => {
    var b = document.getElementById('chatBubble');
    if (b) b.classList.add('chat-widget__bubble--visible');
  }, 1500);

  // Auto-bind all "contact us" buttons to open chat
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-i18n="cart.contact"]');
    if (!btn) { btn = e.target.closest('[onclick*="openChat"]'); }
    if (!btn) return;
    e.preventDefault();
    e.stopPropagation();
    // Try to find product name from nearby elements
    var nameEl = document.querySelector('.product-detail__name');
    var productName = nameEl ? nameEl.textContent.trim() : '';
    window.openChat(productName);
  }, true);

  // Expose open function globally for product page buttons
  window.openChat = function (productName) {
    var p = document.getElementById('chatPanel');
    var b = document.getElementById('chatBubble');
    if (p && b) {
      isOpen = true;
      panel = p;
      bubble = b;
      p.classList.add('chat-widget__panel--open');
      b.classList.add('chat-widget__bubble--active');
      b.classList.add('chat-widget__bubble--visible');

      // Show email options right away
      var qb = document.getElementById('chatQuick');
      var msgs = document.getElementById('chatMessages');

      // Show email options
      if (qb) {
        qb.style.display = 'flex';
        qb.style.flexWrap = 'wrap';
        qb.innerHTML = '';
        var subject = productName ? 'Inquiry about ' + productName : 'SIMIER Inquiry';
        var opts = [
          {label:'🛋️ Product Inquiry', q:'product'},
          {label:'📦 Order Question', q:'order'},
          {label:'🤝 Partnership', q:'partnership'},
          {label:'📰 Press / Media', q:'press'},
          {label:'💬 Other', q:'other'}
        ];
        opts.forEach(function(o){
          var btn = document.createElement('button');
          btn.className = 'chat-widget__quick-btn';
          btn.textContent = o.label;
          btn.addEventListener('click', function(){
            var body = 'Hi SIMIER team,\n\nI have a ' + o.label.replace(/[^\w\s]/g,'').trim() + '.\n\n';
            if (productName) body += 'Product: ' + productName + '\n\n';
            body += '[Please describe your inquiry here]\n\nBest regards';
            window.location.href = 'mailto:hello@simier.top?subject=' + encodeURIComponent(subject + ' — ' + o.label) + '&body=' + encodeURIComponent(body);
            addMessage('Opening your email app with a pre-filled message template ✉️', 'bot');
          });
          qb.appendChild(btn);
        });
      }

      // Show welcome message
      if (msgs) {
        var prodMsg = productName ? 'about <b>' + productName + '</b>' : '';
        addMessage('Thanks for reaching out! Choose an option below and your email app will open with a pre-written message to <b>hello@simier.top</b> ✉️', 'bot');
      }

      setTimeout(function () {
        var inp = document.getElementById('chatInput');
        if (inp) inp.focus();
      }, 400);
    }
  };

})();
