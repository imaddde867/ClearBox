# Database Migration

This directory contains scripts for database migrations in the ClearBox application.

## SQLite to PostgreSQL Migration

The `migrate_to_postgres.py` script facilitates migrating data from a SQLite database to a PostgreSQL database.

### Prerequisites

- PostgreSQL server installed and running
- Python dependencies installed (from requirements.txt)
- Valid PostgreSQL connection URL

### Usage

1. Create and configure your PostgreSQL database on AWS RDS or your preferred host.
2. Update the PostgreSQL connection URL in your production `.env` file.
3. Run the migration script:

```bash
# From the backend directory
python -m migrations.migrate_to_postgres --sqlite-path clearbox.db --pg-url postgresql://username:password@hostname:5432/database_name
```

Or, if your connection details are in your `.env` file:

```bash
python -m migrations.migrate_to_postgres --env-file .env
```

### Backup

The script automatically creates a backup of your SQLite database before migration.

### Troubleshooting

If you encounter issues during migration:

1. Check the migration log file that is created in the current directory.
2. Verify that your PostgreSQL connection URL is correct.
3. Ensure you have appropriate permissions on your PostgreSQL database.
4. Check that your tables in PostgreSQL have compatible schemas with the SQLite database.

## Database Backup Strategy for Production

### Regular Backups

For AWS RDS PostgreSQL, set up automated backups:

1. In the AWS RDS console, select your database instance
2. Go to "Modify" and set:
   - Backup retention period: 7 days (or as needed)
   - Backup window: During off-peak hours

### Manual Backups

To create a manual backup (snapshot):

1. In the AWS RDS console, select your database
2. Click "Actions" > "Take snapshot"
3. Name the snapshot and click "Create"

### Database Dump

To create a local backup:

```bash
# Replace with your database details
pg_dump -h your-rds-endpoint -U username -d database_name -f backup_$(date +%Y%m%d).sql
```

### Restoration Procedure

To restore from a backup:

1. From an RDS snapshot:
   - In AWS RDS console, select the snapshot
   - Click "Actions" > "Restore snapshot"
   - Follow the wizard to create a new instance

2. From a SQL dump:
   ```bash
   psql -h your-rds-endpoint -U username -d database_name -f backup_file.sql
   ``` 