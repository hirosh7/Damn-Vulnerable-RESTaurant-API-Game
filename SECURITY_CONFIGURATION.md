# Security Configuration Guide

This document provides security configuration guidelines for deploying the Damn Vulnerable RESTaurant API securely.

## ⚠️ IMPORTANT SECURITY NOTICE

This application was originally designed with intentional vulnerabilities for educational purposes. The codebase has been hardened with security countermeasures. However, additional production-hardening is required before any real-world deployment.

## Required Configuration for Production

### 1. TLS/HTTPS Configuration (T21)

**CRITICAL:** Always use HTTPS in production. Never expose the API over plain HTTP.

#### Option A: Reverse Proxy (Recommended)
Use nginx or another reverse proxy to terminate TLS:

```nginx
server {
    listen 443 ssl http2;
    server_name api.restaurant.com;
    
    # TLS 1.3 only (or TLS 1.2 minimum)
    ssl_protocols TLSv1.3 TLSv1.2;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    
    # SSL certificate
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    location / {
        proxy_pass http://web:8091;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Option B: Uvicorn with TLS
```bash
uvicorn main:app --host 0.0.0.0 --port 8091 \
    --ssl-keyfile=/path/to/key.pem \
    --ssl-certfile=/path/to/cert.pem
```

### 2. Environment Variables (T76)

**CRITICAL:** Never use default passwords or hardcoded secrets in production.

Create a `.env` file with secure values:

```env
# JWT Configuration
JWT_SECRET_KEY=<generate-with-'openssl-rand-hex-32'>
JWT_VERIFY_SIGNATURE=true

# Database Credentials - USE STRONG PASSWORDS
POSTGRES_USER=<secure-username>
POSTGRES_PASSWORD=<strong-password-min-20-chars>
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_DB=restaurant

# Chef Admin Account
CHEF_USERNAME=chef

# Environment
ENV=production
```

Generate secure secrets:
```bash
# Generate JWT secret (256-bit)
openssl rand -hex 32

# Generate database password
openssl rand -base64 32
```

### 3. Database Security (T19, T2598, T2599)

#### Connection Security
- Use SSL/TLS for database connections
- Configure connection pooling (already implemented in `db/session.py`)
- Use read-only database users where appropriate

#### Query Security
- All queries use parameterized statements (SQLAlchemy ORM)
- Result set limits enforced (max 100 records)
- Connection string protected from injection

### 4. Docker Security (T4746, T4751, T1917)

The Dockerfile has been hardened:
- Runs as non-root user
- Minimal base image (slim-bookworm)
- No sudo access
- Removed unnecessary packages

Additional recommendations:
```yaml
# In docker-compose.yml
services:
  web:
    # Use specific image tags, not 'latest'
    image: restaurant-api:1.0.0
    
    # Security options (already implemented)
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    read_only: false  # Set to true if possible
    
    # Resource limits
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '1'
          memory: 512M
```

### 5. Rate Limiting (T1362, T70)

Rate limiting is implemented using SlowAPI:
- Login endpoint: 10 attempts/minute
- Registration: 5 attempts/hour
- Password reset: 5 attempts/minute
- Account lockout after 5 failed logins (15 minutes)

Configure limits in `rate_limiting.py` based on your needs.

### 6. Authentication & Authorization (T338, T378, T184)

Implemented security measures:
- Password requirements: 12+ chars, uppercase, lowercase, digit, special char
- JWT tokens with signature verification enabled
- Role-based access control (RBAC)
- IDOR protection on all endpoints
- Account lockout on failed login attempts

### 7. Input Validation

All user inputs are validated:
- Menu items: XSS protection, length limits
- Orders: Quantity limits (1-100), item count limits (1-50)
- Addresses and phone numbers: Format validation
- URLs: HTTPS-only, SSRF protection

### 8. Logging & Monitoring (T2602, T349)

Secure logging configured in `secure_logging.py`:
- Separate log files (security, application, error)
- Log rotation (10MB per file, 5 backups)
- Restrictive file permissions (0600)
- Log injection protection

### 9. API Security Headers

Security headers automatically added to all responses:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000`
- `Content-Security-Policy: default-src 'self'`
- Server header removed

### 10. CORS Configuration

CORS is configured with explicit allowed origins:
```python
allow_origins=[
    "https://restaurant.com",
    "https://www.restaurant.com",
]
```

Update these domains based on your frontend applications.

## Security Checklist for Production

- [ ] Configure HTTPS/TLS with valid certificates
- [ ] Set all environment variables securely (no defaults)
- [ ] Enable JWT signature verification (JWT_VERIFY_SIGNATURE=true)
- [ ] Use strong database passwords (20+ characters)
- [ ] Configure firewall rules to restrict access
- [ ] Set up log monitoring and alerting
- [ ] Disable debug endpoints (set ENV=production)
- [ ] Review and update CORS allowed origins
- [ ] Implement intrusion detection
- [ ] Regular security scanning and updates
- [ ] Database backups with encryption
- [ ] Rotate JWT secrets periodically

## Additional Recommendations

1. **Web Application Firewall (WAF):** Deploy a WAF (e.g., ModSecurity, Cloudflare) in front of the API
2. **API Gateway:** Use an API gateway for additional security, rate limiting, and monitoring
3. **Container Scanning:** Regularly scan Docker images for vulnerabilities
4. **Dependency Updates:** Keep all dependencies updated (use Dependabot or similar)
5. **Security Testing:** Regular penetration testing and security audits
6. **Incident Response:** Have an incident response plan ready

## Compliance

This configuration helps meet requirements for:
- OWASP Top 10 API Security
- OWASP Top 10 Web Application Security
- General security best practices

## Support

For security questions or concerns, contact the security team.
