-- ============================================================
-- Script SQL para crear la tabla "items" en Supabase.
-- Ejecutar este script en el SQL Editor de Supabase.
-- ============================================================

-- Activamos la extensión pgcrypto para poder generar UUIDs.
-- Un UUID es un identificador único universal, como un "DNI" para cada fila.
create extension if not exists "pgcrypto";

-- Creamos la tabla "items" en el schema público.
-- Cada fila de esta tabla representa un producto o item.
create table if not exists public.items (

  -- "id" es la clave primaria. Se genera automáticamente con un UUID.
  -- El usuario NO necesita enviar este campo al crear un item.
  id uuid primary key default gen_random_uuid(),

  -- "name" es el nombre del item. Es obligatorio (not null).
  name text not null,

  -- "description" es una descripción opcional del item.
  -- Si no se envía, queda como NULL (vacío).
  description text,

  -- "price" es el precio. Acepta hasta 10 dígitos con 2 decimales.
  -- El "check" impide que se guarden precios negativos.
  price numeric(10, 2) not null check (price >= 0),

  -- "available" indica si el item está disponible.
  -- Si no se envía, por defecto queda en true (disponible).
  available boolean not null default true,

  -- "created_at" guarda la fecha y hora de creación.
  -- Se genera automáticamente con now() (la hora actual del servidor).
  created_at timestamptz not null default now(),

  -- "updated_at" guarda la fecha de la última actualización.
  -- También se genera automáticamente, y un trigger la actualiza
  -- cada vez que se modifica la fila (ver más abajo).
  updated_at timestamptz not null default now()
);

-- Creamos un índice para que las consultas ordenadas por fecha
-- de creación sean más rápidas. "desc" significa orden descendente
-- (los más recientes primero).
create index if not exists idx_items_created_at
  on public.items (created_at desc);

-- Creamos una función que se ejecutará automáticamente (trigger).
-- Su único trabajo es actualizar el campo "updated_at" con la hora actual
-- cada vez que se modifica una fila.
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

-- Eliminamos el trigger si ya existe, para evitar duplicados.
drop trigger if exists trg_items_updated_at on public.items;

-- Creamos el trigger: antes de cada UPDATE en la tabla items,
-- PostgreSQL ejecutará la función set_updated_at() automáticamente.
-- Así no necesitamos actualizar "updated_at" manualmente desde Python.
create trigger trg_items_updated_at
before update on public.items
for each row
execute function public.set_updated_at();
