from functions.get_files_content import get_file_content

print(len(get_file_content("calculator", "lorem.txt")))
print("test 2:")
print(get_file_content("calculator", "pkg/calculator.py"))
print("test 3:")
print(get_file_content("calculator", "/bin/cat"))
print("test 4:")
print(get_file_content("calculator", "pkg/does_not_exist.py"))
print("test 5:")
print(get_file_content("calculator", "main.py"))