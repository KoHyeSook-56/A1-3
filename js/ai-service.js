/**
 * 쵸이셀코리아 (ChoiCell Korea) - AI 맞춤 두피/모발 진단 솔루션 스크립트
 * UX 플로우: 스텝별 문진 -> 유효성 검사 -> fetch('/api/recommend') -> 로딩 애니메이션 -> 결과 렌더링
 */

document.addEventListener('DOMContentLoaded', () => {
  const formSteps = document.querySelectorAll('.form-step');
  const stepItems = document.querySelectorAll('.step-item');
  const errorNotice = document.getElementById('error-notice');
  const errorText = document.getElementById('error-text');
  const loadingBox = document.getElementById('ai-loading-box');
  const resultWrap = document.getElementById('diagnosis-result-wrap');
  const formWrap = document.getElementById('diagnosis-form-wrap');
  const progressFill = document.querySelector('.loading-progress-fill');
  const loadingSubText = document.querySelector('.loading-text-sub');

  let currentStep = 1;
  let selectedScalpType = '';
  let selectedConcerns = [];
  let selectedAgeGroup = '30대';
  let dailyHabits = '1일 1회 저녁 샴푸';

  // 1. 라디오 카드 선택 처리 (Step 1: 두피 타입)
  const scalpCards = document.querySelectorAll('.scalp-option-card');
  scalpCards.forEach(card => {
    card.addEventListener('click', () => {
      scalpCards.forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      const radio = card.querySelector('input[type=\"radio\"]');
      if (radio) {
        radio.checked = true;
        selectedScalpType = radio.value;
      }
      hideError();
    });
  });

  // 2. 칩 체크박스 선택 처리 (Step 2: 주요 고민)
  const concernChips = document.querySelectorAll('.concern-chip');
  concernChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const checkbox = chip.querySelector('input[type=\"checkbox\"]');
      if (checkbox) {
        checkbox.checked = !checkbox.checked;
        chip.classList.toggle('selected', checkbox.checked);
        
        // 배열 업데이트
        selectedConcerns = Array.from(document.querySelectorAll('.concern-chip input[type=\"checkbox\"]:checked'))
                               .map(cb => cb.value);
      }
      hideError();
    });
  });

  // 3. 연령대 라디오 선택 (Step 3)
  const ageRadios = document.querySelectorAll('input[name=\"ageGroup\"]');
  ageRadios.forEach(radio => {
    radio.addEventListener('change', () => {
      if (radio.checked) selectedAgeGroup = radio.value;
    });
  });

  // 4. 에러 표시 & 숨기기 함수
  function showError(msg) {
    if (errorNotice && errorText) {
      errorText.textContent = msg;
      errorNotice.classList.add('visible');
      errorNotice.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } else {
      alert(msg);
    }
  }

  function hideError() {
    if (errorNotice) {
      errorNotice.classList.remove('visible');
    }
  }

  // 5. 스텝 전환 함수
  function updateStepView(stepNumber) {
    hideError();
    currentStep = stepNumber;

    formSteps.forEach(step => {
      step.classList.remove('active');
      if (parseInt(step.getAttribute('data-step')) === stepNumber) {
        step.classList.add('active');
      }
    });

    stepItems.forEach((item, idx) => {
      const stepIdx = idx + 1;
      item.classList.remove('active', 'completed');
      if (stepIdx === stepNumber) {
        item.classList.add('active');
      } else if (stepIdx < stepNumber) {
        item.classList.add('completed');
      }
    });

    window.scrollTo({ top: 200, behavior: 'smooth' });
  }

  // 다음 버튼 클릭들
  const btnNext1 = document.getElementById('btn-next-1');
  if (btnNext1) {
    btnNext1.addEventListener('click', () => {
      if (!selectedScalpType) {
        showError('두피 타입을 1가지 선택해 주세요.');
        return;
      }
      updateStepView(2);
    });
  }

  const btnNext2 = document.getElementById('btn-next-2');
  if (btnNext2) {
    btnNext2.addEventListener('click', () => {
      if (selectedConcerns.length === 0) {
        showError('현재 고민되는 두피/모발 증상을 최소 1개 이상 선택해 주세요.');
        return;
      }
      updateStepView(3);
    });
  }

  // 이전 버튼 클릭들
  const btnPrev2 = document.getElementById('btn-prev-2');
  if (btnPrev2) {
    btnPrev2.addEventListener('click', () => updateStepView(1));
  }

  const btnPrev3 = document.getElementById('btn-prev-3');
  if (btnPrev3) {
    btnPrev3.addEventListener('click', () => updateStepView(2));
  }

  // 6. AI 진단 제출 처리 (fetch /api/recommend)
  const submitBtn = document.getElementById('btn-submit-ai');
  if (submitBtn) {
    submitBtn.addEventListener('click', async (e) => {
      e.preventDefault();
      hideError();

      // 최종 유효성 검사
      if (!selectedScalpType) {
        showError('두피 타입이 선택되지 않았습니다. 1단계로 돌아가 선택해 주세요.');
        updateStepView(1);
        return;
      }
      if (selectedConcerns.length === 0) {
        showError('고민 증상이 선택되지 않았습니다. 2단계로 돌아가 선택해 주세요.');
        updateStepView(2);
        return;
      }

      const habitInput = document.getElementById('dailyHabits');
      const memoInput = document.getElementById('userMemo');
      const habitVal = habitInput ? habitInput.value : dailyHabits;
      const memoVal = memoInput ? memoInput.value : '';

      const requestPayload = {
        scalpType: selectedScalpType,
        mainConcerns: selectedConcerns,
        ageGroup: selectedAgeGroup,
        dailyHabits: habitVal,
        memo: memoVal
      };

      // 폼 숨기고 로딩 인디케이터 활성화
      if (formWrap) formWrap.style.display = 'none';
      if (loadingBox) loadingBox.classList.add('active');

      // 로딩 진행바 애니메이션
      runLoadingSequence();

      try {
        const response = await fetch('/api/recommend', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestPayload)
        });

        if (!response.ok) {
          const errData = await response.json().catch(() => ({}));
          throw new Error(errData.error || `서버 응답 오류 (상태 코드: ${response.status})`);
        }

        const data = await response.json();
        
        // 1.5초 후 결과 표시
        setTimeout(() => {
          if (loadingBox) loadingBox.classList.remove('active');
          renderDiagnosisResult(data.data || data);
        }, 1500);

      } catch (err) {
        console.error('AI Diagnosis API Error:', err);
        // 에러 발생 시 알림 표시 후 폼 복구
        if (loadingBox) loadingBox.classList.remove('active');
        if (formWrap) formWrap.style.display = 'block';
        showError(`AI 진단 요청 중 오류가 발생했습니다: ${err.message}. 잠시 후 다시 시도해 주세요.`);
      }
    });
  }

  // 로딩 단계 텍스트 전환
  function runLoadingSequence() {
    let progress = 0;
    if (progressFill) progressFill.style.width = '0%';
    
    const messages = [
      '고객님의 두피 유형 및 고민 패턴을 분석 중입니다...',
      '쵸이셀 엑소좀 & 줄기세포 바이오 적합도를 계산 중입니다...',
      '1:1 맞춤형 3단계 두피 케어 솔루션을 처방 중입니다...',
      '두피 건강 리포트 작성이 완료되었습니다!'
    ];

    let msgIdx = 0;
    const interval = setInterval(() => {
      progress += 25;
      if (progressFill) progressFill.style.width = `${progress}%`;
      if (loadingSubText && messages[msgIdx]) {
        loadingSubText.textContent = messages[msgIdx];
        msgIdx++;
      }
      if (progress >= 100) {
        clearInterval(interval);
      }
    }, 400);
  }

  // 7. 결과 렌더링 함수
  function renderDiagnosisResult(result) {
    if (!resultWrap) return;
    resultWrap.classList.add('active');

    // 1) 점수 애니메이션
    const scoreValEl = document.getElementById('res-score-value');
    const targetScore = result.healthScore || 75;
    if (scoreValEl) {
      animateCounter(scoreValEl, 0, targetScore, 1000);
    }

    // 2) 두피 유형 & 요약
    const scalpTypeEl = document.getElementById('res-scalp-type');
    const summaryEl = document.getElementById('res-analysis-summary');
    if (scalpTypeEl) scalpTypeEl.textContent = result.scalpTypeKorean || '맞춤 바이오 진단형';
    if (summaryEl) summaryEl.textContent = result.analysisSummary || '분석이 완료되었습니다.';

    // 3) 3단계 루틴
    const routineContainer = document.getElementById('res-routine-timeline');
    if (routineContainer && result.routines) {
      routineContainer.innerHTML = result.routines.map(r => 
        `<div class="routine-card">
          <div class="routine-step-badge">${r.step}</div>
          <div class="routine-body">
            <h4>${r.title}</h4>
            <p>${r.description}</p>
            <span class="routine-usage"><i class="fa-solid fa-circle-check"></i> ${r.usage}</span>
          </div>
        </div>`
      ).join('');
    }

    // 4) 추천 제품 리스트
    const prodContainer = document.getElementById('res-products-grid');
    if (prodContainer && result.recommendedProducts) {
      prodContainer.innerHTML = result.recommendedProducts.map(p => 
        `<div class="result-product-card">
          <img src="${p.image}" alt="${p.name}">
          <div class="result-product-name">${p.name}</div>
          <div class="result-product-price">${p.price}</div>
          <a href="${p.link}" target="_blank" class="btn-buy"><i class="fa-solid fa-bag-shopping"></i> 구매하기</a>
        </div>`
      ).join('');
    }

    // 5) 생활 습관 팁
    const tipsContainer = document.getElementById('res-lifestyle-tips');
    if (tipsContainer && result.lifestyleTips) {
      tipsContainer.innerHTML = result.lifestyleTips.map(t => 
        `<li><i class="fa-solid fa-circle-check"></i> ${t}</li>`
      ).join('');
    }

    // 6) 연구원 소견
    const commentEl = document.getElementById('res-specialist-comment');
    if (commentEl && result.specialistComment) {
      commentEl.textContent = result.specialistComment;
    }

    // 로컬 스토리지에 결과 저장
    localStorage.setItem('choicell_last_diagnosis', JSON.stringify(result));

    resultWrap.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // 숫자 카운트업
  function animateCounter(el, start, end, duration) {
    let startTime = null;
    function step(currentTime) {
      if (!startTime) startTime = currentTime;
      const progress = Math.min((currentTime - startTime) / duration, 1);
      el.textContent = Math.floor(progress * (end - start) + start);
      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    }
    window.requestAnimationFrame(step);
  }

  // 8. 결과 화면 액션 버튼
  const btnRestart = document.getElementById('btn-restart-diagnosis');
  if (btnRestart) {
    btnRestart.addEventListener('click', () => {
      if (resultWrap) resultWrap.classList.remove('active');
      if (formWrap) formWrap.style.display = 'block';
      updateStepView(1);
    });
  }

  const btnCopyResult = document.getElementById('btn-copy-result');
  if (btnCopyResult) {
    btnCopyResult.addEventListener('click', () => {
      const summaryText = document.getElementById('res-analysis-summary')?.textContent || '';
      const score = document.getElementById('res-score-value')?.textContent || '';
      const shareText = `[쵸이셀코리아 AI 두피 진단 결과]\n두피 건강 점수: ${score}점\n진단 내용: ${summaryText}\n홈페이지: https://www.choicellkorea.co.kr/`;

      navigator.clipboard.writeText(shareText).then(() => {
        alert('진단 결과가 클립보드에 복사되었습니다. 카카오톡이나 메모장에 공유해 보세요!');
      }).catch(() => {
        alert('클립보드 복사에 실패했습니다.');
      });
    });
  }

  const btnPrintResult = document.getElementById('btn-print-result');
  if (btnPrintResult) {
    btnPrintResult.addEventListener('click', () => {
      window.print();
    });
  }
});
