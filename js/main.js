/* ============================================================
   OBJET — Main JavaScript
   ============================================================ */

(function () {
  'use strict';

  // --- DOM References ---
  const header = document.getElementById('header');
  const menuToggle = document.getElementById('menuToggle');
  const mainNav = document.getElementById('mainNav');
  const newsletterForm = document.getElementById('newsletterForm');

  // --- State ---
  let isMenuOpen = false;
  let lastScrollY = 0;

  // ============================================================
  // HEADER SCROLL BEHAVIOR
  // ============================================================
  function updateHeader() {
    const scrollY = window.scrollY;
    if (scrollY > 60) {
      header.classList.add('header--scrolled');
    } else {
      header.classList.remove('header--scrolled');
    }
    lastScrollY = scrollY;
  }

  // ============================================================
  // MOBILE MENU
  // ============================================================
  function openMenu() {
    isMenuOpen = true;
    menuToggle.classList.add('active');
    mainNav.classList.add('active');
    header.classList.add('header--scrolled');
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    isMenuOpen = false;
    menuToggle.classList.remove('active');
    mainNav.classList.remove('active');
    document.body.style.overflow = '';
    updateHeader(); // Restore correct header state
  }

  function toggleMenu() {
    if (isMenuOpen) {
      closeMenu();
    } else {
      openMenu();
    }
  }

  menuToggle.addEventListener('click', toggleMenu);

  // Close menu when clicking a nav link
  mainNav.querySelectorAll('.header__link').forEach(link => {
    link.addEventListener('click', () => {
      if (isMenuOpen) closeMenu();
    });
  });

  // ============================================================
  // INTERSECTION OBSERVER — REVEAL ANIMATIONS
  // ============================================================
  const revealElements = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            revealObserver.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.12,
        rootMargin: '0px 0px -40px 0px',
      }
    );

    revealElements.forEach(el => revealObserver.observe(el));
  } else {
    // Fallback: show all immediately
    revealElements.forEach(el => el.classList.add('visible'));
  }

  // ============================================================
  // SMOOTH SCROLL FOR ANCHOR LINKS
  // ============================================================
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;

      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const headerHeight = header.offsetHeight;
        const targetPosition = target.getBoundingClientRect().top + window.scrollY - headerHeight;

        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth',
        });
      }
    });
  });

  // ============================================================
  // NEWSLETTER FORM
  // ============================================================
  if (newsletterForm) {
    newsletterForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const input = this.querySelector('.newsletter__input');
      const button = this.querySelector('button');

      if (!input.value.trim()) return;

      // Visual feedback
      const originalText = button.textContent;
      button.textContent = '欢迎加入 ✓';
      button.style.background = '#9CAF88';
      input.value = '';

      setTimeout(() => {
        button.textContent = originalText;
        button.style.background = '';
      }, 2500);
    });
  }

  // ============================================================
  // CONTACT FORM
  // ============================================================
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const btn = this.querySelector('button');
      const original = btn.textContent;
      btn.textContent = 'Message Sent — Thank You';
      btn.style.background = '#9CAF88';
      btn.style.color = '#fff';
      btn.style.border = 'none';
      this.reset();
      setTimeout(() => {
        btn.textContent = original;
        btn.style.background = '';
        btn.style.color = '';
        btn.style.border = '';
      }, 3000);
    });
  }

  // ============================================================
  // PARALLAX-LIKE EFFECT ON HERO
  // ============================================================
  const heroBg = document.querySelector('.hero__bg');
  if (heroBg) {
    window.addEventListener('scroll', () => {
      const scrollY = window.scrollY;
      const heroSection = document.getElementById('hero');
      if (!heroSection) return;

      const heroHeight = heroSection.offsetHeight;
      if (scrollY <= heroHeight) {
        const offset = scrollY * 0.35;
        heroBg.style.transform = `scale(1.05) translateY(${offset}px)`;
      }
    }, { passive: true });
  }

  // ============================================================
  // INIT
  // ============================================================
  // Set initial header state
  header.classList.add('header--scrolled');
  updateHeader();

  // Listen for scroll
  window.addEventListener('scroll', updateHeader, { passive: true });

  // Handle resize (close menu on desktop breakpoint)
  window.addEventListener('resize', () => {
    if (window.innerWidth > 768 && isMenuOpen) {
      closeMenu();
    }
  });

})();
