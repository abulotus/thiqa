-- =====================================================

-- =====================================================
-- ENABLE EXTENSIONS
-- =====================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- MERCHANTS TABLE
-- =====================================================

CREATE TABLE merchants (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    business_name_ar VARCHAR(255) NOT NULL,
    
    business_name_en VARCHAR(255),
    
    owner_name VARCHAR(255),

    username VARCHAR(100) UNIQUE NOT NULL,

    password_hash TEXT NOT NULL,

    mobile_number VARCHAR(50),

    city VARCHAR(100),

    address TEXT,

    registration_number VARCHAR(100),

    trust_level INTEGER DEFAULT 50,

    status VARCHAR(50) DEFAULT 'ACTIVE',

    created_at TIMESTAMP DEFAULT NOW(),

    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_merchants_username
ON merchants(username);

CREATE INDEX idx_merchants_mobile
ON merchants(mobile_number);

-- =====================================================
-- USERS / CUSTOMERS TABLE
-- =====================================================

CREATE TABLE users (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    merchant_id UUID REFERENCES merchants(id),

    full_name_ar VARCHAR(255) NOT NULL,

    full_name_en VARCHAR(255),

    mobile_number VARCHAR(50) UNIQUE NOT NULL,

    national_id VARCHAR(100) UNIQUE NOT NULL,

    date_of_birth DATE,

    gender VARCHAR(20),

    city VARCHAR(100),

    address TEXT,

    total_credit DECIMAL(12,2) DEFAULT 0,

    balance_remaining DECIMAL(12,2) DEFAULT 0,

    risk_level VARCHAR(50) DEFAULT 'UNKNOWN',

    status VARCHAR(50) DEFAULT 'ACTIVE',

    created_at TIMESTAMP DEFAULT NOW(),

    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_mobile
ON users(mobile_number);

CREATE INDEX idx_users_national_id
ON users(national_id);

CREATE INDEX idx_users_name
ON users(full_name_ar);

-- =====================================================
-- CREDIT ACCOUNTS
-- =====================================================

CREATE TABLE credit_accounts (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    user_id UUID NOT NULL REFERENCES users(id),

    merchant_id UUID NOT NULL REFERENCES merchants(id),

    product_type VARCHAR(100),

    principal_amount DECIMAL(12,2) NOT NULL,

    total_payable DECIMAL(12,2) NOT NULL,

    installment_count INTEGER NOT NULL,

    installment_value DECIMAL(12,2),

    start_date DATE,

    due_date DATE,

    status VARCHAR(50) DEFAULT 'ACTIVE',

    created_at TIMESTAMP DEFAULT NOW(),

    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_credit_accounts_user
ON credit_accounts(user_id);

CREATE INDEX idx_credit_accounts_merchant
ON credit_accounts(merchant_id);

-- =====================================================
-- PAYMENT EVENTS
-- =====================================================

CREATE TABLE payment_events (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    credit_account_id UUID
    REFERENCES credit_accounts(id),

    amount_paid DECIMAL(12,2) NOT NULL,

    payment_method VARCHAR(50),

    payment_date TIMESTAMP DEFAULT NOW(),

    collector_name VARCHAR(255),

    geo_lat DECIMAL(10,7),

    geo_long DECIMAL(10,7),

    notes TEXT,

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_payment_credit_account
ON payment_events(credit_account_id);

CREATE INDEX idx_payment_date
ON payment_events(payment_date);

-- =====================================================
-- CREDIT SCORES
-- =====================================================

CREATE TABLE credit_scores (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    user_id UUID REFERENCES users(id),

    score_value INTEGER NOT NULL,

    risk_band VARCHAR(50),

    model_version VARCHAR(50),

    explanation_json JSONB,

    generated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_credit_scores_user
ON credit_scores(user_id);

CREATE INDEX idx_credit_scores_value
ON credit_scores(score_value);

-- =====================================================
-- USER REFERENCES
-- =====================================================

CREATE TABLE user_references (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    user_id UUID REFERENCES users(id),

    reference_name VARCHAR(255),

    mobile_number VARCHAR(50),

    relationship VARCHAR(100),

    verified BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- DEVICES TABLE
-- =====================================================

CREATE TABLE devices (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    device_fingerprint TEXT,

    imei_hash TEXT,

    platform VARCHAR(50),

    created_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- USER DEVICES LINK
-- =====================================================

CREATE TABLE user_devices (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    user_id UUID REFERENCES users(id),

    device_id UUID REFERENCES devices(id),

    first_seen TIMESTAMP DEFAULT NOW(),

    last_seen TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- USER CONSENTS
-- =====================================================

CREATE TABLE user_consents (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    user_id UUID REFERENCES users(id),

    consent_type VARCHAR(100),

    granted BOOLEAN DEFAULT TRUE,

    granted_at TIMESTAMP DEFAULT NOW(),

    revoked_at TIMESTAMP
);

-- =====================================================
-- AUDIT LOGS
-- =====================================================

CREATE TABLE audit_logs (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    actor_type VARCHAR(100),

    actor_id UUID,

    action VARCHAR(100),

    entity_type VARCHAR(100),

    entity_id UUID,

    old_values JSONB,

    new_values JSONB,

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_entity
ON audit_logs(entity_type, entity_id);

-- =====================================================
-- MERCHANT REPORTING QUALITY
-- =====================================================

CREATE TABLE merchant_reporting_quality (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    merchant_id UUID REFERENCES merchants(id),

    late_submission_rate DECIMAL(5,2),

    suspicious_activity_score DECIMAL(5,2),

    fraud_flag_count INTEGER DEFAULT 0,

    updated_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- SAMPLE MERCHANT
-- =====================================================

INSERT INTO merchants (

    business_name_ar,
    business_name_en,
    owner_name,
    username,
    password_hash,
    mobile_number,
    city

) VALUES (

'متجر دمشق',
    'Damascus Mobile Store',
    'Ahmad Khaled',
    'merchant1',

    '$2b$12$samplehashedpassword',

    '+963999999999',
    'Damascus'
);

-- =====================================================
-- SSL CONNECTION EXAMPLE
-- =====================================================

-- Example PostgreSQL SSL connection string:

-- postgresql://username:password@server_ip:5432/creditdb?sslmode=require

-- =====================================================
-- PYTHON SQLALCHEMY SSL EXAMPLE
-- =====================================================

-- Example:

-- DATABASE_URL =
-- "postgresql+psycopg2://user:password@server:5432/creditdb?sslmode=require"

-- =====================================================
-- IMPORTANT SECURITY NOTES
-- =====================================================

-- 1. Use SSL ALWAYS
-- sslmode=require

-- 2. Encrypt backups

-- 3. Restrict DB access to private network only

-- 4. Never expose PostgreSQL publicly

-- 5. Use strong passwords

-- 6. Enable firewall rules

-- 7. Use connection pooling later

-- =====================================================
-- RECOMMENDED NEXT STEP
-- =====================================================

-- Build FastAPI ORM models matching this schema.
-- Then create:
--
-- POST /customers
-- POST /payments
-- GET  /score
-- GET  /merchant-dashboard
--
-- APIs first, frontend second.