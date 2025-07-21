CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS clients (
    uuid       uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    tin        varchar(10) NOT NULL,
    preferences varchar(50),
    division    varchar(50),
    ca_type     varchar(50)
);

CREATE TABLE IF NOT EXISTS managers (
    uuid      uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name text NOT NULL
);

CREATE TABLE IF NOT EXISTS surveys (
    uuid       uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name       text NOT NULL,
    start_date timestamptz NOT NULL,
    end_date   timestamptz NOT NULL,
    manager_id   uuid,
    CONSTRAINT fk_manager
         FOREIGN KEY (manager_id)
         REFERENCES managers(uuid)
);

CREATE TABLE IF NOT EXISTS questions (
    uuid      uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    survey_id uuid NOT NULL,
    text      text NOT NULL,
    CONSTRAINT fk_survey
        FOREIGN KEY (survey_id)
        REFERENCES surveys(uuid)
        ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS answers (
    client_id   uuid NOT NULL,
    survey_id   uuid NOT NULL,
    question_id   uuid NOT NULL,
    answer_int  int,
    answer_text text,
    PRIMARY KEY(client_id, survey_id),
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