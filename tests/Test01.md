



# ── 1. Root ──────────────────────────────────────────
curl http://127.0.0.1:8000/


# ── 2. News (Misbah) ─────────────────────────────────
curl 'http://127.0.0.1:8000/api/news/?offset=0&limit=3'


# ── 3. Topics (Hani) ─────────────────────────────────
curl -X POST http://127.0.0.1:8000/api/topics/ \
  -H 'Content-Type: application/json' \
  -d '{"title":"My Topic","content":"Line 1\nLine 2","author":"Hani"}'
curl 'http://127.0.0.1:8000/api/topics/?offset=0&limit=10'
curl http://127.0.0.1:8000/api/topics/1



# ── 4. Referral Lookup (Zeel) ────────────────────────
curl http://127.0.0.1:8000/api/referral/lookup/ha8080k
curl http://127.0.0.1:8000/api/referral/lookup/ze7070r




# ── 5. Admin Login + Friends (Zeel) ──────────────────

ADMIN_TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/admin/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"hani2902","password":"Hani203040@#"}' \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')
curl http://127.0.0.1:8000/api/admin/me \
  -H "Authorization: Bearer $ADMIN_TOKEN"
curl http://127.0.0.1:8000/api/admin/1/friends \
  -H "Authorization: Bearer $ADMIN_TOKEN"




# ── 6. Wizard (needs test JWT — uses gen_test_jwt.py) ─
TEST_JWT=$(cd backend && python gen_test_jwt.py 1)
curl -X POST http://127.0.0.1:8000/api/auth/wizard \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $TEST_JWT" \
  -d '{"name":"John","phone":"9876543210","interest":"React","referred_by_id":2}'



# ── 7. Google OAuth (needs GOOGLE_CLIENT_ID in .env) ──
# curl -X POST http://127.0.0.1:8000/api/auth/google \
#   -H 'Content-Type: application/json' \
#   -d '{"id_token":"<REAL_GOOGLE_ID_TOKEN>"}'