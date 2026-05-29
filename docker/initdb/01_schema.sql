-- Bacula Community Edition PostgreSQL Catalog Schema
-- Based on Bacula 9.x CE catalog DDL

CREATE TABLE Status (
    JobStatus     text        NOT NULL,
    JobStatusLong text,
    Severity      integer,
    PRIMARY KEY (JobStatus)
);

CREATE TABLE Client (
    ClientId      serial      NOT NULL,
    Name          text        NOT NULL,
    Uname         text        NOT NULL,
    AutoPrune     smallint    DEFAULT 0,
    FileRetention bigint      DEFAULT 0,
    JobRetention  bigint      DEFAULT 0,
    PRIMARY KEY (ClientId)
);
CREATE UNIQUE INDEX client_name_idx ON Client (Name);

CREATE TABLE FileSet (
    FileSetId  serial      NOT NULL,
    FileSet    text        NOT NULL,
    MD5        text        DEFAULT '',
    CreateTime timestamp   WITHOUT TIME ZONE,
    PRIMARY KEY (FileSetId)
);

CREATE TABLE Pool (
    PoolId            serial      NOT NULL,
    Name              text        NOT NULL,
    NumVols           integer     DEFAULT 0,
    MaxVols           integer     DEFAULT 0,
    UseOnce           smallint    DEFAULT 0,
    UseCatalog        smallint    DEFAULT 1,
    AcceptAnyVolume   smallint    DEFAULT 0,
    VolRetention      bigint      DEFAULT 0,
    VolUseDuration    bigint      DEFAULT 0,
    MaxVolJobs        integer     DEFAULT 0,
    MaxVolFiles       integer     DEFAULT 0,
    MaxVolBytes       bigint      DEFAULT 0,
    AutoPrune         smallint    DEFAULT 0,
    Recycle           smallint    DEFAULT 0,
    ActionOnPurge     smallint    DEFAULT 0,
    PoolType          text        NOT NULL,
    LabelType         smallint    DEFAULT 0,
    LabelFormat       text        NOT NULL,
    Enabled           smallint    DEFAULT 1,
    ScratchPoolId     integer     DEFAULT 0,
    RecyclePoolId     integer     DEFAULT 0,
    NextPoolId        integer     DEFAULT 0,
    MigrationHighBytes bigint     DEFAULT 0,
    MigrationLowBytes  bigint     DEFAULT 0,
    MigrationTime      bigint     DEFAULT 0,
    PRIMARY KEY (PoolId)
);
CREATE UNIQUE INDEX pool_name_idx ON Pool (Name);

CREATE TABLE Storage (
    StorageId   serial  NOT NULL,
    Name        text    NOT NULL,
    AutoChanger integer DEFAULT 0,
    PRIMARY KEY (StorageId)
);
CREATE UNIQUE INDEX storage_name_idx ON Storage (Name);

CREATE TABLE MediaType (
    MediaTypeId serial  NOT NULL,
    MediaType   text    NOT NULL,
    ReadOnly    integer DEFAULT 0,
    PRIMARY KEY (MediaTypeId)
);

CREATE TABLE Device (
    DeviceId                  serial  NOT NULL,
    Name                      text    NOT NULL,
    MediaTypeId               integer DEFAULT 0,
    StorageId                 integer DEFAULT 0,
    DevMounts                 integer DEFAULT 0,
    DevReadBytes              bigint  DEFAULT 0,
    DevWriteBytes             bigint  DEFAULT 0,
    DevReadBytesSinceCleaning bigint  DEFAULT 0,
    DevWriteBytesSinceCleaning bigint DEFAULT 0,
    DevReadTime               bigint  DEFAULT 0,
    DevWriteTime              bigint  DEFAULT 0,
    DevReadTimeSinceCleaning  bigint  DEFAULT 0,
    DevWriteTimeSinceCleaning bigint  DEFAULT 0,
    CleaningDate              timestamp WITHOUT TIME ZONE,
    CleaningPeriod            bigint  DEFAULT 0,
    PRIMARY KEY (DeviceId)
);

CREATE TABLE Job (
    JobId          serial      NOT NULL,
    Job            text        NOT NULL,
    Name           text        NOT NULL,
    Type           char(1)     NOT NULL,
    Level          char(1)     NOT NULL,
    ClientId       integer     DEFAULT 0,
    JobStatus      char(1)     NOT NULL,
    SchedTime      timestamp   WITHOUT TIME ZONE,
    StartTime      timestamp   WITHOUT TIME ZONE,
    EndTime        timestamp   WITHOUT TIME ZONE,
    RealEndTime    timestamp   WITHOUT TIME ZONE,
    JobTDate       bigint      DEFAULT 0,
    VolSessionId   integer     DEFAULT 0,
    VolSessionTime integer     DEFAULT 0,
    JobFiles       integer     DEFAULT 0,
    JobBytes       bigint      DEFAULT 0,
    ReadBytes      bigint      DEFAULT 0,
    JobErrors      integer     DEFAULT 0,
    JobMissingFiles integer    DEFAULT 0,
    PoolId         integer     DEFAULT 0,
    FileSetId      integer     DEFAULT 0,
    PriorJobId     integer     DEFAULT 0,
    PurgedFiles    smallint    DEFAULT 0,
    HasBase        smallint    DEFAULT 0,
    HasCache       smallint    DEFAULT 0,
    Reviewed       smallint    DEFAULT 0,
    Comment        text,
    PRIMARY KEY (JobId)
);
CREATE INDEX job_name_idx ON Job (Name);

CREATE TABLE JobHisto (
    JobId          integer     NOT NULL,
    Job            text        NOT NULL,
    Name           text        NOT NULL,
    Type           char(1)     NOT NULL,
    Level          char(1)     NOT NULL,
    ClientId       integer     DEFAULT 0,
    JobStatus      char(1)     NOT NULL,
    SchedTime      timestamp   WITHOUT TIME ZONE,
    StartTime      timestamp   WITHOUT TIME ZONE,
    EndTime        timestamp   WITHOUT TIME ZONE,
    RealEndTime    timestamp   WITHOUT TIME ZONE,
    JobTDate       bigint      DEFAULT 0,
    VolSessionId   integer     DEFAULT 0,
    VolSessionTime integer     DEFAULT 0,
    JobFiles       integer     DEFAULT 0,
    JobBytes       bigint      DEFAULT 0,
    ReadBytes      bigint      DEFAULT 0,
    JobErrors      integer     DEFAULT 0,
    JobMissingFiles integer    DEFAULT 0,
    PoolId         integer     DEFAULT 0,
    FileSetId      integer     DEFAULT 0,
    PriorJobId     integer     DEFAULT 0,
    PurgedFiles    smallint    DEFAULT 0,
    HasBase        smallint    DEFAULT 0,
    HasCache       smallint    DEFAULT 0,
    Reviewed       smallint    DEFAULT 0,
    Comment        text,
    PRIMARY KEY (JobId)
);
CREATE INDEX jobhisto_name_idx ON JobHisto (Name);

CREATE TABLE Location (
    LocationId integer     NOT NULL,
    Location   text        NOT NULL,
    Cost       integer     DEFAULT 0,
    Enabled    smallint,
    PRIMARY KEY (LocationId)
);

CREATE TABLE Media (
    MediaId           serial      NOT NULL,
    VolumeName        text        NOT NULL,
    Slot              integer     DEFAULT 0,
    PoolId            integer     DEFAULT 0,
    MediaType         text        NOT NULL,
    MediaTypeId       integer     DEFAULT 0,
    LabelType         integer     DEFAULT 0,
    FirstWritten      timestamp   WITHOUT TIME ZONE,
    LastWritten       timestamp   WITHOUT TIME ZONE,
    LabelDate         timestamp   WITHOUT TIME ZONE,
    VolJobs           integer     DEFAULT 0,
    VolFiles          integer     DEFAULT 0,
    VolBlocks         integer     DEFAULT 0,
    VolMounts         integer     DEFAULT 0,
    VolBytes          bigint      DEFAULT 0,
    VolParts          integer     DEFAULT 0,
    VolErrors         integer     DEFAULT 0,
    VolWrites         integer     DEFAULT 0,
    VolCapacityBytes  bigint      DEFAULT 0,
    VolStatus         text        NOT NULL,
    Enabled           smallint    DEFAULT 1,
    Recycle           smallint    DEFAULT 0,
    ActionOnPurge     smallint    DEFAULT 0,
    VolRetention      bigint      DEFAULT 0,
    VolUseDuration    bigint      DEFAULT 0,
    MaxVolJobs        integer     DEFAULT 0,
    MaxVolFiles       integer     DEFAULT 0,
    MaxVolBytes       bigint      DEFAULT 0,
    InChanger         smallint    DEFAULT 0,
    StorageId         integer     DEFAULT 0,
    DeviceId          integer     DEFAULT 0,
    MediaAddressing   smallint    DEFAULT 0,
    VolReadTime       bigint      DEFAULT 0,
    VolWriteTime      bigint      DEFAULT 0,
    EndFile           integer     DEFAULT 0,
    EndBlock          bigint      DEFAULT 0,
    LocationId        integer     DEFAULT 0,
    RecycleCount      integer     DEFAULT 0,
    InitialWrite      timestamp   WITHOUT TIME ZONE,
    ScratchPoolId     integer     DEFAULT 0,
    RecyclePoolId     integer     DEFAULT 0,
    Comment           text,
    PRIMARY KEY (MediaId)
);
CREATE UNIQUE INDEX media_volumename_idx ON Media (VolumeName);

CREATE TABLE JobMedia (
    JobMediaId integer NOT NULL,
    JobId      integer NOT NULL,
    MediaId    integer NOT NULL,
    FirstIndex integer DEFAULT 0,
    LastIndex  integer DEFAULT 0,
    StartFile  integer DEFAULT 0,
    EndFile    integer DEFAULT 0,
    StartBlock bigint  DEFAULT 0,
    EndBlock   bigint  DEFAULT 0,
    VolIndex   integer DEFAULT 0,
    PRIMARY KEY (JobMediaId)
);
CREATE INDEX jobmedia_jobid_idx   ON JobMedia (JobId);
CREATE INDEX jobmedia_mediaid_idx ON JobMedia (MediaId);

CREATE SEQUENCE jobmedia_jobmediaid_seq;

CREATE TABLE File (
    FileId     bigserial   NOT NULL,
    FileIndex  integer     DEFAULT 0,
    JobId      integer     NOT NULL,
    PathId     integer     NOT NULL,
    FileNameId integer     NOT NULL,
    MarkId     integer     DEFAULT 0,
    LStat      text        NOT NULL,
    MD5        text        NOT NULL,
    PRIMARY KEY (FileId)
);
CREATE INDEX file_jobid_idx ON File (JobId);

CREATE TABLE FileName (
    FileNameId serial  NOT NULL,
    Name       text    NOT NULL,
    PRIMARY KEY (FileNameId)
);
CREATE UNIQUE INDEX filename_name_idx ON FileName (Name);

CREATE TABLE Path (
    PathId serial  NOT NULL,
    Path   text    NOT NULL,
    PRIMARY KEY (PathId)
);
CREATE UNIQUE INDEX path_name_idx ON Path (Path);

CREATE TABLE Log (
    LogId   serial      NOT NULL,
    JobId   integer     NOT NULL,
    Time    timestamp   WITHOUT TIME ZONE,
    LogText text        NOT NULL,
    PRIMARY KEY (LogId)
);
CREATE INDEX log_name_idx ON Log (JobId, Time);

CREATE TABLE LocationLog (
    LocLogId     integer     NOT NULL,
    Date         timestamp   WITHOUT TIME ZONE,
    Comment      text        NOT NULL,
    MediaId      integer     DEFAULT 0,
    LocationId   integer     DEFAULT 0,
    NewVolStatus text        NOT NULL,
    NewEnabled   smallint,
    PRIMARY KEY (LocLogId)
);

CREATE TABLE Counters (
    Counter      text    NOT NULL,
    MinValue     integer DEFAULT 0,
    MaxValue     integer DEFAULT 0,
    CurrentValue integer DEFAULT 0,
    WrapCounter  text    NOT NULL,
    PRIMARY KEY (Counter)
);

CREATE TABLE BaseFiles (
    BaseId    serial  NOT NULL,
    JobId     integer NOT NULL,
    FileId    bigint  NOT NULL,
    FileIndex integer,
    BaseJobId integer,
    PRIMARY KEY (BaseId)
);

CREATE TABLE UnsavedFiles (
    UnsavedId  integer NOT NULL,
    JobId      integer NOT NULL,
    PathId     integer NOT NULL,
    FileNameId integer NOT NULL,
    PRIMARY KEY (UnsavedId)
);

CREATE TABLE RestoreObject (
    RestoreObjectId   serial  NOT NULL,
    ObjectName        text    NOT NULL,
    RestoreObject     bytea   NOT NULL,
    PluginName        text    NOT NULL,
    ObjectLength      integer DEFAULT 0,
    ObjectFullLength  integer DEFAULT 0,
    ObjectIndex       integer DEFAULT 0,
    ObjectType        integer DEFAULT 0,
    FileIndex         integer DEFAULT 0,
    JobId             integer,
    ObjectCompression integer DEFAULT 0,
    PRIMARY KEY (RestoreObjectId)
);
CREATE INDEX restore_jobid_idx ON RestoreObject (JobId);

CREATE TABLE CDImages (
    MediaId   integer     NOT NULL,
    LastBurn  timestamp   WITHOUT TIME ZONE NOT NULL
);

CREATE TABLE PathHierarchy (
    PathId  integer NOT NULL,
    PPathId integer NOT NULL,
    UNIQUE (PathId)
);

CREATE TABLE PathVisibility (
    PathId integer NOT NULL,
    JobId  integer NOT NULL,
    Size   bigint  DEFAULT 0,
    Files  bigint  DEFAULT 0,
    PRIMARY KEY (PathId, JobId)
);

CREATE TABLE Version (
    VersionId integer NOT NULL
);

INSERT INTO Version (VersionId) VALUES (12);
