import pickle


def system_to_file(path, system):
    with open(path, "wb") as bin_file:
        bin_data = pickle.dumps(system)
        bin_file.write(bin_data)


def system_from_file(path):
    with open(path, "rb") as bin_file:
        kripke = pickle.load(bin_file)
        return kripke
