# `database-files` Folder

This folder contains all SQL files used to initialize the AlphaTrack database.

When the MySQL container is created, all `.sql` files in this folder are automatically executed in alphabetical order. For this reason, files are prefixed with numbers (e.g., `01_`, `02_`) to ensure the correct execution order.

Typical usage:
- `01_AlphaTrack_ddl.sql` → creates the database schema  
- `02_AlphaTrack_data.sql` → inserts mock data  



## Important Behavior

SQL files are **only executed when the database container is first created**.

If you make changes to any SQL files after the container has already been created, those changes will **NOT** automatically apply.

Simply restarting the container will NOT reload the SQL files.



## How to Reinitialize the Database

To apply changes to the schema or data, you must delete and recreate the database container.

Run:

```bash
docker compose down db -v
docker compose up db
```

### What this does:
- Removes the existing database container  
- Deletes the associated MySQL volume  
- Recreates the database from scratch  
- Re-runs all SQL files in `database-files/`  



## Notes

- The `-v` flag is required to remove the stored database data  
- Without it, old data will persist and SQL files will not rerun  
- This process ensures a clean and consistent database state  

