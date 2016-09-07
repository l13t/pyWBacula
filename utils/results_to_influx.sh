#!/bin/bash

# generate data in proper influxdb format
export PGPASSWORD="[change_to_your_bacula_password]"
psql -h localhost -U bacula -t -A -F"," -c "select
  pool_name, extract(epoch from job_schedtime)*1000 as job_schedtime, sum(pool_size) as pool_size, sum(jobfiles) as jobfiles
from (select
  pool.name as pool_name, date_trunc('day', job.schedtime) as job_schedtime, job.jobbytes as pool_size, job.jobfiles as jobfiles
from
  pool, job
where
  date_trunc('day', job.schedtime) > now() - interval '28 days' and job.poolid = pool.poolid
union
select
  pool.name as pool_name, date_trunc('day', jobhisto.schedtime) as job_schedtime, jobhisto.jobbytes as pool_size, jobhisto.jobfiles as jobfiles
from
  pool, jobhisto
where
  date_trunc('day', jobhisto.schedtime) > now() - interval '28 days' and jobhisto.poolid = pool.poolid
order by
  job_schedtime, pool_name) as foo
group by pool_name, job_schedtime
order by job_schedtime, pool_name;" | awk -F"," '{printf "bacula,host=%s value=%s %s\n", $1, $3, $2}' > /tmp/bacula.txt
# push data to influxdb
# modify this command if you use login and password for influxdb
curl -H 'Content-Type: text/plain' -i -XPOST 'http://localhost:8086/write?db=bacula' --data-binary @/tmp/bacula.txt
rm /tmp/bacula.txt