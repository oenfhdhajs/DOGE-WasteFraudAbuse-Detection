import subprocess
import shutil
import os
import logging
from datetime import datetime

# Setting up logging
logging.basicConfig(filename='admin.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def backup_database(db_name, backup_dir):
    """
    Perform a backup of the database.
    
    :param db_name: Name of the database to backup
    :param backup_dir: Directory to save the backup
    """
    os.makedirs(backup_dir, exist_ok=True)
    backup_file = os.path.join(backup_dir, f'{db_name}_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.sql')
    
    try:
        subprocess.run(['pg_dump', '-U', 'postgres', '-d', db_name, '-f', backup_file], check=True)
        logging.info(f"Database backup completed: {backup_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Database backup failed: {str(e)}")

def manage_users(action, username, role='read_only'):
    """
    Manage database users (create, delete, or alter).
    
    :param action: 'create', 'delete', or 'alter'
    :param username: The username to manage
    :param role: Role to assign if creating or altering (default is 'read_only')
    """
    if action == 'create':
        try:
            subprocess.run(['psql', '-U', 'postgres', '-c', f"CREATE ROLE {username} WITH PASSWORD 'password'; GRANT {role} TO {username};"], check=True)
            logging.info(f"User {username} created with role {role}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to create user {username}: {str(e)}")
    elif action == 'delete':
        try:
            subprocess.run(['psql', '-U', 'postgres', '-c', f"DROP ROLE {username};"], check=True)
            logging.info(f"User {username} deleted")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to delete user {username}: {str(e)}")
    elif action == 'alter':
        try:
            subprocess.run(['psql', '-U', 'postgres', '-c', f"ALTER ROLE {username} WITH ROLE {role};"], check=True)
            logging.info(f"User {username} role altered to {role}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to alter user {username} role: {str(e)}")

def main():
    db_name = 'government_spending_db'
    backup_dir = 'backups'
    backup_database(db_name, backup_dir)
    
    # Example usage for user management
    manage_users('create', 'analyst_user', 'read_only')
    manage_users('alter', 'analyst_user', 'data_analyst')
    # manage_users('delete', 'analyst_user')  # Uncomment to delete the user

if __name__ == "__main__":
    main()
