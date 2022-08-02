import processor
from datahandler.datahandler import DataHandler


def run() -> None:
    datahandler = DataHandler("./test_data/")
    command = input(">> ")
    while command != "exit":
        print(processor.process(datahandler, command))
        command = input(">> ")
