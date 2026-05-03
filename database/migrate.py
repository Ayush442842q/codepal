import sqlite3
from sqlite3 import Error

class MigrationScript:
    def __init__(self, db_name):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_name)
            print(f"Connected to SQLite Database {db_name}")
        except Error as e:
            print(e)

    def create_migration_table(self):
        """Create a migration tracking table"""
        query = """
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """
        try:
            self.conn.execute(query)
            print("Migration table created")
        except Error as e:
            print(e)

    def create_users_table(self):
        """Create the Users table"""
        query = """
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                CONSTRAINT chk_users_username CHECK (username <> ''),
                CONSTRAINT chk_users_password CHECK (password <> ''),
                CONSTRAINT chk_users_email CHECK (email <> '')
            );
            CREATE INDEX IF NOT EXISTS idx_users_username ON Users (username);
        """
        try:
            self.conn.execute(query)
            print("Users table created")
        except Error as e:
            print(e)

    def create_projects_table(self):
        """Create the Projects table with a foreign key to the Users table"""
        query = """
            CREATE TABLE IF NOT EXISTS Projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                userId INTEGER NOT NULL,
                FOREIGN KEY (userId) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE,
                UNIQUE (name, userId),
                CONSTRAINT chk_projects_name CHECK (name <> '')
            );
            CREATE INDEX IF NOT EXISTS idx_projects_userId ON Projects (userId);
        """
        try:
            self.conn.execute(query)
            print("Projects table created")
        except Error as e:
            print(e)

    def create_files_table(self):
        """Create the Files table with a foreign key to the Projects table"""
        query = """
            CREATE TABLE IF NOT EXISTS Files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                content TEXT,
                projectId INTEGER NOT NULL,
                FOREIGN KEY (projectId) REFERENCES Projects (id) ON DELETE CASCADE ON UPDATE CASCADE,
                UNIQUE (name, projectId),
                CONSTRAINT chk_files_name CHECK (name <> '')
            );
            CREATE INDEX IF NOT EXISTS idx_files_projectId ON Files (projectId);
        """
        try:
            self.conn.execute(query)
            print("Files table created")
        except Error as e:
            print(e)

    def create_code_completion_suggestions_table(self):
        """Create the CodeCompletionSuggestions table with a foreign key to the Files table"""
        query = """
            CREATE TABLE IF NOT EXISTS CodeCompletionSuggestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                suggestion TEXT NOT NULL,
                fileId INTEGER NOT NULL,
                FOREIGN KEY (fileId) REFERENCES Files (id) ON DELETE CASCADE ON UPDATE CASCADE,
                CONSTRAINT chk_codeCompletionSuggestions_suggestion CHECK (suggestion <> '')
            );
            CREATE INDEX IF NOT EXISTS idx_codeCompletionSuggestions_fileId ON CodeCompletionSuggestions (fileId);
        """
        try:
            self.conn.execute(query)
            print("CodeCompletionSuggestions table created")
        except Error as e:
            print(e)

    def create_bug_detection_results_table(self):
        """Create the BugDetectionResults table with a foreign key to the Files table"""
        query = """
            CREATE TABLE IF NOT EXISTS BugDetectionResults (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                result TEXT NOT NULL,
                fileId INTEGER NOT NULL,
                FOREIGN KEY (fileId) REFERENCES Files (id) ON DELETE CASCADE ON UPDATE CASCADE,
                CONSTRAINT chk_bugDetectionResults_result CHECK (result <> '')
            );
            CREATE INDEX IF NOT EXISTS idx_bugDetectionResults_fileId ON BugDetectionResults (fileId);
        """
        try:
            self.conn.execute(query)
            print("BugDetectionResults table created")
        except Error as e:
            print(e)

    def create_optimization_recommendations_table(self):
        """Create the OptimizationRecommendations table with a foreign key to the Files table"""
        query = """
            CREATE TABLE IF NOT EXISTS OptimizationRecommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recommendation TEXT NOT NULL,
                fileId INTEGER NOT NULL,
                FOREIGN KEY (fileId) REFERENCES Files (id) ON DELETE CASCADE ON UPDATE CASCADE,
                CONSTRAINT chk_optimizationRecommendations_recommendation CHECK (recommendation <> '')
            );
            CREATE INDEX IF NOT EXISTS idx_optimizationRecommendations_fileId ON OptimizationRecommendations (fileId);
        """
        try:
            self.conn.execute(query)
            print("OptimizationRecommendations table created")
        except Error as e:
            print(e)

    def create_collaborators_table(self):
        """Create the Collaborators table with foreign keys to the Projects and Users tables"""
        query = """
            CREATE TABLE IF NOT EXISTS Collaborators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                projectId INTEGER NOT NULL,
                userId INTEGER NOT NULL,
                FOREIGN KEY (projectId) REFERENCES Projects (id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (userId) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE,
                UNIQUE (projectId, userId)
            );
            CREATE INDEX IF NOT EXISTS idx_collaborators_projectId ON Collaborators (projectId);
            CREATE INDEX IF NOT EXISTS idx_collaborators_userId ON Collaborators (userId);
        """
        try:
            self.conn.execute(query)
            print("Collaborators table created")
        except Error as e:
            print(e)

    def apply_migration(self, migration_name):
        """Apply a migration"""
        self.create_migration_table()
        self.create_users_table()
        self.create_projects_table()
        self.create_files_table()
        self.create_code_completion_suggestions_table()
        self.create_bug_detection_results_table()
        self.create_optimization_recommendations_table()
        self.create_collaborators_table()
        query = "INSERT INTO migrations (name) VALUES (?)"
        try:
            self.conn.execute(query, (migration_name,))
            self.conn.commit()
            print(f"Migration {migration_name} applied")
        except Error as e:
            print(e)

    def rollback_migration(self, migration_name):
        """Rollback a migration"""
        query = "DELETE FROM migrations WHERE name = ?"
        try:
            self.conn.execute(query, (migration_name,))
            self.conn.commit()
            print(f"Migration {migration_name} rolled back")
        except Error as e:
            print(e)

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Connection closed")


if __name__ == "__main__":
    migration_script = MigrationScript("database.db")
    migration_script.apply_migration("initial_migration")
    migration_script.close_connection()