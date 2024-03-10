from datetime import datetime, timedelta
from dateutil.parser import parse
import pkg_resources
import os
import platform
import calendar
# Debugging tool to check the variables, dates, and months
# import pdb
FILE = pkg_resources.resource_filename(__name__,"./test_holidays.txt")
class VariableParser:
    """Parses the variables from the file and stores them in a dictionary
    Attributes
    ----------
        variables : dict -> A dictionary that stores the variables begginning with "$" from the file.
        
    Methods
    -------
        parse(file) -> Parses the variables from the file and stores them in a dictionary.
    """
    def __init__(self,):
        self.variables = {}

    def parse(self, file):
        with open(file, 'r') as file:
            for line in file:
                if line.startswith('#V#'):
                    variable,graphic = line.split(" = ")
                    variable = variable[3:]
                    graphic = graphic.rstrip('\n')
                    self.variables[variable.lower()] = graphic

class DateParser:
    """Parses the dates from the file and stores them in a dictionary
    Attributes
    ----------
        dates : dict -> A dictionary that stores the dates and their correlating holidays correlating with the test_holidays.txt file.
    
    Methods
    -------
        parse(file) -> Parses the dates from the file and stores them in a dictionary.
    """
    def __init__(self,):
        self.dates = {}

    def parse(self, file):
        with open(file, 'r') as file:
            for line in file:
                if line.startswith('$'):
                    holiday,date = line.split(" = ")
                    holiday = holiday.lstrip('$')
                    holiday = holiday.lower()
                    holiday = holiday.replace('"','')
                    date = date.strip()
                    if date.startswith('(#O#'):
                        date = date.lstrip('(#O#')
                        date = date.rstrip(')')
                        date = date.lower()
                        self.dates[date] = holiday
                    elif date.startswith('(#V#'):
                        date = date.lstrip('(#V#')
                        date = date.split(' ')
                        date = date[0]
                    elif ":" in date:
                        start,end = date.split(" : ")
                        month,day,year = start.split("/")
                        month,day,year = int(month), int(day), int(year)
                        start_date = datetime(month=month,day=day,year=year).date()
                        
                        month,day,year = end.split("/")
                        month,day,year = int(month), int(day), int(year)
                        end_date = datetime(month=month,day=day,year=year).date()
                        
                        delta = timedelta(days=1)
                        while start_date <= end_date:
                            self.dates[start_date.strftime("%m/%d/%Y")] = holiday
                            start_date += delta
                        continue

                    if ' ' in holiday:
                        holiday = holiday.split(' ')
                        holiday = ''.join(holiday)

                    self.dates[date] = holiday

class MonthParser:
    """Parses the months from the file and stores them in a dictionary
    Attributes
    ----------
        months : dict -> A dictionary that stores the months and their correlating number.
        data_months : dict -> A dictionary that stores the months from the file.
    
    Methods
    -------
        parse(file) -> Parses the months from the file and stores them in a dictionary.
    """
    def __init__(self,):
        self.months = {1:'january',2:'february',3:'march',4:'april',5:'may',6:'june',7:'july',8:'august',9:'september',10:'october',11:'november',12:'december'}
        self.data_months = {}

    def parse(self, file):
        with open(file, 'r') as file:
            current_month = None
            for line in file:
                if '***' in line:
                    month = line.split(' ')[1]
                    month = month.strip()
                    month = month.lower()
                    self.data_months[month] = []
                    current_month = month
                else:
                    if current_month is not None and ' = ' in line:
                        _,right = line.split(' = ')
                        right = right.strip()
                        self.data_months[current_month].append(right)
                    else:
                        continue

class Format:
    """Parses the file and stores the variables, dates, and months in dictionaries. It also has methods to find the graphics based on the input.
    Attributes
    ----------
        format : str -> The format that the user inputs. It can be a date or a word.
        variables : dict -> A dictionary that stores the variables from the file.
        dates : dict -> A dictionary that stores the dates from the file.
        months : dict -> A dictionary that stores the months from the file.

    Methods
    -------
        _clear_console() -> Clears the console based on the operating system.
        _is_date() -> Checks if the input is a date. If it is, it returns True. If it isn't, it returns False.
        is_char(string:str) -> Checks if the string contains a character. If it does, it returns True. If it doesn't, it returns False.
        find_file(file=None) -> A function that checks the VariableParser dict, DateParser dict and MonthParser dict to find a file in the test_holidays.txt and returns the reference. 
        find_files() -> An extension of the find_file method that allows the user to input multiple formats and find the graphics for each format.
        find_files_month(month=None) -> Finds all the graphics that correlate to the month inputted by the user. Can use either the full month name or the month's number.

    """
    def __init__(self,format=None):
        """
        Parameters
        ----------
            format : str -> The format that the user inputs. It can be a date or a word.
        """
        self.format = format
        variables_dict = VariableParser()
        variables_dict.parse(FILE)
        self.variables = variables_dict.variables
        
        dates_dict = DateParser()
        dates_dict.parse(FILE)
        self.dates = dates_dict.dates

        months_dates = MonthParser()
        months_dates.parse(FILE)
        self.months = months_dates
    
    def _clear_console(self,):
        """Clears the console based on the operating system."""
        if platform.system() == 'Windows':
            os.system('cls')
        elif platform.system() == 'Linux' or platform.system() == 'Darwin':
            os.system('clear')
        else:
            print('\n' * 100)

    def _is_date(self,) -> bool:
        """Checks if the input is a date. If it is, it returns True. If it isn't, it returns False."""
        try:
            parse(self.format,fuzzy=True)
            return True
        except ValueError:
            return False
    
    def is_char(self,string:str) -> bool:
        """Checks if the string contains a character. If it does, it returns True. If it doesn't, it returns False."""
        for char in string:
            if char.isalpha():
                return True
        return False
    def find_file(self,file=None) -> str|bool:
        """A function that checks the VariableParser dict, DateParser dict and MonthParser dict to find a file in the test_holidays.txt and returns the reference. 
        """
        if file is None:
            file = input("Enter the format: Example: 12/25/2020 or Christmas\n")
        self.format = file
        # checks if the input is a date and not a character; if it has a char it will skip to the next line of the program
        if self._is_date() and not self.is_char(self.format):
            self.format = parse(self.format,fuzzy=True).strftime("%m/%d/%Y")
            # I stored the data without the current year so I need to remove the current year when checking for the graphic
            if self.format[-4:] == '2024':
                results = self.dates.get(self.format[:-5],None)
            else:
            # If the input data is already in the correct format, I will check the dates dictionary for the graphic
                results = self.dates.get(self.format,None)

            if results is None:
                return None
            results = results.lower()
            return self.variables.get(results,None)
        else:
            self.format = self.format.lower()
            if len(self.format) > 10:
                return self.variables.get(self.dates.get(self.format,None),None)
            return self.variables.get(self.format,None)
        
    def find_files(self,):
        """An extension of the find_file method that allows the user to input multiple formats and find the graphics for each format.
        """
        # clears the console so the user can input the formats, see the results, and input another format
        self._clear_console()
        while True:
            file = input("Enter the format: Example: 12/25/2020 or Christmas\nEnter 'q' to quit\n\n")
            file = file.split(' ')
            file = ''.join(file)
            file = file.lower()
            if file == 'q':
                break
            if self.find_file(file) is not None:
                print(f'Found the graphic:\n {self.find_file(file)}\n')
            else:
                print(f'Could not find the graphic that correlates to {file}\n')
    
    # def find_files_over(self,dates=None):
    #     self._clear_console()

    #     dates_covered = {}
    #     start,end = dates.split(":")
    #     start = start.strip()
    #     end = end.strip()
    #     if '/' in start:
    #         month,day,year = start.split("/")
    #     else:
    #         month,day,year = start.split(":")
    #     month,day,year = int(month), int(day), int(year)
    #     start_date = datetime(month=month,day=day,year=year).date()
        
    #     if '/' in end:
    #         month,day,year = end.split("/")
    #     else:
    #         month,day,year = end.split(":")
    #     month,day,year = int(month), int(day), int(year)
    #     end_date = datetime(month=month,day=day,year=year).date()
        
    #     delta = timedelta(days=1)
    #     while start_date <= end_date:
    #         with_year = self.find_file(start_date.strftime("%m/%d/%Y"))
    #         without_year = self.find_file(start_date.strftime("%m/%d"))
    #         if results is not None:
    #             dates_covered[start_date.strftime("%m/%d/%Y")] = results
    #         start_date += delta
    #     for date,graphic in dates_covered.items():
    #         print(f'{date} : {graphic}')

    def find_files_month(self,month=None):
        """Finds all the graphics that correlate to the month inputted by the user. Can use either the full month name or the month's number."""
        if isinstance(month,int):
            current_month = calendar.month_name[month].lower()
            return self.months.data_months.get(current_month,None)
        else:
            month = month.lower()
            return self.months.data_months.get(month,None)