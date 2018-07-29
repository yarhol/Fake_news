import os
from os import chdir
from os.path import join


def bit_of_cleaning (source):
    source_folder = join ("C:\\Users\yaron.hollander", "Documents", "fakenews", str(source).capitalize())
    chdir(source_folder)
    files_to_check = [f for f in os.listdir('.')]
    for f in files_to_check:
        the_size = os.stat(f).st_size
        if (the_size < 1000):
            os.remove(f)
            print ("The size of ", f, "was", the_size, ", so I got rid of the bastard.")
        else:
            print("The size of ", f, "was", the_size, ". I like them biiig.")
    # The bit below is for a problem I had with "the telegraph" only.
    if source=="the-telegraph":
        files_to_check = [f for f in os.listdir('.') if f.endswith(".txt")]
        for f in files_to_check:
            with open(f, 'r') as the_file:
                the_text = the_file.read().rstrip()
                if (the_text.endswith("...")):
                    print("File ", f, "was incomplete, so I will get rid of the bastard.")
                    the_file.close()
                    os.remove(f)
                else:
                    print("File ", f, "is cool.")

