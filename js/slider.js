/**
 * 쵸이셀코리아 (ChoiCell Korea) - Main Visual Slider
 */

document.addEventListener('DOMContentLoaded', () => {
  const slides = document.querySelectorAll('.visual-slide .slide-item');
  if (!slides || slides.length === 0) return;

  const currentNumEl = document.querySelector('.visual-pager .current');
  const totalNumEl = document.querySelector('.visual-pager .total');
  const progressFill = document.querySelector('.visual-pager .progress span');
  const prevBtn = document.querySelector('.visual-controls .prev');
  const nextBtn = document.querySelector('.visual-controls .next');
  const pauseBtn = document.querySelector('.visual-pager .pause-btn');

  let currentIndex = 0;
  let isPlaying = true;
  let slideInterval = null;
  const slideDuration = 6000; // 6초

  // 총 슬라이드 수 표시
  if (totalNumEl) {
    totalNumEl.textContent = String(slides.length).padStart(2, '0');
  }

  function goToSlide(index) {
    slides.forEach((s, idx) => {
      s.classList.toggle('active', idx === index);
    });

    currentIndex = index;
    if (currentNumEl) {
      currentNumEl.textContent = String(currentIndex + 1).padStart(2, '0');
    }

    resetProgress();
  }

  function nextSlide() {
    const nextIdx = (currentIndex + 1) % slides.length;
    goToSlide(nextIdx);
  }

  function prevSlide() {
    const prevIdx = (currentIndex - 1 + slides.length) % slides.length;
    goToSlide(prevIdx);
  }

  function resetProgress() {
    if (!progressFill) return;
    progressFill.style.transition = 'none';
    progressFill.style.width = '0%';

    if (isPlaying) {
      setTimeout(() => {
        progressFill.style.transition = `width ${slideDuration}ms linear`;
        progressFill.style.width = '100%';
      }, 50);
    }
  }

  function startAutoPlay() {
    stopAutoPlay();
    isPlaying = true;
    resetProgress();
    slideInterval = setInterval(nextSlide, slideDuration);
    if (pauseBtn) {
      pauseBtn.innerHTML = '<i class=\"fa-solid fa-pause\"></i>';
    }
  }

  function stopAutoPlay() {
    isPlaying = false;
    if (slideInterval) {
      clearInterval(slideInterval);
      slideInterval = null;
    }
    if (progressFill) {
      progressFill.style.width = '0%';
    }
    if (pauseBtn) {
      pauseBtn.innerHTML = '<i class=\"fa-solid fa-play\"></i>';
    }
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      nextSlide();
      if (isPlaying) startAutoPlay();
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      prevSlide();
      if (isPlaying) startAutoPlay();
    });
  }

  if (pauseBtn) {
    pauseBtn.addEventListener('click', () => {
      if (isPlaying) {
        stopAutoPlay();
      } else {
        startAutoPlay();
      }
    });
  }

  // 초기 슬라이드 구동
  goToSlide(0);
  startAutoPlay();
});
