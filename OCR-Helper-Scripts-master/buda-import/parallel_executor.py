from concurrent.futures import ThreadPoolExecutor
import csv
import threading
import logging

class ParallelTaskExecutor():
    def __init__(self, todo_csv_filename, done_csv_filename, func, max_workers=4):
        self.todo_csv_filename = todo_csv_filename
        self.done_csv_filename = done_csv_filename
        self.todos = self._get_todos()
        self.fileslock = threading.Lock()
        self.max_workers = max_workers
        self.func = func

    def run_func(self, todoline):
        logging.info("parallel executor: run function on "+",".join(todoline))
        doneline = self.func(todoline)
        self.set_done(doneline)
        return doneline

    def _get_todos(self):
        res = []
        with open(self.todo_csv_filename) as f:
            csvreader = csv.reader(f)
            for todoline in csvreader:
                res.append(todoline)
        return res

    def set_done(self, doneline):
        self.fileslock.acquire()
        try:
            with open(self.done_csv_filename, "a") as f:
                csvwriter = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(doneline)
        finally:
            self.fileslock.release()        

    def run(self):
        logging.info(f"start parallel processing of {len(self.todos)} tasks ({self.max_workers} in parallel)")
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self.run_func, self.todos, timeout=40)