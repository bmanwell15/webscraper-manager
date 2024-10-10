from rich.table import Table
from rich.console import Console
from rich.box import MINIMAL
from datetime import datetime
import time
import threading



class WebScraperManager:
    sendingCommand = False
    console = Console()
    webScraperClasses = {} # Holds the class definitions of scrapers
    webScrapers = {} # Holds the scraper objects themselves
    lock = threading.Lock()

    def createDataRows():
        rows = []
        index = 1
            
        for scraper in WebScraperManager.webScrapers.values():
            scraperStatus = WebScraperManager.interpretStatusCode(scraper.status)
            cycleTime = f"{scraper.cycleTime} sec" if scraper.mode == "Interval" else "--"
            nextCycleAt = str(datetime.fromtimestamp(scraper.nextCycleTimeAt)) if scraper.nextCycleTimeAt != "--" else "[white]---"
            nextCycleAt = nextCycleAt[:nextCycleAt.find(".")]
            
            lastCycleAt = str(datetime.fromtimestamp(scraper.lastCycleTimeAt)) if scraper.lastCycleTimeAt != "--" else "[white]---"
            lastCycleAt = lastCycleAt[:lastCycleAt.find(".")]
            row = [
                str(index),
                str(scraper.name),
                str(scraper.lastLoopOutput),
                str(scraperStatus),
                str(cycleTime),
                str(lastCycleAt),
                str(nextCycleAt),
                str(scraper.core),
                f"{(scraper.fileSize/1024):.2f}KB"
            ]
            rows.append(row)
            index += 1
        return rows

    def updateDataTable(dowhile=True):
        table = Table(box=MINIMAL)
        table.add_column("Index", style="white bold", width=5)
        table.add_column("Name", style="purple")
        table.add_column("Current Output", style="blue", width=30, justify="left")
        table.add_column("Status", style="bold")
        table.add_column("Cycle Time")
        table.add_column("Last Cycle")
        table.add_column("Next Cycle At", style="green")
        table.add_column("Core")
        table.add_column("File Size")
        for row in WebScraperManager.createDataRows():
            table.add_row(*row)
        
        print("\033c", end="")
        WebScraperManager.console.print(table)

    
    def processCommand(command: str):
        command = command.strip()
        commandSegments = command.split(" ")
        if commandSegments[0] == "load":
            try:
                WebScraperManager.loadScaper(commandSegments[1])
            except FileNotFoundError:
                print("The file", commandSegments[1], "was not found...")
                return
            print("Loaded scraper from", commandSegments[1])
    

    def loadScaper(filepath: str):
        print("Loading scraper from ", filepath, "...", sep="")
        print("Reading file contents...")

        # Read file contents
        scraperFile = open(filepath, "r")
        scraperContent = ''.join(scraperFile.readlines())
        scraperFileSize = len(scraperContent)

        # Define new Class and call start() method
        className = scraperContent[scraperContent.find("class ") + 6: scraperContent.index("(", scraperContent.find("class ") + 6)]
        exec(scraperContent, WebScraperManager.webScraperClasses)
        scraper = WebScraperManager.webScraperClasses[className]() # scraper is of type or subtype Scraper()
        scraper.name = className
        WebScraperManager.webScrapers[scraper.name] = scraper
        scraper.fileSize = scraperFileSize
        
        print("Calling startup...")
        try:
            scraper._start()
        except:
            scraper.status = -1
            print("Failed to start!")
        
        threading.Thread(target=WebScraperManager.processScheduler, daemon=True, args=(scraper)).start()

        WebScraperManager.updateDataTable()
    

    def processScheduler(scraper):
        while not WebScraperManager.sendingCommand:
            for scraperName in WebScraperManager.webScrapers:
                if WebScraperManager.webScrapers[scraperName].nextCycleTimeAt != "--" and time.time() >= WebScraperManager.webScrapers[scraperName].nextCycleTimeAt:
                    WebScraperManager.webScrapers[scraperName].status = 2
                    if not WebScraperManager.sendingCommand:
                        WebScraperManager.updateDataTable()
                    catchException = False
                    try:
                        loopResults = WebScraperManager.webScrapers[scraperName].loop()
                    except:
                        loopResults = ""
                        catchException = True
                        WebScraperManager.webScrapers[scraperName].status = -1
                        return
                    WebScraperManager.webScrapers[scraperName].lastLoopOutput = loopResults
                    if not catchException:
                        WebScraperManager.webScrapers[scraperName].status = 3 if WebScraperManager.webScrapers[scraperName].mode == "Schedule" else 1

                    WebScraperManager.webScrapers[scraperName].lastCycleTimeAt = time.time()
                    if WebScraperManager.webScrapers[scraperName].mode == "Interval":
                        WebScraperManager.webScrapers[scraperName].nextCycleTimeAt = time.time() + WebScraperManager.webScrapers[scraperName].cycleTime
                    else:
                        WebScraperManager.webScrapers[scraperName].nextCycleTimeAt = "--"
                    
                    if not WebScraperManager.sendingCommand:
                        WebScraperManager.updateDataTable()
    

    def interpretStatusCode(code: int):
        if code == 1: return "[green]OK"
        if code == 2: return "[blue]RUNNING"
        if code == 3: return "[cyan]DONE"
        if code > 3: return f"[yellow]WARNING [{code}]"
        if code < 0: return f"[red]ERROR [{code}]"
        return f"UNKOWN"


def main():
    WebScraperManager.updateDataTable()
    while True:
        input()
        WebScraperManager.sendingCommand = True
        print("\033c", end="")
        WebScraperManager.updateDataTable()
        command = input("> ")
        WebScraperManager.processCommand(command)
        WebScraperManager.sendingCommand = False


if __name__ == "__main__":
    main()