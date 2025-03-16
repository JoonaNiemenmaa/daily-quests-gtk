import sqlite3

class TasksDatabase():
    def __init__(self):
        self.DATABASE_PATH = "tasks.db"
        self.connection = sqlite3.connect(self.DATABASE_PATH)
        self.cursor = self.connection.cursor()

        # This checks whether or not the database has been initialized or not
        tables = self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type = 'table' AND tbl_name = 'Tasks';").fetchall()
        if tables == []:
            self.initDatabase()
            print("Database initialized")

        return

    def initDatabase(self):
        self.cursor.execute("""CREATE TABLE Tasks (
                taskid INT,
                date TEXT,
                task TEXT NOT NULL DEFAULT '',
                status INT NOT NULL DEFAULT FALSE,
                PRIMARY KEY (taskid, date),
                CHECK(status IN (0, 1))
            );""")
        self.connection.commit()
        return

    def insertTask(self, taskid, date, task):
        self.cursor.execute("INSERT INTO Tasks (taskid, date, task) VALUES (?, ?, ?);", [(taskid), (date), (task)])
        self.connection.commit()
        return

    def tasksByDate(self, date):
        tasks = self.cursor.execute("SELECT taskid, task, status FROM Tasks WHERE date = ? ORDER BY taskid", [(date)])
        self.connection.commit()
        return tasks

    def deleteTask(self, taskid, date):
        rows_to_update = int(self.cursor.execute("SELECT COUNT(taskid) FROM Tasks WHERE taskid > ? AND date = ?;", [(taskid), (date)]).fetchall()[0][0])
        self.cursor.execute("DELETE FROM Tasks WHERE taskid = ? AND date = ?;", [(taskid), (date)])
        for i in range(rows_to_update):
            self.cursor.execute("UPDATE Tasks SET taskid = ? WHERE taskid = ? AND date = ?;", [(taskid + i), (taskid + i + 1), (date)])
        self.connection.commit()
        return

