from functions.get_files_info import get_files_info
print("results of test 1:")
print(get_files_info("calculator"))
print("results of test 2:")
print(get_files_info("calculator", "pkg"))
print("results of test 3:")
print(get_files_info("calculator", "/bin"))
print("results of test 4:")
print(get_files_info("caclculator", "../"))
