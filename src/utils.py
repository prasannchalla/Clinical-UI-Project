from datetime import datetime 

def input_and_parse_date():
    while True:
        entered_date = input("Enter visit date (any format): ")
        try:
            parsed_date = parse_date(entered_date)
            return parsed_date
        except ValueError:
            print("Invalid date format. Try again (e.g., 2025-05-15, 15/05/2025, May 15, 2025).")
    

#formating any date format to YYYY-MM-DD
def parse_date(date_str):
    """Try multiple date formats and return standardized YYYY-MM-DD format."""
    formats = ["%Y-%m-%d", "%m-%d-%Y", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y", "%B %d, %Y", "%b %d, %Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError("Invalid date format.")