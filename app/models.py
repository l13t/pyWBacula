LEVELS = {
    'F': 'Full',
    'I': 'Incremental',  # since last backup
    'D': 'Differential',  # since last full backup
    'S': 'Since',
    'C': 'Verify from catalog',
    'V': 'Verify safe from DB',
    'O': 'Verify Volume to catalog',
    'd': 'Verify Disk to catalog',
    'A': 'Verify data on volume',
    'B': 'Base level job',
    ' ': 'Restore/Admin',
    'f': 'Virtual full',
}
TYPES = {
    'B': 'Backup',
    'M': 'Migrated',
    'V': 'Verify',
    'R': 'Restore',
    'U': 'Console',
    'D': 'Admin',
    'A': 'Archive',
    'C': 'Copy of a Job',
    'c': 'Copy',
    'g': 'Migration',
    'S': 'Scan',
}
VOLUME_STATUS_SEVERITY = {
    "Append": 'ok',
    "Archive": 'unknown',
    "Disabled": 'unknown',
    "Full": 'unknown',
    "Used": 'unknown',
    "Cleaning": 'unknown',
    "Purged": 'unknown',
    "Recycle": 'unknown',
    "Read-Only": 'unknown',
    "Error": 'error',
}

