# def ave_spd(uphill_time_mins, uphill_rate_mph, downhill_rate_mph):
#     # Convert uphill time from minutes to hours
#     uphill_time_hours = uphill_time_mins / 60

#     # Calculate distances traveled uphill and downhill
#     uphill_distance = uphill_rate_mph * uphill_time_hours
#     downhill_distance = downhill_rate_mph * uphill_time_hours

#     # Total distance traveled
#     total_distance = uphill_distance + downhill_distance

#     # Total time spent traveling uphill and downhill
#     total_time_hours = uphill_time_hours * 2  # Both uphill and downhill times are the same in terms of total time

#     # Calculate average speed
#     average_speed = total_distance / total_time_hours

#     # Return the average speed as an integer (no rounding)
#     return round(average_speed)

# # Test cases
# print(ave_spd(18, 20, 60))  # ➞ 30
# print(ave_spd(30, 10, 30))  # ➞ 15
# print(ave_spd(30, 8, 24))  # ➞ 12



# def sum_of_squares(n):
#     """Calculate the sum of squares of digits of n."""
#     return sum(int(digit) ** 2 for digit in str(n))

# def is_happy_number(n, seen=None):
#     """Determine if a number is a happy number using recursion."""
#     if seen is None:
#         seen = set()

#     # Base case: If n becomes 1, return True
#     if n == 1:
#         return True

#     # If we encounter a cycle that includes 4, return False
#     if n in seen:
#         return False

#     # Add the current number to the seen set
#     seen.add(n)

#     # Recursive case: Calculate sum of squares and call itself
#     next_number = sum_of_squares(n)
#     return is_happy_number(next_number, seen)

# def is_happy(number):
#     """Check if the given number is a happy number."""
#     return is_happy_number(number)

# # Test cases
# print(is_happy(67))       # ➞ False
# print(is_happy(89))        # ➞ False
# print(is_happy(139))       # ➞ True
# print(is_happy(1327))      # ➞ False
# print(is_happy(2871))      # ➞ False
# print(is_happy(3970))      # ➞ True

def is_happy(n, seen = {1}):
    if n in seen:
        return False

    seen.add(n)

    while n != 1 and n not in [x**2 for x in seen]:
        n = sum(int(digit)**2 for digit in str(n))

    return n == 1

result = is_happy(581)
print(result)