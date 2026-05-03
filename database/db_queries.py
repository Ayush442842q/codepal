import sqlite3
import logging

# Create a logger
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                userId INTEGER NOT NULL,
                FOREIGN KEY (userId) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE,
                UNIQUE (name, userId)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                content TEXT,
                projectId INTEGER NOT NULL,
                FOREIGN KEY (projectId) REFERENCES Projects (id) ON DELETE CASCADE ON UPDATE CASCADE,
                UNIQUE (name, projectId)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS CodeCompletionSuggestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                suggestion TEXT NOT NULL,
                fileId INTEGER NOT NULL,
                FOREIGN KEY (fileId) REFERENCES Files (id) ON DELETE CASCADE ON UPDATE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS BugDetectionResults (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                result TEXT NOT NULL,
                fileId INTEGER NOT NULL,
                FOREIGN KEY (fileId) REFERENCES Files (id) ON DELETE CASCADE ON UPDATE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS OptimizationRecommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recommendation TEXT NOT NULL,
                fileId INTEGER NOT NULL,
                FOREIGN KEY (fileId) REFERENCES Files (id) ON DELETE CASCADE ON UPDATE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Collaborators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                projectId INTEGER NOT NULL,
                userId INTEGER NOT NULL,
                FOREIGN KEY (projectId) REFERENCES Projects (id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (userId) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE,
                UNIQUE (projectId, userId)
            )
        ''')
        self.conn.commit()

        # Create indexes for frequently queried columns
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON Users (username)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_projects_userId ON Projects (userId)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_files_projectId ON Files (projectId)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_codeCompletionSuggestions_fileId ON CodeCompletionSuggestions (fileId)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_bugDetectionResults_fileId ON BugDetectionResults (fileId)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_optimizationRecommendations_fileId ON OptimizationRecommendations (fileId)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_collaborators_projectId ON Collaborators (projectId)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_collaborators_userId ON Collaborators (userId)')

        # Create check constraints to validate data
        self.cursor.execute('ALTER TABLE Users ADD CONSTRAINT IF NOT EXISTS chk_users_username CHECK (username <> "")')
        self.cursor.execute('ALTER TABLE Users ADD CONSTRAINT IF NOT EXISTS chk_users_password CHECK (password <> "")')
        self.cursor.execute('ALTER TABLE Users ADD CONSTRAINT IF NOT EXISTS chk_users_email CHECK (email <> "")')
        self.cursor.execute('ALTER TABLE Projects ADD CONSTRAINT IF NOT EXISTS chk_projects_name CHECK (name <> "")')
        self.cursor.execute('ALTER TABLE Files ADD CONSTRAINT IF NOT EXISTS chk_files_name CHECK (name <> "")')
        self.cursor.execute('ALTER TABLE CodeCompletionSuggestions ADD CONSTRAINT IF NOT EXISTS chk_codeCompletionSuggestions_suggestion CHECK (suggestion <> "")')
        self.cursor.execute('ALTER TABLE BugDetectionResults ADD CONSTRAINT IF NOT EXISTS chk_bugDetectionResults_result CHECK (result <> "")')
        self.cursor.execute('ALTER TABLE OptimizationRecommendations ADD CONSTRAINT IF NOT EXISTS chk_optimizationRecommendations_recommendation CHECK (recommendation <> "")')

        self.conn.commit()

    # CRUD operations for Users table
    def create_user(self, username, password, email):
        try:
            self.cursor.execute('INSERT INTO Users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f'Error creating user: {e}')
            return None

    def read_user(self, user_id):
        try:
            self.cursor.execute('SELECT * FROM Users WHERE id = ?', (user_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f'Error reading user: {e}')
            return None

    def update_user(self, user_id, username, password, email):
        try:
            self.cursor.execute('UPDATE Users SET username = ?, password = ?, email = ? WHERE id = ?', (username, password, email, user_id))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f'Error updating user: {e}')
            return None

    def delete_user(self, user_id):
        try:
            self.cursor.execute('DELETE FROM Users WHERE id = ?', (user_id,))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f'Error deleting user: {e}')
            return None

    # CRUD operations for Projects table
    def create_project(self, name, description, user_id):
        try:
            self.cursor.execute('INSERT INTO Projects (name, description, userId) VALUES (?, ?, ?)', (name, description, user_id))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f'Error creating project: {e}')
            return None

    def read_project(self, project_id):
        try:
            self.cursor.execute('SELECT * FROM Projects WHERE id = ?', (project_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f'Error reading project: {e}')
            return None

    def update_project(self, project_id, name, description, user_id):
        try:
            self.cursor.execute('UPDATE Projects SET name = ?, description = ?, userId = ? WHERE id = ?', (name, description, user_id, project_id))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f'Error updating project: {e}')
            return None

    def delete_project(self, project_id):
        try:
            self.cursor.execute('DELETE FROM Projects WHERE id = ?', (project_id,))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f'Error deleting project: {e}')
            return None

    # CRUD operations for Files table
    def create_file(self, name, content, project_id):
        try:
            self.cursor.execute('INSERT INTO Files (name, content, projectId) VALUES (?, ?, ?)', (name, content, project_id))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f'Error creating file: {e}')
            return None

    def read_file(self, file_id):
        try:
            self.cursor.execute('SELECT * FROM Files WHERE id = ?', (file_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f'Error reading file: {e}')
            return None

    def update_file(self, file_id, name, content, project_id):
        try:
            self.cursor.execute('UPDATE Files SET name = ?, content = ?, projectId = ? WHERE id = ?', (name, content, project_id, file_id))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f'Error updating file: {e}')
            return None

    def delete_file(self, file_id):
        try:
            self.cursor.execute('DELETE FROM Files WHERE id = ?', (file_id,))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f'Error deleting file: {e}')
            return None

    # CRUD operations for CodeCompletionSuggestions table
    def create_code_completion_suggestion(self, suggestion, file_id):
        try:
            self.cursor.execute('INSERT INTO CodeCompletionSuggestions (suggestion, fileId) VALUES (?, ?)', (suggestion, file_id))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f'Error creating code completion suggestion: {e}')
            return None

    def read_code_completion_suggestion(self, suggestion_id):
        try:
            self.cursor.execute('SELECT * FROM CodeCompletionSuggestions WHERE id = ?', (suggestion_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f'Error reading code completion suggestion: {e}')
            return None

    def update_code_completion_suggestion(self, suggestion_id, suggestion, file_id):
        try:
            self.cursor.execute('UPDATE CodeCompletionSuggestions SET suggestion = ?, fileId = ? WHERE id = ?', (suggestion, file_id, suggestion_id))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f'Error updating code completion suggestion: {e}')
            return None

    def delete_code_completion_suggestion(self, suggestion_id):
        try:
            self.cursor.execute('DELETE FROM CodeCompletionSuggestions WHERE id = ?', (suggestion_id,))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f'Error deleting code completion suggestion: {e}')
            return None

    # CRUD operations for BugDetectionResults table
    def create_bug_detection_result(self, result, file_id):
        try:
            self.cursor.execute('INSERT INTO BugDetectionResults (result, fileId) VALUES (?, ?)', (result, file_id))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f'Error creating bug detection result: {e}')
            return None

    def read_bug_detection_result(self, result_id):
        try:
            self.cursor.execute('SELECT * FROM BugDetectionResults WHERE id = ?', (result_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f'Error reading bug detection result: {e}')
            return None

    def update_bug_detection_result(self, result_id, result, file_id):
        try:
            self.cursor.execute('UPDATE BugDetectionResults SET result = ?, fileId = ? WHERE id = ?', (result, file_id, result_id))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f'Error updating bug detection result: {e}')
            return None

    def delete_bug_detection_result(self, result_id):
        try:
            self.cursor.execute('DELETE FROM BugDetectionResults WHERE id = ?', (result_id,))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f'Error deleting bug detection result: {e}')
            return None

    # CRUD operations for OptimizationRecommendations table
    def create_optimization_recommendation(self, recommendation, file_id):
        try:
            self.cursor.execute('INSERT INTO OptimizationRecommendations (recommendation, fileId) VALUES (?, ?)', (recommendation, file_id))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f'Error creating optimization recommendation: {e}')
            return None

    def read_optimization_recommendation(self, recommendation_id):
        try:
            self.cursor.execute('SELECT * FROM OptimizationRecommendations WHERE id = ?', (recommendation_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f'Error reading optimization recommendation: {e}')
            return None

    def update_optimization_recommendation(self, recommendation_id, recommendation, file_id):
        try:
            self.cursor.execute('UPDATE OptimizationRecommendations SET recommendation = ?, fileId = ? WHERE id = ?', (recommendation, file_id, recommendation_id))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f'Error updating optimization recommendation: {e}')
            return None

    def delete_optimization_recommendation(self, recommendation_id):
        try:
            self.cursor.execute('DELETE FROM OptimizationRecommendations WHERE id = ?', (recommendation_id,))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f'Error deleting optimization recommendation: {e}')
            return None

    # CRUD operations for Collaborators table
    def create_collaborator(self, project_id, user_id):
        try:
            self.cursor.execute('INSERT INTO Collaborators (projectId, userId) VALUES (?, ?)', (project_id, user_id))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f'Error creating collaborator: {e}')
            return None

    def read_collaborator(self, collaborator_id):
        try:
            self.cursor.execute('SELECT * FROM Collaborators WHERE id = ?', (collaborator_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f'Error reading collaborator: {e}')
            return None

    def update_collaborator(self, collaborator_id, project_id, user_id):
        try:
            self.cursor.execute('UPDATE Collaborators SET projectId = ?, userId = ? WHERE id = ?', (project_id, user_id, collaborator_id))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f'Error updating collaborator: {e}')
            return None

    def delete_collaborator(self, collaborator_id):
        try:
            self.cursor.execute('DELETE FROM Collaborators WHERE id = ?', (collaborator_id,))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f'Error deleting collaborator: {e}')
            return None

    # Join queries
    def get_project_files(self, project_id):
        try:
            self.cursor.execute('SELECT * FROM Files WHERE projectId = ?', (project_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f'Error getting project files: {e}')
            return None

    def get_file_code_completion_suggestions(self, file_id):
        try:
            self.cursor.execute('SELECT * FROM CodeCompletionSuggestions WHERE fileId = ?', (file_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f'Error getting file code completion suggestions: {e}')
            return None

    def get_file_bug_detection_results(self, file_id):
        try:
            self.cursor.execute('SELECT * FROM BugDetectionResults WHERE fileId = ?', (file_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f'Error getting file bug detection results: {e}')
            return None

    def get_file_optimization_recommendations(self, file_id):
        try:
            self.cursor.execute('SELECT * FROM OptimizationRecommendations WHERE fileId = ?', (file_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f'Error getting file optimization recommendations: {e}')
            return None

    # Search/filter queries
    def search_users(self, query):
        try:
            self.cursor.execute('SELECT * FROM Users WHERE username LIKE ? OR email LIKE ?', (f'%{query}%', f'%{query}%'))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f'Error searching users: {e}')
            return None

    def search_projects(self, query):
        try:
            self.cursor.execute('SELECT * FROM Projects WHERE name LIKE ? OR description LIKE ?', (f'%{query}%', f'%{query}%'))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f'Error searching projects: {e}')
            return None

    def search_files(self, query):
        try:
            self.cursor.execute('SELECT * FROM Files WHERE name LIKE ? OR content LIKE ?', (f'%{query}%', f'%{query}%'))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f'Error searching files: {e}')
            return None

    # Pagination support
    def get_users(self, offset, limit):
        try:
            self.cursor.execute('SELECT * FROM Users ORDER BY id LIMIT ? OFFSET ?', (limit, offset))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f'Error getting users: {e}')
            return None

    def get_projects(self, offset, limit):
        try:
            self.cursor.execute('SELECT * FROM Projects ORDER BY id LIMIT ? OFFSET ?', (limit, offset))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f'Error getting projects: {e}')
            return None

    def get_files(self, offset, limit):
        try:
            self.cursor.execute('SELECT * FROM Files ORDER BY id LIMIT ? OFFSET ?', (limit, offset))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f'Error getting files: {e}')
            return None

if __name__ == '__main__':
    db = Database('codepal.db')
    db.create_tables()