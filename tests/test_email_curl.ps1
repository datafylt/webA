$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiaXNfc3VwZXJ1c2VyIjp0cnVlLCJleHAiOjE3NzExODAyMDV9.myUEkD_sy55l_85jjH8sXuKKDL9qk7Up2LUHA8Rcd48"

Write-Host "Testing email endpoint..." -ForegroundColor Yellow

$response = Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/v1/email/test-send?to_email=ric.seedoo@gmail.com" `
    -Method POST `
    -Headers @{ "token" = $token } `
    -ContentType "application/json"

Write-Host "Status Code: $($response.StatusCode)" -ForegroundColor Green
Write-Host "Response:" -ForegroundColor Cyan
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
