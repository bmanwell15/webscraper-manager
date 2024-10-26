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
                f"{(scraper.fileSize/1024):.2f}KB"
            ]
            rows.append(row)
            index += 1
        return rows

    def updateDataTable(dowhile=True):
        WebScraperManager.lock.acquire()
        table = Table(box=MINIMAL)
        table.add_column("Index", style="white bold", width=5)
        table.add_column("Name", style="purple")
        table.add_column("Current Output", style="blue", width=30, justify="left")
        table.add_column("Status", style="bold")
        table.add_column("Cycle Time")
        table.add_column("Last Cycle")
        table.add_column("Next Cycle At", style="green")
        table.add_column("File Size")
        for row in WebScraperManager.createDataRows():
            table.add_row(*row)
        
        print("\033c", end="")
        WebScraperManager.console.print(table)
        WebScraperManager.lock.release()

    
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
        elif commandSegments[0] == "save":
            print("Saving data...")
            WebScraperManager.save()
            print("Save complete!")
        elif commandSegments[0] == "restore":
            print("Loading Save...")
            WebScraperManager.restoreSave()
            print("Complete!")
        elif commandSegments[0] == "delete":
            try:
                a = commandSegments[2]
            except IndexError:
                commandSegments.append("filepath")

            print("Deleting scraper from", commandSegments[1])
            for scraper in WebScraperManager.webScrapers:
                if (commandSegments[2] == "filepath" and scraper.filePath == commandSegments[1]) or (commandSegments[2] == "name" and scraper.name == commandSegments[1]) or (commandSegments[2] == "mode" and scraper.mode == commandSegments[1]):
                    WebScraperManager.webScrapers.pop(scraper.name)
                    WebScraperManager.webScraperClasses.pop(scraper.name)
                    break
            print("Deleted Scraper")
        elif commandSegments[0] == "help":
            print("Running Webscraper Manager V1.0.0")
            print("List of commands:")
            print("\t- help\n\tShows this page")
            print("\n\t- load [filepath]\n\tLoads the scraper from the specified file path. The filepath but lead to a python file that contains one subclass of a Scraper type.")
            print("\n\t- save\n\tSaves the current scrapers into a save file that can be restored if the program is stopped")
            print("\n\t- restore\n\tLoads all scapers in the save file (save.data).")
            print("\n\t- delete [filepath] [specifier]\n\tDeletes the specified scraper. The specifier flag is optional and it specifies how the scraper will be found. Possible options are name, filepath, or mode. The default is filepath.")
            print("\n\nPress enter to return.")
            input()
            WebScraperManager.updateDataTable()
    

    def loadScaper(filepath: str, resoringSave=False):
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
        scraper.filePath = filepath
        WebScraperManager.webScrapers[scraper.name] = scraper
        scraper.fileSize = scraperFileSize
        
        print("Calling startup...")
        try:
            scraper._start()
        except:
            scraper.status = -1
            print("Failed to start!")
        
        threading.Thread(target=WebScraperManager.processScheduler, daemon=True, args=[scraper]).start()
        if not resoringSave:
            WebScraperManager.updateDataTable()
    
    def save():
        saveFile = open("save.data", "w")
        for scraper in WebScraperManager.webScrapers.values():
            print(scraper.filePath, file=saveFile)
    
    def restoreSave():
        saveFile = open("save.data", "r")
        lines = saveFile.readlines()
        saveFile.close()
        index = 1
        for line in lines:
            print("Loading Scraper", index, "of", len(lines))
            line = line.replace("\n", "")
            try:
                WebScraperManager.loadScaper(line, True)
            except FileNotFoundError:
                print("The file", line, "was not found...")
            index += 1
    

    def processScheduler(scraper):
        while True:
            if scraper.isDeleted: break
            if (scraper.nextCycleTimeAt != "--" and time.time() >= scraper.nextCycleTimeAt):
                scraper.status = 2
                if not WebScraperManager.sendingCommand:
                    WebScraperManager.updateDataTable()

                catchException = False
                try:
                    loopResults = scraper.loop()
                except:
                    loopResults = ""
                    catchException = True
                    scraper.status = -1
                    return

                if not catchException:
                    scraper.status = 3 if scraper.mode == "Schedule" else 1

                scraper.lastCycleTimeAt = time.time()
                scraper.lastLoopOutput = loopResults

                if scraper.mode == "Interval":
                    scraper.nextCycleTimeAt = time.time() + scraper.cycleTime
                elif scraper.mode == "Schedule":
                    scraper.nextCycleTimeAt = "--"
                elif scraper.mode == "Time":
                    scraper.nextCycleTimeAt = time.time() + (24 * 60 * 60) # Seconds in one day
                
                if not WebScraperManager.sendingCommand:
                    WebScraperManager.updateDataTable()
                
                if scraper.mode == "Schedule": break
                if scraper.mode == "Time": time.sleep(120)
    

    def interpretStatusCode(code: int):
        if code == 1: return "[green]OK"
        if code == 2: return "[blue]RUNNING"
        if code == 3: return "[cyan]DONE"
        if code > 3: return f"[yellow]WARNING [{code}]"
        if code < 0: return f"[red]ERROR [{code}]"
        return f"UNKOWN"
# END CLASS

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