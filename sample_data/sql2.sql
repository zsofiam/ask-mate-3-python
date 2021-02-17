

INSERT INTO users (username, password) VALUES ('try@feature.com', '$2b$12$8iAOEYVpPWIltSqyHMwShe1Sgj3jYleSAO0sEE10qiNR7TbTrXz9.');
INSERT INTO users (username, password) VALUES ('admin@admin.com', '$2b$12$O4YeiiR0bU8FDp9.KJnIxuJid19NldXk0fzkrgw3Tez9i7.G2DsJu');
UPDATE question set user_id = 1 WHERE id = 0;
UPDATE question set user_id = 1 WHERE id = 1;
UPDATE question set user_id = 2 WHERE id = 2;

UPDATE answer set user_id = 1 WHERE id = 1;
UPDATE answer set user_id = 1 WHERE id = 2;


UPDATE comment set user_id = 2 WHERE id = 1;
UPDATE comment set user_id = 2 WHERE id = 2;

UPDATE question set user_id = 1 WHERE id = 0;
UPDATE question set user_id = 1 WHERE id = 1;
UPDATE question set user_id = 2 WHERE id = 2;

UPDATE answer set user_id = 1 WHERE id = 1;
UPDATE answer set user_id = 1 WHERE id = 2;


UPDATE comment set user_id = 2 WHERE id = 1;
UPDATE comment set user_id = 2 WHERE id = 2;

UPDATE users set registration_date = '2021-02-16 16:55:00.000000' WHERE id = 1;
UPDATE users set registration_date = '2021-02-15 18:55:00.000000' WHERE id = 2;
UPDATE users set reputation = 0 WHERE id = 1;
UPDATE users set reputation = 0 WHERE id = 2;