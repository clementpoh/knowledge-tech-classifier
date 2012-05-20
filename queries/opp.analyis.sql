 create table opp_analysis as
 select t1.category as category
    , t1.word as word
    , avg(t1.cfreq) as cfreq
    , avg(t1.ctotal) as ctotal
    , sum(case when t1.category=t2.category then 0 else t2.cfreq end) as xcfreq
    , sum(case when t1.category=t2.category then 0 else t2.ctotal end) as xctotal
from cat_analysis as t1, cat_analysis as t2 
where t1.word = t2.word
group by t1.category, t1.word;
