
create table registered_user (
  id integer primary key autoincrement,
  firstname text not null,
  lastname text not null,
  username text not null,
  'password' text not null
);


create table advertisements(
  id integer primary key autoincrement,
  title text not null,
  category txt not null,
  price integer not null,
  name text not null,
  mobile integer not null,
  email text not null,
  address text not null,
  user_id references registered_user(id) on delete cascade

);
/*create table users (
  id integer primary key autoincrement,
  username text not null,
  'password' text not null
);




create table posted (
  id integer primary key autoincrement.
  title text not null,
  description text not null,
   
);*/
