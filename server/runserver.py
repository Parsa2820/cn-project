import processor


def run() -> None:
    command = input(">> ")
    while command != "exit":
        print(processor.process(command))
        command = input(">> ")
