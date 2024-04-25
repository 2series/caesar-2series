## Qs

>max total layoffs
SELECT MAX(total_laid_off)
FROM layoffs_staging2;

>Look at percentage to see how big layoffs were
SELECT MAX(percentage_laid_off),  MIN(percentage_laid_off)
FROM layoffs_staging2
WHERE percentage_laid_off IS NOT NULL;

>Layoffs by <company>
>Which companies had 100% layoffs
SELECT *
FROM layoffs_staging2
WHERE percentage_laid_off = 1;

>Which companies had a 100% layoff? order by total layoffs descending
SELECT *
FROM layoffs_staging2
WHERE percentage_laid_off = 1
ORDER BY total_laid_off DESC;

>Which companies had 100% layoffs based on funds raised? order by funds raised descending
SELECT *
FROM layoffs_staging2
WHERE  percentage_laid_off = 1
ORDER BY funds_raised_millions DESC;

>which companies had the most layoffs? sum total_laid_off. group by company and order by 2 descending
SELECT company, SUM(total_laid_off) AS total_laid_off
FROM layoffs_staging2
GROUP BY company
ORDER BY total_laid_off DESC;

>video
SELECT company, SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY company
ORDER BY 2 DESC;

>look at `date` range of layoffs
SELECT MAX(new_date), MIN(new_date)
FROM layoffs_staging2;


>Layoffs by <industry>:
>which industry had the most layoffs? sum total_laid_off. group by industry and order by 2 descending 
SELECT industry, SUM(total_laid_off) AS total_laid_off
FROM layoffs_staging2
GROUP BY industry
ORDER BY total_laid_off DESC;

>video
SELECT industry, SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY industry
ORDER BY 2 DESC;

>Layoffs by <country>:
>which country had the most layoffs? sum total_laid_off. group by country and order by 2 descending
SELECT country, SUM(total_laid_off) AS total_laid_off
FROM layoffs_staging2
GROUP BY country
ORDER BY total_laid_off DESC;


>Layoff by <date>:
>in which date period had the most layoffs? sum total_laid_off. group by date and order by 2 descending
SELECT date, SUM(total_laid_off) AS total_laid_off
FROM layoffs_staging2
GROUP BY new_date
ORDER BY total_laid_off DESC;

>which year had the most layoffs? sum total_laid_off. group by year and order by 2 descending
SELECT year(date), SUM(total_laid_off) AS total_laid_off
FROM layoffs_staging2
GROUP BY year(new_date)
ORDER BY total_laid_off DESC;


>Layoff by <stage>:
>which stage had the most layoffs? sum total_laid_off. group by stage and order by 2 descending
SELECT stage, SUM(total_laid_off) AS total_laid_off
FROM layoffs_staging2
GROUP BY stage
ORDER BY total_laid_off DESC;


>Layoff by <Rolling month totol>:
>Layoff by rolling total of layoffs by month (rolling 12 months) and year and is not null
SELECT date, SUM(total_laid_off) AS total_laid_off
FROM layoffs_staging2
WHERE date IS NOT NULL
GROUP BY date
ORDER BY date DESC;

>video
select substring(new_date, 1, 7), sum(total_laid_off) as total_laid_off
from layoffs_staging2
where substring(new_date, 1, 7) is not null
group by 'month'
order by 1 asc;

>video - now use it in a CTE so we can query off of it
><CTE> (Common Table Expression): a temporary result set that is defined within a SELECT, INSERT, UPDATE, or DELETE statement.
><Rolling total>: a calculation that adds up the values in a column over a specified period of time.
><Partition by>: a clause that divides a result set into partitions based on one or more columns.
WITH DATE_CTE AS 
(
SELECT SUBSTRING(date,1,7) as dates, SUM(total_laid_off) AS total_laid_off
FROM layoffs_staging2
GROUP BY dates
ORDER BY dates ASC
)
SELECT dates, SUM(total_laid_off) OVER (ORDER BY dates ASC) as rolling_total_layoffs
FROM DATE_CTE
ORDER BY dates ASC;

>Layoff by <Rolling month, company, industry, country totols>:

>Layoff by <Rolling year, company, industry, country totols rankings> partition by year oreder by total_laid_off DESC and ranked by <= 5. i.e companies that have had the most layoffs over time:


