drop table data;

create table data (
	id_hash VARCHAR(64) PRIMARY KEY,
    time_entry BIGINT NOT NULL,
    time_exit BIGINT NOT NULL
)