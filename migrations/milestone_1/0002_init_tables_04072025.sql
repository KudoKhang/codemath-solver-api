-- =============================================================================
-- II. TẠO CÁC BẢNG CHÍNH (KHÔNG CÓ KHÓA NGOẠI HOẶC ÍT PHỤ THUỘC)
-- =============================================================================

-- Bảng: accounts
-- Mục đích: Quản lý thông tin tài khoản người dùng và quyền hạn.
CREATE TABLE accounts (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  fullname VARCHAR(100),
  email VARCHAR(255) UNIQUE NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  role INTEGER CHECK (role IN (1, 2, 3)) NOT NULL DEFAULT 1, -- 1: USER, 2: EDITOR, 3: ADMIN
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  credits INT NOT NULL DEFAULT 0,
  amount INT NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  CONSTRAINT credits_must_be_non_negative CHECK (credits >= 0)
);

-- Bảng: platforms
-- Mục đích: Quản lý danh sách các nền tảng (ví dụ: LeetCode, Codeforces).
CREATE TABLE platforms (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  base_url VARCHAR(255),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO platforms (id, name, base_url)
VALUES
  (1, 'codemath', 'https://laptrinh.codemath.vn/');

-- Bảng: programming_languages
-- Mục đích: Quản lý danh sách các ngôn ngữ lập trình được hỗ trợ.
CREATE TABLE programming_languages (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  version VARCHAR(20),
  slug VARCHAR(50) UNIQUE NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Bảng: tags
-- Mục đích: Quản lý các thẻ (tags) để phân loại bài toán.
CREATE TABLE tags (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL,
  slug VARCHAR(50) UNIQUE NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- =============================================================================
-- III. TẠO CÁC BẢNG PHỤ THUỘC (CÓ KHÓA NGOẠI)
-- =============================================================================

-- Bảng: credit_transactions
-- Mục đích: Ghi lại lịch sử giao dịch credit của người dùng.
CREATE TABLE credit_transactions (
  id SERIAL PRIMARY KEY,
  account_id INT NOT NULL,
  change_amount INT,
  change_credit INT,
  reason VARCHAR(255),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  -- Ràng buộc khóa ngoại: Nếu một tài khoản bị xóa, các giao dịch của họ cũng bị xóa.
  CONSTRAINT fk_credit_transactions_account
    FOREIGN KEY(account_id)
    REFERENCES accounts(id)
    ON DELETE CASCADE
);

-- Bảng: problems
-- Mục đích: Lưu trữ thông tin chi tiết về các bài toán.
CREATE TABLE problems (
  id SERIAL PRIMARY KEY,
  platform_id INT,
  platform_specific_code VARCHAR(100) NOT NULL,
  title VARCHAR(255) NOT NULL,
  difficulty INTEGER CHECK (difficulty IN (1, 2, 3)), -- 1: EASY, 2: MEDIUM, 3: HARD
  description TEXT,
  content_format INTEGER CHECK (content_format IN (1, 2, 3, 4)), -- 1: MARKDOWN, 2: PLAINTEXT, 3: PDF_URL, 4: IMG_URL
  content TEXT NOT NULL,
  created_by INT NOT NULL,
  last_edited_by INT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  -- Ràng buộc khóa ngoại
  CONSTRAINT fk_problems_platform FOREIGN KEY(platform_id) REFERENCES platforms(id) ON DELETE SET NULL,
  CONSTRAINT fk_problems_created_by FOREIGN KEY(created_by) REFERENCES accounts(id) ON DELETE RESTRICT,
  CONSTRAINT fk_problems_last_edited_by FOREIGN KEY(last_edited_by) REFERENCES accounts(id) ON DELETE SET NULL,

  -- Ràng buộc duy nhất: Đảm bảo không có bài toán trùng lặp trên cùng một nền tảng.
  CONSTRAINT uq_problem_on_platform UNIQUE (platform_id, platform_specific_code)
);

-- Bảng: solutions
-- Mục đích: Lưu trữ các lời giải bằng code cho các bài toán.
-- Lưu ý: Dựa trên thảo luận trước, trường `source_code_type` đã được loại bỏ để tránh trùng lặp với `language_id`.
CREATE TABLE solutions (
  id SERIAL PRIMARY KEY,
  problem_id INT NOT NULL,
  created_by INT NOT NULL,
  last_edited_by INT,
  language_id INT NOT NULL,
  description TEXT,
  source_code TEXT NOT NULL,
  status INTEGER CHECK (status IN (1, 2, 3, 4, 5)), -- 1: PENDING, 2: ACCEPTED, 3: WRONG_ANSWER, 4: TIME_LIMIT_EXCEEDED, 5: RUNTIME_ERROR
  score INT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  -- Ràng buộc khóa ngoại
  CONSTRAINT fk_solutions_problem FOREIGN KEY(problem_id) REFERENCES problems(id) ON DELETE CASCADE,
  CONSTRAINT fk_solutions_created_by FOREIGN KEY(created_by) REFERENCES accounts(id) ON DELETE RESTRICT,
  CONSTRAINT fk_solutions_last_edited_by FOREIGN KEY(last_edited_by) REFERENCES accounts(id) ON DELETE SET NULL,
  CONSTRAINT fk_solutions_language FOREIGN KEY(language_id) REFERENCES programming_languages(id) ON DELETE RESTRICT,

  -- Ràng buộc kiểm tra: Điểm số phải nằm trong một khoảng hợp lý, ví dụ 0-100.
  CONSTRAINT score_range CHECK (score IS NULL OR (score >= 0 AND score <= 100))
);

-- Bảng: explanations
-- Mục đích: Lưu trữ các bài viết giải thích chi tiết về thuật toán, cách tiếp cận.
CREATE TABLE explanations (
  id SERIAL PRIMARY KEY,
  problem_id INT NOT NULL,
  created_by INT NOT NULL,
  last_edited_by INT,
  title VARCHAR(255),
  description TEXT,
  content TEXT NOT NULL,
  upvotes INT NOT NULL DEFAULT 0,
  downvotes INT NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  -- Ràng buộc khóa ngoại
  CONSTRAINT fk_explanations_problem FOREIGN KEY(problem_id) REFERENCES problems(id) ON DELETE CASCADE,
  CONSTRAINT fk_explanations_created_by FOREIGN KEY(created_by) REFERENCES accounts(id) ON DELETE RESTRICT,
  CONSTRAINT fk_explanations_last_edited_by FOREIGN KEY(last_edited_by) REFERENCES accounts(id) ON DELETE SET NULL,

  -- Ràng buộc kiểm tra: Số vote không được là số âm.
  CONSTRAINT votes_must_be_non_negative CHECK (upvotes >= 0 AND downvotes >= 0)
);

-- Bảng: problem_tags (Bảng trung gian)
-- Mục đích: Tạo mối quan hệ nhiều-nhiều giữa bài toán và các thẻ.
CREATE TABLE problem_tags (
  problem_id INT NOT NULL,
  tag_id INT NOT NULL,

  -- Ràng buộc khóa ngoại
  CONSTRAINT fk_problem_tags_problem FOREIGN KEY(problem_id) REFERENCES problems(id) ON DELETE CASCADE,
  CONSTRAINT fk_problem_tags_tag FOREIGN KEY(tag_id) REFERENCES tags(id) ON DELETE CASCADE,

  -- Khóa chính kết hợp: Đảm bảo một bài toán chỉ được gán một thẻ một lần.
  PRIMARY KEY (problem_id, tag_id)
);


-- =============================================================================
-- IV. TẠO INDEX ĐỂ TĂNG TỐC ĐỘ TRUY VẤN
-- Các khóa chính và ràng buộc UNIQUE đã tự động tạo index.
-- Chúng ta có thể thêm index cho các cột khóa ngoại và các cột thường được dùng để lọc.
-- =============================================================================

CREATE INDEX idx_problems_created_by ON problems(created_by);
CREATE INDEX idx_solutions_problem_id ON solutions(problem_id);
CREATE INDEX idx_solutions_created_by ON solutions(created_by);
CREATE INDEX idx_explanations_problem_id ON explanations(problem_id);
CREATE INDEX idx_explanations_created_by ON explanations(created_by);

-- =============================================================================
-- V. TỰ ĐỘNG TRIGGERS ĐỂ CẬP NHẬT TRƯỜNG `updated_at`
-- Tạo trigger để tự động cập nhật trường `updated_at` mỗi khi có thay đổi
-- =============================================================================
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON problems
FOR EACH ROW
EXECUTE FUNCTION trigger_set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON solutions
FOR EACH ROW
EXECUTE FUNCTION trigger_set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON explanations
FOR EACH ROW
EXECUTE FUNCTION trigger_set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON accounts
FOR EACH ROW
EXECUTE FUNCTION trigger_set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON tags
FOR EACH ROW
EXECUTE FUNCTION trigger_set_timestamp();
