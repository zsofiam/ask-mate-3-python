DROP TABLE IF EXISTS public.users_statistics;
CREATE TABLE users_statistics (
                         id serial NOT NULL,
                         question_count integer,
                         answer_count integer,
                         comment_count integer,
                         user_id integer
);

ALTER TABLE ONLY users_statistics
    ADD CONSTRAINT pk_users_statistics_id PRIMARY KEY (id);

ALTER TABLE ONLY users_statistics
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);

INSERT INTO users_statistics VALUES (1, 0, 0, 0, 1);
INSERT INTO users_statistics VALUES (2, 0, 0, 0, 2);
-- INSERT INTO users_statistics VALUES (3, 0, 0, 0, 3);