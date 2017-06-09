create table meals
(
	id int auto_increment
		primary key,
	name text not null,
	description text null
)
;

create table menus
(
	date date not null,
	id int auto_increment
		primary key,
	venue int not null,
	meal int not null,
	constraint eindeutig
		unique (venue, date, meal),
	constraint menus_meals_id_fk
		foreign key (meal) references hunger.meals (id)
)
;

create index menus_meals_id_fk
	on menus (meal)
;

create table venues
(
	id int auto_increment
		primary key,
	name text null
)
;

alter table menus
	add constraint menus_ibfk_1
		foreign key (venue) references hunger.venues (id)
;

