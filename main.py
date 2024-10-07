
# print("Please enter a date in DD/MM/YYYY format")
#
# date_input = input()
#
# def validate_date_format(date_str):
#
#   is_format_ok = True
#   day_str = date_str[0:1]
#   month_str = date_str[3:4]
#   year_str = date_str[6:9]
#
#   if int(day_str) not in range(1, 31):
#     print("day str", day_str)
#     is_format_ok = False
#     print("Date should be between 1 and 31!")
#   elif int(month_str) not in range(1, 12):
#     print("month_str", month_str)
#     is_format_ok = False
#     print("Month should be between 1 and 12!")
#   elif int(year_str) not in range(1, 10000):
#     print("year_str", year_str)
#     is_format_ok = False
#     print("Year should be between 1 and 10000")
#   return is_format_ok
#
# def validate_date(date_to_validate):
#   is_valid = True
#   if date_to_validate == "":
#     print(
#         "That's my favorite day! Now please actually enter a date with the DD/MM/YYYY"
#         + " format!")
#     is_valid = False
#   elif len(date_to_validate) != 10:
#     print(
#         "Date is not 10 characters long !Please enter the date in DD/MM/YYYY format"
#     )
#     is_valid = False
#   elif not validate_date_format(date_to_validate):
#     is_valid = False
#
#   return is_valid
#
# validated_date = validate_date(date_input)
#
# if validated_date:
#   print("You entered a valid date! Well done!")
# else:
#   print("")
#
# # write a function to split a date in dd/mm/yyyy format into day, month and year
def split_date(date_str):
  day = date_str[0:2]
  month = date_str[3:5]
  year = date_str[6:10]
  return day, month, year

day, month, year = split_date("12/12/2020")
print("Day: ", day)
print("Month: ", month)
print("Year: ", year)
