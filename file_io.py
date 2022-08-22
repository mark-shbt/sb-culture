import os
import datetime
from user import User


class FileIO:
    @staticmethod
    def write_to_file(user_list: list[User], file_name: str) -> None:
        o_file = open(file_name, "w")
        o_file.write("name,total points,first close guess,first perfect guess\n")
        for user in user_list:
            o_file.write(
                f"{user.name},{user.points},{user.num_first_close_guess},{user.num_first_perfect_guess}\n"
            )
        o_file.close()
