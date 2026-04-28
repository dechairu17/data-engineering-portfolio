create table if not exists books (
    id serial,
    title text not null,
    author_name text,
    first_publish_year text
);
