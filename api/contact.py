# -*- coding: utf-8 -*-
"""
쵸이셀코리아(ChoiCell Korea) 온라인 상담 및 가맹 문의 접수 API
Vercel Serverless Function (Python 3.9+)
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from datetime import datetime


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
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._send_cors_headers()
        self.end_headers()
        res = {
            "status": "online",
            "service": "ChoiCell Korea Contact API",
            "version": "1.0.0"
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
                "error": "요청 데이터가 없습니다.",
                "code": "EMPTY_BODY"
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
                "error": "JSON 파싱 오류",
                "code": "INVALID_JSON"
            }
            self.wfile.write(json.dumps(err_res, ensure_ascii=False).encode("utf-8"))
            return

        name = body.get("name", "").strip()
        phone = body.get("phone", "").strip()
        category = body.get("category", "제품상담").strip()
        message = body.get("message", "").strip()

        if not name or not phone:
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._send_cors_headers()
            self.end_headers()
            err_res = {
                "success": False,
                "error": "성함과 연락처는 필수 입력 항목입니다.",
                "code": "MISSING_FIELDS"
            }
            self.wfile.write(json.dumps(err_res, ensure_ascii=False).encode("utf-8"))
            return

        # 성공 응답 (실제 배포 환경에서는 이메일/DB/웹훅 연동 가능)
        receipt_id = f"CCK-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        res_data = {
            "success": True,
            "receiptId": receipt_id,
            "message": "상담 문의가 성공적으로 접수되었습니다. 전문 상담원이 빠른 시일 내에 연락드리겠습니다.",
            "data": {
                "name": name,
                "phone": phone,
                "category": category,
                "receivedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(res_data, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    from http.server import HTTPServer
    port = int(os.environ.get("PORT", 8001))
    server = HTTPServer(("0.0.0.0", port), handler)
    print(f"[*] 쵸이셀코리아 상담 접수 API 서버 실행 중: http://localhost:{port}/api/contact")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
