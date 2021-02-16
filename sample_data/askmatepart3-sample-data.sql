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