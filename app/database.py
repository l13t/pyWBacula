from sqlalchemy import Table, Column, Integer, MetaData, ForeignKey, \
    Text, DateTime, SmallInteger, BigInteger, BINARY, LargeBinary

metadata = MetaData()
client = Table(
    'client', metadata,
    Column('clientid', Integer, primary_key=True),
    Column('name', Text(collation='utf8'), nullable=False),
    Column('uname', Text(collation='utf8'), nullable=False),
    Column('autoprune', SmallInteger),
    Column('fileretention', BigInteger),
    Column('jobretention', BigInteger),
)

jobhist = Table(
    'jobhisto', metadata,
    Column('jobid', Integer, primary_key=True),
    Column('job', Text(collation='utf8'), nullable=False),
    Column('name', Text(collation='utf8'), nullable=False),
    Column('type', BINARY, nullable=False),
    Column('level', BINARY, nullable=False),
    Column('clientid', None, ForeignKey('client')),
    Column('jobstatus', BINARY, nullable=False),
    Column('schedtime', DateTime, nullable=False),
    Column('starttime', DateTime, nullable=False),
    Column('endtime', DateTime, nullable=False),
    Column('jobtdate', BigInteger, nullable=False),
    Column('volsessionid', Integer, nullable=False),
    Column('volsessiontime', Integer, nullable=False),
    Column('jobfiles', Integer, nullable=False),
    Column('jobbytes', Integer, nullable=False),
    Column('jobtrrors', Integer, nullable=False),
    Column('jobmissinggiles', Integer, nullable=False),
    Column('poolid', None, ForeignKey('pool')),
    Column('filesetid', SmallInteger, nullable=False),
    Column('purgedfiles', SmallInteger, nullable=False),
    Column('hasbase', SmallInteger, nullable=False),
)

job = Table(
    'job', metadata,
    Column('jobid', Integer, primary_key=True),
    Column('job', Text(collation='utf8'), nullable=False),
    Column('name', Text(collation='utf8'), nullable=False),
    Column('type', BINARY, nullable=False),
    Column('level', BINARY, nullable=False),
    Column('clientid', None, ForeignKey('client')),
    Column('jobstatus', BINARY, nullable=False),
    Column('schedtime', DateTime, nullable=False),
    Column('starttime', DateTime, nullable=False),
    Column('endtime', DateTime, nullable=False),
    Column('jobtdate', BigInteger, nullable=False),
    Column('volsessionid', Integer, nullable=False),
    Column('volsessiontime', Integer, nullable=False),
    Column('jobfiles', Integer, nullable=False),
    Column('jobbytes', Integer, nullable=False),
    Column('jobtrrors', Integer, nullable=False),
    Column('jobmissinggiles', Integer, nullable=False),
    Column('poolid', None, ForeignKey('pool')),
    Column('filesetid', SmallInteger, nullable=False),
    Column('purgedfiles', SmallInteger, nullable=False),
    Column('hasbase', SmallInteger, nullable=False),
)

pool = Table(
    'pool', metadata,
    Column('poolid', Integer, primary_key=True),
    Column('name', Text(collation='utf8'), nullable=False),
    Column('numvols', Integer, nullable=False),
    Column('maxvols', Integer, nullable=False),
    Column('useonce', SmallInteger, nullable=False),
    Column('usecatalog', SmallInteger, nullable=False),
    Column('acceptanyvolume', SmallInteger, nullable=False),
    Column('volretention', BigInteger, nullable=False),
    Column('voluseduration', BigInteger, nullable=False),
    Column('maxvoljobs', Integer, nullable=False),
    Column('maxvolfiles', Integer, nullable=False),
    Column('maxvolbytes', BigInteger, nullable=False),
    Column('autoprune', SmallInteger, nullable=False),
    Column('recycle', SmallInteger, nullable=False),
    Column('actiononpurge', SmallInteger, nullable=False),
    Column('pooltype', Text(collation='utf8'), nullable=False),
    Column('labeltype', SmallInteger, nullable=False),
    Column('labelformat', Text(collation='utf8'), nullable=False),
    Column('enabled', SmallInteger, nullable=False),
    Column('scratchpoolid', Integer, nullable=False),
    Column('recyclepoolid', Integer, nullable=False),
    Column('nextpoolid', Integer, nullable=False),
    Column('migrationhighbytes', BigInteger, nullable=False),
    Column('migrationlowbytes', BigInteger, nullable=False),
    Column('migrationtime', BigInteger, nullable=False),
)

files = Table(
    'file', metadata,
    Column('fileid', Integer, primary_key=True),
    Column('fileindex', Integer, nullable=False),
    Column('jobid', None, ForeignKey('job')),
    Column('pathid', None, ForeignKey('path')),
    Column('filenameid', None, ForeignKey('filename')),
    Column('markid', Integer, nullable=False),
    Column('lstat', Text(collation='utf8'), nullable=False),
    Column('md5', Text(collation='utf8'), nullable=False),
)

filename = Table(
    'filename', metadata,
    Column('filenameid', Integer, primary_key=True),
    Column('name', Text(collation='utf8'), nullable=False),
)

path = Table(
    'path', metadata,
    Column('pathid', Integer, primary_key=True),
    Column('path', Text(collation='utf8'), nullable=False),
)

restoreobject = Table(
    'restoreobject', metadata,
    Column('restoreobjectid', Integer, primary_key=True),
    Column('objectname', Text(collation='utf8'), nullable=False),
    Column('restoreobject', LargeBinary, nullable=False),
    Column('pluginname', Text(collation='utf8'), nullable=False),
    Column('objectlength', Integer, nullable=False),
    Column('objectfulllength', Integer, nullable=False),
    Column('objectindex', Integer, nullable=False),
    Column('objecttype', Integer, nullable=False),
    Column('fileindex', Integer, nullable=False),
    Column('jobid', Integer, nullable=False),
    Column('objectcompression', Integer, nullable=False),
)

location = Table(
    'location', metadata,
    Column('locationid', Integer, primary_key=True),
    Column('location', Text(collation='utf8'), nullable=False),
    Column('cost', Integer, nullable=False),
    Column('enabled', SmallInteger, nullable=False),
)

fileset = Table(
    'fileset', metadata,
    Column('filesetid', Integer, primary_key=True),
    Column('fileset', Text(collation='utf8'), nullable=False),
    Column('md5', Text(collation='utf8'), nullable=False),
    Column('createtime', DateTime(timezone=False), nullable=False),
)

jobmedia = Table(
    'jobmedia', metadata,
    Column('jobmediaid', Integer, primary_key=True),
    Column('jobid', Integer, nullable=False),
    Column('mediaid', Integer, nullable=False),
    Column('firstindex', Integer, nullable=False),
    Column('lastindex', Integer, nullable=False),
    Column('startfile', Integer, nullable=False),
    Column('endfile', Integer, nullable=False),
    Column('startblock', BigInteger, nullable=False),
    Column('endblock', BigInteger, nullable=False),
    Column('volindex', Integer, nullable=False),
)

media = Table(
    'media', metadata,
    Column('mediaid', Integer, primary_key=True),
    Column('volumename', Text(collation='utf8'), nullable=False),
    Column('slot', Integer, nullable=False),
    Column('poolid', Integer, nullable=False),
    Column('mediatype', Text(collation='utf8'), nullable=False),
    Column('mediatypeid', Integer, nullable=False),
    Column('labeltype', Integer, nullable=False),
    Column('firstwritten', DateTime(timezone=False)),
    Column('lastwritten', DateTime(timezone=False)),
    Column('labeldate', DateTime(timezone=False)),
    Column('voljobs', Integer, nullable=False),
    Column('volfiles', Integer, nullable=False),
    Column('volblocks', Integer, nullable=False),
    Column('volmounts', Integer, nullable=False),
    Column('volbytes', BigInteger, nullable=False),
    Column('volparts', Integer, nullable=False),
    Column('volerrors', Integer, nullable=False),
    Column('volwrites', Integer, nullable=False),
    Column('volcapacitybytes', BigInteger, nullable=False),
    Column('volstatus', Text(collation='utf8'), nullable=False),
    Column('enabled', SmallInteger, nullable=False),
    Column('recycle', SmallInteger, nullable=False),
    Column('actiononpurge', SmallInteger, nullable=False),
    Column('volretention', BigInteger, nullable=False),
    Column('voluseduration', BigInteger, nullable=False),
    Column('maxvoljobs', Integer, nullable=False),
    Column('maxvolfiles', Integer, nullable=False),
    Column('maxvolbytes', BigInteger, nullable=False),
    Column('inchanger', SmallInteger, nullable=False),
    Column('storageid', Integer, nullable=False),
    Column('deviceid', Integer, nullable=False),
    Column('mediaaddressing', SmallInteger, nullable=False),
    Column('volreadtime', BigInteger, nullable=False),
    Column('volwritetime', BigInteger, nullable=False),
    Column('endfile', Integer, nullable=False),
    Column('endblock', BigInteger, nullable=False),
    Column('locationid', Integer, nullable=False),
    Column('recyclecount', Integer, nullable=False),
    Column('initialwrite', DateTime(timezone=False)),
    Column('scratchpoolid', Integer, nullable=False),
    Column('recyclepoolid', Integer, nullable=False),
    Column('comment', Text(collation='utf8'), nullable=False),
)

mediatype = Table(
    'mediatype', metadata,
    Column('mediatypeid', Integer, primary_key=True),
    Column('mediatype', Text(collation='utf8'), nullable=False),
    Column('readonly', Integer, nullable=False),
)

storage = Table(
    'storage', metadata,
    Column('storageid', Integer, primary_key=True),
    Column('name', Text(collation='utf8'), nullable=False),
    Column('autochanger', Integer, nullable=False),
)

device = Table(
    'device', metadata,
    Column('deviceid', Integer, primary_key=True),
    Column('name', Text(collation='utf8'), nullable=False),
    Column('mediatypeid', Integer, nullable=False),
    Column('storageid', Integer, nullable=False),
    Column('devmounts', Integer, nullable=False),
    Column('devreadbytes', BigInteger, nullable=False),
    Column('devwritebytes', BigInteger, nullable=False),
    Column('devreadbytessincecleaning', BigInteger, nullable=False),
    Column('devwritebytessincecleaning', BigInteger, nullable=False),
    Column('devreadtime', BigInteger, nullable=False),
    Column('devwritetime', BigInteger, nullable=False),
    Column('devreadtimesincecleaning', BigInteger, nullable=False),
    Column('devwritetimesincecleaning', BigInteger, nullable=False),
    Column('cleaningdate', DateTime(timezone=False)),
    Column('cleaningperiod', BigInteger, nullable=False),
)

log = Table(
    'log', metadata,
    Column('logid', Integer, primary_key=True),
    Column('jobid', Integer, nullable=False),
    Column('time', DateTime(timezone=False)),
    Column('logtext', Text(collation='utf8'), nullable=False),
)

locationlog = Table(
    'locationlog', metadata,
    Column('loclogid', Integer, primary_key=True),
    Column('date', DateTime(timezone=False)),
    Column('comment', Text(collation='utf8'), nullable=False),
    Column('mediaid', Integer, nullable=False),
    Column('locationid', Integer, nullable=False),
    Column('newvolstatus', Text(collation='utf8'), nullable=False),
    Column('newenabled', SmallInteger),
)

counters = Table(
    'counters', metadata,
    Column('counter', Text(collation='utf8'), nullable=False),
    Column('minvalue', Integer, nullable=False),
    Column('maxvalue', Integer, nullable=False),
    Column('currentvalue', Integer, nullable=False),
    Column('wrapcounter', Text(collation='utf8'), nullable=False),
)

basefiles = Table(
    'basefiles', metadata,
    Column('baseid', Integer, primary_key=True),
    Column('jobid', Integer, nullable=False),
    Column('fileid', BigInteger, nullable=False),
    Column('fileindex', Integer),
    Column('basejobid', Integer),
)

unsavedfiles = Table(
    'unsavedfiles', metadata,
    Column('unsavedid', Integer, nullable=False),
    Column('jobid', Integer, nullable=False),
    Column('pathid', Integer, nullable=False),
    Column('filenameid', Integer, nullable=False),
)

cdimages = Table(
    'cdimages', metadata,
    Column('mediaid', Integer, nullable=False),
    Column('lastburn', DateTime(timezone=False), nullable=False),
)

pathhierarchy = Table(
    'pathhierarchy', metadata,
    Column('pathid', Integer, nullable=False),
    Column('ppathid', Integer, nullable=False),
)

pathvisibility = Table(
    'pathvisibility', metadata,
    Column('pathid', Integer, nullable=False),
    Column('jobid', Integer, nullable=False),
    Column('size', BigInteger, nullable=False),
    Column('files', BigInteger, nullable=False),
)

version = Table(
    'version', metadata,
    Column('versionid', Integer, nullable=False),
)

status = Table(
    'status', metadata,
    Column('jobstatus', Text(collation='utf8'), nullable=False),
    Column('jobstatuslong', Text),
    Column('severity', BigInteger),
)
