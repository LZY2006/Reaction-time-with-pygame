
import pickle
import datetime, pytz, time

if __name__ == "__main__":

    with open("time.log", "rb") as f:
        data = pickle.load(f)
        #print(data)
        for i in data:
            dt = datetime.datetime.fromtimestamp(i[0], pytz.timezone("Asia/Shanghai"))
            t = i[1]
            print("time:", t*1000, "ms", ", date:", dt)