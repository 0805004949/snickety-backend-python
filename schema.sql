CREATE TABLE users(
	id int not null auto_increment, 
	name varchar(100) not null, 
	email varchar(100) not null, 
	hashed_password varchar(100) not null, 
	profile varchar(200) not null, 
	created_at TIMESTAMP not null default current_timestamp, 
	updated_at TIMESTAMP not null ON UPDATE current_timestamp, 
	PRIMARY KEY (id), 
	UNIQUE KEY email(email)
);

CREATE TABLE users_follow_list(
user_id int not null, 
follow_user_id int not null, 
created_at TIMESTAMP not null default current_timestamp, 
PRIMARY KEY (user_id, follow_user_id), 
CONSTRAINT users_follow_list_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id),
CONSTRAINT users_follow_list_follow_user_id_fkey FOREIGN KEY (follow_user_id) REFERENCES users(id)
);

CREATE TABLE tweets(
id int not null auto_increment, 
user_id int not null, 
tweet VARCHAR(300) not null, 
created_at TIMESTAMP not null default current_timestamp, 
PRIMARY KEY (id),
CONSTRAINT tweets_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id));