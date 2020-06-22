from configparser import ConfigParser

filename = r".\init\data.ini"


def dbinit():
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section("postgresql"):
        params = parser.items("postgresql")
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("postgre not found")

    return db


def reddinit():
    parser = ConfigParser()
    parser.read(r".\init\data.ini")
    db = {}
    if parser.has_section("reddit"):
        params = parser.items("reddit")
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("reddit section not found")
    
    return db


if __name__ == "__main__":
    print(config())
    print(reddinit())
