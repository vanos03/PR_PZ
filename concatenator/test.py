import sys
import subprocess

def append_to_boot(input_files):
    try:
        with open("boot", 'ab') as out_file:
            for input_file in input_files:
                with open(input_file, 'rb') as in_file:
                    file_content = in_file.read()
                    out_file.write(file_content)
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py input_file1 [input_file2 ...]")
        sys.exit(1)

    input_files = sys.argv[1:]

    append_to_boot(input_files)
