
import string, os, json
import pandas as pd
from database import SqlAlchemy

db_client = SqlAlchemy('./database.db')

class Country:
    def __init__(self, *args) -> None:
        row_data = args[0]
        (self.index, self.name, self.area, self.population) = row_data
        self.calculate_density()

    def calculate_density(self):
        self.density = self.population / self.area
    
    def json(self) -> dict:
        return self.__dict__


def db_to_csv(
    db_client: SqlAlchemy, 
    out_file_path: str = f'./files/out_csv_file.csv'
):
    """
    Puts all the info fro a db into a csv file.
    The 'db_client' object defines a connection to the database.
    """
    records = db_client.execute_sql_statement("select * from countries;")
    df = pd.DataFrame.from_records(records)
    df.columns = ['index', 'name', 'area_sqkm', 'population_2013']

    df['density'] = df['population_2013'] / df['area_sqkm']
    df = df.drop('index', axis=1)
    df_to_file(df, header=True, output_file=out_file_path)


def write_alphabet_on_file(filename: str, letters_in_line = 3):
    """
    Writes alphabet on file.
    :param str filename: Name of the file in which we write the data.
    :param int letters_in_file: Number of consecutive letters in each line of 
    the file to be written.
    """

    slices_of_letters = []
    for i in range(0, letters_in_line):
        slices_of_letters.append(string.ascii_lowercase[i::letters_in_line])

    with open(filename, 'w') as file:
        for consecutive_letters in zip(*slices_of_letters):
            file.write(''.join(consecutive_letters) + '\n')            


def generate_letter_files(directory_path: str = "./letters"):
    """
    Generates several files with the name of the letter of the alphabet.
    Inside each file, it appears the letter of the alphabet.
    """

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    for letter in string.ascii_lowercase:
        with open(f"{directory_path}/{letter}.txt", 'w') as file:
            file.write(letter)


def create_list_from_letter_files(
    match_string: str = 'python', 
    directory_path: str = "./letters"
):
    """
    Creates and returns a list containing all the letters from the alphabet.
    We read the letters from files.
    Each alphabet file contains the letter shown in the file name.

    The only letters included in the list are those considered in the `match_string`
    given as input parameter from the function.
    """
    alphabet_list = []

    if not os.path.exists(directory_path):
        print(f"Directory {directory_path} does not exist...")
        return alphabet_list

    for file_name in os.listdir(directory_path):
        if file_name.split(".")[0] in match_string:
            with open(f"{directory_path}/{file_name}", "r") as file:
                alphabet_list.append(file.read())
    
    return alphabet_list


def dict_to_json(dictionary: dict, target_file_name: str = "./json/employees.json"):
    """
    Creates a json file out of a dictionary.
    :param str dictionary: Input dictionary.
    :param str target_file_name: Target file name.
    """
    with open(target_file_name, 'w') as file:
        json.dump(dictionary, file, indent=4)

    
def json_to_dictionary(target_file_name: str = "./json/employees.json"):
    """
    Given an input json file, it returns a dictionary.
    """
    with open(target_file_name, 'r') as file:
        dictionary = json.load(file)

    return dictionary


def ask_username_and_password() -> tuple:
    """
    Asks for input username and password.
    Validates password.
    Password conditions
    1. Password must contain at least one number.
    2. Password must contain one uppercase letter.
    3. Password has to be at least 5 characters long.

    If password does not satisfies the conditions, it returns ('', '')
    In other case, it returns (username, password)
    """
    input_username = input("Please introduce your username: ")
    input_password = input("Please introduce your desired password: ")

    password_error_conditions = [
        (
            "Password has to be at least 5 characters long", 
            len(input_password) > 4
        ),
        (
            "Password must contain one uppercase letter", 
            any(char.isupper() for char in input_password)
        ),
        (
            "Password must contain at least one number", 
            any(char.isdigit() for char in input_password)
        ),
    ]

    password_conditions = [x[1] for x in password_error_conditions]

    if all(password_conditions):
        print("Password is fine!")
        return (input_username, input_password)
    
    
    error_messages = [x[0] for x in password_error_conditions]
    error_indexes = [
        index_condition 
        for index_condition, condition 
        in enumerate(password_conditions)
        if not(condition)
    ]

    for error_index in error_indexes:
        print(f"Password error: {error_messages[error_index]}")

    return ('', '')    


def process_countries(filename: str, target_filename: str):
    """
    Reads countries files, processes it, and creates a new file out of it.
    """
    removable_characters = ["", "Top of Page\n"]
    returned_data = ""
    with open(filename, 'r') as file:
        for line in file:
            returned_data += line if line not in removable_characters and len(line)>2 else ''                

    with open(target_filename, 'w') as file:
        file.write(returned_data)    


def df_to_file(
    df: pd.DataFrame, 
    output_file: str, 
    index=False, 
    header=None
):
    """
    Given the output filepath, it exports a dataframe 
    data to the specified target file.
    """
    df.to_csv(output_file, index=index, header=header)


def return_registered_countries(
    input_countries: list, 
    filename_path: str = "./files/countries_clean.txt"
) -> list:
    """
    Given a list of countries, the list is filtered so that we only 
    get the countries that exists on the given txt file path.
    """
    if not os.path.exists(filename_path):
        raise Exception(f"Filepath '{filename_path}' does not exist...")
    
    with open(filename_path, 'r') as file:
        file_countries = file.read().splitlines()

    return list(filter(lambda c: c in file_countries, input_countries))


#############



