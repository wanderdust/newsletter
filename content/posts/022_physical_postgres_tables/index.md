---
title: '022_physical_postgres_tables'
date: '2025-08-11T19:49:37+01:00'
draft: true 
summary: ''
tags: []
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---

In this blog post I want to demistify Postgres to show that it is not that scary under the hood. 

I will do a step by step walk through so that we create a table and inspect what it looks like under the hood.

## The Setup

To setup this experiment, we will install Postgres locally and create table.

**Install & start Postgres**

Install postgres using brew
```bash
brew install postgresql@17
```

Start the database service
```bash
brew services start postgresql@17
```

Use psql create a shell inside the database where we can start running commands.

```bash
psql postgres
```

The next step is to create a dummy table. Run the following queries within the psql console.

```sql
CREATE TABLE films (
    code        char(5) CONSTRAINT firstkey PRIMARY KEY,
    title       varchar(40) NOT NULL,
    did         integer NOT NULL,
    date_prod   date,
    kind        varchar(10),
    len         interval hour to minute
);
```

and add some data to the table

```SQL
INSERT INTO films (code, title, did, date_prod, kind, len) VALUES
('B6717', 'The Shawshank Redemption', 101, '1994-09-23', 'Drama', '02:22'),
('C8874', 'Inception',                102, '2010-07-16', 'Sci-Fi', '02:28'),
('A1234', 'The Godfather',            103, '1972-03-24', 'Crime', '02:55'),
('D4521', 'Interstellar',             104, '2014-11-07', 'Sci-Fi', '02:49'),
('E7789', 'Parasite',                  105, '2019-05-30', 'Thriller', '02:12');
```

## Physical Structure of Postgres

A postgres database is basically a single directory containing all its data inside it. 

In Postgres, we can find this directory by running this query inside psql

```sql
show data_directory;

> /opt/homebrew/var/postgresql@17
```

## Digging in


Use this function to find out where the table lives.

```sql
SELECT pg_relation_filepath('films');

pg_relation_filepath
----------------------
  base/5/16388
 (1 row)
```

We can verify this by running

```
ls -lah /opt/homebrew/var/postgresql@17/base/5/16388
-rw-------@ 1 pablolopez  admin   8.0K 11 Aug 20:08 /opt/homebrew/var/postgresql@17/base/5/16388
```

The tables are stored in the `base` directory. The number `5` refers to the Database Object ID (OID) `Postgres`. We can verify this by looking at the database name with ID 5. 

```sql
SELECT oid, datname
FROM pg_database
WHERE oid = 5;

 oid | datname
-----+----------
   5 | postgres
(1 row)
```

And `16388` is the table relfiledode, which is the ID that identifies the data file. We can verify by running

```sql
SELECT relname, oid, relfilenode FROM pg_class WHERE relname = 'films'

 relname |  oid  | relfilenode
---------+-------+-------------
 films   | 16388 |       16388
(1 row)
```
In this case the relfilenode is the same as the OID.

## Postgres Tables

Inside a data file, it is divided into pages. Pages have fixed lenght which is 8192 bytes (8 KB) by default. The internal layout depends on the data type (table, indexes). Lets try to visualise the table file directly:


```bash
cat /opt/homebrew/var/postgresql@17/base/5/16388
C8874InceptionfhSci-Fi�id\�
Drama���%
```

The page is divided into 2 sections, the page header and the data tuples which contain the actual data.

To view the page headers we can run the following command

```sql
SELECT * FROM page_header(get_raw_page('films', 0));

    lsn    | checksum | flags | lower | upper | special | pagesize | version | prune_xid
-----------+----------+-------+-------+-------+---------+----------+---------+-----------
 0/15DA5B0 |        0 |     0 |   380 |   400 |    8192 |     8192 |       4 |         0
(1 row)
```

To view the actual tuples and the line pointers we can run these commands

```sql
SELECT *
FROM heap_page_items(get_raw_page('films', 0));

lp | lp_off | lp_flags | lp_len | t_xmin | t_xmax | t_field3 | t_ctid | t_infomask2 | t_infomask | t_hoff | t_bits | t_oid |                                                               t_data
----+--------+----------+--------+--------+--------+----------+--------+-------------+------------+--------+--------+-------+------------------------------------------------------------------------------------------------------------------------------------
  1 |   8104 |        1 |     88 |    750 |      0 |        0 | (0,1)  |           6 |       2306 |     24 |        |       | \x0d42363731373354686520536861777368616e6b20526564656d7074696f6e00650000007af8ffff0d4472616d61000000e2d4fb010000000000000000000000
  2 |   8032 |        1 |     72 |    750 |      0 |        0 | (0,2)  |           6 |       2306 |     24 |        |       | \x0d433838373415496e63657074696f6e66000000090f00000f5363692d466900000c4a11020000000000000000000000
  3 |   7952 |        1 |     80 |    750 |      0 |        0 | (0,3)  |           6 |       2306 |     24 |        |       | \x0d41313233341d54686520476f646661746865726700000060d8ffff0d4372696d650000000000000049d971020000000000000000000000
  4 |   7872 |        1 |     80 |    750 |      0 |        0 | (0,4)  |           6 |       2306 |     24 |        |       | \x0d44343532311b496e7465727374656c6c61720068000000301500000f5363692d46690000000000001f645c020000000000000000000000
  5 |   7792 |        1 |     80 |    750 |      0 |        0 | (0,5)  |           6 |       2306 |     24 |        |       | \x0d45373738391350617261736974650069000000b11b000013546872696c6c657200000000000000009c11d8010000000000000000000000
(5 rows)
```

Some definitions of the relevant items
- tuple: contains a row of data
- lp: line pointer id, or the position of the tuple
- lp_off: line pointer offset in bytes where the data tuple begins
- lp_flags:  1 = normal tuple, others indicate dead, redirected, etc.
- lp_len: lenght in bytes of the tuple
- t_xmin: transaction id that inserted this tuple
- t_xmax: transaction id that deleted this tuple (0 if still alive)
- t_ctid: physical location of this tuple as (block_number, offset_number).
- t_data: Raw tuple data bytes (hex-encoded)



## Reading the data - Reading

How does postgres find the tuples when a read query is exected. Lets take a sequential scan as an example. In a sequential scan, each page in the data file (heap table) is scanned and all the tuples in the scanned are checked.

Lets take this example query

```sql
SELECT * FROM films
WHERE title = 'Inception';
```

THis is the process to find the tuples.
1. Read the first page header to find the line pointer ids, and offsets
2. For each tuple, 
  - Use the line pointer to find the tuple in the page
  - Check transaction visibility (t_xmin, t_xmax, t_infomask) to see if the tuple is visible to your transaction (MVCC rules) (Out of scope - point to docs)
  - If visible decode the tuple's data columns and evaluate the WHERE condition
3. If condition is not met continue to end of page. Move on to next page afterwards
4. Stop when all pages have been scanned or a limit condition is met.

### Index scans

Index data is similarly stored to data files. For index files, each index tuple points to the correct tuples in the data files.


## Inserting and deleting tuples

todo

# Resources

https://www.interdb.jp/pg/pgsql01/03.html
