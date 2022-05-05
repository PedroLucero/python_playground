### By Pedro Lucero, 2022
# A "grade calculator" that shows you a school class' final grade. 
# Made this since most school websites to check grades don't work properly 
# if you don't have at least one grade in each section, showing you a lower grade than you have. 

# I'll make this into a webpage later.
###

import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)


class GradeCalculator(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        # I've the icon in my PC so you'll have to bear with the tk feather
        tk.Tk.wm_title(self, "Grade Calculator")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainPage, ResultsPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MainPage(tk.Frame):  # Get all into two frames managed by pack, that are sub-managed by grid

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Grade Calculator", font=LARGE_FONT)
        label.pack()

        ### This whole section is dedicated to the treeview frame ###
        self.average_grade = tk.StringVar()
        tree_frame = tk.Frame(self, height=1, width=1)
        tree_frame.pack(padx=10, pady=10)

        treeview = ttk.Treeview(tree_frame)
        treeview.grid(row=0, column=1, columnspan=3)

        # Column setup
        treeview["columns"] = ("grade", "weight")
        treeview.column("#0", width=105, minwidth=105)
        treeview.column("grade", width=60, minwidth=60)  # Can also anchor N-S-E-W
        treeview.column("weight", width=60, minwidth=60)

        # Heading setup
        treeview.heading("#0", text="Section")  # Can also anchor
        treeview.heading("grade", text="Grade")
        treeview.heading("weight", text="weight")

        treeview.bind("<BackSpace>", lambda x: self.del_value(treeview))

        del_btn = ttk.Button(tree_frame, text="Delete selected row", command=lambda: self.del_value(treeview))
        del_btn.grid(row=1, column=1, sticky="w")

        grade_label = ttk.Label(tree_frame, textvariable=self.average_grade)
        grade_label.grid(row=1, column=3)
        ### Ends here ###

        ### add_frame section ###
        self.adding_parent = True
        self.entry_boxes = []
        self.control_vars = []
        self.all_info = {}  # This is a dict of iid's and GradeSection objects

        add_frame = tk.Frame(self, height=1, width=1)
        add_frame.pack(padx=100, pady=10)

        names_btn = ttk.Button(add_frame, text="Section")
        names_btn.configure(command=lambda: self.layout_swap(names_btn, num_label, names_entry))
        names_btn.grid(row=0, column=0)

        num_label = tk.Label(add_frame, text="Weight")
        num_label.grid(row=0, column=1)

        names_var = tk.StringVar()
        self.control_vars.append(names_var)
        names_entry = ttk.Entry(add_frame, textvariable=names_var)  # Entry for section name and grade name
        names_entry.grid(row=1, column=0)
        self.entry_boxes.append(names_entry)

        nums_var = tk.IntVar()
        self.control_vars.append(nums_var)
        vcmd = (controller.register(self.validate_cmd), "%P")
        num_entry = ttk.Entry(add_frame, textvariable=nums_var, validate="key",
                              validatecommand=vcmd)  # Entry for grades and numbers
        num_entry.grid(row=1, column=1)
        self.entry_boxes.append(num_entry)

        add_btn = ttk.Button(add_frame, text="Add values", command=lambda: [self.add_value(treeview, add_btn), self.grade_calc()])
        add_btn.grid(row=3, column=1, sticky="e")

        num_entry.bind("<ButtonRelease-1>", lambda x: self.button_enable(add_btn))
        num_entry.bind("<Return>", lambda x: [self.add_value(treeview, add_btn), self.grade_calc()])
        num_entry.bind("<Tab>", lambda x: self.layout_swap(names_btn, num_label, names_entry))

        ### Ends here ###

    # Works
    def layout_swap(self, btn, label, entry):
        for box in self.entry_boxes:
            box.delete(0, tk.END)
        if self.adding_parent:
            entry.configure(state=tk.DISABLED)
            btn.configure(text="Grade")
            label.configure(text="Your score:")
            self.adding_parent = False
            return
        entry.configure(state=tk.NORMAL)
        btn.configure(text="Section")
        label.configure(text="Weight value (%)")
        self.adding_parent = True
        return

    # Works
    # This one is implemented weird cuz of the .register() Tkinter method
    def validate_cmd(self, final_value):  # Root is the Page's controller
        weight_left = 100 # This is the total grade's "weight" (percentage pased on 100%)
        for section in self.all_info.values():
            weight_left -= section.weight

        if len(final_value) == 0:  # I'm unsure if this is the best position for this check but... it works!
            self.control_vars[1].set(0)
        if not final_value.isnumeric():  # Here we check if there is no str or it's not a num
            return False
        if final_value[0] == "0" and len(final_value) > 1:  # Here we correct the str to not have octal numbers added
            self.control_vars[1].set(int(final_value[1:]))
        if self.adding_parent and int(final_value) > weight_left:  # Here we make sure the total wt is 100%
            self.control_vars[1].set(weight_left)
        if not self.adding_parent and int(final_value) > 100:  # Checking if the grade is not > than 100%
            self.control_vars[1].set(100)
        return True

    # Works
    def button_enable(self, btn):
        if str(btn["state"]) == "disabled":
            btn.configure(text="Add values", state=tk.NORMAL)

    # Works
    def button_disable(self, btn, msg):
        btn.configure(text=msg, state=tk.DISABLED)

    # Works
    def del_value(self, treeview):
        if not treeview.selection():
            return
        for row in treeview.selection():
            parent = treeview.parent(row)
            if parent:
                grade = int(treeview.item(row, "values")[0])
                self.all_info[parent].grade -= grade
                self.all_info[parent].amount -= 1

                self.change_selection(treeview, row)
                treeview.delete(row)
                continue

            self.all_info.pop(row) # Only need to pop item from dictionary and all in it will be deleted

            self.change_selection(treeview, row)
            treeview.delete(row)
        return

    # Works
    def add_value(self, treeview, btn):
        # Get info from the entries' control vars
        name = self.control_vars[0].get()
        num = self.control_vars[1].get()
        if name == "":
            name = "Section: "

        for box in self.entry_boxes:
            box.delete(0, tk.END)

        # This is for when no elements exist in the treeview, since there can be no treeview.selection()
        if not treeview.selection():
            if num == 0: # Makes no sense to add a section with 0 weight
                return
            if self.adding_parent:
                # HOLY SHIT .insert() RETURNS THE ROW'S IID
                iid = treeview.insert(parent='', index=tk.END, text=name, values=("", str(num) + "%"))
                self.all_info[iid] = GradeSection(num, 1)  # Adding weight as key to the dictionary
                treeview.identify_row(0)
                return
            self.button_disable(btn, "Can't add grade without section!") # Gotta change here in next version, don't like it
            return

        row = treeview.selection()[0]
        add_row = treeview.index(row) + 1

        if self.adding_parent:
            iid = treeview.insert(parent='', index=add_row, text=name, values=("", str(num) + "%"))
            self.all_info[iid] = GradeSection(num, add_row)  # Adding weight as key to the dictionary
            #print(self.all_info)
            return

        parent = treeview.parent(treeview.selection()[0])  # Used to prevent infinite nesting

        # Key difference between this and the next is the "parent"
        if parent: # This is for when treeview.selection() is a child
            treeview.insert(parent=parent, index=add_row, text="Your grade:", values=(num, ""))
            self.add_grade(parent, num)
            return

        # This is for when treeview.selection() is a parent
        treeview.item(row, open=True)
        treeview.insert(parent=row, index=add_row, text="Your Grade:", values=(num, ""))
        self.add_grade(row, num)

    # Works
    def add_grade(self, iid, grade):
        self.all_info[iid].grade += int(grade)
        self.all_info[iid].amount += 1

    # Works
    def grade_calc(self):
        total_grade = 0
        for section in self.all_info.values():
            total_grade += section.average()

        self.average_grade.set(f"Total grade is: {total_grade}%")

    @staticmethod
    def change_selection(treeview, row):
        new_row = treeview.next(row)
        if new_row == "":
            new_row = treeview.prev(row)

        treeview.selection_set(new_row)


class GradeSection:
    def __init__(self, weight, id):
        self.id = id # Not necessary rn but might come in handy; id is the section's "row"
        self.weight = weight
        self.amount = 0
        self.grade = 0

    def average(self):
        if self.amount == 0:
            return 0
        grade = (self.grade/self.amount) * self.weight / 100
        return round(grade, 2)


class ResultsPage(tk.Frame): # This is not used at all rn

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=20)

        button1 = ttk.Button(self, text="Return", command=lambda: controller.show_frame(MainPage))
        button1.pack()


app = GradeCalculator()
app.mainloop()
