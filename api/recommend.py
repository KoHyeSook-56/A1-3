"""AI scalp diagnosis endpoint for Vercel: POST /api/recommend."""

import json
import os
import sys
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()


def diagnosis(scalp_type, concerns, age_group, daily_habits, memo):
    labels = {
        "oily": "지성 / 과다 피지형 두피",
        "dry": "건성 / 수분 부족형 두피",
        "sensitive": "민감성 / 자극 반응형 두피",
        "hairLoss": "탈모 진행 / 모근 약화형 두피",
        "complex": "복합성 / 두피 불균형형 두피",
    }
    scalp_label = labels.get(scalp_type, "복합성 두피")
    score = max(35, min(90, 78 - len(concerns) * 8))
    summary = f"현재 두피 상태는 {scalp_label}으로 분석됩니다. 선택한 고민을 기준으로 수분·유분 균형과 두피 자극을 함께 관리하는 루틴을 권장합니다."
    if memo:
        summary += f" 전달해 주신 내용({memo})도 관리 방향에 반영했습니다."

    return {
        "scalpTypeKorean": scalp_label,
        "healthScore": score,
        "analysisSummary": summary,
        "ageGroup": age_group or "미입력",
        "concerns": concerns,
        "routines": [
            {"step": "STEP 1. 두피 세정", "title": "저자극 샴푸", "description": "미온수로 두피와 모발의 노폐물을 부드럽게 세정합니다.", "usage": "주 3~7회, 2~3분간 마사지 후 충분히 헹궈 주세요."},
            {"step": "STEP 2. 영양 관리", "title": "두피 영양 앰플", "description": "두피에 수분과 영양을 공급해 컨디션 회복을 돕습니다.", "usage": "샴푸 후 물기를 제거한 뒤 두피에 고르게 도포하세요."},
            {"step": "STEP 3. 모발 보호", "title": "모발 보호 트리트먼트", "description": "손상된 모발 표면을 보호하고 건조함을 줄입니다.", "usage": "모발 중간부터 끝까지 바른 뒤 2~3분 후 헹궈 주세요."},
        ],
        "recommendedProducts": [
            {"name": "두피 영양 앰플", "category": "두피 케어", "price": "60,000원", "image": "https://www.choicellkorea.co.kr/theme/choicell/img/main_pro_01.jpg", "link": "#", "tag": "추천"},
            {"name": "저자극 샴푸", "category": "데일리 클렌징", "price": "55,000원", "image": "https://www.choicellkorea.co.kr/theme/choicell/img/main_pro_02.jpg", "link": "#", "tag": "추천"},
            {"name": "모발 보호 트리트먼트", "category": "보습·영양", "price": "66,000원", "image": "https://www.choicellkorea.co.kr/theme/choicell/img/main_pro_03.jpg", "link": "#", "tag": "강화"},
        ],
        "lifestyleTips": ["미온수로 샴푸하고 두피를 완전히 말려 주세요.", "주 1~2회 두피 마사지를 병행해 보세요.", "수면과 수분 섭취를 꾸준히 관리해 주세요."],
        "specialistComment": "3주간 권장 루틴을 유지한 뒤 두피 상태 변화를 확인해 보세요.",
    }


def call_gemini(payload):
    """Use Gemini when configured; safely fall back when it is unavailable."""
    if not GEMINI_API_KEY:
        return None
    prompt = "Return only JSON for a Korean scalp-care report with scalpTypeKorean, healthScore, analysisSummary, routines, lifestyleTips, specialistComment."
    request_body = {"contents": [{"parts": [{"text": f"{prompt}\nInput: {json.dumps(payload, ensure_ascii=False)}"}]}], "generationConfig": {"response_mime_type": "application/json"}}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    try:
        request = urllib.request.Request(url, data=json.dumps(request_body).encode(), headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(request, timeout=15) as response:
            text = json.loads(response.read().decode())["candidates"][0]["content"]["parts"][0]["text"]
            result = json.loads(text.removeprefix("```json").removeprefix("```").removesuffix("```").strip())
            return result
    except (urllib.error.URLError, KeyError, IndexError, json.JSONDecodeError, TimeoutError) as error:
        print(f"Gemini request failed; returning local diagnosis: {error}", file=sys.stderr)
        return None


class handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_json(200, {"status": "ok"})

    def do_GET(self):
        self.send_json(200, {"status": "online", "service": "ChoiCell Korea AI diagnosis API"})

    def do_POST(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode("utf-8"))
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
            self.send_json(400, {"success": False, "error": "올바른 JSON 요청이 필요합니다."})
            return
        scalp_type = str(body.get("scalpType", "")).strip()
        concerns = body.get("mainConcerns", [])
        if not scalp_type or not isinstance(concerns, list) or not concerns:
            self.send_json(400, {"success": False, "error": "두피 유형과 주요 고민을 입력해 주세요."})
            return
        result = call_gemini(body) or diagnosis(scalp_type, concerns, str(body.get("ageGroup", "")), str(body.get("dailyHabits", "")), str(body.get("memo", "")).strip())
        result["ageGroup"] = str(body.get("ageGroup", ""))
        result["concerns"] = concerns
        self.send_json(200, {"success": True, "mode": "Gemini" if GEMINI_API_KEY else "Local", "data": result})
