def copyFile(src_file, dirt_file):
    with open(src_file, "rb") as root_file:
        with open(dirt_file, "wb") as copy_file:
            while True:
                data = root_file.read(1024)
                if data:
                    copy_file.write(data)
                else:
                    break