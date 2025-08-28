-- public."0-1:24.2.3" definition

-- Drop table

-- DROP TABLE public."0-1:24.2.3";

CREATE TABLE public."0-1:24.2.3" (
                                     ts timestamptz NOT NULL,
                                     value numeric(10, 3) NOT NULL,
                                     CONSTRAINT "0-1:24.2.3_pk" PRIMARY KEY (ts)
);


-- public."0-2:24.2.1" definition

-- Drop table

-- DROP TABLE public."0-2:24.2.1";

CREATE TABLE public."0-2:24.2.1" (
                                     ts timestamptz NOT NULL,
                                     value numeric(10, 3) NOT NULL,
                                     CONSTRAINT "0-2:24.2.1_pk" PRIMARY KEY (ts)
);


-- public."1-0:1.6.0" definition

-- Drop table

-- DROP TABLE public."1-0:1.6.0";

CREATE TABLE public."1-0:1.6.0" (
                                    ts timestamptz NOT NULL,
                                    value numeric(10, 3) NOT NULL,
                                    CONSTRAINT "1-0:1.6.0_pk" PRIMARY KEY (ts)
);


-- public."1-0:1.7.0" definition

-- Drop table

-- DROP TABLE public."1-0:1.7.0";

CREATE TABLE public."1-0:1.7.0" (
                                    ts timestamptz NOT NULL,
                                    value numeric(10, 3) NOT NULL,
                                    CONSTRAINT "1-0:1.7.0_pk" PRIMARY KEY (ts)
);


-- public."1-0:1.8.1" definition

-- Drop table

-- DROP TABLE public."1-0:1.8.1";

CREATE TABLE public."1-0:1.8.1" (
                                    ts timestamptz NOT NULL,
                                    value numeric(10, 3) NOT NULL,
                                    CONSTRAINT "1-0:1.8.1_pk" PRIMARY KEY (ts)
);


-- public."1-0:1.8.2" definition

-- Drop table

-- DROP TABLE public."1-0:1.8.2";

CREATE TABLE public."1-0:1.8.2" (
                                    ts timestamptz NOT NULL,
                                    value numeric(10, 3) NOT NULL,
                                    CONSTRAINT "1-0:1.8.2_pk" PRIMARY KEY (ts)
);


-- public."1-0:2.7.0" definition

-- Drop table

-- DROP TABLE public."1-0:2.7.0";

CREATE TABLE public."1-0:2.7.0" (
                                    ts timestamptz NOT NULL,
                                    value numeric(10, 3) NOT NULL,
                                    CONSTRAINT "1-0:2.7.0_pk" PRIMARY KEY (ts)
);


-- public."1-0:2.8.1" definition

-- Drop table

-- DROP TABLE public."1-0:2.8.1";

CREATE TABLE public."1-0:2.8.1" (
                                    ts timestamptz NOT NULL,
                                    value numeric(10, 3) NOT NULL,
                                    CONSTRAINT "1-0:2.8.1_pk" PRIMARY KEY (ts)
);


-- public."1-0:2.8.2" definition

-- Drop table

-- DROP TABLE public."1-0:2.8.2";

CREATE TABLE public."1-0:2.8.2" (
                                    ts timestamptz NOT NULL,
                                    value numeric(10, 3) NOT NULL,
                                    CONSTRAINT "1-0:2.8.2_pk" PRIMARY KEY (ts)
);


-- public.omnik definition

-- Drop table

-- DROP TABLE public.omnik;

CREATE TABLE public.omnik (
                              ts timestamptz NOT NULL,
                              today numeric(4, 2) NULL,
                              total numeric(6, 1) NULL,
                              CONSTRAINT omnik_pk PRIMARY KEY (ts)
);


-- public.omnikpower definition

-- Drop table

-- DROP TABLE public.omnikpower;

CREATE TABLE public.omnikpower (
                                   ts timestamptz NOT NULL,
                                   power int2 NULL,
                                   CONSTRAINT omnikpower_pk PRIMARY KEY (ts)
);