from research.Parsing.AvitoParser import AvitoParser


if __name__ == "__main__":
    print("Начинается сбор квартир")
    parser = AvitoParser()
    parser.start()