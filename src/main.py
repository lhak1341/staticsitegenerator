import os
import shutil


def main():
    PUBLIC_PATH = "./public"
    STATIC_PATH = "./static"
    if os.path.exists(PUBLIC_PATH):
        shutil.rmtree(PUBLIC_PATH)
    os.mkdir(PUBLIC_PATH)
    recursive_copy(STATIC_PATH, PUBLIC_PATH)

def recursive_copy(src, dest):
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            # print(f"Copied {src_path} to {dest_path}")
        else:
            os.mkdir(dest_path)
            recursive_copy(src_path, dest_path)

if __name__ == "__main__":
    main()
