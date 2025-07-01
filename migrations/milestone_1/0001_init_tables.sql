-- Table `problems`: Store main information of problems
-- ===================================================
CREATE TABLE problems (
    id SERIAL PRIMARY KEY, -- Auto-increment primary key, INT type
    problem_code VARCHAR(50) UNIQUE NOT NULL, -- Unique problem code, e.g.: "helloworld"
    title VARCHAR(255) NOT NULL, -- Full name of the problem
    source VARCHAR(100), -- Source: "codemath", "SPOJ", "Self-made"
    difficulty VARCHAR(20) CHECK (difficulty IN ('easy', 'medium', 'hard', 'special')), -- Difficulty, use CHECK constraint to limit values
    problem_pdf_url VARCHAR(512), -- URL to the problem PDF file
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), -- Creation time, TIMESTAMPTZ stores timezone
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create an index on `problem_code` to speed up queries
CREATE INDEX idx_problems_problem_code ON problems(problem_code);
-- Create an index on `source` for faster source-based search
CREATE INDEX idx_problems_source ON problems(source);


-- Table `solutions`: Store solutions for a problem
-- ===================================================
CREATE TABLE solutions (
    id SERIAL PRIMARY KEY,
    problem_id INTEGER NOT NULL, -- Foreign key to `problems` table
    language VARCHAR(50) NOT NULL, -- Programming language: "Python", "C++"
    code_file_url VARCHAR(512), -- URL to code file on cloud storage
    description TEXT, -- Short description of the algorithm used
    is_accepted BOOLEAN DEFAULT FALSE, -- Accepted status: TRUE if solution is accepted
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Set up foreign key
    CONSTRAINT fk_problem
        FOREIGN KEY(problem_id)
        REFERENCES problems(id)
        ON DELETE CASCADE -- If a problem is deleted, all related solutions are also deleted
);

-- Create index on `problem_id` for faster solution lookup by problem
CREATE INDEX idx_solutions_problem_id ON solutions(problem_id);


-- Table `explanations`: Store detailed explanations
-- ===================================================
CREATE TABLE explanations (
    id SERIAL PRIMARY KEY,
    problem_id INTEGER UNIQUE NOT NULL, -- Ensure one problem has only one explanation (1-1 relationship)
    content TEXT, -- Explanation content, stored as Markdown
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Set up foreign key
    CONSTRAINT fk_problem
        FOREIGN KEY(problem_id)
        REFERENCES problems(id)
        ON DELETE CASCADE
);


-- Table `tags`: Store tags for classifying problems
-- ===================================================
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL -- Tag name must be unique, e.g.: "dynamic-programming"
);

-- Create index on `name` for faster tag search and to support UNIQUE constraint
CREATE INDEX idx_tags_name ON tags(name);


-- Table `problem_tags`: Join table for many-to-many relationship between problems and tags
-- ===================================================
CREATE TABLE problem_tags (
    problem_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,

    -- Set up composite primary key
    PRIMARY KEY (problem_id, tag_id),

    -- Set up foreign keys
    CONSTRAINT fk_problem
        FOREIGN KEY(problem_id)
        REFERENCES problems(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_tag
        FOREIGN KEY(tag_id)
        REFERENCES tags(id)
        ON DELETE CASCADE
);

-- Create triggers to automatically update `updated_at` column
-- =============================================================
-- This is a common pattern in PostgreSQL to avoid updating `updated_at` in the application layer

-- 1. Create a trigger function
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 2. Attach the trigger to the necessary tables
CREATE TRIGGER set_timestamp
BEFORE UPDATE ON problems
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON solutions
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON explanations
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();
