from tkinter import *
import requests
from tkinter import messagebox
from IATA_finder import IATAFinder

BG_COLOR = "#B1DDC6"
TEXT_COLOR = "#FF5D5D"
FLIGHT_COLOR = "#205375"
ALT_BG_COLOR = "#413F42"

IATA_f = IATAFinder()


class UserInterface:
    def __init__(self):
        self.sheety_endpoint_post = "https://api.sheety.co/ebe6533ebeca0ea09b7256f6fe3d64b3/flightData/sheet1"
        self.sheety_header = {
            "Authorization": "######"
        }
        self.body = {}
        self.flag = 0
        self.window = Tk()
        self.window.configure(bg=BG_COLOR)
        self.window.geometry("500x500")
        self.window.title("FLow")
        self.logo = PhotoImage(file="flowgo1.png")
        self.canvasheader = Canvas()
        self.canvasheader.configure(bg=ALT_BG_COLOR, width=500, height=74, highlightthickness=0)
        self.canvasheader.create_image(100, 37, image=self.logo)
        self.canvasheader.create_text(300, 40,
                                      text="Cheapest Flights\nOn your fingertips",
                                      width=200,
                                      font=("Arial", 12, "bold"),
                                      fill="white"
                                      )
        self.canvasbody = Canvas()
        self.canvasbody.configure(bg=ALT_BG_COLOR, width=200, height=426, highlightthickness=0)
        self.canvasbody.grid(row=4, column=0, rowspan=200)
        self.canvasbody.create_text(100, 115,
                                    text="Where from?: ",
                                    fill="white",
                                    width=200,
                                    font=("Arial", 20, "bold"),
                                    )
        self.canvasbody.create_text(100, 180,
                                    text="Where to?: ",
                                    fill="white",
                                    width=200,
                                    font=("Arial", 24, "bold"),
                                    )
        self.canvasbody.create_text(100, 50,
                                    text="Phone No.: ",
                                    fill="white",
                                    width=200,
                                    font=("Arial", 24, "bold"),
                                    )
        self.canvasbody.create_text(100, 245,
                                    text="Min Price: ",
                                    fill="white",
                                    width=200,
                                    font=("Arial", 24, "bold"),
                                    )
        self.canvasheader.grid(row=1, columnspan=200, rowspan=3)
        self.to_entry = Entry(width=30)
        self.from_entry = Entry(width=30)
        self.ph_entry = Entry(width=30)
        self.price_entry = Entry(width=30)
        self.from_entry.grid(row=63, column=70)
        self.to_entry.grid(row=96, column=70)
        self.ph_entry.grid(row=35, column=70)
        self.price_entry.grid(row=127, column=70)
        self.button_img = PhotoImage(file="right.png")
        self.add_button = Button(highlightthickness=0, width=50, height=50,
                                 text="ADD DETAILS",
                                 fg=TEXT_COLOR,
                                 bg=BG_COLOR,
                                 image=self.button_img,
                                 command=self.add
                                 )
        self.add_button.grid(row=180, column=30, columnspan=100)
        self.window.mainloop()

    def add(self):
        to_input = (self.to_entry.get()).title()
        from_input = (self.from_entry.get()).title()
        ph_number = self.ph_entry.get()
        min_price = self.price_entry.get()
        if to_input != "" and from_input != "":
            to_loc = IATA_f.find(to_input)
            from_loc = IATA_f.find(from_input)
            if to_loc != "notfound" or from_loc != "notfound":
                self.body = {
                    "sheet1": {
                        "to": to_loc,
                        "from": from_loc,
                        "number": self.ph_entry.get(),
                        "min": self.price_entry.get()
                    }
                }
                self.flag = 0
            else:
                messagebox.showinfo(title="Failure",
                                    message="No Such Destinations\nCheck Spelling maybe"
                                    )
                self.flag = 1

        if ph_number != "" and min_price != "" and len(ph_number) == 10 and self.flag == 0:
            messagebox.showinfo(title="Success",
                                message="This data has been added successfully, you will get a message when the price drops"
                                )
            send = requests.post(url=self.sheety_endpoint_post, headers=self.sheety_header, json=self.body)

        elif to_input == "" or from_input == "" or ph_number == "" or min_price == "":
            messagebox.showinfo(title="Failure",
                                message="Any field left empty wont give results!\nPlease fill all the fields in their correct formats"
                                )
        elif len(ph_number) < 10:
            messagebox.showinfo(title="Failure",
                                message="Please enter a 10 digit mobile number"
                                )

        self.to_entry.delete(0, END)
        self.from_entry.delete(0, END)
        self.price_entry.delete(0, END)
