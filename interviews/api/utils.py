from datetime import datetime
import dateutil.parser as parser


def get_date(start_date_str):
    #start_date = datetime.strptime(start_date_str.strip(), "%Y-%m-%d %H:%M")
    start_date = parser.isoparse(start_date_str)
    return start_date

# def get_date(start_date_str):
#     start_date = datetime.strptime(start_date_str.strip(), "%Y-%m-%d %H:%M")
#     return start_date

# def get_end_date(end_date_str):
#     end_date = datetime.strptime(end_date_str.strip(), "%Y-%m-%d %H:%M")
#     return end_date
