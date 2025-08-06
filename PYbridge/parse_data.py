
import pandas as pd

class To_Csv():

    #take name of folder open csv file/make
    def open_file(self, name):
        with open(name, "w") as csv:
            csv.write("Value\n") #header

    #get displacement
    def calc_dis(self, name):
        df = pd.read_csv(name, header=0)
        df["displacement"] = df["Value"].diff().fillna(0)  # Calculate displacement
        df.to_csv(name, index=False) #replaces original csv with new data

    def write_file(self, name, data):
        with open(name, "a") as f:
            f.write(f"{data}\n")



