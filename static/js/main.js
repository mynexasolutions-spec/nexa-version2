/* â”€â”€ Navbar scroll float â”€â”€ */
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 60);
  });
}

/* â”€â”€ Hamburger menu â”€â”€ */
const hamburgerBtn = document.getElementById('hamburgerBtn');
const navLinks = document.querySelector('.nav-links');

if (hamburgerBtn && navLinks) {
  const closeMobileNav = () => {
    hamburgerBtn.classList.remove('open');
    navLinks.classList.remove('open');
    hamburgerBtn.setAttribute('aria-expanded', 'false');
    document.querySelectorAll('.has-dropdown').forEach((d) => d.classList.remove('open'));
  };

  hamburgerBtn.addEventListener('click', () => {
    const isOpen = hamburgerBtn.classList.toggle('open');
    navLinks.classList.toggle('open', isOpen);
    hamburgerBtn.setAttribute('aria-expanded', String(isOpen));
  });

  navLinks.querySelectorAll('a:not(.dropdown-toggle)').forEach((link) => {
    link.addEventListener('click', closeMobileNav);
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
      closeMobileNav();
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      closeMobileNav();
    }
  });
}

/* ── Tools dropdown (mobile accordion) ── */
// Dropdown toggles: prevent navigation and toggle open state. Works on desktop and mobile.
document.querySelectorAll('.dropdown-toggle').forEach((toggle) => {
  toggle.addEventListener('click', (e) => {
    e.preventDefault();
    const parent = toggle.closest('.has-dropdown');
    if (!parent) return;
    const isOpen = parent.classList.toggle('open');
    // Close other open dropdowns
    document.querySelectorAll('.has-dropdown.open').forEach((d) => {
      if (d !== parent) d.classList.remove('open');
    });
    // On mobile, also expand the nav container if necessary
    if (window.innerWidth <= 768) {
      parent.classList.toggle('open', isOpen);
    }
  });
});

// Close dropdowns when clicking outside
document.addEventListener('click', (e) => {
  if (e.target.closest('.has-dropdown')) return;
  document.querySelectorAll('.has-dropdown.open').forEach((d) => d.classList.remove('open'));
});

/* â”€â”€ Projects scroll observer â”€â”€ */
const projectItems = document.querySelectorAll('.project-target');
const numberTrack = document.getElementById('projectNumberTrack');
const numbers = document.querySelectorAll('.project-number');

if (projectItems.length && numberTrack) {
  let activeProjectIndex = 0;
  let projectTicking = false;

  const syncProjectDisplay = (index) => {
    const numberHeight = numbers[0] ? numbers[0].offsetHeight : 160;
    numbers.forEach((num) => num.classList.remove('active'));
    if (numbers[index]) {
      numbers[index].classList.add('active');
    }
    numberTrack.style.transform = `translateY(-${index * numberHeight}px)`;
    projectItems.forEach((item) => item.classList.remove('active'));
    if (projectItems[index]) {
      projectItems[index].classList.add('active');
    }
    activeProjectIndex = index;
  };

  const getProjectActivationLine = () => {
    return window.innerWidth <= 768 ? window.innerHeight * 0.4 : window.innerHeight * 0.52;
  };

  const updateActiveProject = () => {
    const activationLine = getProjectActivationLine();
    let nextIndex = activeProjectIndex;
    let closestDistance = Number.POSITIVE_INFINITY;

    projectItems.forEach((item, index) => {
      const rect = item.getBoundingClientRect();
      const itemCenter = rect.top + (rect.height / 2);
      const distance = Math.abs(itemCenter - activationLine);

      if (distance < closestDistance) {
        closestDistance = distance;
        nextIndex = index;
      }
    });

    if (nextIndex !== activeProjectIndex) {
      syncProjectDisplay(nextIndex);
    }

    projectTicking = false;
  };

  const requestProjectSync = () => {
    if (projectTicking) {
      return;
    }

    projectTicking = true;
    window.requestAnimationFrame(updateActiveProject);
  };

  syncProjectDisplay(0);
  requestProjectSync();
  window.addEventListener('scroll', requestProjectSync, { passive: true });
  window.addEventListener('resize', requestProjectSync);
}

/* ── Reviews slider arrows ── */
const reviewsGrid = document.querySelector('.reviews-grid');
const prevArrow = document.querySelector('.reviews-arrow-prev');
const nextArrow = document.querySelector('.reviews-arrow-next');
if (reviewsGrid && prevArrow && nextArrow) {
  const scrollAmount = () => {
    const card = reviewsGrid.querySelector('.review-card');
    return card ? card.offsetWidth + 24 : 380;
  };
  prevArrow.addEventListener('click', () => {
    reviewsGrid.scrollBy({ left: -scrollAmount(), behavior: 'smooth' });
  });
  nextArrow.addEventListener('click', () => {
    reviewsGrid.scrollBy({ left: scrollAmount(), behavior: 'smooth' });
  });
}

/* ── Why Us horizontal rail (Ultra-Smooth) ── */
const whyUsRail = document.getElementById('whyUsRail');
if (whyUsRail) {
  const whyUsTrack = whyUsRail.querySelector('.why-us-grid');
  let whyUsRaf = null;
  let lastTick = 0;
  let isDraggingRail = false;
  let isWhyUsPaused = false;
  let dragStartX = 0;
  let dragStartXPos = 0;
  let currentX = 0;

  const pauseMotion = () => { isWhyUsPaused = true; };
  const resumeMotion = () => { isWhyUsPaused = false; };

  const setupCardInteractions = (card) => {
    card.addEventListener('mouseenter', pauseMotion);
    card.addEventListener('mouseleave', resumeMotion);
    // For mobile: pause only when touching a specific card
    card.addEventListener('touchstart', pauseMotion, { passive: true });
    card.addEventListener('touchend', resumeMotion, { passive: true });
    card.addEventListener('touchcancel', resumeMotion, { passive: true });
  };

  // Initialize original cards and clones for infinite loop
  if (whyUsTrack && !whyUsTrack.dataset.loopReady) {
    const originalCards = Array.from(whyUsTrack.children);
    originalCards.forEach((card) => {
      setupCardInteractions(card);
      const clone = card.cloneNode(true);
      clone.classList.remove('reveal', 'visible');
      clone.removeAttribute('data-delay');
      setupCardInteractions(clone);
      whyUsTrack.appendChild(clone);
    });
    whyUsTrack.dataset.loopReady = 'true';
  }

  let cachedLoopWidth = 0;
  window.addEventListener('resize', () => { cachedLoopWidth = 0; });

  const getLoopWidth = () => {
    if (!whyUsTrack) return 0;
    if (cachedLoopWidth === 0) {
      cachedLoopWidth = whyUsTrack.scrollWidth / 2;
    }
    return cachedLoopWidth;
  };

  const animateWhyUsRail = (ts) => {
    if (isWhyUsPaused || isDraggingRail) {
      lastTick = ts;
      whyUsRaf = window.requestAnimationFrame(animateWhyUsRail);
      return;
    }
    if (!lastTick) lastTick = ts;
    const dt = ts - lastTick;
    lastTick = ts;

    const loopWidth = getLoopWidth();
    if (loopWidth > 0) {
      currentX -= dt * 0.07; // Peppier speed as requested
      if (currentX <= -loopWidth) currentX += loopWidth;
      if (currentX > 0) currentX -= loopWidth;
      whyUsTrack.style.transform = `translate3d(${currentX}px, 0, 0)`;
    }

    whyUsRaf = window.requestAnimationFrame(animateWhyUsRail);
  };

  const startRailDrag = (clientX) => {
    isDraggingRail = true;
    whyUsRail.classList.add('dragging');
    dragStartX = clientX;
    dragStartXPos = currentX;
  };

  const moveRailDrag = (clientX) => {
    if (!isDraggingRail) return;
    const delta = clientX - dragStartX;
    currentX = dragStartXPos + delta;

    const loopWidth = getLoopWidth();
    if (currentX <= -loopWidth) currentX += loopWidth;
    if (currentX > 0) currentX -= loopWidth;
    whyUsTrack.style.transform = `translate3d(${currentX}px, 0, 0)`;
  };

  const endRailDrag = () => {
    if (!isDraggingRail) return;
    isDraggingRail = false;
    whyUsRail.classList.remove('dragging');
  };

  // Rail Dragging (Area-wide)
  whyUsRail.addEventListener('mousedown', (e) => startRailDrag(e.clientX));
  window.addEventListener('mousemove', (e) => moveRailDrag(e.clientX));
  window.addEventListener('mouseup', endRailDrag);

  // Mobile Dragging (Allow swiping across the whole rail)
  whyUsRail.addEventListener('touchstart', (e) => {
    startRailDrag(e.touches[0].clientX);
  }, { passive: true });
  whyUsRail.addEventListener('touchmove', (e) => {
    moveRailDrag(e.touches[0].clientX);
  }, { passive: true });
  whyUsRail.addEventListener('touchend', endRailDrag, { passive: true });
  whyUsRail.addEventListener('touchcancel', endRailDrag, { passive: true });

  // Why Us Arrow Listeners
  const whyPrev = document.querySelector('.why-arrow-prev');
  const whyNext = document.querySelector('.why-arrow-next');
  if (whyPrev && whyNext) {
    const scrollJump = () => {
      const card = whyUsTrack.querySelector('.why-card');
      return card ? card.offsetWidth + 30 : 400; // card width + gap
    };

    whyPrev.addEventListener('click', (e) => {
      e.stopPropagation();
      const jump = scrollJump();
      currentX += jump;
      const loopWidth = getLoopWidth();
      if (currentX > 0) currentX -= loopWidth;
      
      whyUsTrack.style.transition = 'transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1)';
      whyUsTrack.style.transform = `translate3d(${currentX}px, 0, 0) rotate(-0.5deg)`;
      setTimeout(() => { whyUsTrack.style.transition = ''; }, 500);
    });

    whyNext.addEventListener('click', (e) => {
      e.stopPropagation();
      const jump = scrollJump();
      currentX -= jump;
      const loopWidth = getLoopWidth();
      if (currentX <= -loopWidth) currentX += loopWidth;
      
      whyUsTrack.style.transition = 'transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1)';
      whyUsTrack.style.transform = `translate3d(${currentX}px, 0, 0) rotate(-0.5deg)`;
      setTimeout(() => { whyUsTrack.style.transition = ''; }, 500);
    });

    // Pause on arrow interaction
    [whyPrev, whyNext].forEach(arrow => {
      arrow.addEventListener('mouseenter', pauseMotion);
      arrow.addEventListener('mouseleave', resumeMotion);
    });
  }

  whyUsRaf = window.requestAnimationFrame(animateWhyUsRail);
}

/* â”€â”€ Why Us Lottie icons â”€â”€ */
document.querySelectorAll('.why-lottie').forEach((iconEl) => {
  const animationKey = iconEl.getAttribute('data-animation-key');
  const animationPath = iconEl.getAttribute('data-animation');
  const registry = window.NEXA_ANIMATIONS || window.whyUsAnimations || null;
  const animationData = (registry && animationKey) ? registry[animationKey] : null;

  if (!animationPath && !animationData) {
    return;
  }

  const options = {
    container: iconEl,
    renderer: 'svg',
    loop: true,
    autoplay: true,
    rendererSettings: {
      preserveAspectRatio: 'xMidYMid meet'
    }
  };

  if (animationData) {
    options.animationData = animationData;
  } else {
    options.path = animationPath;
  }

  try {
    lottie.loadAnimation(options);
  } catch (err) {
    console.warn('Why Us animation failed to load:', animationKey || animationPath, err);
  }
});

/* â”€â”€ Scroll reveal for new sections â”€â”€ */
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const delay = parseInt(entry.target.dataset.delay || '0', 10);
      setTimeout(() => entry.target.classList.add('visible'), delay);
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

/* â”€â”€ Contact form â”€â”€ */
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    if (contactForm.getAttribute('action')) {
      return;
    }

    e.preventDefault();
    const btn = contactForm.querySelector('.contact-submit');
    const original = btn.innerHTML;
    btn.textContent = 'Message Sent \u2713';
    btn.style.background = 'rgba(255,255,255,0.65)';
    btn.disabled = true;
    setTimeout(() => {
      btn.innerHTML = original;
      btn.style.background = '';
      btn.disabled = false;
      contactForm.reset();
    }, 3500);
  });
}

if (typeof lottie !== 'undefined' && document.getElementById('lottie-bg')) {
  lottie.loadAnimation({
    container: document.getElementById('lottie-bg'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: '/static/animations/hero-wireframe.json'
  });
}
