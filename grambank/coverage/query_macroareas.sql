select 
    l.id, m.name, m.id 
from 
    language as l, languoid as ll, languoidmacroarea as lm, macroarea as m
where 
    l.pk = ll.pk and ll.pk = lm.languoid_pk and lm.macroarea_pk = m.pk and l.active and ll.level = 'language' 
order by 
    l.id
