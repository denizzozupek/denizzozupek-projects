import customtkinter, os, uuid, time, tkinter as tk
from PIL import Image

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.mode_var = tk.IntVar(value=0)
        self.title("To-Do App")
        self.resizable(True, True)
        self.geometry("810x610")
        self.iconbitmap('icons/icon.ico')
        self.configure(fg_color=("#e6f0fa", "#2b2b2b"))
        self.load_settings()

        self.checkbox_dict = {}
        self.custom_button_frames = {}
        self.current_frame_name = "today"
        self.active_button_color = ("#d0e2ff", "#2b2b2b")
        self.inactive_button_color = ("#f5f7fa", "#353535")
        self.custom_buttons = []

        self.frames = {} #for store all frames for each sidebar task category

        self.entry_and_button()
        self.sidebar()

        self.frame_title = customtkinter.CTkLabel(self, fg_color="transparent", text="", font=("Poppins", 24, "bold"),
                                                  text_color=("#1a4486", "white"))
        self.frame_title.grid(row=1, column=1, sticky="nw", padx=(25,0))

        for name in ["today", "tomorrow", "next_week", "completed", "all.tasks"]:
            self.create_scrollable_frame(name) #creating a scrollable frames for every category in sidebar

        # Grid configure rows: Title and mode switch,  Task list, Entry Box and Buttons,Bottom padding
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=5)
        self.grid_rowconfigure(3, weight=1)

        # Grid configure columns: Sidebar, Main content , Right Padding
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=2)
        self.grid_columnconfigure(3, weight=1)

        self.load_custom_lists()
        self.load_file()
        self.entry.focus()
        self.create_switch_mode()
        self.show_frame(self.current_frame_name) #show default frame for application


    def create_scrollable_frame(self, name): #create and configure a scrollable frame
        frame = customtkinter.CTkScrollableFrame(self, width=520, height=420, corner_radius=10,
        fg_color=("#e6f0fa", "#2b2b2b"), scrollbar_fg_color=("transparent"),
        scrollbar_button_color=("#cfd8dc", "#4a4a4a"), scrollbar_button_hover_color=("#b0bec5", "#666666"))

        #place the frame in the grid but hide it initially - only 'today' will be shown at start
        frame.grid(row=2, column=1, sticky="nsew", pady=(20, 20), padx=(10, 0), columnspan=3)
        frame.grid_remove()
        self.frames[name] = frame #Storing each name in list as a key and assign a corresponding scrollable frame to it

        #Hide all frames and then show only the selected one by the user via sidebar buttons
    def show_frame(self, frame_name, clicked_button = None):
        self.current_frame_name = frame_name
        for frame in self.frames.values():
            frame.grid_remove()
        if frame_name in self.frames:
            self.frames[frame_name].grid()

        if frame_name == "completed" or frame_name == "all.tasks":
            self.entry_button_frame.grid_remove()
        else:
            self.entry_button_frame.grid()

        for button in self.buttons + self.custom_buttons:
            button.configure(fg_color=self.inactive_button_color)

        if clicked_button:
            clicked_button.configure(fg_color=self.active_button_color)

        titles = {
            "today": "Today's Tasks",
            "tomorrow": "Tomorrow's Tasks",
            "next_week": "Next Week's Tasks",
            "completed": "Completed Tasks",
            "all.tasks": "All Tasks"
        }

        self.frame_title.configure(text=titles.get(frame_name, frame_name.capitalize()))
    def load_settings(self):
        try:
            if not os.path.exists("settings.txt"):
                open("settings.txt", "w", encoding="utf-8").close()
            with open("settings.txt", "r", encoding="utf-8") as file:
                for setting in file:
                    setting = setting.strip()
                    if not setting:
                        continue
                    try:
                        user_mode = setting.split("=", 1)
                        if user_mode[0] == "mode":
                            if user_mode[1] == "dark":
                                customtkinter.set_appearance_mode("dark")
                                self.mode_var.set(1)
                            else:
                                customtkinter.set_appearance_mode("light")
                                self.mode_var.set(0)
                    except ValueError:
                        print(f"Invalid line format: {setting}")
        except Exception as e:
            print(f"Error loading file: {e}")

    def save_settings(self):
        try:
            with open("settings.txt", "w", encoding="utf-8") as file:
                if self.mode_var.get() == 0:
                    file.write("mode=light\n")
                else:
                    file.write("mode=dark\n")

        except Exception as e:
            print(f"Error loading file: {e}")

    def load_file(self):
        try:
            if not os.path.exists("tasks.txt"):#At the start, check if 'tasks.txt' exists. If not, create an empty one
                open("tasks.txt", "w", encoding="utf-8").close()
            tasks = []
            with open("tasks.txt", "r", encoding="utf-8") as file:#Then open the file in read and go through each line
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        frame_name, task_text, task_id, created_at = line.split("|", 3)
                        task_text = task_text.replace("||","|")
                        if task_text.strip():
                            tasks.append((frame_name, task_text, task_id, float(created_at)))

                    except ValueError:
                        print(f"Invalid line format: {line}")
            tasks.sort(key=lambda x: x[3])

            for frame_name, task_text, task_id, created_at in tasks:
                self.create_task_checkbox(task_text=task_text, frame_name=frame_name, task_id=task_id,
                                          created_at=float(created_at))
        except Exception as e:
            print(f"Error loading file: {e}")

    #open the file in write mode, loop in all stored checkboxes, get the text of each and write the task text to txt
    def save_all_tasks(self):
        try:
            with open("tasks.txt", "w", encoding="utf-8") as file:
                items = sorted(self.checkbox_dict.items(), key=lambda item: item[1]["created_at"])
                for task_id, value in items:
                    frame_name = value["frame_name"]
                    task_text = value["checkbox"].cget("text").replace("|","||")
                    created_at = value["created_at"]
                    file.write(f"{frame_name}|{task_text.strip()}|{task_id}|{created_at}\n")
        except Exception as e:
            print(f"Error loading file: {e}")

    def save_user_tasks(self):
        try:
            with open("users_frames.txt", "w", encoding="utf-8") as file:
                for user_task_id, value in self.custom_button_frames.items():
                    name = value["name"].replace("|", "||")
                    created_at = value["user_created_at"]
                    file.write(f"{name}|{user_task_id}|{created_at}\n")
        except Exception as e:
            print(f"Error saving user lists: {e}")

    #Create entry and button in a frame, enter key or button click add a new task
    def entry_and_button(self):
        self.entry_button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.entry_button_frame.grid(row=3, column=1, sticky="n", padx=(20, 10), columnspan=3, pady=(0, 20))
        self.entry = customtkinter.CTkEntry(self.entry_button_frame, placeholder_text="Enter Task", corner_radius=30,
                                            width=350, height=45,
                                            fg_color=("#f0f0f0", "#3a3a3a"))
        self.entry.pack(side="left", padx=(20, 10))
        self.entry.bind("<Return>", self.create_task_checkbox_event)#enter key in entry box creating a checkbox

        self.button = customtkinter.CTkButton(self.entry_button_frame, text="Add", corner_radius=20, width=100,
        height=45, command=self.create_task_checkbox, fg_color="#ff1c00", hover_color="#ef1515")
        self.button.pack(side="left")

    def add_custom_button(self):
        list_name = self.new_task_entry.get().strip()
        if not list_name:
            return

        users_task_id = str(uuid.uuid4())
        user_created_at = time.time()

        self.create_user_list(list_name, users_task_id, user_created_at)
        self.save_user_tasks()
        self.new_task_entry.delete(0, "end")

    def create_user_list(self, list_name, users_task_id, user_created_at):
        userstask_image = customtkinter.CTkImage(Image.open("icons/todo.png"), size=(26, 26))
        new_frame = self.create_scrollable_frame(list_name)

        list_item_frame = customtkinter.CTkFrame(self.dynamic_lists_frame, fg_color="transparent")
        list_item_frame.pack(fill="x", pady=2)

        new_button = customtkinter.CTkButton(list_item_frame, text=list_name, anchor="w",
        text_color=("black", "white"),hover_color = ("#e6e6e6", "#666666"),fg_color=("#f5f7fa", "#353535"),
        font=("Helvetica", 15, "bold"), image=userstask_image, height=40)
        new_button.pack(side="left", padx=(0, 5), fill="x", expand=True)
        new_button.configure(command= lambda n=list_name , b=new_button : self.show_frame(n, clicked_button=b))

        trash_icon = customtkinter.CTkImage(Image.open("icons/trash.png"), size=(20, 20))
        delete_button = customtkinter.CTkButton(list_item_frame, text="", image=trash_icon, width=40, height=40,
                                                fg_color="transparent", hover_color="#ffcccc",
                                                command=lambda uid=users_task_id: self.delete_user_list(uid))
        delete_button.pack(side="left", padx=(5, 10))

        self.custom_button_frames[users_task_id]={"users_task_id": users_task_id,"name": list_name,"button": new_button,
        "frame": self.frames[list_name],"user_created_at": user_created_at,"container": list_item_frame}
        self.custom_buttons.append(new_button)

    def delete_user_list(self, users_task_id):
        if users_task_id not in self.custom_button_frames:
            return
        confirm = customtkinter.CTkToplevel(self)
        confirm.title("Confirm Delete")
        confirm.overrideredirect(False)
        confirm.geometry("300x150")
        confirm.grab_set()

        label = customtkinter.CTkLabel(confirm, text="Are you sure you want to delete this list?")
        label.pack(pady=(20,10))

        def confirm_delete():
            value = self.custom_button_frames[users_task_id]
            frame_name = value["name"]

            task_ids_to_remove = [task_id for task_id, value in self.checkbox_dict.items()
                                  if value["frame_name"] == frame_name]

            for task_id in task_ids_to_remove:
                self.checkbox_dict[task_id].destroy()
                if self.checkbox_dict[task_id]["all.tasks_frame"]:
                    self.checkbox_dict[task_id]["all.tasks_frame"].destroy()
                del self.checkbox_dict[task_id]

            value["button"].destroy()
            value["container"].destroy()
            value["frame"].destroy()
            value["button"].destroy()
            if value["button"] in self.custom_buttons:
                self.custom_buttons.remove(value["button"])

            del self.custom_button_frames[users_task_id]
            self.save_user_tasks()
            self.save_all_tasks()

            confirm.destroy()

        confirm_button = customtkinter.CTkButton(confirm, text="Yes", command=confirm_delete, fg_color="red")
        confirm_button.pack(pady=(0, 5))

        cancel_button = customtkinter.CTkButton(confirm, text="Cancel", command=confirm.destroy)
        cancel_button.pack()

    def load_custom_lists(self):
        try:
            if not os.path.exists("users_frames.txt"):
                open("users_frames.txt", "w", encoding="utf-8").close()

            with open("users_frames.txt", "r", encoding="utf-8") as file:  # Then open the file in read and go through each line
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        list_name, users_task_id, created_at = line.split("|")
                        list_name = list_name.replace("||", "|")
                        users_task_id = users_task_id.strip()
                        created_at = float(created_at)

                        self.create_user_list(list_name, users_task_id, created_at)
                    except ValueError:
                        print(f"Invalid line format: {line}")
        except Exception as e:
            print(f"Error loading file: {e}")

    def sidebar(self):
        self.sidebar_frame = customtkinter.CTkFrame(self, width=240, height=610, fg_color=("#f5f7fa", "#353535"))
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", rowspan=4)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)

        # Title
        self.title_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="To-Do List",font=("Poppins", 28, "bold"),text_color=("#1a4486", "white"))
        self.title_label.grid(row=0, column=0, sticky="nsew", pady=(30,30))

        # Default buttons (row 1–5)
        self.sidebar_buttons()

        # scrollable frames for user lists
        self.dynamic_lists_frame = customtkinter.CTkScrollableFrame(self.sidebar_frame, fg_color="transparent")
        self.dynamic_lists_frame.grid(row=6, column=0, sticky="nsew", padx=0)
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        # add list frame
        self.bottom_add_frame = customtkinter.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.bottom_add_frame.grid(row=7, column=0, sticky="ew", padx=10, pady=(10, 10))

        self.new_task_entry = customtkinter.CTkEntry(self.bottom_add_frame, placeholder_text="Add new list",
                                                     corner_radius=10, height=30)
        self.new_task_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.new_task_entry.bind("<Return>", lambda event: self.add_custom_button())

        self.add_list_button = customtkinter.CTkButton(self.bottom_add_frame, text="Add", width=60, corner_radius=10,
                                                       command=self.add_custom_button, height=30)
        self.add_list_button.pack(side="left")
        self.sidebar_frame.grid_rowconfigure(7, weight=0, minsize=50)

        self.sidebar_buttons()
    def sidebar_buttons(self):
        #button icons
        today_image = customtkinter.CTkImage(Image.open("icons/today.ico"), size=(26,26))
        tomorrow_image = customtkinter.CTkImage(Image.open("icons/tomorrow.ico"), size=(26,26))
        next_week_image = customtkinter.CTkImage(Image.open("icons/next_week.png"), size=(26,26))
        completed_image = customtkinter.CTkImage(Image.open("icons/completed.png"), size=(26,26))
        alltasks_image = customtkinter.CTkImage(Image.open("icons/all.tasks.png"), size=(26,26))

        button_config = {"height":40, "fg_color": ("#f5f7fa", "#353535"),
                         "text_color": ("#1f1f1f", "white"), "hover_color": ("#e6e6e6", "#666666")}

        self.today_button = customtkinter.CTkButton(self.sidebar_frame, text="Today", **button_config,
        image=today_image, font=("Helvetica", 15), anchor="w",
            command=lambda: self.show_frame("today", clicked_button=self.today_button))

        self.tomorrow_button = customtkinter.CTkButton(self.sidebar_frame, text="Tomorrow", **button_config,
        image=tomorrow_image, font=("Helvetica", 15), anchor="w",
            command=lambda: self.show_frame("tomorrow", clicked_button=self.tomorrow_button))

        self.next_week_button = customtkinter.CTkButton(self.sidebar_frame, text="Next Week", **button_config,
        image=next_week_image, font=("Helvetica", 15), anchor="w",
            command=lambda: self.show_frame("next_week", clicked_button=self.next_week_button))

        self.completed_button = customtkinter.CTkButton(self.sidebar_frame, text="Completed", **button_config,
        image=completed_image, font=("Helvetica", 15), anchor="w",
            command=lambda: self.show_frame("completed", clicked_button=self.completed_button))

        self.alltasks_button = customtkinter.CTkButton(self.sidebar_frame, text="All Tasks", **button_config,
        image=alltasks_image, font=("Helvetica", 15), anchor="w",
            command=lambda: self.show_frame("all.tasks", clicked_button=self.alltasks_button))

        self.buttons = [self.today_button, self.tomorrow_button,
                   self.next_week_button, self.completed_button, self.alltasks_button]

        self.today_button.grid(row=1, column=0, padx=5, sticky="nsew", pady=1)
        self.tomorrow_button.grid(row=2, column=0, padx=5, sticky="nsew", pady=1)
        self.next_week_button.grid(row=3, column=0, padx=5, sticky="nsew", pady=1)
        self.completed_button.grid(row=4, column=0, padx=5, sticky="nsew", pady=1)
        self.alltasks_button.grid(row=5, column=0, padx=5, sticky="nsew", pady=1)

    def create_switch_mode(self):
        switch_frame = customtkinter.CTkFrame(self, fg_color=("#e6f0fa", "#2b2b2b"))
        switch_frame.grid(row=0, column=3, sticky="e", pady=(20,10), padx=(0,5))
        self.switch = customtkinter.CTkSwitch(switch_frame, variable=self.mode_var,
                                        text="", onvalue=1, offvalue=0, command=self.switch_mode
                                        ,text_color=("#1a4486", "white"), width=20)
        self.switch.pack(side = "left")
        dark_mode_image = customtkinter.CTkImage(Image.open("icons/dark-mode.png"), size=(20, 20))
        self.image_label = customtkinter.CTkLabel(switch_frame, image=dark_mode_image, text="")
        self.image_label.pack(side = "left")

    def switch_mode(self):
        value = self.mode_var.get()
        if value:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")
        self.save_settings()

    def create_task_checkbox(self, task_text=None, frame_name=None, task_id=None, created_at=None):
        if not task_text and self.entry.get().strip() == "":
            return

        if not task_id:
            task_id = str(uuid.uuid4())

        if not created_at:
            created_at = time.time()

        if not frame_name:
            frame_name = self.current_frame_name

        text = task_text if task_text else self.entry.get().strip()
        if not task_text:
            self.entry.delete(0, "end")

        check_var = customtkinter.StringVar()
        if frame_name == "completed":
            check_var.set("on")
        else:
            check_var.set("off")

        frame = self.frames[frame_name]
        checkbox_frame = customtkinter.CTkFrame(frame, fg_color=("white", "#3a3a3a"),
                                                corner_radius=7, width=500, height=50)
        checkbox_frame.pack(fill="x", pady=2)

        def checkbox_command():
            if check_var.get() == "on":
                # if its already in completed, don't add
                if self.checkbox_dict[task_id]["frame_name"] == "completed":
                    return
                # delete old checkbox
                self.checkbox_dict[task_id]["frame"].destroy()
                if self.checkbox_dict[task_id]["alltasks_frame"] is not None:
                    self.checkbox_dict[task_id]["alltasks_frame"].destroy()
                del self.checkbox_dict[task_id]

                # create new "completed" checkbox in completed
                self.create_task_checkbox(
                    task_text=text,
                    frame_name="completed",
                    task_id=task_id,
                    created_at=created_at
                )

            else:
                if self.checkbox_dict[task_id]["frame_name"] == "completed":
                    self.checkbox_dict[task_id]["frame"].destroy()
                    if self.checkbox_dict[task_id]["alltasks_frame"] is not None:
                        self.checkbox_dict[task_id]["alltasks_frame"].destroy()
                    del self.checkbox_dict[task_id]
                    self.save_all_tasks()

        checkbox = customtkinter.CTkCheckBox(checkbox_frame, text=text, font=("Helvetica", 20),
                                             border_width=2, variable=check_var,
                                             onvalue="on", offvalue="off", corner_radius=50,
                                             command=checkbox_command)
        checkbox.pack(fill="both", expand=True, padx=10, pady=10)

        if frame_name != "completed":
            alltasks_frame = self.frames["all.tasks"]
            alltasks_checkbox_frame = customtkinter.CTkFrame(alltasks_frame, fg_color=("white", "#3a3a3a"), corner_radius=7)
            alltasks_checkbox_frame.pack(fill="x", pady=2)

            alltasks_checkbox = customtkinter.CTkCheckBox(alltasks_checkbox_frame, text=text, font=("Helvetica", 20),
                                                          border_width=2, variable=check_var,
                                                          onvalue="on", offvalue="off", corner_radius=50,
                                                          command=checkbox_command)
            alltasks_checkbox.pack(fill="both", expand=True, padx=10, pady=10)

        else:
            alltasks_checkbox = None
            alltasks_checkbox_frame = None

        self.checkbox_dict[task_id] = {
            "checkbox": checkbox,
            "alltasks_checkbox": alltasks_checkbox,
            "var": check_var,
            "frame": checkbox_frame,
            "alltasks_frame": alltasks_checkbox_frame,
            "frame_name": frame_name,
            "created_at": created_at
}

        self.save_all_tasks()

    def create_task_checkbox_event(self, event):
        self.create_task_checkbox()

if __name__ == "__main__":
    app = App()
    app.mainloop()