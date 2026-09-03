# -*- coding: utf-8 -*-
"""
쵸이셀코리아(ChoiCell Korea) AI 맞춤 두피/모발 진단 및 솔루션 추천 API
Vercel Serverless Function (Python 3.9+)
"""

import json
import os
import sys
import re
from http.server import BaseHTTPRequestHandler

# 환경 변수로부터 API 키 로드
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()


def generate_fallback_diagnosis(scalp_type, main_concerns, age_group, daily_habits, memo):
    """
    API 키가 없거나 외부 AI 호출 실패 시 작동하는 쵸이셀 바이오 임상 진단 알고리즘 엔진
    """
    scalp_names = {
        "oily": "지성 / 과다 피지 분비형 두피",
        "dry": "건성 / 수분 부족 각질형 두피",
        "sensitive": "민감성 / 붉은기 & 트러블형 두피",
        "hairLoss": "탈모 진행 / 모근 약화형 두피",
        "complex": "복합성 / 두피열 & 불균형 두피"
    }
    
    scalp_korean = scalp_names.get(scalp_type, "복합성 두피")
    concerns_str = ", ".join(main_concerns) if isinstance(main_concerns, list) else str(main_concerns)
    
    # 건강 지수 계산 (고민 개수와 타입 기반)
    base_score = 78
    concern_count = len(main_concerns) if isinstance(main_concerns, list) else 1
    health_score = max(35, min(90, base_score - (concern_count * 8)))
    
    # 맞춤 진단 분석 텍스트 생성
    analysis_text = f"현재 고객님의 두피 상태는 [{scalp_korean}]로 분석되었습니다. "
    if "탈모" in concerns_str or scalp_type == "hairLoss":
        analysis_text += "모주기 단축과 모근 영양 불균형으로 인해 모발 탈락 및 연모화가 진행될 위험이 있습니다. 모낭 디톡스와 엑소좀 영양 공급이 시급합니다."
    elif "지성" in scalp_korean or "비듬" in concerns_str:
        analysis_text += "과다 피지와 산화된 노폐물이 모공을 막아 모낭 염증 및 가려움증을 유발하고 있습니다. 딥스케일링과 유수분 밸런싱이 핵심입니다."
    elif "민감성" in scalp_korean or "가려움" in concerns_str:
        analysis_text += "두피 장벽이 약화되어 외부 자극에 민감하게 반응하고 열감이 누적된 상태입니다. 저자극 진정과 두피 쿨링 케어가 필요합니다."
    else:
        analysis_text += "수분 부족으로 인한 두피 당김과 각질 탈락 주기가 무너져 있습니다. 천연 보습 인자 공급과 두피 유연화가 필요합니다."
        
    if memo:
        analysis_text += f" (추가 전달 사항: '{memo}'에 대한 맞춤 바이오 처방이 함께 반영되었습니다.)"

    # 3단계 케어 루틴 구성
    routines = [
        {
            "step": "STEP 1. 두피 디톡스 & 모공 딥클렌징",
            "title": "쵸이셀 올인원 스칼프 샴푸 (500ml)",
            "description": "미세 거품이 묵은 각질과 피지 산화물을 자극 없이 배출시키며, 특허 생약 추출물이 두피열을 즉각 낮춰줍니다.",
            "usage": "미온수로 두피를 충분히 적신 후 3분간 두피 마사지 후 깨끗이 헹구어 냅니다."
        },
        {
            "step": "STEP 2. 모근 집중 영양 & 두피 재생",
            "title": "쵸이셀 두피스캘프 젤크림 (220ml)",
            "description": "줄기세포 배양액 및 엑소좀 활성 펩타이드가 모낭 깊숙이 침투하여 모근을 단단하게 고정하고 탄력을 부여합니다.",
            "usage": "샴푸 후 타월 드라이한 두피에 골고루 도포한 뒤 손끝으로 가볍게 두드려 흡수시킵니다."
        },
        {
            "step": "STEP 3. 모발 큐티클 단백질 코팅 & 볼륨 케어",
            "title": "쵸이셀 바이오 헤어트리트먼트 (500ml)",
            "description": "손상된 모발 큐티클에 고농축 단백질과 세라마이드 보호막을 형성하여 끊어짐을 예방하고 윤기 있는 볼륨을 선사합니다.",
            "usage": "모발 끝을 중심으로 도포 후 2~3분 방치 후 가볍게 헹구어 냅니다."
        }
    ]

    # 추천 제품 리스트
    recommended_products = [
        {
            "name": "쵸이셀 두피스캘프 젤크림 (220ml)",
            "category": "스칼프 케어 / 탈모 완화",
            "price": "60,000원",
            "image": "https://www.choicellkorea.co.kr/theme/choicell/img/main_pro_01.jpg",
            "link": "https://smartstore.naver.com/choicellbeauty/products/4884579788",
            "tag": "베스트셀러"
        },
        {
            "name": "쵸이셀 올인원 샴푸 (500ml)",
            "category": "데일리 딥클렌징",
            "price": "55,000원",
            "image": "https://www.choicellkorea.co.kr/theme/choicell/img/main_pro_02.jpg",
            "link": "https://smartstore.naver.com/choicellbeauty/products/4880979382",
            "tag": "추천"
        },
        {
            "name": "쵸이셀 바이오 헤어트리트먼트 (500ml)",
            "category": "단백질 영양 공급",
            "price": "66,000원",
            "image": "https://www.choicellkorea.co.kr/theme/choicell/img/main_pro_03.jpg",
            "link": "https://smartstore.naver.com/choicellbeauty/products/4884626386",
            "tag": "모발 강화"
        }
    ]

    # 생활 습관 솔루션
    lifestyle_tips = [
        "샴푸는 가급적 저녁에 진행하여 하루 동안 쌓인 미세먼지와 산화 피지를 완벽히 세정하세요.",
        "드라이 시 뜨거운 바람 대신 미온풍 또는 냉풍으로 두피 속까지 100% 바짝 건조해 주세요.",
        "주 2회 쵸이셀 두피스캘프 젤크림으로 정수리 림프 순환 마사지를 5분간 병행하세요."
    ]

    return {
        "success": True,
        "mode": "Bio-Clinical-Engine",
        "data": {
            "scalpTypeKorean": scalp_korean,
            "healthScore": health_score,
            "analysisSummary": analysis_text,
            "ageGroup": age_group or "전 연령",
            "concerns": main_concerns,
            "routines": routines,
            "recommendedProducts": recommended_products,
            "lifestyleTips": lifestyle_tips,
            "specialistComment": "쵸이셀코리아 바이오 융합 연구소에서는 고객님의 두피 환경 개선을 위해 3주간의 홈케어 루틴 실천을 권장합니다."
        }
    }


def call_gemini_api(scalp_type, main_concerns, age_group, daily_habits, memo):
    """
    Google Gemini API 호출 함수 (GEMINI_API_KEY 설정 시)
    """
    import urllib.request
    import urllib.error

    system_prompt = (
        "당신은 프리미엄 바이오 두피/모발 웰니스 기업 '쵸이셀코리아(ChoiCell Korea)'의 수석 바이오 연구원입니다. "
        "사용자의 두피 타입, 고민 증상, 연령대, 생활 습관 정보를 바탕으로 전문적이고 신뢰감 있는 두피 진단 리포트를 작성하세요. "
        "반드시 순수한 JSON 형식으로만 응답해야 하며, 아래 키를 포함해야 합니다:\n"
        "{\n"
        '  "scalpTypeKorean": "지성 / 과다 피지 분비형 두피",\n'
        '  "healthScore": 65,\n'
        '  "analysisSummary": "두피 상태 정밀 분석 요약 문장...",\n'
        '  "routines": [\n'
        '    {"step": "STEP 1. 두피 디톡스", "title": "쵸이셀 올인원 샴푸 (500ml)", "description": "...", "usage": "..."},\n'
        '    {"step": "STEP 2. 모근 집중 영양", "title": "쵸이셀 두피스캘프 젤크림 (220ml)", "description": "...", "usage": "..."},\n'
        '    {"step": "STEP 3. 단백질 코팅", "title": "쵸이셀 헤어트리트먼트 (500ml)", "description": "...", "usage": "..."}\n'
        "  ],\n"
        '  "lifestyleTips": ["팁1", "팁2", "팁3"],\n'
        '  "specialistComment": "연구원 맞춤 소견..."\n'
        "}"
    )

    user_content = (
        f"[시스템 지시사항]\n{system_prompt}\n\n"
        f"[사용자 입력 정보]\n"
        f"두피타입: {scalp_type}, 주요고민: {main_concerns}, "
        f"연령대: {age_group}, 습관: {daily_habits}, 메모: {memo}"
    )

    req_body = {
        "contents": [{
            "parts": [{"text": user_content}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "response_mime_type": "application/json"
        }
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    req = urllib.request.Request(
        url,
        data=json.dumps(req_body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            content = res_data["candidates"][0]["content"]["parts"][0]["text"]
            
            # Markdown JSON block 제거 (경우에 따라 gemini가 렌더링할 때 발생 가능)
            if content.startswith("```json"):
                content = content.strip()[7:-3]
            elif content.startswith("```"):
                content = content.strip()[3:-3]
                
            parsed_json = json.loads(content)
            
            # 제품 리스트 추가
            parsed_json["ageGroup"] = age_group
            parsed_json["concerns"] = main_concerns
            parsed_json["recommendedProducts"] = [
                {
                    "name": "쵸이셀 두피스캘프 젤크림 (220ml)",
                    "category": "스칼프 케어 / 탈모 완화",
                    "price": "60,000원",
                    "image": "https://www.choicellkorea.co.kr/theme/choicell/img/main_pro_01.jpg",
                    "link": "https://smartstore.naver.com/choicellbeauty/products/4884579788",
                    "tag": "베스트셀러"
                },
                {
                    "name": "쵸이셀 올인원 샴푸 (500ml)",
                    "category": "데일리 딥클렌징",
                    "price": "55,000원",
                    "image": "https://www.choicellkorea.co.kr/theme/choicell/img/main_pro_02.jpg",
                    "link": "https://smartstore.naver.com/choicellbeauty/products/4880979382",
                    "tag": "추천"
                },
                {
                    "name": "쵸이셀 바이오 헤어트리트먼트 (500ml)",
                    "category": "단백질 영양 공급",
                    "price": "66,000원",
                    "image": "https://www.choicellkorea.co.kr/theme/choicell/img/main_pro_03.jpg",
                    "link": "https://smartstore.naver.com/choicellbeauty/products/4884626386",
                    "tag": "모발 강화"
                }
            ]
            
            return {
                "success": True,
                "mode": "Gemini-1.5-Flash",
                "data": parsed_json
            }
    except Exception as e:
        print(f"[Gemini API Error] Fallback으로 전환합니다: {e}", file=sys.stderr)
        return generate_fallback_diagnosis(scalp_type, main_concerns, age_group, daily_habits, memo)


class handler(BaseHTTPRequestHandler):
    """
    Vercel Serverless Function Handler
    """
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        """헬스 체크 및 API 안내 엔드포인트"""
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._send_cors_headers()
        self.end_headers()
        res = {
            "status": "online",
            "service": "ChoiCell Korea AI Scalp & Hair Diagnosis API",
            "version": "1.0.0",
            "instructions": "POST /api/recommend with JSON body {scalpType, mainConcerns, ageGroup, ...}"
        }
        self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._send_cors_headers()
            self.end_headers()
            err_res = {
                "success": False,
                "error": "요청 본문(Body)이 비어 있습니다.",
                "code": "EMPTY_REQUEST_BODY"
            }
            self.wfile.write(json.dumps(err_res, ensure_ascii=False).encode("utf-8"))
            return

        try:
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data.decode("utf-8"))
        except Exception as e:
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._send_cors_headers()
            self.end_headers()
            err_res = {
                "success": False,
                "error": "잘못된 JSON 형식입니다.",
                "detail": str(e),
                "code": "INVALID_JSON"
            }
            self.wfile.write(json.dumps(err_res, ensure_ascii=False).encode("utf-8"))
            return

        # 필수값 검증
        scalp_type = body.get("scalpType", "").strip()
        main_concerns = body.get("mainConcerns", [])
        age_group = body.get("ageGroup", "").strip()
        daily_habits = body.get("dailyHabits", "")
        memo = body.get("memo", "").strip()

        # 빈값 예외 처리
        if not scalp_type or not main_concerns:
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._send_cors_headers()
            self.end_headers()
            err_res = {
                "success": False,
                "error": "필수 입력값(두피 타입, 주요 고민)이 누락되었습니다. 항목을 모두 선택해 주세요.",
                "code": "MISSING_REQUIRED_FIELDS"
            }
            self.wfile.write(json.dumps(err_res, ensure_ascii=False).encode("utf-8"))
            return

        # AI 진단 결과 생성
        if GEMINI_API_KEY:
            result = call_gemini_api(scalp_type, main_concerns, age_group, daily_habits, memo)
        else:
            result = generate_fallback_diagnosis(scalp_type, main_concerns, age_group, daily_habits, memo)

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))


# 로컬 테스트용 Standalone 서버 구동 지원
if __name__ == "__main__":
    from http.server import HTTPServer
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), handler)
    print(f"[*] 쵸이셀코리아 AI 진단 API 서버가 포트 {port}에서 실행 중입니다...")
    print(f"[*] 테스트 주소: http://localhost:{port}/api/recommend")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] 서버를 종료합니다.")
        server.server_close()
