create table users
(
    id       integer generated always as identity
        constraint users_pkey
            primary key,
    username text,
    password text
);
INSERT INTO users (username, password) VALUES ('csilla@hegedus.com', '$2b$12$.UkJaJTato0fHdaPxegRm.kYJB/oEk.EiWcn6Di6BMa9WYSUYbjZi');