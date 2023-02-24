from application import salary;
from application.db import people;

from datetime import datetime;

import confound_prediction;

if __name__ == '__main__':
    print(salary.calculate_salary());
    print(people.get_employees())

    print(f"Текущая дата:  {datetime.today()}")