-- UUID 扩展
CREATE EXTENSION IF NOT EXISTS pgcrypto;

------------------------------------------------
-- 1. chat_sessions
------------------------------------------------
CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    tenant_id VARCHAR(64) NOT NULL DEFAULT 'default',
    user_id VARCHAR(64) NOT NULL,

    title VARCHAR(255) NOT NULL DEFAULT '新对话',

    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_chat_sessions_user
ON chat_sessions(user_id);

CREATE INDEX IF NOT EXISTS idx_chat_sessions_tenant
ON chat_sessions(tenant_id);


------------------------------------------------
-- 2. chat_messages
------------------------------------------------
CREATE TABLE IF NOT EXISTS chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    tenant_id VARCHAR(64) NOT NULL DEFAULT 'default',

    session_id UUID NOT NULL
        REFERENCES chat_sessions(id)
        ON DELETE CASCADE,

    role VARCHAR(20) NOT NULL,

    content TEXT NOT NULL,

    meta_data JSONB NOT NULL DEFAULT '{}'::jsonb,

    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 查询历史消息必须的索引
CREATE INDEX IF NOT EXISTS idx_chat_messages_session
ON chat_messages(session_id);

CREATE INDEX IF NOT EXISTS idx_chat_messages_tenant
ON chat_messages(tenant_id);