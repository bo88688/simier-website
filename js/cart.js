/* ============================================================
   SIMIER Shopping Cart
   ============================================================ */

(function () {
  'use strict';

  // Get cart from localStorage
  function getCart() {
    try {
      return JSON.parse(localStorage.getItem('simier_cart') || '[]');
    } catch (e) {
      return [];
    }
  }

  // Save cart to localStorage
  function saveCart(cart) {
    localStorage.setItem('simier_cart', JSON.stringify(cart));
  }

  // Update cart count badge
  function updateBadge() {
    const cart = getCart();
    const icon = document.querySelector('.header__icon-btn--cart');
    if (!icon) return;
    let badge = icon.querySelector('.cart-badge');
    if (cart.length === 0) {
      if (badge) badge.remove();
      return;
    }
    if (!badge) {
      badge = document.createElement('span');
      badge.className = 'cart-badge';
      icon.appendChild(badge);
    }
    badge.textContent = cart.length;
  }

  // Show toast notification
  function showToast(msg) {
    const toast = document.createElement('div');
    toast.className = 'cart-toast';
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add('cart-toast--visible'), 10);
    setTimeout(() => {
      toast.classList.remove('cart-toast--visible');
      setTimeout(() => toast.remove(), 400);
    }, 2500);
  }

  // Add to cart
  function addToCart(name, price, image) {
    const cart = getCart();
    // Check for duplicates
    const exists = cart.find(item => item.name === name);
    if (exists) {
      showToast('"' + name + '" is already in your cart');
      return;
    }
    cart.push({ name: name, price: price, image: image });
    saveCart(cart);
    updateBadge();
    showToast('Added "' + name + '" to cart ✓');
  }

  // Handle "Add to Cart" button clicks
  function setupButtons() {
    const btn = document.querySelector('.btn--add-cart');
    if (!btn) return;
    const name = btn.dataset.name;
    const price = btn.dataset.price;
    const image = btn.dataset.image;
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      addToCart(name, price, image);
    });
  }

  // Render cart page
  function renderCartPage() {
    const container = document.getElementById('cartItems');
    const empty = document.getElementById('cartEmpty');
    const summary = document.getElementById('cartSummary');
    if (!container) return;

    const cart = getCart();
    if (cart.length === 0) {
      if (empty) empty.style.display = 'block';
      if (container) container.style.display = 'none';
      if (summary) summary.style.display = 'none';
      return;
    }

    if (empty) empty.style.display = 'none';
    if (container) container.style.display = 'block';
    if (summary) summary.style.display = 'block';

    let html = '';
    cart.forEach((item, i) => {
      const priceNum = parseFloat(item.price.replace(/[^0-9.]/g, ''));
      html += '<div class="cart-item">';
      if (item.image) {
        html += '<div class="cart-item__image" style="background-image:url(\'' + item.image + '\')"></div>';
      }
      html += '<div class="cart-item__info">';
      html += '<h4 class="cart-item__name">' + item.name + '</h4>';
      html += '<p class="cart-item__price">' + item.price + '</p>';
      html += '</div>';
      html += '<button class="cart-item__remove" data-index="' + i + '" aria-label="Remove">×</button>';
      html += '</div>';
    });
    container.innerHTML = html;

    // Total
    const total = cart.reduce((sum, item) => {
      return sum + parseFloat(item.price.replace(/[^0-9.]/g, ''));
    }, 0);
    document.getElementById('cartTotal').textContent = '$' + total.toLocaleString();

    // Remove buttons
    container.querySelectorAll('.cart-item__remove').forEach(btn => {
      btn.addEventListener('click', function () {
        const idx = parseInt(this.dataset.index);
        const newCart = getCart();
        newCart.splice(idx, 1);
        saveCart(newCart);
        updateBadge();
        renderCartPage();
      });
    });
  }

  // Email cart
  function setupEmailCart() {
    const btn = document.getElementById('emailCartBtn');
    const input = document.getElementById('emailCartInput');
    const status = document.getElementById('emailCartStatus');
    if (!btn || !input) return;

    btn.addEventListener('click', function () {
      const email = input.value.trim();
      if (!email) {
        if (status) { status.textContent = 'Please enter your email address'; status.style.color = '#e74c3c'; }
        return;
      }

      const cart = getCart();
      let body = '🛒 Your SIMIER Cart:\n\n';
      cart.forEach((item, i) => {
        body += (i + 1) + '. ' + item.name + ' — ' + item.price + '\n';
      });
      const total = cart.reduce((s, i) => s + parseFloat(i.price.replace(/[^0-9.]/g, '')), 0);
      body += '\n💰 Total: $' + total.toLocaleString() + '\n\n';
      body += 'To complete your order, reply to this email or visit simier.top\n';
      body += 'Your cart will be saved for 30 days.\n';

      window.location.href = 'mailto:' + encodeURIComponent(email) +
        '?subject=' + encodeURIComponent('🛒 My SIMIER Cart — ' + cart.length + ' items') +
        '&body=' + encodeURIComponent(body);

      if (status) {
        status.textContent = 'Opening your email app... ✉️';
        status.style.color = '#4a9c6d';
      }
    });
  }

  // Save cart for later — email reminder
  function setupEmailReminder() {
    const btn = document.getElementById('saveCartBtn');
    if (!btn) return;
    btn.addEventListener('click', function () {
      const cart = getCart();
      if (cart.length === 0) return;
      let body = '🛒 Saved SIMIER Cart:\n\n';
      cart.forEach((item, i) => {
        body += (i + 1) + '. ' + item.name + ' — ' + item.price + '\n';
      });
      const total = cart.reduce((s, i) => s + parseFloat(i.price.replace(/[^0-9.]/g, '')), 0);
      body += '\n💰 Total: $' + total.toLocaleString() + '\n\n';
      body += 'Come back anytime to simier.top to continue shopping. Your cart items are saved in your browser.\n';

      const subject = '🛒 Your SIMIER Cart — Save for Later';
      window.location.href = 'mailto:?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    });
  }

  // Initialize
  document.addEventListener('DOMContentLoaded', function () {
    updateBadge();
    setupButtons();

    // Check if we're on the cart page
    if (document.getElementById('cartItems')) {
      renderCartPage();
      setupEmailCart();
      setupEmailReminder();
    }

    // Listen for add-to-cart events from product pages
    document.querySelectorAll('[data-add-cart]').forEach(btn => {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        addToCart(this.dataset.name, this.dataset.price, this.dataset.image || '');
      });
    });
  });

  // Expose to window
  window.SIMIER_Cart = {
    add: addToCart,
    get: getCart,
    updateBadge: updateBadge,
  };

})();
