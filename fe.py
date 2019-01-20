from tkinter import *
from core import AllegroCore
import webbrowser
from tkinter import filedialog

al=AllegroCore()
output=al.get_verification_url()
verification_url=output['verification_uri_complete']
window = Tk()

window.title("Allegro Search App")
window.geometry('1000x800')

class FrontEnd:

    def create_button(self):
        self.auth_button=Button(window, text="Click Me", command=self.open_browser)
        self.auth_button.grid(column=0, row=1)

    def open_browser(self):
        webbrowser.open_new(verification_url)
        al.poll_verification()
        self.lbl.configure(fg='green')
        self.lbl.configure(text='Verified')
        self.auth_button.destroy()
        self.create_upload_file_btn()



    def create_label(self):
        self.lbl = Label(window, text="Click Button to verify Authenticate")
        self.lbl.grid(column=0, row=0)

    def create_upload_file_btn(self):
        self.ubtn=Button(window, text="Upload File", command=self.opendialog)
        self.ubtn.grid(column=0, row=2)

    def opendialog(self):
        window.filename = filedialog.askopenfilename(initialdir="/", title="Select file")
        al.read_excel(window.filename)
        self.show_radio_buttons()

    def show_radio_buttons(self):
        self.mode = StringVar()
        self.search_type=StringVar()
        self.fallback = StringVar()
        self.fifty_check=BooleanVar()
        self.fifty_check.set(True)
        self.searchMode= Label(window, text="Search Mode")
        self.searchMode.grid(column=0, row=3)
        self.mode.set('REGULAR')
        self.search_type.set('Product')

        self.fallback.set('false')
        self.rd1=Radiobutton(window,
                       text="REGULAR",
                       padx=20,
                       variable=self.mode,
                       value='REGULAR')
        self.rd2=Radiobutton(window,
                       text="DESCRIPTION -",
                       padx=20,
                       variable=self.mode,
                       value="DESCRIPTION")
        self.rd1.grid(column=0,row=4)
        self.rd2.grid(column=1,row=4)
        self.searchtype = Label(window, text="Search Type")
        self.searchtype.grid(column=0, row=6)
        self.rd3 = Radiobutton(window,
                               text="Phrase",
                               padx=20,
                               variable=self.search_type,
                               value="Product")
        self.rd4 = Radiobutton(window,
                               text="EAN",
                               padx=20,
                               variable=self.search_type,
                               value="EAN")
        self.rd3.grid(column=0, row=7)
        self.rd4.grid(column=1, row=7)


        self.falllab = Label(window, text="Activate Fallback")
        self.falllab.grid(column=0, row=11)
        self.rd5 = Radiobutton(window,
                               text="true",
                               padx=20,
                               variable=self.fallback,
                               value="true")
        self.rd6 = Radiobutton(window,
                               text="false",
                               padx=20,
                               variable=self.fallback,
                               value="false")
        self.rd5.grid(column=0, row=12)
        self.rd6.grid(column=1, row=12)
        self.fifty_check_label = Label(window, text="Not more than 50 ?")
        self.fifty_check_label.grid(column=0, row=13)
        self.rd7 = Radiobutton(window,
                               text="true",
                               padx=20,
                               variable=self.fifty_check,
                               value=True)
        self.rd8 = Radiobutton(window,
                               text="false",
                               padx=20,
                               variable=self.fifty_check,
                               value=False)
        self.rd7.grid(column=0, row=14)
        self.rd8.grid(column=1, row=14)

        self.sbtn = Button(window, text="Start Search", command=self.search)
        self.sbtn.grid(column=0, row=15)
    def search(self):
        al.search_type=self.search_type.get()
        al.mode=self.mode.get()
        al.fallback=self.fallback.get()
        al.fifty_check = self.fifty_check.get()
        self.sbtn.configure(text='Loading ... ')

        status=al.start_search()

        print(status)
        if status == True:
            self.sbtn.configure(text='Start Search ')
            self.lbl.configure(text='Done searching, check your root folder , also upload new file')
    def __init__(self):
        self.create_label()
        self.create_button()
fe=FrontEnd()
window.mainloop()