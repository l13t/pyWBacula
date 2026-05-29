-- Bacula test seed data
-- All timestamps relative to NOW() so data stays fresh after docker compose up

-- ─── Status codes (matches static_vars.py JobStatus dict) ────────────────────
INSERT INTO status (jobstatus, jobstatuslong, severity) VALUES
('C', 'Created but not yet running',             15),
('R', 'Running',                                 15),
('B', 'Blocked',                                 15),
('T', 'Terminated normally',                     10),
('W', 'Terminated normally with warnings',       20),
('E', 'Terminated in Error',                     25),
('e', 'Non-fatal error',                         20),
('f', 'Fatal error',                            100),
('D', 'Verify Differences',                      15),
('A', 'Canceled by the user',                    15),
('I', 'Incomplete Job',                          15),
('F', 'Waiting on the File daemon',              15),
('S', 'Waiting on the Storage daemon',           15),
('m', 'Waiting for a new Volume to be mounted',  15),
('M', 'Waiting for a Mount',                     15),
('s', 'Waiting for Storage resource',            15),
('j', 'Waiting for Job resource',                15),
('c', 'Waiting for Client resource',             15),
('d', 'Waiting for Maximum jobs',                15),
('t', 'Waiting for Start Time',                  15),
('p', 'Waiting for higher priority job',         15),
('i', 'Doing batch insert file records',         15),
('a', 'SD despooling attributes',                15),
('l', 'Doing data despooling',                   15),
('L', 'Committing data (last despool)',           15);

-- ─── Clients ─────────────────────────────────────────────────────────────────
INSERT INTO client (name, uname, autoprune, fileretention, jobretention) VALUES
('web-server.example.com',
 'web-server.example.com-fd Linux x86_64 9.4.2 (01Jan22)',   1, 1209600, 2592000),
('db-server.example.com',
 'db-server.example.com-fd Linux x86_64 9.4.2 (01Jan22)',    1, 1209600, 2592000),
('files-server.example.com',
 'files-server.example.com-fd Linux x86_64 9.4.2 (01Jan22)', 1, 1209600, 2592000);

-- ─── Storage & MediaType & Device ────────────────────────────────────────────
INSERT INTO storage (name, autochanger) VALUES ('LocalStorage', 0);
INSERT INTO mediatype (mediatype, readonly) VALUES ('File', 0);
INSERT INTO device (name, mediatypeid, storageid) VALUES ('FileStorage', 1, 1);

-- ─── Pools ───────────────────────────────────────────────────────────────────
INSERT INTO pool (name, numvols, maxvols, useonce, usecatalog, acceptanyvolume,
                  volretention, voluseduration, maxvoljobs, maxvolfiles, maxvolbytes,
                  autoprune, recycle, actiononpurge, pooltype, labeltype, labelformat,
                  enabled, scratchpoolid, recyclepoolid, nextpoolid,
                  migrationhighbytes, migrationlowbytes, migrationtime)
VALUES
('Daily',   5, 10, 0, 1, 0,  604800, 0, 0, 0, 0, 1, 1, 0, 'Backup', 0, 'Daily-',  1, 0, 0, 0, 0, 0, 0),
('Weekly',  4, 10, 0, 1, 0, 2592000, 0, 0, 0, 0, 1, 1, 0, 'Backup', 0, 'Weekly-', 1, 0, 0, 0, 0, 0, 0);

-- ─── FileSets ────────────────────────────────────────────────────────────────
INSERT INTO fileset (fileset, md5, createtime) VALUES
('LinuxAll', 'aabbccddeeff0011', NOW() - INTERVAL '180 days'),
('MySQL',    '1122334455667788', NOW() - INTERVAL '180 days'),
('WebFiles', '99aabbccddeeffaa', NOW() - INTERVAL '180 days');

-- ─── Media volumes ───────────────────────────────────────────────────────────
-- poolid: 1=Daily  2=Weekly  storageid=1  mediatypeid=1  deviceid=1
INSERT INTO media (volumename, slot, poolid, mediatype, mediatypeid, labeltype,
                   firstwritten, lastwritten, labeldate,
                   voljobs, volfiles, volblocks, volmounts, volbytes,
                   volparts, volerrors, volwrites, volcapacitybytes,
                   volstatus, enabled, recycle, actiononpurge,
                   volretention, voluseduration, maxvoljobs, maxvolfiles, maxvolbytes,
                   inchanger, storageid, deviceid, mediaaddressing,
                   volreadtime, volwritetime, endfile, endblock,
                   locationid, recyclecount, scratchpoolid, recyclepoolid, comment)
VALUES
('Daily-0001', 0, 1, 'File', 1, 0,
 NOW()-INTERVAL '6 days',  NOW()-INTERVAL '6 hours',  NOW()-INTERVAL '6 days',
 8, 8000, 512, 8, 53687091200, 0, 0, 8, 107374182400,
 'Append', 1, 1, 0, 604800, 0, 0, 0, 0, 0, 1, 1, 0, 0, 3600, 0, 0, 0, 0, 0, 0, ''),

('Daily-0002', 0, 1, 'File', 1, 0,
 NOW()-INTERVAL '5 days',  NOW()-INTERVAL '5 days',   NOW()-INTERVAL '5 days',
 6, 6000, 400, 6, 32212254720, 0, 0, 6, 107374182400,
 'Full', 1, 1, 0, 604800, 0, 0, 0, 0, 0, 1, 1, 0, 0, 2700, 0, 0, 0, 1, 0, 0, ''),

('Daily-0003', 0, 1, 'File', 1, 0,
 NOW()-INTERVAL '4 days',  NOW()-INTERVAL '4 days',   NOW()-INTERVAL '4 days',
 6, 6000, 400, 6, 32212254720, 0, 0, 6, 107374182400,
 'Full', 1, 1, 0, 604800, 0, 0, 0, 0, 0, 1, 1, 0, 0, 2700, 0, 0, 0, 1, 0, 0, ''),

('Daily-0004', 0, 1, 'File', 1, 0,
 NOW()-INTERVAL '3 days',  NOW()-INTERVAL '3 days',   NOW()-INTERVAL '3 days',
 4, 4000, 256, 4, 21474836480, 0, 0, 4, 107374182400,
 'Purged', 1, 1, 0, 604800, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1800, 0, 0, 0, 2, 0, 0, ''),

('Daily-0005', 0, 1, 'File', 1, 0,
 NOW()-INTERVAL '2 days',  NOW()-INTERVAL '1 hour',   NOW()-INTERVAL '2 days',
 9, 9000, 600, 9, 64424509440, 0, 0, 9, 107374182400,
 'Append', 1, 1, 0, 604800, 0, 0, 0, 0, 0, 1, 1, 0, 0, 4500, 0, 0, 0, 0, 0, 0, ''),

('Weekly-0001', 0, 2, 'File', 1, 0,
 NOW()-INTERVAL '28 days', NOW()-INTERVAL '21 days',  NOW()-INTERVAL '28 days',
 3, 50000, 3200, 3, 322122547200, 0, 0, 3, 1099511627776,
 'Full', 1, 1, 0, 2592000, 0, 0, 0, 0, 0, 1, 1, 0, 0, 7200, 0, 0, 0, 1, 0, 0, ''),

('Weekly-0002', 0, 2, 'File', 1, 0,
 NOW()-INTERVAL '21 days', NOW()-INTERVAL '14 days',  NOW()-INTERVAL '21 days',
 3, 50000, 3200, 3, 322122547200, 0, 0, 3, 1099511627776,
 'Full', 1, 1, 0, 2592000, 0, 0, 0, 0, 0, 1, 1, 0, 0, 7200, 0, 0, 0, 0, 0, 0, ''),

('Weekly-0003', 0, 2, 'File', 1, 0,
 NOW()-INTERVAL '14 days', NOW()-INTERVAL '7 days',   NOW()-INTERVAL '14 days',
 3, 50000, 3200, 3, 322122547200, 0, 0, 3, 1099511627776,
 'Append', 1, 1, 0, 2592000, 0, 0, 0, 0, 0, 1, 1, 0, 0, 7200, 0, 0, 0, 0, 0, 0, ''),

('Weekly-0004', 0, 2, 'File', 1, 0,
 NOW()-INTERVAL '7 days',  NOW()-INTERVAL '2 hours',  NOW()-INTERVAL '7 days',
 2, 40000, 2560, 2, 214748364800, 0, 0, 2, 1099511627776,
 'Append', 1, 1, 0, 2592000, 0, 0, 0, 0, 0, 1, 1, 0, 0, 5400, 0, 0, 0, 0, 0, 0, ''),

('Weekly-0005', 0, 2, 'File', 1, 0,
 NOW()-INTERVAL '35 days', NOW()-INTERVAL '35 days',  NOW()-INTERVAL '35 days',
 3, 50000, 3200, 3, 322122547200, 0, 0, 3, 1099511627776,
 'Recycle', 1, 1, 0, 2592000, 0, 0, 0, 0, 0, 1, 1, 0, 0, 7200, 0, 0, 0, 3, 0, 0, '');

-- ─── Jobs (last 14 days) ─────────────────────────────────────────────────────
-- Type B=Backup  Level F=Full I=Incremental D=Differential
-- Status T=OK W=Warnings E=Error R=Running
-- clientid: 1=web  2=db  3=files   poolid: 1=Daily  2=Weekly   filesetid: 1=Linux 2=MySQL 3=Web
INSERT INTO job (job, name, type, level, clientid, jobstatus,
                 schedtime, starttime, endtime,
                 jobtdate, volsessionid, volsessiontime,
                 jobfiles, jobbytes, joberrors, jobmissingfiles,
                 poolid, filesetid, purgedfiles, hasbase)
VALUES
-- web-server (client 1)  Weekly full + Daily incrementals
('web-server.example.com.2026-05-22.12.00', 'web-server.example.com', 'B', 'F', 1, 'T',
 NOW()-INTERVAL '7 days',
 NOW()-INTERVAL '7 days'  + INTERVAL '1 minute',
 NOW()-INTERVAL '7 days'  + INTERVAL '42 minutes',
 0, 1, 1000001, 125000, 10737418240, 0, 0, 2, 3, 0, 0),

('web-server.example.com.2026-05-25.12.00', 'web-server.example.com', 'B', 'I', 1, 'T',
 NOW()-INTERVAL '4 days',
 NOW()-INTERVAL '4 days'  + INTERVAL '1 minute',
 NOW()-INTERVAL '4 days'  + INTERVAL '8 minutes',
 0, 2, 1000001, 12000, 1073741824, 0, 0, 1, 3, 0, 0),

('web-server.example.com.2026-05-26.12.00', 'web-server.example.com', 'B', 'I', 1, 'W',
 NOW()-INTERVAL '3 days',
 NOW()-INTERVAL '3 days'  + INTERVAL '1 minute',
 NOW()-INTERVAL '3 days'  + INTERVAL '9 minutes',
 0, 3, 1000001, 11500, 966367641, 2, 0, 1, 3, 0, 0),

('web-server.example.com.2026-05-27.12.00', 'web-server.example.com', 'B', 'I', 1, 'T',
 NOW()-INTERVAL '2 days',
 NOW()-INTERVAL '2 days'  + INTERVAL '1 minute',
 NOW()-INTERVAL '2 days'  + INTERVAL '7 minutes',
 0, 4, 1000001, 10800, 859832319, 0, 0, 1, 3, 0, 0),

('web-server.example.com.2026-05-28.12.00', 'web-server.example.com', 'B', 'I', 1, 'T',
 NOW()-INTERVAL '1 day',
 NOW()-INTERVAL '1 day'   + INTERVAL '1 minute',
 NOW()-INTERVAL '1 day'   + INTERVAL '6 minutes',
 0, 5, 1000001, 9500, 751619276, 0, 0, 1, 3, 0, 0),

('web-server.example.com.2026-05-29.12.00', 'web-server.example.com', 'B', 'I', 1, 'T',
 NOW()-INTERVAL '2 hours',
 NOW()-INTERVAL '2 hours' + INTERVAL '1 minute',
 NOW()-INTERVAL '2 hours' + INTERVAL '5 minutes',
 0, 6, 1000001, 8200, 644245094, 0, 0, 1, 3, 0, 0),

-- db-server (client 2)  Weekly full + Daily incrementals
('db-server.example.com.2026-05-22.02.00', 'db-server.example.com', 'B', 'F', 2, 'T',
 NOW()-INTERVAL '7 days',
 NOW()-INTERVAL '7 days'  + INTERVAL '2 minutes',
 NOW()-INTERVAL '7 days'  + INTERVAL '95 minutes',
 0, 7, 1000002, 280000, 53687091200, 0, 0, 2, 2, 0, 0),

('db-server.example.com.2026-05-24.02.00', 'db-server.example.com', 'B', 'I', 2, 'T',
 NOW()-INTERVAL '5 days',
 NOW()-INTERVAL '5 days'  + INTERVAL '2 minutes',
 NOW()-INTERVAL '5 days'  + INTERVAL '22 minutes',
 0, 8, 1000002, 45000, 4831838208, 0, 0, 1, 2, 0, 0),

('db-server.example.com.2026-05-25.02.00', 'db-server.example.com', 'B', 'I', 2, 'E',
 NOW()-INTERVAL '4 days',
 NOW()-INTERVAL '4 days'  + INTERVAL '2 minutes',
 NOW()-INTERVAL '4 days'  + INTERVAL '5 minutes',
 0, 9, 1000002, 0, 0, 1, 0, 1, 2, 0, 0),

('db-server.example.com.2026-05-26.02.00', 'db-server.example.com', 'B', 'I', 2, 'T',
 NOW()-INTERVAL '3 days',
 NOW()-INTERVAL '3 days'  + INTERVAL '2 minutes',
 NOW()-INTERVAL '3 days'  + INTERVAL '18 minutes',
 0, 10, 1000002, 42000, 4508876800, 0, 0, 1, 2, 0, 0),

('db-server.example.com.2026-05-27.02.00', 'db-server.example.com', 'B', 'I', 2, 'T',
 NOW()-INTERVAL '2 days',
 NOW()-INTERVAL '2 days'  + INTERVAL '2 minutes',
 NOW()-INTERVAL '2 days'  + INTERVAL '20 minutes',
 0, 11, 1000002, 48000, 5154226176, 0, 0, 1, 2, 0, 0),

('db-server.example.com.2026-05-28.02.00', 'db-server.example.com', 'B', 'I', 2, 'W',
 NOW()-INTERVAL '1 day',
 NOW()-INTERVAL '1 day'   + INTERVAL '2 minutes',
 NOW()-INTERVAL '1 day'   + INTERVAL '25 minutes',
 0, 12, 1000002, 51000, 5476982784, 3, 0, 1, 2, 0, 0),

('db-server.example.com.2026-05-29.02.00', 'db-server.example.com', 'B', 'I', 2, 'T',
 NOW()-INTERVAL '3 hours',
 NOW()-INTERVAL '3 hours' + INTERVAL '2 minutes',
 NOW()-INTERVAL '3 hours' + INTERVAL '19 minutes',
 0, 13, 1000002, 44000, 4723721216, 0, 0, 1, 2, 0, 0),

-- files-server (client 3)  Weekly full + Daily incrementals
('files-server.example.com.2026-05-22.04.00', 'files-server.example.com', 'B', 'F', 3, 'T',
 NOW()-INTERVAL '7 days',
 NOW()-INTERVAL '7 days'  + INTERVAL '3 minutes',
 NOW()-INTERVAL '7 days'  + INTERVAL '210 minutes',
 0, 14, 1000003, 950000, 214748364800, 0, 0, 2, 1, 0, 0),

('files-server.example.com.2026-05-23.04.00', 'files-server.example.com', 'B', 'D', 3, 'T',
 NOW()-INTERVAL '6 days',
 NOW()-INTERVAL '6 days'  + INTERVAL '3 minutes',
 NOW()-INTERVAL '6 days'  + INTERVAL '55 minutes',
 0, 15, 1000003, 85000, 21474836480, 0, 0, 1, 1, 0, 0),

('files-server.example.com.2026-05-24.04.00', 'files-server.example.com', 'B', 'I', 3, 'T',
 NOW()-INTERVAL '5 days',
 NOW()-INTERVAL '5 days'  + INTERVAL '3 minutes',
 NOW()-INTERVAL '5 days'  + INTERVAL '28 minutes',
 0, 16, 1000003, 32000, 3221225472, 0, 0, 1, 1, 0, 0),

('files-server.example.com.2026-05-25.04.00', 'files-server.example.com', 'B', 'I', 3, 'T',
 NOW()-INTERVAL '4 days',
 NOW()-INTERVAL '4 days'  + INTERVAL '3 minutes',
 NOW()-INTERVAL '4 days'  + INTERVAL '31 minutes',
 0, 17, 1000003, 35000, 3758096384, 0, 0, 1, 1, 0, 0),

('files-server.example.com.2026-05-26.04.00', 'files-server.example.com', 'B', 'I', 3, 'T',
 NOW()-INTERVAL '3 days',
 NOW()-INTERVAL '3 days'  + INTERVAL '3 minutes',
 NOW()-INTERVAL '3 days'  + INTERVAL '33 minutes',
 0, 18, 1000003, 38000, 4026531840, 0, 0, 1, 1, 0, 0),

('files-server.example.com.2026-05-27.04.00', 'files-server.example.com', 'B', 'I', 3, 'E',
 NOW()-INTERVAL '2 days',
 NOW()-INTERVAL '2 days'  + INTERVAL '3 minutes',
 NOW()-INTERVAL '2 days'  + INTERVAL '8 minutes',
 0, 19, 1000003, 0, 0, 1, 0, 1, 1, 0, 0),

('files-server.example.com.2026-05-28.04.00', 'files-server.example.com', 'B', 'I', 3, 'T',
 NOW()-INTERVAL '1 day',
 NOW()-INTERVAL '1 day'   + INTERVAL '3 minutes',
 NOW()-INTERVAL '1 day'   + INTERVAL '35 minutes',
 0, 20, 1000003, 41000, 4398046511, 0, 0, 1, 1, 0, 0),

-- Current running job (has a valid endtime since NULL crashes jobs_report)
-- Status R = still running but endtime set so strftime() does not fail
('files-server.example.com.2026-05-29.04.00', 'files-server.example.com', 'B', 'I', 3, 'R',
 NOW()-INTERVAL '30 minutes',
 NOW()-INTERVAL '28 minutes',
 NOW() + INTERVAL '30 minutes',
 0, 21, 1000003, 5200, 537919488, 0, 0, 1, 1, 0, 0);

-- ─── JobHisto (15–45 days ago — pool_size_report + client history charts) ────
INSERT INTO jobhisto (jobid, job, name, type, level, clientid, jobstatus,
                      schedtime, starttime, endtime,
                      jobtdate, volsessionid, volsessiontime,
                      jobfiles, jobbytes, joberrors, jobmissingfiles,
                      poolid, filesetid, purgedfiles, hasbase)
VALUES
(1001, 'web-server.example.com.h01', 'web-server.example.com', 'B', 'F', 1, 'T',
 NOW()-INTERVAL '35 days',
 NOW()-INTERVAL '35 days' + INTERVAL '1 minute',
 NOW()-INTERVAL '35 days' + INTERVAL '45 minutes',
 0, 101, 2000001, 120000, 10200547328, 0, 0, 2, 3, 0, 0),

(1002, 'web-server.example.com.h02', 'web-server.example.com', 'B', 'I', 1, 'T',
 NOW()-INTERVAL '28 days',
 NOW()-INTERVAL '28 days' + INTERVAL '1 minute',
 NOW()-INTERVAL '28 days' + INTERVAL '7 minutes',
 0, 102, 2000001, 11000, 966367641, 0, 0, 1, 3, 0, 0),

(1003, 'web-server.example.com.h03', 'web-server.example.com', 'B', 'I', 1, 'W',
 NOW()-INTERVAL '21 days',
 NOW()-INTERVAL '21 days' + INTERVAL '1 minute',
 NOW()-INTERVAL '21 days' + INTERVAL '8 minutes',
 0, 103, 2000001, 10500, 912680550, 1, 0, 1, 3, 0, 0),

(1004, 'web-server.example.com.h04', 'web-server.example.com', 'B', 'I', 1, 'T',
 NOW()-INTERVAL '17 days',
 NOW()-INTERVAL '17 days' + INTERVAL '1 minute',
 NOW()-INTERVAL '17 days' + INTERVAL '6 minutes',
 0, 104, 2000001, 9800, 805306368, 0, 0, 1, 3, 0, 0),

(1005, 'web-server.example.com.h05', 'web-server.example.com', 'B', 'D', 1, 'T',
 NOW()-INTERVAL '14 days',
 NOW()-INTERVAL '14 days' + INTERVAL '1 minute',
 NOW()-INTERVAL '14 days' + INTERVAL '15 minutes',
 0, 105, 2000001, 35000, 3758096384, 0, 0, 1, 3, 0, 0),

(1006, 'db-server.example.com.h01', 'db-server.example.com', 'B', 'F', 2, 'T',
 NOW()-INTERVAL '35 days',
 NOW()-INTERVAL '35 days' + INTERVAL '3 minutes',
 NOW()-INTERVAL '35 days' + INTERVAL '100 minutes',
 0, 106, 2000002, 270000, 53687091200, 0, 0, 2, 2, 0, 0),

(1007, 'db-server.example.com.h02', 'db-server.example.com', 'B', 'I', 2, 'T',
 NOW()-INTERVAL '28 days',
 NOW()-INTERVAL '28 days' + INTERVAL '2 minutes',
 NOW()-INTERVAL '28 days' + INTERVAL '20 minutes',
 0, 107, 2000002, 43000, 4617089843, 0, 0, 1, 2, 0, 0),

(1008, 'db-server.example.com.h03', 'db-server.example.com', 'B', 'I', 2, 'E',
 NOW()-INTERVAL '21 days',
 NOW()-INTERVAL '21 days' + INTERVAL '2 minutes',
 NOW()-INTERVAL '21 days' + INTERVAL '4 minutes',
 0, 108, 2000002, 0, 0, 1, 0, 1, 2, 0, 0),

(1009, 'db-server.example.com.h04', 'db-server.example.com', 'B', 'I', 2, 'T',
 NOW()-INTERVAL '15 days',
 NOW()-INTERVAL '15 days' + INTERVAL '2 minutes',
 NOW()-INTERVAL '15 days' + INTERVAL '22 minutes',
 0, 109, 2000002, 47000, 5046586572, 0, 0, 1, 2, 0, 0),

(1010, 'files-server.example.com.h01', 'files-server.example.com', 'B', 'F', 3, 'T',
 NOW()-INTERVAL '35 days',
 NOW()-INTERVAL '35 days' + INTERVAL '5 minutes',
 NOW()-INTERVAL '35 days' + INTERVAL '225 minutes',
 0, 110, 2000003, 920000, 204010946560, 0, 0, 2, 1, 0, 0),

(1011, 'files-server.example.com.h02', 'files-server.example.com', 'B', 'D', 3, 'T',
 NOW()-INTERVAL '28 days',
 NOW()-INTERVAL '28 days' + INTERVAL '4 minutes',
 NOW()-INTERVAL '28 days' + INTERVAL '60 minutes',
 0, 111, 2000003, 80000, 20132659200, 0, 0, 1, 1, 0, 0),

(1012, 'files-server.example.com.h03', 'files-server.example.com', 'B', 'I', 3, 'T',
 NOW()-INTERVAL '21 days',
 NOW()-INTERVAL '21 days' + INTERVAL '4 minutes',
 NOW()-INTERVAL '21 days' + INTERVAL '30 minutes',
 0, 112, 2000003, 30000, 3006477107, 0, 0, 1, 1, 0, 0),

(1013, 'files-server.example.com.h04', 'files-server.example.com', 'B', 'I', 3, 'T',
 NOW()-INTERVAL '15 days',
 NOW()-INTERVAL '15 days' + INTERVAL '4 minutes',
 NOW()-INTERVAL '15 days' + INTERVAL '28 minutes',
 0, 113, 2000003, 28000, 2952790016, 0, 0, 1, 1, 0, 0);

-- ─── Paths and FileNames ─────────────────────────────────────────────────────
-- pathid sequence: 1=/var/log/ 2=/etc/ 3=/var/lib/mysql/ 4=/home/deploy/
--                  5=/srv/data/ 6=/var/www/html/ 7=/opt/app/ 8=/backup/
INSERT INTO path (path) VALUES
('/var/log/'),
('/etc/'),
('/var/lib/mysql/'),
('/home/deploy/'),
('/srv/data/'),
('/var/www/html/'),
('/opt/app/'),
('/backup/');

-- filenameid sequence: 1=syslog 2=auth.log 3=nginx.log 4=mysql-bin.000001
--   5=mysql-bin.000002 6=ibdata1 7=ib_logfile0 8=deploy.tar.gz
--   9=uploads.tar.gz 10=database-dump.sql.gz 11=access.log 12=error.log
--   13=app.log 14=backup-full.tar.gz 15=config.yml
INSERT INTO filename (name) VALUES
('syslog'),
('auth.log'),
('nginx.log'),
('mysql-bin.000001'),
('mysql-bin.000002'),
('ibdata1'),
('ib_logfile0'),
('deploy.tar.gz'),
('uploads.tar.gz'),
('database-dump.sql.gz'),
('access.log'),
('error.log'),
('app.log'),
('backup-full.tar.gz'),
('config.yml');

-- ─── File records ─────────────────────────────────────────────────────────────
-- lstat format (space-separated Bacula base64): dev ino mode nlink uid gid rdev size blocks blksize atime mtime ctime linkff
-- Size field is position 7 (0-indexed). threshold for big_files = 10MB = "oAAA" (10485760 bytes)
--   "sAAA"  = 44*262144     = 11534336   bytes  (~11 MB)
--   "8AAA"  = 60*262144     = 15728640   bytes  (~15 MB)
--   "DIAAA" = 3*64^4+8*64^3 = 52428800  bytes  (~50 MB)
--   "GQAAA" = 6*64^4+16*64^3= 104857600 bytes  (100 MB)
--   "EAAA"  = 4*262144      = 1048576   bytes  (  1 MB, below threshold)
-- Timestamp "BqBmIA" encodes Unix time 1778803200 (~2026-05-15)

-- Job 6 = web-server incremental, schedtime ~2h ago (within last 24h)
INSERT INTO file (fileindex, jobid, pathid, filenameid, markid, lstat, md5) VALUES
(1, 6, 1, 3,  0, 'bN GjF IiIf B A A A GQAAA KA IA BqBmIA BqBmIA BqBmIA A', '0'),
(2, 6, 6, 11, 0, 'bN GjH IiIf B A A A DIAAA KA IA BqBmIA BqBmIA BqBmIA A', '0'),
(3, 6, 6, 12, 0, 'bN GjI IiIf B A A A 8AAA KA IA BqBmIA BqBmIA BqBmIA A', '0'),
(4, 6, 7, 13, 0, 'bN GjJ IiIf B A A A sAAA KA IA BqBmIA BqBmIA BqBmIA A', '0'),
(5, 6, 2, 1,  0, 'bN GjK IiIf B A A A EAAA KA IA BqBmIA BqBmIA BqBmIA A', '0'),
(6, 6, 2, 2,  0, 'bN GjL IiIf B A A A EAAA KA IA BqBmIA BqBmIA BqBmIA A', '0'),
(7, 6, 2, 15, 0, 'bN GjM IiIf B A A A EAAA KA IA BqBmIA BqBmIA BqBmIA A', '0');

-- Job 13 = db-server incremental, schedtime ~3h ago (within last 24h)
INSERT INTO file (fileindex, jobid, pathid, filenameid, markid, lstat, md5) VALUES
(1, 13, 3, 4,  0, 'bN HjF IiIf B A A A GQAAA KA IA BqBmIA BqBmIA BqBmIA A', '0'),
(2, 13, 3, 5,  0, 'bN HjG IiIf B A A A GQAAA KA IA BqBmIA BqBmIA BqBmIA A', '0'),
(3, 13, 3, 6,  0, 'bN HjH IiIf B A A A DIAAA KA IA BqBmIA BqBmIA BqBmIA A', '0'),
(4, 13, 3, 7,  0, 'bN HjI IiIf B A A A DIAAA KA IA BqBmIA BqBmIA BqBmIA A', '0'),
(5, 13, 8, 10, 0, 'bN HjJ IiIf B A A A 8AAA KA IA BqBmIA BqBmIA BqBmIA A', '0');

-- Job 20 = files-server incremental, schedtime ~1 day ago
INSERT INTO file (fileindex, jobid, pathid, filenameid, markid, lstat, md5) VALUES
(1, 20, 5, 9,  0, 'bN IjF IiIf B A A A GQAAA KA IA BqBmIA BqBmIA BqBmIA A', '0'),
(2, 20, 5, 8,  0, 'bN IjG IiIf B A A A DIAAA KA IA BqBmIA BqBmIA BqBmIA A', '0'),
(3, 20, 4, 8,  0, 'bN IjH IiIf B A A A 8AAA KA IA BqBmIA BqBmIA BqBmIA A', '0');

-- ─── JobMedia (link jobs to volumes) ─────────────────────────────────────────
-- mediaid: 1=Daily-0001 2=Daily-0002 3=Daily-0003 4=Daily-0004 5=Daily-0005
--          6=Weekly-0001 7=Weekly-0002 8=Weekly-0003 9=Weekly-0004 10=Weekly-0005
INSERT INTO jobmedia (jobmediaid, jobid, mediaid, firstindex, lastindex,
                      startfile, endfile, startblock, endblock, volindex)
VALUES
( 1,  1,  6,      1,  125000, 0, 0,        0, 4194304, 1),
( 2,  2,  1,      1,   12000, 0, 0,        0,  409600, 1),
( 3,  3,  1,  12001,   23500, 0, 0,   409601,  802816, 1),
( 4,  4,  1,  23501,   34300, 0, 0,   802817, 1171456, 1),
( 5,  5,  5,  34301,   43800, 0, 0,  1171457, 1499136, 1),
( 6,  6,  5,  43801,   52000, 0, 0,  1499137, 1777664, 1),
( 7,  7,  7,      1,  280000, 0, 0,        0, 9175040, 1),
( 8,  8,  5,  52001,   97000, 0, 0,  1777665, 3178496, 1),
( 9,  9,  5,  97001,   97001, 0, 0,  3178497, 3178497, 1),
(10, 10,  5,  97002,  139000, 0, 0,  3178498, 4554752, 1),
(11, 11,  2, 139001,  187000, 0, 0,  4554753, 6152192, 1),
(12, 12,  2, 187001,  238000, 0, 0,  6152193, 7782400, 1),
(13, 13,  5, 238001,  282000, 0, 0,  7782401, 9232384, 1),
(14, 14,  8,      1,  950000, 0, 0,        0,31457280, 1),
(15, 15,  5, 282001,  367000, 0, 0,  9232385,12091392, 1),
(16, 16,  5, 367001,  399000, 0, 0, 12091393,13139968, 1),
(17, 17,  5, 399001,  434000, 0, 0, 13139969,14286848, 1),
(18, 18,  3, 434001,  472000, 0, 0, 14286849,15532032, 1),
(19, 19,  3, 472001,  472001, 0, 0, 15532033,15532033, 1),
(20, 20,  3, 472002,  513000, 0, 0, 15532034,16875520, 1),
(21, 21,  5, 513001,  518200, 0, 0, 16875521,17046528, 1),
(22,  1,  9,      1,  120000, 0, 0,        0, 3932160, 2),
(23,  7, 10,      1,  270000, 0, 0,        0, 8847360, 2),
(24, 14,  6,      1,  920000, 0, 0,        0,30146560, 2);

-- ─── Logs for warning/error jobs ─────────────────────────────────────────────
INSERT INTO log (jobid, time, logtext) VALUES
(3,  NOW()-INTERVAL '3 days' + INTERVAL '10 minutes',
 'web-server.example.com-fd JobId 3: Warning: /var/log/syslog: file size shrunk by 1024 bytes; not saved.'),
(12, NOW()-INTERVAL '1 day'  + INTERVAL '27 minutes',
 'db-server.example.com-fd JobId 12: Warning: /var/lib/mysql/mysql-bin.000001: file changed.'),
(12, NOW()-INTERVAL '1 day'  + INTERVAL '27 minutes',
 'db-server.example.com-fd JobId 12: Warning: /var/lib/mysql/mysql-bin.000002: file changed.'),
(12, NOW()-INTERVAL '1 day'  + INTERVAL '28 minutes',
 'db-server.example.com-dir JobId 12: Warning: 3 files not saved due to file permission error.');
