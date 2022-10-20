from reader import ReaderProcess, DeviceEngine

# from multiprocessing import Process, Manager
# concurrent.futures

# column_names = ['F7', 'Fp1', 'Fp2', 'F8', 'F3', 'Fz', 'F4', 'C3', 'Cz', 'P8', 'P7', 'Pz', 'P4', 'T3', 'P3', 'O1',
#                 'O2', 'C4', 'T4', 'A2']

# def run():
#     pass


if __name__ == '__main__':
    # with Manager() as manager:
    #     data_exchange = manager.dict()


    device_engine = DeviceEngine()
    reader_process = ReaderProcess({}, device_engine) # FileEngine("binary_ivan.dat"))

    reader_process.run()
        # reader = Process(target=run, args=(data_exchange,))
        # reader.start()

