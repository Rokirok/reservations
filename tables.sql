create table users
(
    id             uuid                                      not null
        constraint users_pk
            primary key,
    name           varchar                                   not null,
    email          varchar                                   not null
        constraint users_pk2
            unique,
    role           varchar default 'user'::character varying not null,
    allowed_access boolean default false                     not null,
    password_hash  varchar                                   not null
);

create table services
(
    id        uuid    not null
        constraint services_pk
            primary key,
    name      varchar not null,
    price_snt integer not null
);

create table locations
(
    id          uuid    not null
        constraint locations_pk
            primary key,
    name        varchar not null,
    address     varchar not null,
    cover_image varchar
);

create table reservable_timeslots
(
    id        uuid      not null
        constraint reservable_timeslots_pk
            primary key,
    timestamp timestamp not null,
    location  uuid      not null
        constraint reservable_timeslots_locations_id_fk
            references locations,
    employee  uuid      not null
        constraint reservable_timeslots_users_id_fk
            references users,
    service   uuid      not null
        constraint reservable_timeslots_services_id_fk
            references services
);

create table reservations
(
    id              uuid                  not null
        constraint reservations_pk
            primary key,
    pin             varchar(6)            not null,
    timeslot        uuid                  not null
        constraint reservations_reservable_timeslots_id_fk
            references reservable_timeslots,
    customer_name   varchar               not null,
    customer_email  varchar               not null,
    customer_mobile varchar               not null,
    message         text,
    completed       boolean default false not null
);
