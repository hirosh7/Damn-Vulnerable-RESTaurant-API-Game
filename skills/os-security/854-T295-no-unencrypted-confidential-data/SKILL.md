---
name: 854-t295-no-unencrypted-confidential-data
description: Ensure sensitive PII fields (phone numbers, delivery addresses) are not stored in plaintext. Currently only passwords are hashed; other PII is stored unencrypted in PostgreSQL.
---

# 854-T295: Avoid Storing Unencrypted Confidential Data Without Access Control

**Category:** CODE_FIX
**SD Elements:** [854-T295](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 7

**Current Data Model:**

```python
# app/db/models.py:33-46
class User(Base):
    username = Column(String)         # plaintext
    password = Column(String)         # bcrypt hashed — GOOD
    first_name = Column(String)       # plaintext PII
    last_name = Column(String)        # plaintext PII
    phone_number = Column(String)     # plaintext PII
    reset_password_code = Column(String, nullable=True)  # plaintext token!

class Order(Base):
    delivery_address = Column(String) # plaintext PII
    phone_number = Column(String)     # plaintext PII
```

**Required Fixes:**

1. **Reset password codes must not be stored in plaintext** — see T2 for hashing.
2. **Phone numbers**: Consider applying application-level encryption (AES-256-GCM).
3. **At minimum**: Ensure PostgreSQL access is restricted (T19) to limit who can query raw PII.
4. **Document** the data classification: what is PII, what is encrypted, who can access.

```python
# Option: Use encrypted fields library
# pip install sqlalchemy-utils
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

class User(Base):
    phone_number = Column(EncryptedType(String, SECRET_KEY, AesEngine, 'pkcs5'))
    # store as encrypted; decrypt on read
```

**Note:** This change requires a database migration and updated indexes (encrypted fields cannot be indexed for equality).

**Success Criteria:**

- Reset password codes stored as hashes (not plaintext) — see T2
- Database access is restricted (see T19)
- PII encryption strategy documented in README
- No sensitive tokens stored in plaintext

**Status:** Pending
