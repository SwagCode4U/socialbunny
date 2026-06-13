

Phase 1 : Super Admin Login (session1)

Super_Admin = Hani, Misbah, Zeel

1. Mysql -- DB                                                      --> Workbench
2. utils.py ---> hash_password() + verify_password() with bcrypt    ---> Hani@9090 turn into $746267832867dsjhgdsd
3. utils.py — create_access_token() with JWT 30min expiry           ---> Decode the JWT on https://jwt.io and see {"sub":"1","exp":...} JWT 30min expiry
4. admin_routes.py — POST /api/admin/login    ---> curl test: 

--------------------------------------------------





5. seed_admins.py — insert Hani, Zeel, Misbah       
6. SuperAdminLogin.jsx + AdminDashboard.jsx

