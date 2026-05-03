-- Drop existing tables to ensure a clean start
DROP TABLE IF EXISTS Collaborators;
DROP TABLE IF EXISTS OptimizationRecommendations;
DROP TABLE IF EXISTS BugDetectionResults;
DROP TABLE IF EXISTS CodeCompletionSuggestions;
DROP TABLE IF EXISTS Files;
DROP TABLE IF EXISTS Projects;
DROP TABLE IF EXISTS Users;

-- Create the Users table
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

-- Create the Projects table with a foreign key to the Users table
CREATE TABLE Projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    userId INTEGER NOT NULL,
    FOREIGN KEY (userId) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (name, userId)
);

-- Create the Files table with a foreign key to the Projects table
CREATE TABLE Files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    content TEXT,
    projectId INTEGER NOT NULL,
    FOREIGN KEY (projectId) REFERENCES Projects (id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (name, projectId)
);

-- Create the CodeCompletionSuggestions table with a foreign key to the Files table
CREATE TABLE CodeCompletionSuggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    suggestion TEXT NOT NULL,
    fileId INTEGER NOT NULL,
    FOREIGN KEY (fileId) REFERENCES Files (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create the BugDetectionResults table with a foreign key to the Files table
CREATE TABLE BugDetectionResults (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    result TEXT NOT NULL,
    fileId INTEGER NOT NULL,
    FOREIGN KEY (fileId) REFERENCES Files (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create the OptimizationRecommendations table with a foreign key to the Files table
CREATE TABLE OptimizationRecommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recommendation TEXT NOT NULL,
    fileId INTEGER NOT NULL,
    FOREIGN KEY (fileId) REFERENCES Files (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create the Collaborators table with foreign keys to the Projects and Users tables
CREATE TABLE Collaborators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    projectId INTEGER NOT NULL,
    userId INTEGER NOT NULL,
    FOREIGN KEY (projectId) REFERENCES Projects (id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (userId) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (projectId, userId)
);

-- Create indexes for frequently queried columns
CREATE INDEX idx_users_username ON Users (username);
CREATE INDEX idx_projects_userId ON Projects (userId);
CREATE INDEX idx_files_projectId ON Files (projectId);
CREATE INDEX idx_codeCompletionSuggestions_fileId ON CodeCompletionSuggestions (fileId);
CREATE INDEX idx_bugDetectionResults_fileId ON BugDetectionResults (fileId);
CREATE INDEX idx_optimizationRecommendations_fileId ON OptimizationRecommendations (fileId);
CREATE INDEX idx_collaborators_projectId ON Collaborators (projectId);
CREATE INDEX idx_collaborators_userId ON Collaborators (userId);

-- Add check constraints to validate data
ALTER TABLE Users ADD CONSTRAINT chk_users_username CHECK (username <> '');
ALTER TABLE Users ADD CONSTRAINT chk_users_password CHECK (password <> '');
ALTER TABLE Users ADD CONSTRAINT chk_users_email CHECK (email <> '');
ALTER TABLE Projects ADD CONSTRAINT chk_projects_name CHECK (name <> '');
ALTER TABLE Files ADD CONSTRAINT chk_files_name CHECK (name <> '');
ALTER TABLE CodeCompletionSuggestions ADD CONSTRAINT chk_codeCompletionSuggestions_suggestion CHECK (suggestion <> '');
ALTER TABLE BugDetectionResults ADD CONSTRAINT chk_bugDetectionResults_result CHECK (result <> '');
ALTER TABLE OptimizationRecommendations ADD CONSTRAINT chk_optimizationRecommendations_recommendation CHECK (recommendation <> '');