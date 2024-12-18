# Webscraper Manager

This program can store, organize, and rum multiple webscrapers at the same time. Using some of the built-in classes, complex webscraping can easily be maintained to run at specific times or intervals.

Created By Benjamin Manwell

## Version Log

| Version | Date       | Release Notes                                                                                     |
| ------- | ---------- | ------------------------------------------------------------------------------------------------- |
| 1.0.0   | 10/26/2024 | Initial Release                                                                                   |
| 1.0.1   | 10/28/2024 | Added quit command.&nbsp;*save* and *restore* commands can now take filepaths as parameters. |
| 1.0.2   | 11/19/2024 | Added RUN scraper type. Small optimization improvements |

## Using the Manager

Make sure that the following dependencies has been installed:

```bash
    pip install selenium
    pip install rich
```

When running the program, press enter to switch to command mode. This will be designated by a ">" symbol next to the cursor. Type help to see a list of avaliable commands.

## Making a Scraper

#### Importing files

When making a scraper that is compatible with the manager, the scraper will have to be a subclass of a premade template. To add the template to your file, import the scraper.py classes:

```python
    from Scrapers.Scraper import *
```

Notice that the filepath of the import statement is relitive to the root directory of the project.

#### Creating the class

To Make the class compatible with the manager, it must be a subclass of one of the following scraper templates:
    - Interval Scraper: This scraper will execute every *x* amount of seconds.
    - Scheduled Scraper: This scraper will execute **ONCE** on the specified date and time.
    - Timed Scraper: This scraper will execute once a day at the specified time.
    - Run Scraper: This scraper will execute immediently once the scraper is loaded into the program

Below are basic examples on how to initialize each type. Note how each one takes differenr parameters to initialize.

```python
class Interval(IntervalScraper):
    def __init__(self, cycleTime=30) -> None:
        super().__init__(cycleTime)

    def setup(self):
        # Do stuff when init into manager program
        self.driver = Scraper.getDriver()
        self.driver.get("URL")
  
    def loop(self):
        # Do stuff every self.cycleTime seconds
        return output
```

```python
class Scheduled(ScheduledScraper):
    def __init__(self):
        #                         Y     M   D   H   m   s
        super().__init__(datetime(2024, 10, 10, 16, 15, 0))

    def setup(self):
        # Do stuff when init into manager program
        self.driver = Scraper.getDriver()
        self.driver.get("URL")
  
    def execute(self):
        # Do stuff when time hits
        return output
```

```python
class Timed(TimedScraper):
    def __init__(self):
        #                         Y     M   D   H   m
        super().__init__(datetime(2024, 10, 10, 20, 42))

    def setup(self):
        # Do stuff when init into manager program
        self.driver = Scraper.getDriver()
        self.driver.get("URL")
  
    def loop(self):
        # Do stuff at specific time
        return output
```

```python
class Run(RunScraper):
    MC_VERSION = "1.21.3"
    def __init__(self) -> None:
        super().__init__()

    def setup(self):
        # Do stuff when init into manager program
        self.driver = Scraper.getDriver()
    
    def loop(self):
        # Do stuff when init into program (essentually the same as set up in this case)
        return output
```

Note the Scraper.getDriver() function is being used to automatically get a driver.
