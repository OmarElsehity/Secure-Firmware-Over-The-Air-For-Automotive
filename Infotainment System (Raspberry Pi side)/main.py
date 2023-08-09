"""
******* Author: Omar Elsehity & Emad Heikal *******
        ***** Sponsered by Swift ACT *****
"""
from cryptography.fernet import Fernet
import base64, os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import time
import customtkinter
import webbrowser
import os
from PIL import Image
import sys
sys.path.append("/home/emad/Desktop/gui/3rd_trial/3nd_Trial/MCP2515_Lib")
import MCP2515_Lib

def CAN_ID_103():

    file = open("/home/emad/Downloads/103_Wave.txt", "r")

    flag=0
    padding=0
    arr=[0x68,0x65,0x6c,0x6c,0x6f,0x31,0x32,0x33]
    MCP2515_Lib.MCP2515_Reset()  
    MCP2515_Lib.MCP2515_ConfigurationMode()
    MCP2515_Lib.MCP2515_CANInit()  
    MCP2515_Lib.MCP2515_SetID(0x103)  
    MCP2515_Lib.MCP2515_SetDataLength(8 )  
    MCP2515_Lib.MCP2515_SetPriorityHigh(0)  
    ##MCP2515_Lib.MCP2515_NormalMode()   
    MCP2515_Lib.MCP2515_OneShotMode()  
    ## 
    MCP2515_Lib.MCP2515_Configure_Rx_Buffers()
    time.sleep(1)
    while flag != 1 :
        if(MCP2515_Lib.MCP2515_Message_RxBuffer0_Flag()):
          
            ID=MCP2515_Lib.MCP2515_Get_RXB0_ID ()  
            print("ID : ",hex(ID))  
            data_length=MCP2515_Lib.MCP2515_Get_RXB0_Data_Length()  
            print("data length :",data_length)      
            ID=MCP2515_Lib.MCP2515_Get_RXB0_ID ()  
            data_length=MCP2515_Lib.MCP2515_Get_RXB0_Data_Length()  
            if(ID==259): 
                RX=MCP2515_Lib.MCP2515_Read_RXBuffer0_byte()  
                print(RX)

        # Read the file character by character
        count=0
        char = file.read(48)
        if not char:
            flag=1
        while (count <48):
            for i in range(8):
                
                if ((i+count)== len(char)):
                    print('HERE!!!!')
                    offset = len(char)% 8
                    for it in range (offset,7):
                        MCP2515_Lib.MCP2515_LoadData(it,ord('0'))
                    MCP2515_Lib.MCP2515_LoadData(7,ord('\n'))
                        
                    flag=1
                    file.close()
                    break
                else:    
                    MCP2515_Lib.MCP2515_LoadData(i,ord(char[i+count]))
            count+=8
            MCP2515_Lib.MCP2515_StartTransmission_instruction(0)
            if(flag==1):
                break
        time.sleep(0)
    
    
def CAN_ID_205():
    
    file = open("/home/emad/Downloads/205_High.txt", "r")

    Cflag=0
    padding=0
    arr=[0x68,0x65,0x6c,0x6c,0x6f,0x31,0x32,0x33]
    MCP2515_Lib.MCP2515_Reset()  
    MCP2515_Lib.MCP2515_ConfigurationMode()
    MCP2515_Lib.MCP2515_CANInit()  
    MCP2515_Lib.MCP2515_SetID(0x205)  
    MCP2515_Lib.MCP2515_SetDataLength(8 )  
    MCP2515_Lib.MCP2515_SetPriorityHigh(0)  
    ##MCP2515_Lib.MCP2515_NormalMode()   
    MCP2515_Lib.MCP2515_OneShotMode()  
    ## 
    MCP2515_Lib.MCP2515_Configure_Rx_Buffers()
    time.sleep(1)
    while Cflag != 1 :
        if(MCP2515_Lib.MCP2515_Message_RxBuffer0_Flag()):
          
            ID=MCP2515_Lib.MCP2515_Get_RXB0_ID ()  
            print("ID : ",hex(ID))  
            data_length=MCP2515_Lib.MCP2515_Get_RXB0_Data_Length()  
            print("data length :",data_length)      
            ID=MCP2515_Lib.MCP2515_Get_RXB0_ID ()  
            data_length=MCP2515_Lib.MCP2515_Get_RXB0_Data_Length()  
            if(ID==259): 
                RX=MCP2515_Lib.MCP2515_Read_RXBuffer0_byte()  
                print(RX)

        # Read the file character by character
        count=0
        char = file.read(48)
        if not char:
            Cflag=1
        while (count <48):
            for i in range(8):
                
                if ((i+count)== len(char)):
                    print('HERE!!!!')
                    offset = len(char)% 8
                    for it in range (offset,7):
                        MCP2515_Lib.MCP2515_LoadData(it,ord('0'))
                    MCP2515_Lib.MCP2515_LoadData(7,ord('\n'))
                        
                    Cflag=1
                    file.close()
                    break
                else:    
                    MCP2515_Lib.MCP2515_LoadData(i,ord(char[i+count]))
            count+=8
            MCP2515_Lib.MCP2515_StartTransmission_instruction(0)
            if(Cflag==1):
                break
        time.sleep(0)
        

def get_key(password): #get a key from a password by passing it through a key derivation function and converting it to base64
    password = password.encode()
    with open('salt.txt','rb') as saltFile:
        salt = saltFile.read()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key



def decrypt_file(key, filenameFrom, filenameTo): #decrypt a file and save the plaintext in a new file
    with open(filenameFrom,'rb') as file:
        encrypted=file.read() #read encrypted data
    fernet = Fernet(key)
    decrypted=fernet.decrypt(encrypted)
    with open(filenameTo, 'wb') as file:
        file.write(decrypted) #write decrypted data to new file
    #os.remove(filenameFrom) #delete original file

def new_salt():
    with open('salt.txt','wb') as saltFile:
        saltFile.write(os.urandom(16))


customtkinter.set_default_color_theme("green")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.username_var = str()
        self.password_var = str()

        self.title("SFOTA Car Dashboard")
        self.geometry("1024x610")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
                                                 size=(26, 26))

        self.car_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "car.png")), size=(500, 150))

        self.apple_music = customtkinter.CTkImage(Image.open(os.path.join(image_path, "apple_music.png")),
                                                  size=(120, 120))

        self.youtube_music = customtkinter.CTkImage(Image.open(os.path.join(image_path, "youtube_music.png")),
                                                    size=(120, 120))

        self.spotify = customtkinter.CTkImage(Image.open(os.path.join(image_path, "spotify.png")), size=(120, 120))

        self.rainy_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "rainy.png")), size=(50, 50))

        self.sunny_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "sunny.png")), size=(50, 50))

        self.temperature_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "temperature.png")),
                                                        size=(50, 50))

        self.battery_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "battery1.png")),
                                                    size=(125, 170))

        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                                 size=(20, 20))

        self.music_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "music_light.png")),
                                                  dark_image=Image.open(os.path.join(image_path, "music_dark.png")),
                                                  size=(20, 20))

        self.settings_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "settings_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "settings_light.png")),
            size=(20, 20))

        self.profile_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "profile_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "profile_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=15, border_width=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=" SFOTA ", corner_radius=38,
                                                             image=self.logo_image, compound="left", fg_color="#384447",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=30)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=100,
                                                   border_spacing=10, text="Car\nOverview",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="NSEW",
                                                   command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=100,
                                                      border_spacing=10, text="Update\nCenter",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.profile_image, anchor="NSEW",
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=100,
                                                      border_spacing=10, text="Music",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.music_image, anchor="NSEW",
                                                      command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=100,
                                                      border_spacing=10, text="Settings ",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.settings_image, anchor="NSEW",
                                                      command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark"],
                                                                command=self.change_appearance_mode_event,
                                                                fg_color="#067C75", button_color='#067C75')
        self.appearance_mode_menu.grid(row=5, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=0)

        self.home_frame_car = customtkinter.CTkLabel(self.home_frame, text="", image=self.car_image)
        self.home_frame_car.grid(row=0, column=0, padx=20, pady=40, columnspan=2)

        # battery frame
        self.battery_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=7, width=300, height=320,
                                                    fg_color="#008080", border_width=0)
        self.battery_frame.grid(row=1, column=0, padx=20, pady=10, sticky='nsew')

        self.battery_word_label = customtkinter.CTkLabel(self.battery_frame, text="Battery Data",
                                                         text_color=("gray10", "gray90"),
                                                         font=customtkinter.CTkFont(size=17))
        self.battery_word_label.grid(row=0, column=0, padx=20, pady=15, sticky='nw')

        self.battery_frame_label = customtkinter.CTkLabel(self.battery_frame, text="", image=self.battery_image)
        self.battery_frame_label.grid(row=1, column=0, padx=7, pady=15)

        self.battery_KM_label = customtkinter.CTkLabel(self.battery_frame, text="400 Km Traveled\t\n\n350 Km Left\t\n"
                                                                                "\nkeep your Speed\t\nBelow 50 Km/h\t",
                                                       font=customtkinter.CTkFont(size=14, weight="bold"))
        self.battery_KM_label.grid(row=1, column=1, padx=10, pady=80, sticky='nw')

        # weather frame
        self.weather_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=7, width=440, height=320,
                                                    fg_color="#008080", border_width=0)
        self.weather_frame.grid(row=1, column=1, padx=30, pady=10, sticky='nsew')

        self.weather_word_label = customtkinter.CTkLabel(self.weather_frame, text="Weather Data",
                                                         text_color=("gray10", "gray90"),
                                                         font=customtkinter.CTkFont(size=17))
        self.weather_word_label.grid(row=0, column=0, padx=20, pady=15, sticky='nw')

        self.weather_sunny_label = customtkinter.CTkLabel(self.weather_frame, text="", image=self.sunny_image)
        self.weather_sunny_label.grid(row=1, column=0, padx=50, pady=15)

        self.weather_sunny_label = customtkinter.CTkLabel(self.weather_frame, text="Sunny",
                                                          font=customtkinter.CTkFont(size=16, weight="bold"))
        self.weather_sunny_label.grid(row=2, column=0, padx=25, pady=5)

        self.weather_sunny_label = customtkinter.CTkLabel(self.weather_frame, text="Wind Speed\n 17Km/h",
                                                          font=customtkinter.CTkFont(size=15, weight="bold"))
        self.weather_sunny_label.grid(row=3, column=0, padx=25, pady=25)

        self.weather_temp_label = customtkinter.CTkLabel(self.weather_frame, text="", image=self.temperature_image)
        self.weather_temp_label.grid(row=1, column=1, padx=50, pady=25)

        self.weather_sunny_label = customtkinter.CTkLabel(self.weather_frame, text="Inside Car\n  21 C",
                                                          font=customtkinter.CTkFont(size=15, weight="bold"))
        self.weather_sunny_label.grid(row=2, column=1, padx=10, pady=5)

        self.weather_sunny_label = customtkinter.CTkLabel(self.weather_frame, text="Outside\n 26 C",
                                                          font=customtkinter.CTkFont(size=15, weight="bold"))
        self.weather_sunny_label.grid(row=3, column=1, padx=10, pady=25)

        self.weather_rainy_label = customtkinter.CTkLabel(self.weather_frame, text="", image=self.rainy_image)
        self.weather_rainy_label.grid(row=1, column=2, padx=50, pady=25)

        self.weather_sunny_label = customtkinter.CTkLabel(self.weather_frame, text="33%\n Humidity",
                                                          font=customtkinter.CTkFont(size=15, weight="bold"))
        self.weather_sunny_label.grid(row=2, column=2, padx=10, pady=5)

        self.weather_sunny_label = customtkinter.CTkLabel(self.weather_frame, text="20%\n Perception",
                                                          font=customtkinter.CTkFont(size=15, weight="bold"))
        self.weather_sunny_label.grid(row=3, column=2, padx=10, pady=25)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)

        self.login_label = customtkinter.CTkLabel(self.second_frame, text="To Request Update Please Login First",
                                                  font=customtkinter.CTkFont(size=35, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=20, pady=(80, 15))

        self.username_entry = customtkinter.CTkEntry(self.second_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))

        self.password_entry = customtkinter.CTkEntry(self.second_frame, width=200, show="*",
                                                     placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))

        self.login_button = customtkinter.CTkButton(self.second_frame, text="Login", command=self.login_event,
                                                    width=200, fg_color="#008080", hover_color=("gray30", "gray30"))
        self.login_button.grid(row=3, column=0, padx=30, pady=(15, 15))

        self.progress_bar = customtkinter.CTkProgressBar(self.second_frame, width=500, height=50, mode='determinate',
                                                         determinate_speed=0.09, progress_color="#008080")

        self.Loading = customtkinter.CTkLabel(self.second_frame, text="Loading...",
                                              font=customtkinter.CTkFont(size=15, weight="bold"))

        self.Installing = customtkinter.CTkLabel(self.second_frame, text="Installing...",
                                                 font=customtkinter.CTkFont(size=15, weight="bold"))

        self.label_hidden = customtkinter.CTkLabel(self.second_frame, text="",
                                                   font=customtkinter.CTkFont(size=25, weight="bold"))
        self.label_hidden.grid(row=5, column=0, padx=30, pady=(50, 15))



        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(0, weight=0)

        self.space_button = customtkinter.CTkButton(self.third_frame, text="")
        self.space_button.grid(row=3, column=0, padx=100, pady=200)

        self.spotify_button = customtkinter.CTkButton(self.third_frame, text="", image=self.spotify,
                                                      fg_color="transparent", hover_color=("gray30", "gray30"))
        self.spotify_button.grid(row=3, column=0, padx=25, pady=220)
        self.spotify_button.bind("<Button-1>", lambda e: webbrowser.open_new("https://open.spotify.com/"))

        self.apple_music_button = customtkinter.CTkButton(self.third_frame, text="", image=self.apple_music,
                                                          fg_color="transparent", hover_color=("gray30", "gray30"))
        self.apple_music_button.grid(row=3, column=1, padx=40, pady=220)
        self.apple_music_button.bind("<Button-1>", lambda e: webbrowser.open_new("https://music.apple.com/"))

        self.youtube_music_button = customtkinter.CTkButton(self.third_frame, text="", image=self.youtube_music,
                                                            fg_color="transparent", hover_color=("gray30", "gray30"))
        self.youtube_music_button.grid(row=3, column=2, padx=70, pady=220)
        self.youtube_music_button.bind("<Button-1>", lambda e: webbrowser.open_new("https://music.youtube.com/"))

        # create fourth frame
        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.fourth_frame.grid_columnconfigure(0, weight=1)

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    def login_event(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if (username == '123') and (password == '123'):
            webbrowser.open_new("http://swiftact.6te.net/mydashboard2.php")
            webbrowser.open_new("http://swiftact.6te.net/mydashboard.php")
            self.Loading.grid(row=5, column=0, padx=5, pady=0)
            time.sleep(8)
            filenameFrom = "/home/emad/Downloads/103_Wave_enc.txt"
            filenameTo = "/home/emad/Downloads/103_Wave.txt"
            password = "123"
            key = get_key(password)
            decrypt_file(key, filenameFrom, filenameTo)

            filenameFrom = "/home/emad/Downloads/205_High_enc.txt"
            filenameTo = "/home/emad/Downloads/205_High.txt"
            password = "123"
            key = get_key(password)
            decrypt_file(key, filenameFrom, filenameTo)
            #self.Loading.grid_forget()
            self.progress_bar.grid(row=4, column=0, padx=5, pady=(25, 15))
            self.progress_bar.start()
            self.Installing.grid(row=5, column=0, padx=5, pady=0)
            time.sleep(3)
            CAN_ID_103()
            #self.progress_bar.grid_forget()
            #self.Installing.grid_forget()

            time.sleep(3)
            self.progress_bar.grid(row=4, column=0, padx=5, pady=(25, 15))
            self.progress_bar.start()
            self.Installing.grid(row=5, column=0, padx=5, pady=0)
            CAN_ID_205()
            #self.Installing.grid_forget()
            #self.progress_bar.grid_forget()
            self.on_show_label_click()
            file.close()

    def on_show_label_click(self):
        if self.label_hidden.cget("text") == "":
            self.label_hidden.configure(text="System is Updated Successfully")
        else:
            self.label_hidden.configure(text="")

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
