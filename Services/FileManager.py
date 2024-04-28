import pickle  # Importing the pickle module for object serialization.


def system_to_file(path, system):
    """
    Serialize the given system object to a file.

    Args:
        path (str): The path to the file where the serialized data will be stored.
        system (object): The object representing the system to be serialized.

    Returns:
        None
    """
    with open(path, "wb") as bin_file:
        bin_data = pickle.dumps(system)
        bin_file.write(bin_data)


def system_from_file(path):
    """
    Deserialize a system object from a file.

    Args:
        path (str): The path to the file containing the serialized data.

    Returns:
        object: The deserialized system object.
    """
    with open(path, "rb") as bin_file:
        kripke = pickle.load(bin_file)
        return kripke
