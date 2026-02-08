# Email Service Tests

Test utilities for debugging and verifying the email service configuration.

## Files

### `check_config.py`
Displays the current SMTP configuration settings at runtime.

**Usage:**
```bash
python tests/check_config.py
```

**Shows:**
- SMTP host, port, user
- TLS/SSL settings
- EMAIL_TEST_MODE status

---

### `test_email_service.py`
Tests the email service directly (bypasses API layer).

**Usage:**
```bash
python tests/test_email_service.py
```

**Tests:**
- SMTP connection
- Direct email sending via email_service
- Configuration validation

---

### `test_email_curl.ps1`
PowerShell script to test the email API endpoint.

**Usage:**
```powershell
powershell -ExecutionPolicy Bypass -File tests/test_email_curl.ps1
```

**Tests:**
- Email API endpoint (`/api/v1/email/test-send`)
- Authentication with token
- Full API request/response cycle

---

## Notes

- These tests send real emails to `ric.seedoo@gmail.com`
- Ensure your `.env` file has correct SMTP credentials
- Set `EMAIL_TEST_MODE=true` in `.env` to simulate emails without sending
