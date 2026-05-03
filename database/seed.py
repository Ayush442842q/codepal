import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the tables
cursor.execute('''
    DROP TABLE IF EXISTS Collaborators;
    DROP TABLE IF EXISTS OptimizationRecommendations;
    DROP TABLE IF EXISTS BugDetectionResults;
    DROP TABLE IF EXISTS CodeCompletionSuggestions;
    DROP TABLE IF EXISTS Files;
    DROP TABLE IF EXISTS Projects;
    DROP TABLE IF EXISTS Users;
''')

cursor.execute('''
    CREATE TABLE Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );
''')

cursor.execute('''
    CREATE TABLE Projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        userId INTEGER NOT NULL,
        FOREIGN KEY (userId) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE,
        UNIQUE (name, userId)
    );
''')

cursor.execute('''
    CREATE TABLE Files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        content TEXT,
        projectId INTEGER NOT NULL,
        FOREIGN KEY (projectId) REFERENCES Projects (id) ON DELETE CASCADE ON UPDATE CASCADE,
        UNIQUE (name, projectId)
    );
''')

cursor.execute('''
    CREATE TABLE CodeCompletionSuggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        suggestion TEXT NOT NULL,
        fileId INTEGER NOT NULL,
        FOREIGN KEY (fileId) REFERENCES Files (id) ON DELETE CASCADE ON UPDATE CASCADE
    );
''')

cursor.execute('''
    CREATE TABLE BugDetectionResults (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        result TEXT NOT NULL,
        fileId INTEGER NOT NULL,
        FOREIGN KEY (fileId) REFERENCES Files (id) ON DELETE CASCADE ON UPDATE CASCADE
    );
''')

cursor.execute('''
    CREATE TABLE OptimizationRecommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recommendation TEXT NOT NULL,
        fileId INTEGER NOT NULL,
        FOREIGN KEY (fileId) REFERENCES Files (id) ON DELETE CASCADE ON UPDATE CASCADE
    );
''')

cursor.execute('''
    CREATE TABLE Collaborators (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        projectId INTEGER NOT NULL,
        userId INTEGER NOT NULL,
        FOREIGN KEY (projectId) REFERENCES Projects (id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (userId) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE,
        UNIQUE (projectId, userId)
    );
''')

cursor.execute('''
    CREATE INDEX idx_users_username ON Users (username);
    CREATE INDEX idx_projects_userId ON Projects (userId);
    CREATE INDEX idx_files_projectId ON Files (projectId);
    CREATE INDEX idx_codeCompletionSuggestions_fileId ON CodeCompletionSuggestions (fileId);
    CREATE INDEX idx_bugDetectionResults_fileId ON BugDetectionResults (fileId);
    CREATE INDEX idx_optimizationRecommendations_fileId ON OptimizationRecommendations (fileId);
    CREATE INDEX idx_collaborators_projectId ON Collaborators (projectId);
    CREATE INDEX idx_collaborators_userId ON Collaborators (userId);
''')

cursor.execute('''
    ALTER TABLE Users ADD CONSTRAINT chk_users_username CHECK (username <> '');
    ALTER TABLE Users ADD CONSTRAINT chk_users_password CHECK (password <> '');
    ALTER TABLE Users ADD CONSTRAINT chk_users_email CHECK (email <> '');
    ALTER TABLE Projects ADD CONSTRAINT chk_projects_name CHECK (name <> '');
    ALTER TABLE Files ADD CONSTRAINT chk_files_name CHECK (name <> '');
    ALTER TABLE CodeCompletionSuggestions ADD CONSTRAINT chk_codeCompletionSuggestions_suggestion CHECK (suggestion <> '');
    ALTER TABLE BugDetectionResults ADD CONSTRAINT chk_bugDetectionResults_result CHECK (result <> '');
    ALTER TABLE OptimizationRecommendations ADD CONSTRAINT chk_optimizationRecommendations_recommendation CHECK (recommendation <> '');
''')

# Insert seed data into the Users table
users = [
    ('john_doe', 'password123', 'johndoe@example.com'),
    ('jane_doe', 'password456', 'janedoe@example.com'),
    ('bob_smith', 'password789', 'bobsmith@example.com'),
    ('alice_johnson', 'password012', 'alicejohnson@example.com'),
    ('mike_brown', 'password345', 'mikebrown@example.com')
]

cursor.executemany('INSERT INTO Users (username, password, email) VALUES (?, ?, ?)', users)

# Insert seed data into the Projects table
projects = [
    ('Project 1', 'This is project 1', 1),
    ('Project 2', 'This is project 2', 1),
    ('Project 3', 'This is project 3', 2),
    ('Project 4', 'This is project 4', 3),
    ('Project 5', 'This is project 5', 4)
]

cursor.executemany('INSERT INTO Projects (name, description, userId) VALUES (?, ?, ?)', projects)

# Insert seed data into the Files table
files = [
    ('file1.txt', 'This is the content of file1', 1),
    ('file2.txt', 'This is the content of file2', 1),
    ('file3.txt', 'This is the content of file3', 2),
    ('file4.txt', 'This is the content of file4', 3),
    ('file5.txt', 'This is the content of file5', 4)
]

cursor.executemany('INSERT INTO Files (name, content, projectId) VALUES (?, ?, ?)', files)

# Insert seed data into the CodeCompletionSuggestions table
code_completion_suggestions = [
    ('This is a suggestion for file1', 1),
    ('This is a suggestion for file2', 2),
    ('This is a suggestion for file3', 3),
    ('This is a suggestion for file4', 4),
    ('This is a suggestion for file5', 5)
]

cursor.executemany('INSERT INTO CodeCompletionSuggestions (suggestion, fileId) VALUES (?, ?)', code_completion_suggestions)

# Insert seed data into the BugDetectionResults table
bug_detection_results = [
    ('This is a bug detection result for file1', 1),
    ('This is a bug detection result for file2', 2),
    ('This is a bug detection result for file3', 3),
    ('This is a bug detection result for file4', 4),
    ('This is a bug detection result for file5', 5)
]

cursor.executemany('INSERT INTO BugDetectionResults (result, fileId) VALUES (?, ?)', bug_detection_results)

# Insert seed data into the OptimizationRecommendations table
optimization_recommendations = [
    ('This is an optimization recommendation for file1', 1),
    ('This is an optimization recommendation for file2', 2),
    ('This is an optimization recommendation for file3', 3),
    ('This is an optimization recommendation for file4', 4),
    ('This is an optimization recommendation for file5', 5)
]

cursor.executemany('INSERT INTO OptimizationRecommendations (recommendation, fileId) VALUES (?, ?)', optimization_recommendations)

# Insert seed data into the Collaborators table
collaborators = [
    (1, 2),
    (1, 3),
    (2, 4),
    (3, 5),
    (4, 1)
]

cursor.executemany('INSERT INTO Collaborators (projectId, userId) VALUES (?, ?)', collaborators)

# Commit the changes
conn.commit()

# Close the connection
conn.close()