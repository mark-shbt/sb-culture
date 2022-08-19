import os
import datetime

class FileWriter:
    @staticmethod
    def write_to_file(file_name: str, dict_name: str, db: dict, to_master: bool, sorted: bool = False) -> None:
        if not to_master:
            curr_date = datetime.datetime.now().strftime('%Y-%m-%d')
            dir_name = f'db/{curr_date}'
            if not os.path.isdir(dir_name):
                os.mkdir(f'db/{curr_date}')
        else:
            dir_name = 'db/master'
        if sorted:
            dict_name = f"SORTED_{dict_name}"
        file_name = f'{dir_name}/{file_name}.py'
        out_file = open(file_name, 'w')
        opening = f"{dict_name} = "
        opening += "{ \n"
        out_file.write(opening)
        for user, value in db.items():
            f_write = f'"{user}": {value},\n'
            out_file.write(f_write)
        out_file.write('}')
        out_file.close()
    
    @staticmethod
    def sort_and_write(users_dict: dict, words_dict: dict, to_master: bool) -> None:
        users = dict(sorted(users_dict.items()))
        sorted_users = dict(
            sorted(users_dict.items(), key=lambda x: x[1], reverse=True))
        words = dict(sorted(words_dict.items()))
        sorted_words = dict(sorted(words_dict.items(), key=lambda x: x[1], reverse=True))
        FileWriter.write_to_file('users', 'USERS', users, to_master)
        FileWriter.write_to_file('sorted_users', 'USERS', sorted_users, to_master, sorted=True)
        FileWriter.write_to_file('words', 'WORDS', words, to_master)
        FileWriter.write_to_file('sorted_words', 'WORDS', sorted_words, to_master, sorted=True)
