-- we don't know how to generate root <with-no-name> (class Root) :(
create table covid_regions
(
	id int not null
		primary key,
	description varchar(32) null,
	population int default 0 not null
);

create table counties
(
	name varchar(32) not null
		primary key,
	population int default 0 not null,
	region int default 0 not null,
	lat decimal(11,4) default 0.0000 not null,
	lon decimal(11,4) default 0.0000 not null,
	COVIDRegion int default 0 not null,
	constraint counties_covid_regions_id_fk
		foreign key (COVIDRegion) references covid_regions (id)
);

create table cli_metrics
(
	update_date datetime default CURRENT_TIMESTAMP not null,
	county_name varchar(32) default 'Lake' not null,
	value int default 0 not null,
	primary key (update_date, county_name),
	constraint cli_metrics_counties_name_fk
		foreign key (county_name) references counties (name)
);

create table districts
(
	id varchar(13) default '0' not null
		primary key,
	county_name varchar(32) not null,
	region_code char(2) default '0' not null,
	county_code char(3) default '0' not null,
	district_code char(3) default '0' not null,
	extra_code char default '0' not null,
	district_type int not null,
	name varchar(64) not null,
	base_zip_code int not null,
	enabled tinyint(1) default 0 not null,
	constraint districts_counties_name_fk
		foreign key (county_name) references counties (name)
);

create table inc_metrics
(
	update_date datetime default CURRENT_TIMESTAMP not null,
	county_name varchar(32) default 'Lake' not null,
	value int default 0 not null,
	primary key (update_date, county_name),
	constraint inc_metrics_counties_name_fk
		foreign key (county_name) references counties (name)
);

create table ppe_items
(
	id int auto_increment
		primary key,
	description text not null
);

create table room_types
(
	id int auto_increment
		primary key,
	description varchar(64) not null
);

create table staff_roles
(
	role_type_id int auto_increment
		primary key,
	role_type varchar(32) not null
);

create table tat_metrics
(
	update_date datetime default CURRENT_TIMESTAMP not null,
	county_name varchar(32) default 'Lake' not null,
	value int default 0 not null,
	primary key (update_date, county_name),
	constraint tat_metrics_counties_name_fk
		foreign key (county_name) references counties (name)
);

create table user_roles
(
	role_id int not null
		primary key,
	description varchar(64) default '0' not null,
	permset int default 0 not null
);

create table users
(
	id int auto_increment
		primary key,
	name varchar(100) not null,
	email varchar(40) not null,
	password varchar(200) not null,
	created_on datetime null,
	last_login datetime null,
	district_id varchar(13) null,
	constraint users_email_uindex
		unique (email),
	constraint users_districts_id_fk
		foreign key (district_id) references districts (id)
);

create table bus_groups
(
	bus_group_id int auto_increment
		primary key,
	description varchar(32) not null,
	district_id varchar(13) default '0' not null,
	available int default 0 not null,
	required int default 0 not null,
	update_date datetime default CURRENT_TIMESTAMP null,
	recorder_id int not null,
	constraint bus_groups_districts_id_fk
		foreign key (district_id) references districts (id),
	constraint bus_groups_users_id_fk
		foreign key (recorder_id) references users (id)
);

create table configurations
(
	district_id varchar(13) not null
		primary key,
	configuration json not null,
	update_date datetime default CURRENT_TIMESTAMP null,
	recorder_id int null,
	constraint configurations_districts_id_fk
		foreign key (district_id) references districts (id),
	constraint configurations_users_id_fk
		foreign key (recorder_id) references users (id)
);

create table user_district_roles
(
	id int auto_increment
		primary key,
	district_id varchar(13) not null,
	user_id int not null,
	role_id int not null,
	update_date datetime default CURRENT_TIMESTAMP null,
	recorder_id int null,
	constraint user_district_roles_districts_id_fk
		foreign key (district_id) references districts (id),
	constraint user_district_roles_user_roles_role_id_fk
		foreign key (role_id) references user_roles (role_id),
	constraint user_district_roles_users_id_fk
		foreign key (user_id) references users (id),
	constraint user_district_roles_users_id_fk_2
		foreign key (recorder_id) references users (id)
);

create table users_districts
(
	user_id int not null,
	district_id varchar(13) not null,
	primary key (user_id, district_id),
	constraint users_districts_districts_id_fk
		foreign key (district_id) references districts (id),
	constraint users_districts_users_id_fk
		foreign key (user_id) references users (id)
);

create table zip_codes
(
	zip_code int not null
		primary key,
	population int default 0 not null,
	lat decimal(11,4) not null,
	lon decimal(11,4) not null,
	county_name varchar(32) not null,
	city_name varchar(32) null,
	constraint zip_codes_counties_name_fk
		foreign key (county_name) references counties (name)
);

create table facilities
(
	id varchar(13) default '0' not null
		primary key,
	district_id varchar(13) default '0' not null,
	facility_name varchar(64) not null,
	zip_code int not null,
	grades_served varchar(16) null,
	constraint facilities_districts_id_fk
		foreign key (district_id) references districts (id),
	constraint facilities_zip_codes_zip_code_fk
		foreign key (zip_code) references zip_codes (zip_code)
);

create table ppe_transactions
(
	id int auto_increment
		primary key,
	date datetime default CURRENT_TIMESTAMP null,
	ppe_item_id int not null,
	facility_id varchar(13) not null,
	quantity int default 0 not null,
	recorder_id int not null,
	constraint ppe_transactions_facilities_id_fk
		foreign key (facility_id) references facilities (id),
	constraint ppe_transactions_ppe_items_id_fk
		foreign key (ppe_item_id) references ppe_items (id),
	constraint ppe_transactions_users_id_fk
		foreign key (recorder_id) references users (id)
);

create table room_demand
(
	id int auto_increment
		primary key,
	room_type_id int not null,
	facility_id varchar(13) not null,
	demand int default 0 not null,
	update_date datetime default CURRENT_TIMESTAMP null,
	recorder_id int not null,
	constraint room_demand_facilities_id_fk
		foreign key (facility_id) references facilities (id),
	constraint room_demand_room_types_id_fk
		foreign key (room_type_id) references room_types (id),
	constraint room_demand_users_id_fk
		foreign key (recorder_id) references users (id)
);

create table rooms
(
	id int auto_increment
		primary key,
	room_type_id int not null,
	facility_id varchar(13) not null,
	room_number varchar(8) not null,
	capacity int default 0 not null,
	update_date datetime default CURRENT_TIMESTAMP null,
	recorder_id int not null,
	constraint rooms_facilities_id_fk
		foreign key (facility_id) references facilities (id),
	constraint rooms_room_types_id_fk
		foreign key (room_type_id) references room_types (id),
	constraint rooms_users_id_fk
		foreign key (recorder_id) references users (id)
);

create table staff_updates
(
	id int auto_increment
		primary key,
	update_date datetime default CURRENT_TIMESTAMP null,
	role_type_id int null,
	facility_id varchar(13) not null,
	recorder_id int not null,
	required decimal(4,1) default 0.0 not null,
	available decimal(4,1) default 0.0 not null,
	constraint staff_updates_facilities_id_fk
		foreign key (facility_id) references facilities (id),
	constraint staff_updates_staff_roles_id_fk
		foreign key (role_type_id) references staff_roles (role_type_id),
	constraint staff_updates_users_id_fk
		foreign key (recorder_id) references users (id)
);

create table user_facility_roles
(
	id int auto_increment
		primary key,
	user_id int not null,
	facility_id varchar(13) not null,
	role_id int not null,
	update_date datetime default CURRENT_TIMESTAMP null,
	recorder_id int null,
	constraint user_facility_roles_facilities_id_fk
		foreign key (facility_id) references facilities (id),
	constraint user_facility_roles_user_roles_role_id_fk
		foreign key (role_id) references user_roles (role_id),
	constraint user_facility_roles_users_id_fk
		foreign key (user_id) references users (id),
	constraint user_facility_roles_users_id_fk_2
		foreign key (recorder_id) references users (id)
);

create definer = covidmetrics@`%` view district_zip_codes_vw as
	select `dv`.`id` AS `id`, `f`.`zip_code` AS `zip_code`
from (`covidmetrics`.`districts_vw` `dv`
         left join (select distinct `f`.`district_id` AS `district_id`, `f`.`zip_code` AS `zip_code`
                    from `covidmetrics`.`facilities` `f`
                    where `f`.`district_id` in (select distinct `d`.`id`
                                                from `covidmetrics`.`districts` `d`
                                                where (`d`.`enabled` = true))) `f`
                   on ((`dv`.`id` = `f`.`district_id`)));

create definer = covidmetrics@`%` view districts_vw as
	select `d`.`id` AS `id`, `d`.`district_code` AS `district_code`, `d`.`name` AS `name`
from `covidmetrics`.`districts` `d`
where ((0 <> `d`.`enabled`) is true)
order by `d`.`district_code`;

create definer = covidmetrics@`%` view facilities_vw as
	select `s`.`id` AS `id`, `s`.`facility_name` AS `facility_name`, `d`.`district_code` AS `district_code`
from (`covidmetrics`.`facilities` `s`
         left join `covidmetrics`.`districts` `d` on ((`s`.`district_id` = `d`.`id`)))
where ((0 <> `d`.`enabled`) is true)
order by `d`.`district_code`, `s`.`facility_name`;

create definer = covidmetrics@`%` view ppe_inventory_demand14_vw as
	select `piv`.`ppe_item_id` AS `ppe_item_id`, `piv`.`facility_id` AS `facility_id`, 0 AS `demand14`
from `covidmetrics`.`ppe_inventory_vw` `piv`
group by `piv`.`ppe_item_id`, `piv`.`facility_id`;

create definer = covidmetrics@`%` view ppe_inventory_demand7_vw as
	select `piv`.`ppe_item_id` AS `ppe_item_id`, `piv`.`facility_id` AS `facility_id`, 0 AS `demand7`
from `covidmetrics`.`ppe_inventory_vw` `piv`
group by `piv`.`ppe_item_id`, `piv`.`facility_id`;

create definer = covidmetrics@`%` view ppe_inventory_demand_vw as
	select `piv`.`ppe_item_id`   AS `ppe_item_id`,
       `piv`.`description`   AS `description`,
       `piv`.`facility_id`   AS `facility_id`,
       `piv`.`facility_name` AS `facililty_name`,
       `piv`.`quantity`      AS `quantity`,
       `pid7v`.`demand7`     AS `demand7`,
       `pid14v`.`demand14`   AS `demand14`
from ((`covidmetrics`.`ppe_inventory_vw` `piv` join `covidmetrics`.`ppe_inventory_demand7_vw` `pid7v` on ((
        (`piv`.`ppe_item_id` = `pid7v`.`ppe_item_id`) and (`piv`.`facility_id` = `pid7v`.`facility_id`))))
         join `covidmetrics`.`ppe_inventory_demand14_vw` `pid14v`
              on (((`piv`.`ppe_item_id` = `pid14v`.`ppe_item_id`) and (`piv`.`facility_id` = `pid14v`.`facility_id`))))
order by `piv`.`facility_name`;

create definer = covidmetrics@`%` view ppe_inventory_vw as
	select `pt`.`ppe_item_id`   AS `ppe_item_id`,
       `pi`.`description`   AS `description`,
       `f`.`facility_name`  AS `facility_name`,
       `pt`.`facility_id`   AS `facility_id`,
       sum(`pt`.`quantity`) AS `quantity`,
       max(`pt`.`date`)     AS `update_date`
from ((`covidmetrics`.`ppe_transactions` `pt` join `covidmetrics`.`ppe_items` `pi` on ((`pt`.`ppe_item_id` = `pi`.`id`)))
         join `covidmetrics`.`facilities` `f` on ((`pt`.`facility_id` = `f`.`id`)))
group by `pt`.`ppe_item_id`, `pi`.`description`, `pt`.`facility_id`, `f`.`facility_name`
order by `f`.`facility_name`;

create definer = covidmetrics@`%` view ppe_transactions_vw as
	select `pt`.`id`           AS `id`,
       `pt`.`date`         AS `date`,
       `f`.`id`            AS `facility_id`,
       `f`.`facility_name` AS `facility_name`,
       `pi`.`id`           AS `ppe_item_id`,
       `pi`.`description`  AS `item_description`,
       `pt`.`quantity`     AS `quantity`,
       `u`.`name`          AS `recorder_name`
from (((`covidmetrics`.`ppe_transactions` `pt` left join `covidmetrics`.`facilities` `f` on ((`pt`.`facility_id` = `f`.`id`))) left join `covidmetrics`.`ppe_items` `pi` on ((`pt`.`ppe_item_id` = `pi`.`id`)))
         left join `covidmetrics`.`users` `u` on ((`pt`.`recorder_id` = `u`.`id`)))
order by `f`.`facility_name`;

create definer = covidmetrics@`%` view room_demand_vw as
	select `rt`.`description`  AS `description`,
       `rd`.`room_type_id` AS `room_type_id`,
       `rd`.`facility_id`  AS `facility_id`,
       sum(`rd`.`demand`)  AS `demand`
from (`covidmetrics`.`room_demand` `rd`
         join `covidmetrics`.`room_types` `rt` on ((`rd`.`room_type_id` = `rt`.`id`)))
group by `rt`.`description`, `rd`.`room_type_id`, `rd`.`facility_id`;

create definer = covidmetrics@`%` view room_supply_vw as
	select `rt`.`description`  AS `description`,
       `r`.`room_type_id`  AS `room_type_id`,
       `r`.`facility_id`   AS `facility_id`,
       sum(`r`.`capacity`) AS `capacity`
from (`covidmetrics`.`rooms` `r`
         left join `covidmetrics`.`room_types` `rt` on ((`r`.`room_type_id` = `rt`.`id`)))
group by `rt`.`description`, `r`.`room_type_id`, `r`.`facility_id`;

create definer = covidmetrics@`%` view space_status_vw as
	select `t`.`room_type_id`   AS `room_type_id`,
       `t`.`facility_id`    AS `facility_id`,
       `rt`.`description`   AS `description`,
       `f`.`facility_name`  AS `facility_name`,
       sum(`t`.`available`) AS `available`,
       sum(`t`.`required`)  AS `required`
from (((select distinct `rd`.`room_type_id` AS `room_type_id`,
                        `rd`.`facility_id`  AS `facility_id`,
                        0                   AS `available`,
                        `rd`.`demand`       AS `required`
        from `covidmetrics`.`room_demand` `rd`
        union
        select `r`.`room_type_id`  AS `room_type_id`,
               `r`.`facility_id`   AS `facility_id`,
               sum(`r`.`capacity`) AS `available`,
               0                   AS `required`
        from `covidmetrics`.`rooms` `r`
        group by `r`.`room_type_id`, `r`.`facility_id`) `t` join `covidmetrics`.`room_types` `rt` on ((`t`.`room_type_id` = `rt`.`id`)))
         join `covidmetrics`.`facilities` `f` on ((`t`.`facility_id` = `f`.`id`)))
group by `t`.`room_type_id`, `t`.`facility_id`;

create definer = covidmetrics@`%` view staff_status_vw as
	select `su`.`id`           AS `update_id`,
       `su`.`update_date`  AS `update_date`,
       `sr`.`role_type_id` AS `role_type_id`,
       `sr`.`role_type`    AS `role_type`,
       `su`.`facility_id`  AS `facility_id`,
       `f`.`facility_name` AS `facility_name`,
       `su`.`required`     AS `required`,
       `su`.`available`    AS `available`,
       `u`.`name`          AS `recorder_name`
from ((((`covidmetrics`.`staff_updates` `su` join `covidmetrics`.`staff_roles` `sr` on ((`su`.`role_type_id` = `sr`.`role_type_id`))) join `covidmetrics`.`facilities` `f` on ((`su`.`facility_id` = `f`.`id`))) join `covidmetrics`.`users` `u` on ((`su`.`recorder_id` = `u`.`id`)))
         join (select `m`.`role_type_id`     AS `role_type_id`,
                      `m`.`facility_id`      AS `facility_id`,
                      max(`m`.`update_date`) AS `max_update_date`
               from `covidmetrics`.`staff_updates` `m`
               group by `m`.`role_type_id`, `m`.`facility_id`) `msu`
              on (((`msu`.`role_type_id` = `su`.`role_type_id`) and (`msu`.`facility_id` = `su`.`facility_id`) and
                   (`msu`.`max_update_date` = `su`.`update_date`))));

create definer = covidmetrics@`%` view user_role_targets_vw as
	select `rv`.`user_id`     AS `user_id`,
       `u`.`name`         AS `user_name`,
       `rv`.`target_id`   AS `target_id`,
       `t`.`name`         AS `target_name`,
       `t`.`target_type`  AS `target_type`,
       `t`.`district_id`  AS `district_id`,
       `rv`.`role_id`     AS `role_id`,
       `ur`.`description` AS `role_description`,
       `ur`.`permset`     AS `permset`
from ((((select `udr`.`user_id` AS `user_id`, `udr`.`district_id` AS `target_id`, `udr`.`role_id` AS `role_id`
         from `covidmetrics`.`user_district_roles` `udr`
         union
         select `ufr`.`user_id` AS `user_id`, `ufr`.`facility_id` AS `target_id`, `ufr`.`role_id` AS `role_id`
         from `covidmetrics`.`user_facility_roles` `ufr`) `rv` left join `covidmetrics`.`user_roles` `ur` on ((`rv`.`role_id` = `ur`.`role_id`))) left join `covidmetrics`.`users` `u` on ((`rv`.`user_id` = `u`.`id`)))
         left join (select `d`.`id`   AS `target_id`,
                           `d`.`name` AS `name`,
                           'district' AS `target_type`,
                           `d`.`id`   AS `district_id`
                    from `covidmetrics`.`districts` `d`
                    union
                    select `f`.`id`            AS `target_id`,
                           `f`.`facility_name` AS `name`,
                           'facility'          AS `target_type`,
                           `f`.`district_id`   AS `district_id`
                    from `covidmetrics`.`facilities` `f`) `t` on ((`t`.`target_id` = `rv`.`target_id`)));

create definer = covidmetrics@`%` view users_districts_vw as
	select `ud`.`user_id`     AS `user_id`,
       `u`.`name`         AS `user_name`,
       `ud`.`district_id` AS `district_id`,
       `d`.`name`         AS `district_name`
from ((`covidmetrics`.`users_districts` `ud` join `covidmetrics`.`users` `u` on ((`ud`.`user_id` = `u`.`id`)))
         join `covidmetrics`.`districts` `d` on ((`ud`.`district_id` = `d`.`id`)));

