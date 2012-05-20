create table cat_analysis
as select category as category, word as word, sum(freq) as cfreq, sum(total) as ctotal
from word_analysis
where freq > 1
group by category, word;
