select
    lid, lname, ssfid, ssfname, sfid, sfname, fid, fname, jd
from
(
select
    --l.id, l.name, ssf.id, ssf.name, sf.id, sf.name, f.id, f.name
    l.id as lid, l.name as lname, l.jsondata as jd,
    ssf.id as ssfid, ssf.name as ssfname, 
    sf.id as sfid, sf.name as sfname, 
    f.id as fid, f.name as fname,
    l.pk as lpk,
    sf.pk as sfpk,
    ssf.pk as ssfpk
from
    language as l,
    languoid as ll
left join
    language as f
on
    ll.family_pk = f.pk
left join
    languoid as ff
on
    f.pk = ff.pk
left join
    languoid as sff
on
    sff.father_pk = f.pk
left join
    language as sf
on
    sff.pk = sf.pk
left join
    languoid as ssff
on
    ssff.father_pk = sf.pk
left join
    language as ssf
on
    ssff.pk = ssf.pk
where 
    l.pk = ll.pk and
    l.active = true and
    ll.level = 'language' and
    ll.status = 'established' 
order by
    f.name, sf.name, ssf.name, l.name
) as s
where
    (s.sfpk is null or s.sfpk in (select parent_pk from treeclosuretable where child_pk = s.lpk)) and
    (s.ssfpk is null or s.ssfpk in (select parent_pk from treeclosuretable where child_pk = s.lpk))
;
