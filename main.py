from rich.table import Table
from rich.console import Console
from rich.live import Live
import time
import threading



class WebScraperManager:
    sendingCommand = False
    console = Console()
    webScraperMetaData = [
        {
            "name": "test",
            "output": "This is a test",
            "status": 1,
            "cycleTime": 9000
        },

        {
            "name": "test2",
            "output": "This is also a test",
            "status": -1,
            "cycleTime": 120000
        }
    ]

    def createDataTable(data):
        table = Table(box=None)

        table.add_column("Index", style="white bold", width=5)
        table.add_column("Name", style="purple")
        table.add_column("Current Output", style="blue", width=30, justify="left")
        table.add_column("Status")
        table.add_column("Cycle Time")
        #table.add_column("Core")

        index = 1
        for row in WebScraperManager.webScraperMetaData:
             data = [str(value) for value in row.values()]
             data.insert(0, str(index))
             table.add_row(*data)
             index += 1
        return table

    def updateDataTable(dowhile=True):
        with Live(WebScraperManager.createDataTable(WebScraperManager.webScraperMetaData), console=WebScraperManager.console, refresh_per_second=4) as live:
            while not WebScraperManager.sendingCommand or dowhile:
                live.update(WebScraperManager.createDataTable(WebScraperManager.webScraperMetaData))
                time.sleep(1)
                dowhile = False


def main():
    t = threading.Thread(target=WebScraperManager.updateDataTable, daemon=True)
    t.start()
     
    while True:
        input()
        WebScraperManager.sendingCommand = True
        t.join()
        WebScraperManager.console.clear()
        print("\033c", end="")
        WebScraperManager.updateDataTable()
        comand = input("> ")
        # processCommand(c)
        WebScraperManager.sendingCommand = False
        t = threading.Thread(target=WebScraperManager.updateDataTable, daemon=True)
        t.start()


main()