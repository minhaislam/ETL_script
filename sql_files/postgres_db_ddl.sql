-- public.customers definition

-- Drop table

-- DROP TABLE public.customers;

CREATE TABLE public.customers (
	customernumber int4 NOT NULL,
	customername varchar NOT NULL,
	contactlastname varchar NOT NULL,
	contactfirstname varchar NOT NULL,
	phone varchar NOT NULL,
	addressline1 varchar NOT NULL,
	addressline2 varchar NULL,
	city varchar NOT NULL,
	state varchar NULL,
	postalcode varchar NULL,
	country varchar NOT NULL,
	salesrepemployeenumber int4 NULL,
	creditlimit numeric NULL,
	CONSTRAINT customers_pk PRIMARY KEY (customernumber)
);

-- public.employees definition

-- Drop table

-- DROP TABLE public.employees;

CREATE TABLE public.employees (
	employeenumber int4 NOT NULL,
	lastname varchar NOT NULL,
	firstname varchar NOT NULL,
	"extension" varchar(10) NOT NULL,
	email varchar(100) NOT NULL,
	officecode varchar(10) NOT NULL,
	reportsto int4 NULL,
	jobtitle varchar(50) NOT NULL,
	CONSTRAINT employees_pk PRIMARY KEY (employeenumber)
);



-- public.offices definition

-- Drop table

-- DROP TABLE public.offices;

CREATE TABLE public.offices (
	officecode varchar(10) NOT NULL,
	city varchar(50) NOT NULL,
	phone varchar(50) NOT NULL,
	addressline1 varchar(50) NOT NULL,
	addressline2 varchar(50) NULL,
	state varchar(50) NULL,
	country varchar(50) NOT NULL,
	postalcode varchar(15) NOT NULL,
	territory varchar(10) NOT NULL,
	CONSTRAINT offices_pk PRIMARY KEY (officecode)
);


-- public.orderdetails definition

-- Drop table

-- DROP TABLE public.orderdetails;

CREATE TABLE public.orderdetails (
	ordernumber int4 NOT NULL,
	productcode varchar(15) NOT NULL,
	quantityordered int4 NOT NULL,
	priceeach numeric(10, 2) NOT NULL,
	orderlinenumber int2 NOT NULL,
	CONSTRAINT orderdetails_pk PRIMARY KEY (ordernumber, productcode)
);


-- public.orders definition

-- Drop table

-- DROP TABLE public.orders;

CREATE TABLE public.orders (
	ordernumber int4 NOT NULL,
	orderdate date NOT NULL,
	requireddate date NOT NULL,
	shippeddate date NULL,
	status varchar(15) NOT NULL,
	"comments" text NULL,
	customernumber int4 NOT NULL,
	CONSTRAINT orders_pk PRIMARY KEY (ordernumber)
);


-- public.payments definition

-- Drop table

-- DROP TABLE public.payments;

CREATE TABLE public.payments (
	customernumber int4 NOT NULL,
	checknumber varchar(50) NOT NULL,
	paymentdate date NOT NULL,
	amount numeric(10, 2) NOT NULL,
	CONSTRAINT payments_pk PRIMARY KEY (customernumber, checknumber)
);


-- public.productlines definition

-- Drop table

-- DROP TABLE public.productlines;

CREATE TABLE public.productlines (
	productline varchar(50) NOT NULL,
	textdescription varchar(4000) NULL,
	htmldescription text NULL,
	image text NULL,
	CONSTRAINT productlines_pk PRIMARY KEY (productline)
);


-- public.products definition

-- Drop table

-- DROP TABLE public.products;

CREATE TABLE public.products (
	productcode varchar(15) NOT NULL,
	productname varchar(70) NOT NULL,
	productline varchar(50) NOT NULL,
	productscale varchar(10) NOT NULL,
	productvendor varchar(50) NOT NULL,
	productdescription text NOT NULL,
	quantityinstock int4 NOT NULL,
	buyprice numeric(10, 2) NOT NULL,
	msrp numeric(10, 2) NOT NULL,
	CONSTRAINT products_pk PRIMARY KEY (productcode)
);



-- public.data_etl_log definition

-- Drop table

-- DROP TABLE public.data_etl_log;

CREATE TABLE public.data_etl_log (
	table_name varchar NULL,
	row_count varchar NULL,
	data_insertion_time timestamptz NOT NULL DEFAULT now()
);