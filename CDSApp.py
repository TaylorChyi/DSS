import tkinter as tk
from tkinter import ttk

from utils.algorithm import *
from utils.csv_util import *

from common.constants import *
from common.config import *
from log.logger import *
import platform

from tkinter import messagebox


class CDSApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the icon
        self.set_icon()

        self.title(APP_TITLE)
        self.geometry(GEOMETRY)
        self.resizable(False, False)

        self.main_frame = tk.Frame(self)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.create_widgets()

        # Center the window on the screen
        self.update_idletasks()
        window_width, window_height = self.winfo_width(), self.winfo_height()
        screen_width, screen_height = (
            self.winfo_screenwidth(),
            self.winfo_screenheight(),
        )
        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)
        self.geometry("+{}+{}".format(position_right, position_down))

        # Make the window always on top
        self.attributes("-topmost", True)

    def set_icon(self):
        if platform.system() == "Windows":
            self.iconbitmap("icon.ico")
        elif platform.system() == "Darwin":
            # macOS doesn't support .ico files, so use .icns instead
            img = tk.PhotoImage(file=ICON_PNG)
            self.tk.call("wm", "iconphoto", self._w, img)
        else:
            # For other platforms, you can use .png, .gif, or .ppm formats
            img = tk.PhotoImage(file=ICON_PNG)
            self.iconphoto(True, img)

    def create_widgets(self):
        self.age_label = tk.Label(self.main_frame, text=AGE_LABEL)
        self.age_label.grid(row=0, column=0, padx=20, pady=10)
        self.age_entry = ttk.Spinbox(
            self.main_frame, from_=0, to=120, increment=1, width=10
        )
        self.age_entry.grid(row=0, column=1)
        self.age_entry.delete(0, "end")
        self.age_entry.insert(0, "0")

        self.pregnant_label = tk.Label(self.main_frame, text=PREGNANT_LABEL)
        self.pregnant_label.grid(row=1, column=0, pady=10)
        self.pregnant_var = tk.StringVar()
        self.pregnant_var.set("N")
        self.pregnant_radiobuttons = [
            tk.Radiobutton(
                self.main_frame, text="Yes", variable=self.pregnant_var, value="Y"
            ),
            tk.Radiobutton(
                self.main_frame, text="No", variable=self.pregnant_var, value="N"
            ),
        ]
        for idx, rb in enumerate(self.pregnant_radiobuttons):
            rb.grid(row=1, column=idx + 1)

        self.allergy_label = tk.Label(self.main_frame, text=ALLERGY_LABEL)
        self.allergy_label.grid(row=2, column=0, pady=10)
        self.allergy_var = tk.StringVar()
        self.allergy_var.set("N")
        self.allergy_radiobuttons = [
            tk.Radiobutton(
                self.main_frame, text="Yes", variable=self.allergy_var, value="Y"
            ),
            tk.Radiobutton(
                self.main_frame, text="No", variable=self.allergy_var, value="N"
            ),
        ]
        for idx, rb in enumerate(self.allergy_radiobuttons):
            rb.grid(row=2, column=idx + 1)

        self.weight_label = tk.Label(self.main_frame, text=WEIGHT_LABEL)
        self.weight_label.grid(row=3, column=0, pady=10)
        self.weight_entry = ttk.Spinbox(
            self.main_frame, from_=0, to=300, increment=0.5, width=10
        )
        self.weight_entry.grid(row=3, column=1)
        self.weight_entry.delete(0, "end")
        self.weight_entry.insert(0, "0")

        self.submit_button = tk.Button(
            self.main_frame, text=SUBMIT_BUTTON, command=self.submit
        )
        self.submit_button.grid(row=4, column=0, columnspan=2)

        self.display_button = tk.Button(
            self.main_frame, text="Record", command=self.display_prescriptions
        )
        self.display_button.grid(row=4, column=2)

        self.result_label = tk.Label(self.main_frame, text="== Prescriptions ==")
        self.result_label.grid(row=5, column=0, columnspan=3)

        self.result_var = tk.Text(
            self.main_frame, wrap=tk.WORD, height=4, width=40, state="disabled"
        )
        self.result_var.grid(row=6, column=0, columnspan=3)

        self.main_frame.grid_rowconfigure(6, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    @log_function
    def submit(self):
        try:
            age = int(self.age_entry.get())
            pregnant = self.pregnant_var.get()
            allergy = self.allergy_var.get()
            weight = float(self.weight_entry.get())
        except ValueError:
            self.result_label.config(
                text="Please fill all the fields with valid values."
            )
            return

        if age < 0 or age > 120:
            self.result_label.config(text="Please enter a valid age (0-120).")
            return

        if weight < 0 or weight > 300:
            self.result_label.config(text="Please enter a valid weight (0-300 kg).")
            return

        prescription = self.generate_prescription(age, pregnant, allergy, weight)
        save_to_csv(age, pregnant, allergy, weight, prescription)

        self.result_label.config(text="== Prescriptions ==")
        self.result_var.config(state="normal")
        self.result_var.delete(1.0, tk.END)
        self.result_var.insert(tk.END, prescription.replace("| ", "\n"))
        self.result_var.config(state="disabled")

    @log_function
    def generate_prescription(self, age, pregnant, allergy, weight):
        if pregnant in {"yes", "y"}:
            pregnant = "Y"
        elif pregnant in {"no", "n"}:
            pregnant = "N"

        if allergy in {"yes", "y"}:
            allergy = "Y"
        elif allergy in {"no", "n"}:
            allergy = "N"

        prescription = clincian_decision_system(age, pregnant, allergy, weight)
        if prescription == "" :
            choice = self.choose_antibiotic()
            prescription = clincian_decision_system(choice, age, weight)

        return prescription

    @log_function
    def choose_antibiotic(self):
        choice_window = tk.Toplevel(self)
        choice_window.title("Choose an antibiotic")

        # Create radio buttons and a submit button for antibiotic choices
        self.choice_var = tk.IntVar()
        antibiotics = ["Amoxicillin", "Erythromycin", "Clarithromycin", "Doxycycline"]

        for idx, antibiotic in enumerate(antibiotics):
            radio_button = tk.Radiobutton(
                choice_window, text=antibiotic, variable=self.choice_var, value=idx + 1
            )
            radio_button.pack()

        submit_button = tk.Button(
            choice_window, text="Submit", command=choice_window.destroy
        )
        submit_button.pack()

        # Wait for the user to make a choice and close the window
        self.wait_window(choice_window)

        return self.choice_var.get()

    @log_function
    def display_prescriptions(self):
        DisplayPrescriptions()


class DisplayPrescriptions:
    def __init__(self):
        self.display_prescriptions()

    def display_prescriptions(self):
        try:
            with open(PRESCRIPTIONS_RECORD_CSV, "r", newline="") as csvfile:
                reader = csv.DictReader(csvfile)

                table_window = tk.Toplevel()
                table_window.title(RECORD_TITLE)
                table_window.resizable(width=False, height=False)

                frame = tk.Frame(
                    table_window, width=400, height=500
                )  # Frame to limit the width and height of the treeview
                frame.pack(fill=tk.BOTH)

                tree = ttk.Treeview(frame, show="headings", height=20)
                tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                tree.configure(yscrollcommand=scrollbar.set)

                # 设置列名
                tree["columns"] = list(reader.fieldnames)
                for column in tree["columns"]:
                    tree.heading(column, text=column)

                # 设置列宽度
                tree.column("#1", width=80, anchor="center", minwidth=80, stretch=False)
                tree.column("#2", width=80, anchor="center", minwidth=80, stretch=False)
                tree.column("#3", width=80, anchor="center", minwidth=80, stretch=False)
                tree.column("#4", width=80, anchor="center", minwidth=80, stretch=False)
                tree.column(
                    "#5", width=700, anchor="center", minwidth=700, stretch=False
                )
                # 添加数据
                for row in reader:
                    tree.insert("", "end", values=list(row.values()))

                frame.grid_propagate(
                    False
                )  # Prevent the frame from resizing with the treeview
                frame.update_idletasks()

        except FileNotFoundError:
            messagebox.showerror("Error", "No prescriptions found.")


if __name__ == "__main__":
    setup_logging(True)
    app = CDSApp()
    app.mainloop()
