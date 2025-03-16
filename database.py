import os
import sqlite3

PATH = os.path.expanduser("~/.dailyquests/")
DATABASE_PATH = os.path.join(PATH, "tasks.db")

class TasksDatabase():
    def __init__(self):
        if not os.path.exists(PATH):
            os.mkdir(PATH)
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.connection.cursor()
        if not self.tasksTableExists():
            self.initDatabase()
        return

    def tasksTableExists(self) -> bool:
        tables = self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type = 'table' AND tbl_name = 'Tasks';").fetchall()
        return not tables == []

    def initDatabase(self):
        self.cursor.execute("""CREATE TABLE Tasks (
                taskid INT,
                date INT,
                task TEXT NOT NULL DEFAULT '',
                status INT NOT NULL DEFAULT FALSE,
                PRIMARY KEY (taskid, date),
                CHECK(status IN (0, 1))
            );""")
        self.connection.commit()
        return

    def moveIncompleteTasks(self, date: int):
        new_task_id = 0
        today_max_id = self.cursor.execute("SELECT MAX(taskid) FROM Tasks WHERE date = ?;", [(date)]).fetchall()[0][0]
        if today_max_id != None:
            new_task_id = today_max_id + 1
        tasks_to_move = self.cursor.execute("SELECT taskid, date FROM Tasks WHERE status = False AND date < ?;", [(date)])
        for row in tasks_to_move:
            self.cursor.execute("UPDATE Tasks SET taskid = ?, date = ? WHERE taskid = ? AND date = ?;", [(new_task_id), (date), (int(row[0])), (int(row[1]))])
            new_task_id += 1
        self.connection.commit()
        return

    def insertTask(self, taskid: int, date: int, task: str):
        self.cursor.execute("INSERT INTO Tasks (taskid, date, task) VALUES (?, ?, ?);", [(taskid), (date), (task)])
        self.connection.commit()
        return

    def tasksByDate(self, date: int):
        tasks = self.cursor.execute("SELECT taskid, task, status FROM Tasks WHERE date = ? ORDER BY taskid", [(date)])
        self.connection.commit()
        return tasks

    def deleteTask(self, taskid: int, date: int):
        rows_to_update = int(self.cursor.execute("SELECT COUNT(taskid) FROM Tasks WHERE taskid > ? AND date = ?;", [(taskid), (date)]).fetchall()[0][0])
        self.cursor.execute("DELETE FROM Tasks WHERE taskid = ? AND date = ?;", [(taskid), (date)])
        for i in range(rows_to_update):
            self.cursor.execute("UPDATE Tasks SET taskid = ? WHERE taskid = ? AND date = ?;", [(taskid + i), (taskid + i + 1), (date)])
        self.connection.commit()
        return

    def updateTask(self, taskid: int, date: int, status: bool):
        self.cursor.execute("UPDATE Tasks SET status = ? WHERE taskid = ? AND date = ?;", [(status), (taskid), (date)])
        self.connection.commit()
        return

