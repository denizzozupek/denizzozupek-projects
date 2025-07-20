import customtkinter, os
from PIL.ImageOps import expand

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("To-Do App")
        self.resizable(False, False)
        self.geometry("600x700")
        self.iconbitmap('icon.ico')
        self.configure(fg_color=("#e6f0fa", "#2b2b2b"))


        self.title_label = customtkinter.CTkLabel(self, text="To-Do List", font=("Poppins",28, "bold")
                                                  , text_color=("#1a4486", "white"))
        self.title_label.place(x=50, y=20)

        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter Task", corner_radius=30, width=350, height=45,
                                            fg_color=("#f0f0f0", "#3a3a3a"))
        self.entry.place(x=100, y=75)
        self.entry.bind("<Return>", self.create_task_checkbox_event) #enter key in entry box creating a checkbox


        self.button = customtkinter.CTkButton(self, text="Add", corner_radius=50, width=100, height=45,
                                              command=self.create_task_checkbox, fg_color="#ff1c00", hover_color="#ef1515")
        self.button.place(x=462, y=75)
        self.checkbox_dict = {}
        self.task_frame = customtkinter.CTkScrollableFrame(self, width=520, height=420, corner_radius=10,
                        fg_color=("#e6f0fa", "#2b2b2b"), scrollbar_fg_color=("#e6f0fa", "#1e1e1e"),
        scrollbar_button_color=("#cfd8dc", "#4a4a4a"), scrollbar_button_hover_color=("#b0bec5", "#666666"))
        self.task_frame.place(x=30, y=140)
        self.checkbox_num = 0  #for ordering checkboxes

        #Switching light - dark mode
        def switch_mode():
            value = switch.get()
            if value:
                customtkinter.set_appearance_mode("dark")
            else:
                customtkinter.set_appearance_mode("light")

        switch = customtkinter.CTkSwitch(self, text="Light/Dark", onvalue=1, offvalue=0, command=switch_mode
                                         ,text_color=("#1a4486", "white"), font=("Poppins", 14))
        switch.place(x=470, y=20)

        self.load_file()
        self.focus()

    def load_file(self):
        try:
            if not os.path.exists("tasks.txt"):
                open("tasks.txt", "w").close()

            with open("tasks.txt", "r") as file:
                for line in file:
                    task = line.strip()
                    if task:
                        self.create_task_checkbox(task_text=task)
        except Exception as e:
            print(f"Error loading file: {e}")


    def save_all_tasks(self):
        try:
            with open("tasks.txt", "w") as file:
                for value in self.checkbox_dict.values():
                    file.write(value["checkbox"].cget("text") + "\n")
        except Exception as e:
            print(f"Error loading file: {e}")

    def create_task_checkbox(self, task_text = None):
        check_var = customtkinter.StringVar(value="off")
        checkbox_num = self.checkbox_num

        def delete_completed_task():
            if check_var.get() == "on":
                self.checkbox_dict[checkbox_num]["frame"].destroy()
                del self.checkbox_dict[checkbox_num]
                self.save_all_tasks()

        text = task_text if task_text else self.entry.get()

        if text.strip() == "":
            return

        checkbox_frame = customtkinter.CTkFrame(self.task_frame, fg_color=("white","#3a3a3a"), corner_radius=7, width=500, height=50)
        checkbox_frame.pack(fill="x", pady=7)

        checkbox = customtkinter.CTkCheckBox(checkbox_frame, text=text, font=("Poppins", 20),
        variable=check_var, onvalue="on", offvalue="off", corner_radius=50,
        command=delete_completed_task, border_width=2)
        checkbox.pack(fill = "both", expand=True, padx=10, pady=10)

        self.checkbox_dict[checkbox_num] = {"checkbox": checkbox, "var": check_var, "frame": checkbox_frame}
        self.checkbox_num += 1

        if not task_text:
            self.save_all_tasks()
            self.entry.delete(0, "end")

    def create_task_checkbox_event(self, event):
        self.create_task_checkbox()

app = App()
app.mainloop()
