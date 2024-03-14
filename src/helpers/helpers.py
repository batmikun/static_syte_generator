import os
import shutil

def delete_public_directory(public_path: str) -> None:
    print("Deleting public directory...")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)


def copy_directories(source_path: str, dest_path: str) -> None:
    print("Copying static assets to public directory...")
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    for filename in os.listdir(source_path):
        from_path = os.path.join(source_path, filename)
        to_path = os.path.join(dest_path, filename)

        print(f" * {from_path} -> {to_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            copy_directories(from_path, to_path)

