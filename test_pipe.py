import sys
import os

try:
    # close stdout
    os.close(1)
    print("hello")
except Exception as e:
    # we need to open a new fd to write the error so we can see it
    fd = os.open("error.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    os.write(fd, str(e).encode())
    os.close(fd)
