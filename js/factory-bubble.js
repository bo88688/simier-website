/* ============================================================
   SIMIER Factory Tour Floating Bubble
   ============================================================ */

(function () {
  'use strict';

  var bubble = document.getElementById('factoryBubble');
  if (!bubble) return;

  var closeBtn = document.getElementById('factoryBubbleClose');
  var DISMISS_KEY = 'simier_factory_bubble_dismissed';

  // 如果之前关闭过，不再显示
  if (sessionStorage.getItem(DISMISS_KEY) === '1') {
    bubble.style.display = 'none';
    return;
  }

  // 入场动画后添加浮动效果
  setTimeout(function () {
    bubble.classList.add('factory-bubble--floating');
  }, 800);

  // 关闭按钮
  if (closeBtn) {
    closeBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      sessionStorage.setItem(DISMISS_KEY, '1');
      bubble.style.opacity = '0';
      bubble.style.transform = bubble.style.transform + ' scale(0)';
      setTimeout(function () {
        bubble.style.display = 'none';
      }, 400);
    });
  }

})();
