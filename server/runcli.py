import processor
from datahandler.datahandler import DataHandler


def run() -> None:
    datahandler = DataHandler("../data/", True)
    command = input(">> ")
    while command != "exit":
        print(processor.process(datahandler, command))
        command = input(">> ")
