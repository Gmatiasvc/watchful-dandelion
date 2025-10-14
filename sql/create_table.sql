drop table data;

create table data (
	id_hash VARCHAR(256) PRIMARY KEY,
    time_entry BIGINT NOT NULL,
    time_exit BIGINT NOT NULL
)