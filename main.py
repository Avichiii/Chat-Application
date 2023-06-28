from server import *

if __name__ == "__main__":
    agruments = ArgumentParsing()
    server = Server(agruments.options)
    server.start()
