import GUI
from instrument_DAq import Microscope
from database import Data
if __name__ == "__main__":
    print("Testing program run...")
    # microscope_controller = Microscope()
    # main_window = GUI.Main_window(microscope_controller)
    # main_window.run()
    path = "../test_database.db"
    d = Data(path)
    err = None
    err = d.create_new_db(path)
    if err is not None:
        print(err)
        err = d.database_connect(path)
        if err is not None:
            print(err)
            exit()
    err = None
    site = "CA-SITE-NUMBER"
    unit ="4"
    stratum ="3"
    level ="ff"
    weight ="3"
    image_front ="whatever"
    image_back ="whatever"
    notes = "nope"
    err = d.insert(site, unit, stratum, level, weight, image_front, image_back, notes)
    print(err)
    d.list_all()


    print("Test concluded.")
