# 쵸이셀코리아 (ChoiCell Korea) AI 맞춤 두피 케어 서비스

AI 기술을 활용하여 사용자의 두피 상태와 라이프스타일에 맞춘 1:1 맞춤형 두피/모발 케어 솔루션을 제공하는 웹 서비스입니다.

## 배포 URL (Vercel)
- [배포 링크 입력란 - Vercel 배포 후 업데이트]

## 주요 기능
- **AI 두피 맞춤 진단**: 두피 타입, 고민 증상, 연령대, 생활 습관 등을 입력하면 Google Gemini API를 활용하여 전문적인 분석과 맞춤 3단계 케어 루틴, 추천 제품을 제안합니다.
- **반응형 웹 디자인**: 데스크톱, 태블릿, 모바일 기기에서 최적화된 화면을 제공합니다. (바닐라 CSS/JS 사용)
- **에러 핸들링**: 폼 필수값 누락 검증, API 호출 실패 및 지연 시 사용자 안내 메시지를 표시합니다. API 키 미설정 시 Fallback 로직이 동작하여 기본 진단 결과를 반환합니다.

## 기술 스택
- **Frontend**: HTML5, Vanilla CSS3, Vanilla JavaScript (프레임워크 미사용)
- **Backend**: Python 3.9+ (Vercel Serverless Functions)
- **AI Integration**: Google Gemini API (`gemini-1.5-flash` 모델)
- **Deployment**: Vercel 연동 배포

## 폴더 구조
```
├── index.html            # 메인 페이지
├── introduce.html        # 회사 소개 페이지
├── ai-diagnosis.html     # AI 맞춤 진단 페이지 (기능 구현 핵심)
├── css/                  # 스타일시트 (style.css, responsive.css, ai-diagnosis.css)
├── js/                   # 자바스크립트 로직 (ai-service.js 등)
├── api/                  # Python 서버리스 함수 
│   ├── recommend.py      # AI API 호출 및 진단 로직 (POST /api/recommend)
│   ├── contact.py        # 문의 접수 API
│   └── requirements.txt  # Python 의존성 패키지
├── vercel.json           # Vercel 배포 설정
└── README.md             # 프로젝트 설명 (현재 파일)
```

## 실행 및 테스트 방법 (로컬)
1. 파이썬이 설치된 환경에서 레포지토리를 클론합니다.
2. `api/requirements.txt`에 명시된 패키지를 설치합니다.
3. 터미널을 열고 프로젝트 루트 경로에서 로컬 웹 서버를 실행합니다.
   `python -m http.server 3000`
4. 새로운 터미널을 열고 `api/` 폴더 내의 API 서버(로컬 테스트용 내장 모드)를 실행합니다.
   `cd api && python recommend.py` (기본 8000 포트로 실행됨)
   > 주의: 로컬 환경에서는 `js/ai-service.js` 내부의 `fetch('/api/recommend')` 경로를 `http://localhost:8000/api/recommend`로 일시 변경해야 테스트 가능합니다. Vercel 배포 환경에서는 상대 경로로 정상 동작합니다.

## 환경 변수 설정 (Vercel)
안전한 AI 호출을 위해 Gemini API 키는 프론트엔드 코드에 노출하지 않고 서버(환경변수)에서 관리합니다.

1. Vercel 프로젝트 대시보드 접속 -> `Settings` -> `Environment Variables`
2. 아래의 키를 추가합니다.
   - Key: `GEMINI_API_KEY`
   - Value: (발급받은 Google Gemini API 키)
3. 환경변수 추가 후 Vercel에서 재배포(Redeploy)를 진행해야 적용됩니다.
