create table public.links (
  id bigint generated always as identity primary key,
  nome text not null,
  url text not null,
  categoria text
);

alter table public.links enable row level security;
