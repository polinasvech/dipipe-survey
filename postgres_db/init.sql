-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum type for question types
CREATE TYPE question_type_enum AS ENUM ('NUMERIC', 'STRING');

-- Create clients table
CREATE TABLE IF NOT EXISTS clients (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tin VARCHAR(10) NOT NULL,
    preferences VARCHAR(50),
    division VARCHAR(50),
    ca_type VARCHAR(50)
);

-- Create managers table
CREATE TABLE IF NOT EXISTS managers (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name TEXT NOT NULL
);

-- Create surveys table
CREATE TABLE IF NOT EXISTS surveys (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    manager_id UUID,
    CONSTRAINT fk_manager
        FOREIGN KEY (manager_id)
        REFERENCES managers(uuid)
);

-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    text TEXT NOT NULL
);

-- Create questions table
CREATE TABLE IF NOT EXISTS questions (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    survey_id UUID NOT NULL,
    category_id UUID NOT NULL,
    text TEXT NOT NULL,
    type question_type_enum NOT NULL,
    required BOOLEAN NOT NULL DEFAULT false,
    CONSTRAINT fk_survey
        FOREIGN KEY (survey_id)
        REFERENCES surveys(uuid)
        ON DELETE CASCADE,
    CONSTRAINT fk_category
        FOREIGN KEY (category_id)
        REFERENCES categories(uuid)
        ON DELETE CASCADE
);

-- Create answers table
CREATE TABLE IF NOT EXISTS answers (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL,
    survey_id UUID NOT NULL,
    question_id UUID NOT NULL,
    answer_int INTEGER,
    answer_text TEXT,
    CONSTRAINT fk_client
        FOREIGN KEY (client_id)
        REFERENCES clients(uuid)
        ON DELETE CASCADE,
    CONSTRAINT fk_survey_answer
        FOREIGN KEY (survey_id)
        REFERENCES surveys(uuid)
        ON DELETE CASCADE,
    CONSTRAINT fk_question_answer
        FOREIGN KEY (question_id)
        REFERENCES questions(uuid)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS templates (
    uuid               uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    initial_survey_id  uuid NOT NULL,
    template_text      text,
    CONSTRAINT fk_initial_survey
         FOREIGN KEY (initial_survey_id)
         REFERENCES surveys(uuid)
);
