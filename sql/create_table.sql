drop table data;

create table data (
	record_hash VARCHAR(256) PRIMARY KEY,
    created_at BIGINT NOT NULL,
    updated_at BIGINT NOT NULL
)