from json import load as load_json
from random import choice
import tkinter as tk

# global constant to hold all themes, dict
THEMES = None
class Prime:
    """
    Class holding all the Tkinter code to render a window to accept the number
    and answer weather the number is prime or not. Also contains the function 
    to check for prime number.
    """

    def __init__(self, master:tk.Tk) -> None:
        self.height = 300
        self.width = 500

        # private var to store the result of previously entered number
        self.__oldvalue = ""

        # getting user's screen resolutions
        w = master.winfo_screenwidth()
        h = master.winfo_screenheight()

        # calculate the x and y coordinates to position app window 
        # in center of screen
        x = (w//2) - (self.width//2)
        y = (h//2) - (self.height//2)


        # Window Setup --------------------------------------------------------

        # Setting default theme on app startup
        self.theme_name = 'Blue_Berries'
        self.set_theme()

        # Bind button 't' of keyboard to cycle through themes in random
        master.bind('<t>', self.randomize_theme)


        self.master = master
        self.master.title("Prime Number?")

        # set geometry of the window and its position
        self.master.geometry("{}x{}+{}+{}".format(self.width, 
                                                  self.height, x, y))

        # set window resizable options off
        self.master.resizable(False, False)


        # Widgets -------------------------------------------------------------

        # Frame widget to hold the title and the input text widget. 
        # (Upper Section of the window)
        self.input_frame = tk.Frame(self.master, 
                                    height=self.height//2, 
                                    width=self.width, 
                                    bg=self.col_bg)
        self.input_frame.grid(row=0, column=0)

        # Label for the heading statement...
        self.label_1 = tk.Label(self.input_frame,
                                bg = self.col_bg,
                                fg = self.col_fg,
                                justify = "center",
                                font = "Montserrat 15",
                                text = "Enter your number below")
        self.label_1.place(relx = 0.5, y=10,anchor = "n")

        #  Text variable to get text form the text input field.
        self.test_number = tk.StringVar()
        # connecting the text var to a callback function to monitor 
        # the text in the text box on every key press.
        self.test_number.trace("w", self.entry_callback)

        # text input widget for getting test number
        self.num_entry = tk.Entry(self.input_frame, 
                                  bg=self.col_bg,
                                  fg = self.col_fg,
                                  width=10,
                                  justify="center", 
                                  bd=0, font="Montserrat 40 bold", 
                                  textvariable=self.test_number)
        self.num_entry.place(relx=0.5, rely=0.4, anchor='n')
        self.num_entry.focus()

        # Frame to hold output label and warning/status label 
        # (Lower section of the window)
        self.output_frame = tk.Frame(self.master, 
                                     height=self.height//2, 
                                     width=self.width, 
                                     bg=self.col_bg)
        self.output_frame.grid(row=1, column=0)

        # label to display the number's type (Prime/Not Prime) or waiting for
        # input text ('Umm...').
        self.label_2 = tk.Label(self.output_frame,
                            bg = self.col_bg,
                            fg = self.col_fg,
                            justify = "center",
                            font = "Montserrat 45",
                            text = "Umm..."
                            )
        self.label_2.place(relx = 0.5, y=10, anchor = "n")

        # Label for warnings and status for user's inputs
        self.error_lbl = tk.Label(self.output_frame,
                                  bg = self.col_bg,
                                  fg = self.col_warning,
                                  justify = "center",
                                  font = "Montserrat 10",
                                  text = "Waiting for a number!" )
        self.error_lbl.place(relx=0.5, y=140,anchor="s")
        # END of widgets placements.

    # END of __init__()

    def randomize_theme(self, event) -> None:
        """
        Event Callback on key press.
        Method to select a new color theme from the list of themes randomly.
        """
        # Get names of all themes and remove the name of current theme form the
        # list to avoid repetation.
        themes = list(THEMES.keys())
        themes.remove(self.theme_name)

        self.theme_name = choice(themes)

        self.set_theme()
        self.update_ui()

    def set_theme(self) -> None:
        """
        Method to set all class variable related to widget coloring with
        selected color theme values.
        """

        global THEMES

        # load themes from the json file if not already loaded
        if THEMES is None:
            THEMES = self.get_themes()

        self.current_theme = THEMES[self.theme_name]
        self.col_bg = self.current_theme['bg']
        self.col_fg = self.current_theme['fg']
        self.col_default = self.current_theme['default']
        self.col_not_prime = self.current_theme['not_prime']
        self.col_prime = self.current_theme['prime']
        self.col_warning = self.current_theme['warning']
    
    def get_themes(self) -> dict:
        """
        Returns a dictionary for a json file containing all color schems and
        themes for the application.
        """

        FILE_NAME = "Colors.json"
        
        try:
            with open(FILE_NAME, "r") as themes_file:
                return load_json(themes_file)
        except Exception as e:
            print("Exception Occured: ", e)
            return dict()

    def update_ui(self) -> None:
        """
        Refresh all widgets in the application to change the colors scheme
        after theme change
        """
        self.input_frame.configure(bg=self.col_bg)
        self.output_frame.config(bg=self.col_bg)

        self.label_1.configure(bg=self.col_bg, fg=self.col_fg)
        self.label_2.configure(bg=self.col_bg, fg=self.col_fg)
        self.error_lbl.configure(bg=self.col_bg, fg=self.col_warning)
        self.num_entry.configure(bg=self.col_bg, fg=self.col_fg)
        
    # Callback method to mointor the input text widget on every 
    # character entry...
    def entry_callback(self, *args) -> None:
        """
        Event Callback (Character entry event).
        Method called whenever user enters new number/character in the input 
        field. Warns user if entry gets larger than 10 digits or user inputs
        non-numeric character. Reverts text of entry to previous valid value 
        in case of any invalid inputs.
        """
        # get new input value form the text variable...
        string = self.test_number.get()

        # If length exceeds 10 characters change back to 10 characters and 
        # show a warning msg...
        if len(string) > 10:
            self.test_number.set(self.__oldvalue)
            self.error_lbl['text'] = "Whoa! Hold on, input limit is 10"

        # If the input string in all digits convert it to number type and
        # print its result in result label.
        elif string != "" and string.isdigit():
            number = int(string)

            result_string, color = self.check_prime(number)

            self.label_2['text'] = result_string
            self.label_2['fg'] = color
            self.error_lbl['text'] = ""
            self.__oldvalue = string

        # If the there is no input display the waiting msg
        elif string == "":
            self.label_2['fg'] = self.col_default
            self.label_2['text'] = "Umm..."
            self.error_lbl['text'] = "Waiting for a number!"
            self.__oldvalue = ""

        # If user types any non digit character, revert back to previous input 
        # and diaplay the old numbers result and an error msg 
        # This give an effect as if the non-digit characters were never typed...
        elif not string.isdigit():
            if self.__oldvalue == "":
                self.label_2['fg'] = self.col_default
                self.label_2['text'] = "Umm..."
                self.test_number.set("")
            else:
                self.test_number.set(self.__oldvalue)
                number = int(self.__oldvalue)
                result_string, color = self.check_prime(number)
                self.label_2['text'] = result_string
                self.label_2['fg'] = color

            self.error_lbl['text'] = "Opps... Only Integers Please!"

    def check_prime(self, num) -> tuple:
        """
        Method to check if passed number is Prime or Not.
        Returns a tuple containing status string and color parameter to set the
        message label to.
        """
        if num == 1:
            return ("Not Sure!", self.col_default)
        i=2
        while i*i<=num:
            if num%i == 0:
                return ("Not Prime", self.col_not_prime)
            i+=1
        return ("Prime", self.col_prime)

# Driver function.
def main():
    root = tk.Tk()
    Prime(root)
    root.mainloop()
    pass

if __name__ == "__main__":
    main()