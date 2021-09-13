from flask import Flask, render_template, redirect, url_for, request, flash
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        state = request.form["state"]
        district = request.form["district"]
        season = request.form["season"]
        print(state, district, season)

        # actual processing code

        data = pd.read_csv("./crop-production.csv")
        data.fillna(method="ffill")
        df = data.loc[
            (data["State_Name"] == state)
            & (data["District_Name"] == district)
            & ((data["Season"] == season) | ((data["Season"] == "Whole Year")))
        ]
        gen_mean_prod = df.Production.mean()
        if pd.isna(gen_mean_prod):
            print("No Data Found")
        # print("general mean production is",gen_mean_prod)
        unique_crop = df.Crop.unique()
        production = np.array([])
        crop_name = np.array([])
        for i in unique_crop:
            dff = df.loc[df["Crop"] == i]
            mean_prod = dff.Production.mean()
            # print("mean_prod of ",i," is ",mean_prod)
            if mean_prod >= gen_mean_prod:
                crop_name = np.append(crop_name, i)
                production = np.append(production, mean_prod)
                print(
                    i, "=>", mean_prod
                )  # Crops in demand and quantity(metric ton) needed

        # pie char of crops in demand
        plt.pie(production, labels=crop_name)
        # plt.legend()
        plt.show()

        # graph of production in a particular year
        d = df.Crop_Year.unique()
        x = np.array([])
        for i in d:
            x = np.append(x, i)
        x.sort()
        y = np.array([])
        for i in x:
            y = np.append(y, data.loc[(data["Crop_Year"] == i)].Production.mean())
        plt.xlabel("Years")
        plt.ylabel("Production (Tons)")
        plt.title("Production per year in District(State_name)", size=13, color="blue")
        plt.plot(x, y, marker="o", c="green", mfc="r")
        plt.show()

        return render_template("index.html")

    # try:
    #     return redirect(url_for('homepage'))
    # except:
    #     flash("The username or password does not match our records","info")
    #     return redirect(url_for('login'))


if __name__ == "__main__":
    app.run()
