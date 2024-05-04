-- preview table "hcahps_data"
select *
from "healthcare_survey"."hospital_data".hcahps_data;

-- preview table "hospital_beds"
select *
from "healthcare_survey"."hospital_data".hospital_beds;

-- format "dates" table "hospital_beds"
select provider_ccn,
    hospital_name,
    to_date(fiscal_year_begin_date, 'MM/DD/YYYY') as fiscal_year_begin_date,
    to_date(fiscal_year_end_date, 'MM/DD/YYYY') as fiscal_year_end_date,
    number_of_beds
from "healthcare_survey"."hospital_data".hospital_beds;

-- col "provider_ccn" table "hospital_beds"
-- convert dtype integer to text USING cast()
-- specify character length 6 characters USING lpad (left padding)
-- preview col "provider_ccn" new and old
select lpad(cast(provider_ccn as text), 6, '0') as provider_ccn,
    provider_ccn,
    hospital_name,
    to_date(fiscal_year_begin_date, 'MM/DD/YYYY') as fiscal_year_begin_date,
    to_date(fiscal_year_end_date, 'MM/DD/YYYY') as fiscal_year_end_date,
    number_of_beds
from "healthcare_survey"."hospital_data".hospital_beds;

-- USING (cte) common table expression
-- remove old col "provider_ccn"
with hospital_beds_prep as (
    select lpad(cast(provider_ccn as text), 6, '0') as provider_ccn,
        hospital_name,
        to_date(fiscal_year_begin_date, 'MM/DD/YYYY') as fiscal_year_begin_date,
        to_date(fiscal_year_end_date, 'MM/DD/YYYY') as fiscal_year_end_date,
        number_of_beds
    from "healthcare_survey"."hospital_data".hospital_beds
)

select *
from hospital_beds_prep;

-- identify duplicates
-- add col "nth_row"
-- table "hospital_beds" 6050 records
with hospital_beds_prep as (
    select lpad(cast(provider_ccn as text), 6, '0') as provider_ccn,
        hospital_name,
        to_date(fiscal_year_begin_date, 'MM/DD/YYYY') as fiscal_year_begin_date,
        to_date(fiscal_year_end_date, 'MM/DD/YYYY') as fiscal_year_end_date,
        number_of_beds,
        row_number() over (
            partition by provider_ccn
            order by to_date(fiscal_year_end_date, 'MM/DD/YYYY') desc
        ) as nth_row
    from "healthcare_survey"."hospital_data".hospital_beds
)

select *
from hospital_beds_prep
order by provider_ccn;

-- remove duplicates
-- table "hospital_beds" 5978 records
with hospital_beds_prep as (
    select lpad(cast(provider_ccn as text), 6, '0') as provider_ccn,
        hospital_name,
        to_date(fiscal_year_begin_date, 'MM/DD/YYYY') as fiscal_year_begin_date,
        to_date(fiscal_year_end_date, 'MM/DD/YYYY') as fiscal_year_end_date,
        number_of_beds,
        row_number() over (
            partition by provider_ccn
            order by to_date(fiscal_year_end_date, 'MM/DD/YYYY') desc
        ) as nth_row
    from "healthcare_survey"."hospital_data".hospital_beds
)

select provider_ccn,
    count(*) as count_of_rows
from hospital_beds_prep
where nth_row = 1
group by provider_ccn
order by count(*) desc;

-----------------------table "hcahps_data"

-- preview table "hcahps_data"
select *
from "healthcare_survey"."hospital_data".hcahps_data;

-- col "facility_id" standardized to 6 characters
-- renamed col "facility_id" to "provider_ccn"
select lpad(cast(facility_id as text), 6, '0') as provider_ccn,
    *
from "healthcare_survey"."hospital_data".hcahps_data;

-- format dates
-- renamed col dates
select lpad(cast(facility_id as text), 6, '0') as provider_ccn,
    to_date(start_date, 'MM/DD/YYYY') as start_date_converted,
    to_date(end_date, 'MM/DD/YYYY') as end_date_converted,
    *
from "healthcare_survey"."hospital_data".hcahps_data;

-- NOTE this block with a join statement, Returns an error, coz of order of operations
-- with hospital_beds_prep as (
--     select lpad(cast(provider_ccn as text), 6, '0') as provider_ccn,
--         hospital_name,
--         to_date(fiscal_year_begin_date, 'MM/DD/YYYY') as fiscal_year_begin_date,
--         to_date(fiscal_year_end_date, 'MM/DD/YYYY') as fiscal_year_end_date,
--         number_of_beds,
--         row_number() over (
--             partition by provider_ccn
--             order by to_date(fiscal_year_end_date, 'MM/DD/YYYY') desc
--         ) as nth_row
--     from "healthcare_survey"."hospital_data".hospital_beds
-- )

-- select lpad(cast(facility_id as text), 6, '0') as provider_ccn,
--     to_date(start_date, 'MM/DD/YYYY') as start_date_converted,
--     to_date(end_date, 'MM/DD/YYYY') as end_date_converted,
--     *
-- from "healthcare_survey"."hospital_data".hcahps_data as hcahps
--     left join hospital_beds_prep as beds on hcahps.provider_ccn = beds.provider_ccn
--     and hcahps.nth_row = 1;
	
-- Top-Down code execution (Not how sql works) termed as "order by operations"
-- select
-- from table 1
-- join table 2
-- on
-- where
-- group by
-- having

-- INSTEAD SQL "order by operations" is as follows:
-- from / join
-- where
-- group by
-- having
-- select
-- order by
-- limit
-- this code addresses the error of joining tables
with hospital_beds_prep as (
    select lpad(cast(provider_ccn as text), 6, '0') as provider_ccn,
        hospital_name,
        to_date(fiscal_year_begin_date, 'MM/DD/YYYY') as fiscal_year_begin_date,
        to_date(fiscal_year_end_date, 'MM/DD/YYYY') as fiscal_year_end_date,
        number_of_beds,
        row_number() over (
            partition by provider_ccn
            order by to_date(fiscal_year_end_date, 'MM/DD/YYYY') desc
        ) as nth_row
    from "healthcare_survey"."hospital_data".hospital_beds
)

select lpad(cast(facility_id as text), 6, '0') as provider_ccn,
    to_date(start_date, 'MM/DD/YYYY') as start_date_converted,
    to_date(end_date, 'MM/DD/YYYY') as end_date_converted,
    *
from "healthcare_survey"."hospital_data".hcahps_data as hcahps
    left join hospital_beds_prep as beds on lpad(cast(facility_id as text), 6, '0') = beds.provider_ccn
    and beds.nth_row = 1;

-- bring in additional cols
-- create tableau file, uncomment line 168, run script, export data as csv
-- create table "healthcare_survey"."hospital_data".Tableau_File as
with hospital_beds_prep as (
    select lpad(cast(provider_ccn as text), 6, '0') as provider_ccn,
        hospital_name,
        to_date(fiscal_year_begin_date, 'MM/DD/YYYY') as fiscal_year_begin_date,
        to_date(fiscal_year_end_date, 'MM/DD/YYYY') as fiscal_year_end_date,
        number_of_beds,
        row_number() over (
            partition by provider_ccn
            order by to_date(fiscal_year_end_date, 'MM/DD/YYYY') desc
        ) as nth_row
    from "healthcare_survey"."hospital_data".hospital_beds
)

select lpad(cast(facility_id as text), 6, '0') as provider_ccn,
    to_date(start_date, 'MM/DD/YYYY') as start_date_converted,
    to_date(end_date, 'MM/DD/YYYY') as end_date_converted,
    hcahps,
    *,
    beds.number_of_beds,
    beds.fiscal_year_begin_date as beds_start_report_period,
    beds.fiscal_year_end_date as beds_end_report_period
from "healthcare_survey"."hospital_data".hcahps_data as hcahps
    left join hospital_beds_prep as beds on lpad(cast(facility_id as text), 6, '0') = beds.provider_ccn
    and beds.nth_row = 1;