moku IP: 192.168.73.1


------- Future Improvements

Add waveform parameter customization (frequency, duration, amplitude)

Implement graceful disconnection using inst.close()

Support multiple commands or waveform types

create a main to run : mqtt, gui for pid, voltage control

------- Notes
#get the data from mqtt and put it into a text file
        #write to a csv file
        with open("data.csv", "w") as csv:
            csv.write("value, time\n")

            while count <= 5000:
                value = mqtt.latest_value()  # Get the latest value from MQTT
                count += 1
                if value is not None:
                    #if numbers are getting read, put into csv
                    csv.write(f"{value}, {count}\n")
                    print(f"{value}")

        #parse csv data
        df = pd.read_csv("data.csv", header=0)
        df["displacement"] = df["value"].diff().fillna(0)  # Calculate displacement
        df.to_csv("data.csv", index=False) #replaces original csv with new data