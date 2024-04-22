
import mouse
import keyboard
class MouseMovement():

    def __init__(self):
        pass
    
    top_left = [0, 0]
    bottom_right = [0, 0]
    extract_button = None
    click_count = 0
    enabled=False

    def setEventListener(self, gui) -> None:
        mouse.on_click(lambda: self.setMousePosition(mouse.get_position(), gui))

    def setMousePosition(self, position, gui) -> None:
        if position:
            if self.click_count == 0:
                self.top_left = position
                self.click_count+=1
            elif self.click_count == 1:
                self.bottom_right = position
                mouse.unhook_all()
                self.write_file_with_variables()
                gui.update_status("Inventory Size Selected")
                gui.update_inventory_size_btn(text=f"Select Inventory Size (Currently: {self.top_left}:{self.bottom_right})")
                gui.update_extract_state()
                self.click_count=0
                

    def write_file_with_variables(self):
        try:
            with open("positions.csv", 'w') as file:
                file.write(str(self.top_left) + ";" + str(self.bottom_right))
        except Exception as e:
            print("An error occurred:", e)

    def on_key_press(self, key):
        print(key)
        if self.extract_button == key: 
            self.extractInventory()

    def setExtractListener(self, gui):
        if not self.enabled:
            gui.enable_extraction_status(bool=True)
            keyboard.on_press(self.on_key_press)
            self.enabled = True
        else:
            keyboard.unhook_all()
            gui.enable_extraction_status(bool=False)
            self.enabled = False
        pass

    def initializeData(self):
        self.read_file_with_variables()

    def read_file_with_variables(self):
        try:
            with open("positions.csv", 'r') as file:
                content = file.read()
                tuples = content.split(';')
                self.top_left = eval(tuples[0].strip())
                self.bottom_right = eval(tuples[1].strip())
                
        except Exception as e:
            print("An error occurred:", e)
            return None, None
        
    def extractInventory(self):
        mouse.move(self.top_left[0], self.top_left[1], absolute=True, duration=0.1)

        row_increase = self.calculateRowSize()
        column_increase = self.calculateColumnSize()

        x = self.top_left[0]
        y = self.top_left[1]
        for i in range(8):
            for j in range(8):
                mouse.move(x + (row_increase * j), y + (column_increase * i), absolute=True, duration=0)
                mouse.click('left')

    def calculateRowSize(self) -> int:
        return (self.bottom_right[0] - self.top_left[0]) / 7
   
    def calculateColumnSize(self) -> int:  
        return (self.bottom_right[1] - self.top_left[1]) / 7
    

    def set_extract_hotkey(self, gui): 
        keyboard.on_press(lambda event: self.on_key_press2(event,gui))

    def on_key_press2(self, key, gui):
        self.extract_button = key
        gui.update_extract_key_btn(text=f"Extract Key: {key}")
        gui.update_extract_state()
        keyboard.unhook_all()

        
import tkinter as tk

class GUI():
    mousemovement = MouseMovement()
    
    def select_inventory_size(self):
        self.btn_select_inventory.config(bg="green")
        self.status_bar.config(text="Please click now into the top left and then bottom right slot of your inventory")
        self.mousemovement.setEventListener(self)

    def enable_extraction(self):
        self.status_bar.config(text="Enabling Extraction...")
        self.mousemovement.initializeData()
        self.mousemovement.setExtractListener(self)
        self.root.after(2000, lambda: self.update_status("Extraction Enabled"))

    def set_extract_hotkey(self):
        self.status_bar.config(text="Setting Extract Hotkey...")
        self.btn_set_extract_key.config(bg="green")
        self.mousemovement.set_extract_hotkey(self)

    def update_status(self, text):
        self.btn_select_inventory.config(bg="SystemButtonFace")
        self.status_bar.config(text=text)

    def update_inventory_size_btn(self, text):
        self.btn_select_inventory.config(text=text)

    def update_extract_state(self):
        if self.mousemovement.extract_button is not None:
            self.btn_enable_extraction.config(state="normal")

    def update_extract_key_btn(self, text):
        self.btn_set_extract_key.config(bg="SystemButtonFace")
        self.btn_set_extract_key.config(text=text)        

    def enable_extraction_status(self, bool):
        if bool:
            self.status_bar.config(text="Extraction Enabled")
            self.btn_enable_extraction.config(bg="green")
        else:
            self.status_bar.config(text="Extraction Disabled")
            self.btn_enable_extraction.config(bg="SystemButtonFace")

    def register_gui(self):
        self.mousemovement.read_file_with_variables()

        self.root = tk.Tk()
        self.root.title("Inventory Extractor")

        self.root.geometry("400x200")

        self.root.attributes("-topmost", True)

        screen_width = self.root.winfo_screenwidth()

        x_position = screen_width - 1000

        self.root.geometry(f"400x170+{x_position}+50") 

        self.btn_select_inventory = tk.Button(self.root, text=f"Select Inventory Size (Currently: {self.mousemovement.top_left}:{self.mousemovement.bottom_right})", command=self.select_inventory_size)
        self.btn_select_inventory.pack(pady=10)

        self.btn_enable_extraction = tk.Button(self.root, state="disabled", text="Enable Extraction", command=self.enable_extraction)
        self.btn_enable_extraction.pack(pady=10)

        self.btn_set_extract_key = tk.Button(self.root, text="Set Extract Key", command=self.set_extract_hotkey)
        self.btn_set_extract_key.pack(pady=10)

        self.status_bar = tk.Label(self.root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.root.mainloop()



if __name__ == "__main__":
    gui = GUI()
    gui.register_gui()



    