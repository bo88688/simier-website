/* ============================================================
   SIMIER Factory Tour Floating Bubble
   ============================================================ */

(function () {
  'use strict';

  var bubble = document.getElementById('factoryBubble');
  if (!bubble) return;

  var closeBtn = document.getElementById('factoryBubbleClose');
  var DISMISS_KEY = 'simier_factory_bubble_dismissed';

  // Don't show if user closed it this session
  if (sessionStorage.getItem(DISMISS_KEY) === '1') {
    bubble.style.display = 'none';
    return;
  }

  // Entrance: show after a short delay with bounce
  var showTimer = setTimeout(function () {
    bubble.classList.add('factory-bubble--visible');
    // Start floating after entrance settles
    setTimeout(function () {
      bubble.classList.add('factory-bubble--floating');
    }, 600);
  }, 1800);

  // Close button
  if (closeBtn) {
    closeBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      sessionStorage.setItem(DISMISS_KEY, '1');
      bubble.classList.remove('factory-bubble--visible');
      bubble.classList.remove('factory-bubble--floating');
      setTimeout(function () {
        bubble.style.display = 'none';
      }, 400);
    });
  }

  // Fade out slightly when user scrolls past middle of page
  var scrollHandler = function () {
    var scrollPct = window.scrollY / (document.body.scrollHeight - window.innerHeight);
    if (scrollPct > 0.6) {
      bubble.style.opacity = Math.max(0.15, 1 - (scrollPct - 0.6) * 2);
    } else {
      bubble.style.opacity = '';
    }
  };

  var scrollTicking = false;
  window.addEventListener('scroll', function () {
    if (!scrollTicking) {
      requestAnimationFrame(function () {
        scrollHandler();
        scrollTicking = false;
      });
      scrollTicking = true;
    }
  }, { passive: true });

})();
