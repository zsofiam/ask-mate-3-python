create table users if not exists
(
    id       integer generated always as identity
        constraint users_pkey
            primary key,
    username text,
    password text
);
INSERT INTO users (username, password) VALUES ('csilla@hegedus.com', '$2b$12$.UkJaJTato0fHdaPxegRm.kYJB/oEk.EiWcn6Di6BMa9WYSUYbjZi');
INSERT INTO users (username, password) VALUES ('admin@admin.com', '$2b$12$O4YeiiR0bU8FDp9.KJnIxuJid19NldXk0fzkrgw3Tez9i7.G2DsJu');
UPDATE question set user_id = 1 WHERE id = 0;
UPDATE question set user_id = 1 WHERE id = 1;
UPDATE question set user_id = 2 WHERE id = 2;

UPDATE answer set user_id = 1 WHERE id = 1;
UPDATE answer set user_id = 1 WHERE id = 2;


UPDATE comment set user_id = 2 WHERE id = 1;
UPDATE comment set user_id = 2 WHERE id = 2;
ALTER TABLE ONLY question
    ADD COLUMN user_id integer;

ALTER TABLE ONLY answer
    ADD COLUMN user_id integer;

ALTER TABLE ONLY comment
    ADD COLUMN user_id integer;

ALTER TABLE ONLY question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);
UPDATE question set user_id = 1 WHERE id = 0;
UPDATE question set user_id = 1 WHERE id = 1;
UPDATE question set user_id = 2 WHERE id = 2;

UPDATE answer set user_id = 1 WHERE id = 1;
UPDATE answer set user_id = 1 WHERE id = 2;


UPDATE comment set user_id = 2 WHERE id = 1;
UPDATE comment set user_id = 2 WHERE id = 2;

ALTER TABLE ONLY users
    ADD COLUMN registration_date date,
    ADD COLUMN reputation integer;"public"
UPDATE users set registration_date = '2021-02-16' WHERE id = 1;
UPDATE users set registration_date = '2021-02-15' WHERE id = 2;
UPDATE users set reputation = 0 WHERE id = 1;
UPDATE users set reputation = 0 WHERE id = 2;