-- StimaVeloce – schema database Supabase
-- Incolla tutto in Supabase > SQL Editor > New query e premi Run. Si può rieseguire senza danni.

-- 1) Profili: un profilo per ogni accesso, con il ruolo
create table if not exists public.profiles (
  id uuid primary key references auth.users on delete cascade,
  email text,
  nome text,
  role text not null default 'cliente' check (role in ('cliente', 'perito', 'studio')),
  created_at timestamptz not null default now()
);
alter table public.profiles enable row level security;

create or replace function public.ruolo() returns text
language sql stable security definer set search_path = public as $$
  select role from public.profiles where id = auth.uid()
$$;

drop policy if exists "profilo: leggo il mio" on public.profiles;
create policy "profilo: leggo il mio" on public.profiles for select using (id = auth.uid() or public.ruolo() in ('studio', 'perito'));
drop policy if exists "profilo: aggiorno il mio nome" on public.profiles;
create policy "profilo: aggiorno il mio nome" on public.profiles for update using (id = auth.uid())
  with check (id = auth.uid() and role = public.ruolo());
drop policy if exists "profilo: lo studio gestisce i ruoli" on public.profiles;
create policy "profilo: lo studio gestisce i ruoli" on public.profiles for update using (public.ruolo() = 'studio');

create or replace function public.nuovo_utente() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, email, nome) values (new.id, lower(new.email), new.raw_user_meta_data ->> 'nome')
  on conflict (id) do nothing;
  return new;
end $$;
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users for each row execute function public.nuovo_utente();

-- 2) Pratiche: i dati completi della pratica stanno in "dati" (come nell'app)
create table if not exists public.pratiche (
  id text primary key,
  owner uuid references auth.users on delete set null,
  email text,
  stato text,
  perito uuid references auth.users on delete set null,
  dati jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists pratiche_owner_idx on public.pratiche (owner);
create index if not exists pratiche_email_idx on public.pratiche (lower(email));
alter table public.pratiche enable row level security;

drop policy if exists "pratiche: lettura" on public.pratiche;
create policy "pratiche: lettura" on public.pratiche for select
  using (owner = auth.uid() or public.ruolo() in ('studio', 'perito')
         or (owner is null and lower(email) = lower(auth.jwt() ->> 'email')));
drop policy if exists "pratiche: il cliente crea le sue" on public.pratiche;
create policy "pratiche: il cliente crea le sue" on public.pratiche for insert
  with check (owner = auth.uid() or public.ruolo() = 'studio');
drop policy if exists "pratiche: modifica" on public.pratiche;
create policy "pratiche: modifica" on public.pratiche for update
  using (owner = auth.uid() or public.ruolo() in ('studio', 'perito')
         or (owner is null and lower(email) = lower(auth.jwt() ->> 'email')))
  with check (owner = auth.uid() or public.ruolo() in ('studio', 'perito'));
drop policy if exists "pratiche: solo lo studio elimina" on public.pratiche;
create policy "pratiche: solo lo studio elimina" on public.pratiche for delete using (public.ruolo() = 'studio');

-- Il cliente non può cambiare proprietario o perito assegnato
create or replace function public.pratiche_protezione() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  new.updated_at := now();
  if tg_op = 'UPDATE' and auth.uid() is not null and coalesce(public.ruolo(), 'cliente') = 'cliente' then
    -- una pratica pagata prima di creare l'accesso passa al cliente con la stessa email
    new.owner := coalesce(old.owner, case when lower(old.email) = lower(auth.jwt() ->> 'email') then auth.uid() end);
    new.perito := old.perito;
    -- il cliente non può segnare da solo una pratica come pagata
    if coalesce((old.dati ->> 'pagato')::boolean, false) is distinct from coalesce((new.dati ->> 'pagato')::boolean, false) then
      new.dati := jsonb_set(new.dati, '{pagato}', coalesce(old.dati -> 'pagato', 'false'::jsonb));
    end if;
  end if;
  return new;
end $$;
drop trigger if exists pratiche_protezione on public.pratiche;
create trigger pratiche_protezione before insert or update on public.pratiche for each row execute function public.pratiche_protezione();

-- 3) Pagamenti: li scrive solo il server (Stripe), mai il browser
create table if not exists public.pagamenti (
  id bigint generated always as identity primary key,
  pratica_id text references public.pratiche (id) on delete set null,
  email text,
  servizi text,
  importo_cent integer not null,
  stripe_session text unique,
  stato text not null default 'pagato',
  created_at timestamptz not null default now()
);
alter table public.pagamenti enable row level security;
drop policy if exists "pagamenti: lettura" on public.pagamenti;
create policy "pagamenti: lettura" on public.pagamenti for select
  using (public.ruolo() = 'studio' or lower(email) = lower(auth.jwt() ->> 'email'));

-- 4) Dopo aver creato gli accessi dello Studio e dei periti dal sito, assegna i ruoli così:
-- update public.profiles set role = 'studio' where email = 'studiotecnicodellavecchia@gmail.com';
-- update public.profiles set role = 'perito' where email = 'email-del-perito@esempio.it';
