CREATE TABLE IF NOT EXISTS  users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(30),
    userpassword VARCHAR(200),
    userstatus BOOLEAN,
    user_role INTEGER REFERENCES user_roles(role_id)
);
CREATE TABLE IF NOT EXISTS user_roles(
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(10)
)

INSERT INTO user_roles(role_name) VALUES ('sysadmin'),('support'),('customer service'),('hr'), ('accounts'),('administration');


grant all privileges on users to tom;
grant all privileges on user_roles to tom;
grant usage,select  on sequence users_id_seq to tom;