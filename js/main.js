/**
 * 쵸이셀코리아 (ChoiCell Korea) - Main JavaScript
 * 공통 UI 인터랙션, 모바일 네비게이션, 모달 팝업, 테마 토글
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. 헤더 스크롤 효과
  const header = document.getElementById('header');
  const scrollToTopBtn = document.querySelector('.scroll-to-top');

  window.addEventListener('scroll', () => {
    const scrollPos = window.scrollY || window.pageYOffset;
    if (header) {
      if (scrollPos > 40) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    }

    if (scrollToTopBtn) {
      if (scrollPos > 300) {
        scrollToTopBtn.classList.add('visible');
      } else {
        scrollToTopBtn.classList.remove('visible');
      }
    }
  });

  // 상단으로 이동 클릭
  if (scrollToTopBtn) {
    scrollToTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // 2. 모바일 메뉴 (햄버거 & 드로어)
  const menuBtn = document.querySelector('.m-menu-btn');
  const drawer = document.querySelector('.m-gnb-drawer');
  const drawerClose = document.querySelector('.m-drawer-close');
  const drawerOverlay = document.querySelector('.m-drawer-overlay');

  function openDrawer() {
    if (drawer) drawer.classList.add('open');
    if (drawerOverlay) drawerOverlay.style.display = 'block';
    document.body.style.overflow = 'hidden';
  }

  function closeDrawer() {
    if (drawer) drawer.classList.remove('open');
    if (drawerOverlay) drawerOverlay.style.display = 'none';
    document.body.style.overflow = '';
  }

  if (menuBtn) menuBtn.addEventListener('click', openDrawer);
  if (drawerClose) drawerClose.addEventListener('click', closeDrawer);
  if (drawerOverlay) drawerOverlay.addEventListener('click', closeDrawer);

  // 3. 다크 모드 토글 (보너스 과제)
  const themeToggleBtn = document.querySelector('.theme-toggle-btn');
  const savedTheme = localStorage.getItem('choicell_theme');

  if (savedTheme === 'dark') {
    document.body.classList.add('dark-mode');
    if (themeToggleBtn) themeToggleBtn.innerHTML = '<i class=\"fa-solid fa-sun\"></i>';
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      document.body.classList.toggle('dark-mode');
      const isDark = document.body.classList.contains('dark-mode');
      localStorage.setItem('choicell_theme', isDark ? 'dark' : 'light');
      themeToggleBtn.innerHTML = isDark ? '<i class=\"fa-solid fa-sun\"></i>' : '<i class=\"fa-solid fa-moon\"></i>';
    });
  }

  // 4. 모달 팝업 (개인정보처리방침, 이메일무단수집거부 등)
  const policyBtns = document.querySelectorAll('.open-policy');
  const popupOverlay = document.querySelector('.footer-popup-overlay');
  const popupCloseBtns = document.querySelectorAll('.fp-close');

  policyBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = btn.getAttribute('data-target');
      const targetPopup = document.getElementById(targetId);
      if (targetPopup && popupOverlay) {
        popupOverlay.style.display = 'block';
        targetPopup.style.display = 'flex';
      }
    });
  });

  function closeAllPopups() {
    if (popupOverlay) popupOverlay.style.display = 'none';
    document.querySelectorAll('.footer-popup').forEach(p => {
      p.style.display = 'none';
    });
  }

  popupCloseBtns.forEach(btn => btn.addEventListener('click', closeAllPopups));
  if (popupOverlay) popupOverlay.addEventListener('click', closeAllPopups);

  // 5. FAQ 아코디언
  const faqItems = document.querySelectorAll('.faq-accordion-item');
  faqItems.forEach(item => {
    const header = item.querySelector('.faq-q');
    if (header) {
      header.addEventListener('click', () => {
        const isOpen = item.classList.contains('open');
        faqItems.forEach(i => i.classList.remove('open'));
        if (!isOpen) {
          item.classList.add('open');
        }
      });
    }
  });
});
