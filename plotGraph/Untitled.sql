use test

create table all_prob_203_203 as 
select distinct ADMTNG_ICD9_DGNS_CD, CLM_ADMSN_WEEK, ICD9_DGNS_CD_1, cond_prob from all_probs 
where ADMTNG_ICD9_DGNS_CD = 203 and ICD9_DGNS_CD_1 = 203



select distinct ADMTNG_ICD9_DGNS_CD, ICD9_DGNS_CD_1 ,count(*) from all_probs group by 
ADMTNG_ICD9_DGNS_CD, ICD9_DGNS_CD_1 order by 3 desc

select * from all_prob_203_203 --Osteoarthros
select * from all_probs

select ADMTNG_ICD9_DGNS_CD, b.CCS_CATEGORY_DESCRIPTION , ICD9_DGNS_CD_1, c.CCS_CATEGORY_DESCRIPTION
from all_probs a left join diag_codes as b on a.ADMTNG_ICD9_DGNS_CD = b.CCS_CATEGORY
left join diag_codes as c on a.ICD9_DGNS_CD_1 = c.CCS_CATEGORY


select * from diag_codes

Error Code: 1054. Unknown column 'all_probs.ADMTNG_ICD9_DGNS_CD' in 'on clause'
