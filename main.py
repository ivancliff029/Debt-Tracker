from tkinter import *
from tkinter.ttk import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#import mysql.connector
import database
import sqlite3
from tkinter import messagebox
from datetime import date

listOfUsers = []
userInfo = []

#create the table if not exists
connn = sqlite3.connect("iplannerdb.db")
curCursor = connn.cursor()
curCursor.execute("""
CREATE TABLE IF NOT EXISTS history(
name text,
amount int,
DOL datetime,
DOR datetime
)
""")
curCursor.execute("""
CREATE TABLE IF NOT EXISTS users(
name text,
amount int,
DOL datetime,
DOR datetime
)
""")

connn.commit()
connn.close()

root = Tk()
root.title("iPlanner")
root.geometry("900x600+250+60")
root.resizable(False, False)
root.iconbitmap("logo.ico")

#functions
#get the current date
today = date.today()
d1 = today.strftime("%d/%m/%Y")

def show_dashboard():
    # Create a new window for the dashboard
    dashboard_window = Toplevel(root)
    dashboard_window.title("Debt Tracking Dashboard")
    dashboard_window.geometry("800x600")

    # Get statistics data from the database
    total_borrowed = "2,500,000"
    # Display statistics using labels
    label_title = Label(dashboard_window, text="Debt Tracking Dashboard", font=("Arial", 16, "bold"))
    label_title.pack(pady=10)

    label_total_borrowed = Label(dashboard_window, text=f"Total Borrowed Amount: shs{total_borrowed}", font=("Arial", 12))
    label_total_borrowed.pack(pady=10)

    # Visualize data using a bar chart embedded in the dashboard window
    visualize_data(dashboard_window)

def visualize_data(parent_window):
    # Create a simple bar chart for visualization
    categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug','Sep','Oct','Nov','Dec']
    values = [60000, 80000, 50000, 100000, 120000, 150000, 100000, 56000, 200000, 300000, 250000, 450000]

    # Create a figure and axis
    fig, ax = plt.subplots()
    ax.bar(categories, values)
    ax.set_xlabel('Month')
    ax.set_ylabel('Money Borrowed(shs)')
    ax.set_title('Payment Graph')

    # Embed the chart in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=parent_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(pady=20)
    
def showUserDetails():
    db = sqlite3.connect("iplannerdb.db")
    myCursor = db.cursor()
    myCursor.execute("SELECT *, oid FROM users")
    rs = myCursor.fetchall()

    for row in rs:
        #arrange the data in the same data structure
        data = row
        treeView.insert("",1, text=data[0], values=(data[1], data[2], data[3], "Donated",data[4]))
    db.commit()
    db.close()

def settleUser():
    con = sqlite3.connect("iplannerdb.db")
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE oid = "+ str(listOfUsers[-1]))
    cur.execute("INSERT INTO history VALUES(:name,:amount,:DOL,:DOR)",
    {
    "name":userInfo[5],
    "amount":userInfo[0],
    "DOL":userInfo[1],
    "DOR":userInfo[2]
    })
    userInfo.clear()
    con.commit()
    con.close()
    #Display in the history frame



def updateUser():
    try:
        root = Tk()
        root.title("Update User Data")
        root.geometry("400x200+450+200")

        data = listOfUsers[-1]


        conn = sqlite3.connect("iplannerdb.db")
        myCursor = conn.cursor()
        myCursor.execute("SELECT *, oid FROM users WHERE oid="+str(data))
        result = myCursor.fetchall()
        for row in result:
            Data = [row[0], row[1], row[2],row[3]]
            nameLabel = Label(root, text="Name")
            nameLabel.grid(row=0, column=0)
            amountLabel = Label(root, text="Amount")
            amountLabel.grid(row=1, column=0)
            dolLabel = Label(root, text="DOL")
            dolLabel.grid(row=2, column=0)
            dorLabel = Label(root, text="DOR")
            dorLabel.grid(row=3, column=0)

            nameEntry = Entry(root)
            nameEntry.insert(0,Data[0])
            nameEntry.grid(row=0, column=1)
            amountEntry = Entry(root)
            amountEntry.insert(0,Data[1])
            amountEntry.grid(row=1, column=1)
            dolEntry = Entry(root)
            dolEntry.insert(0,Data[2])
            dolEntry.grid(row=2, column=1)
            dorEntry = Entry(root)
            dorEntry.insert(0,Data[3])
            dorEntry.grid(row=3, column=1)

            def update():
                conn = sqlite3.connect("iplannerdb.db")
                cur = conn.cursor()
                cur.execute("""UPDATE users SET
                name = :name,
                amount = :amount,
                dol = :dol,
                dor = :dor

                WHERE oid = :oid""",
                           {
                               'name':nameEntry.get(),
                               'amount':amountEntry.get(),
                               'dol':dolEntry.get(),
                               'dor':dorEntry.get(),
                               'oid': data
                           })

                conn.commit()
                conn.close()
                root.destroy()
            update = Button(root, text="Update", command=update)
            update.grid(row=4, column=1)
    except IndexError:
        messagebox.showerror("Please Click on the Record you want to Update first");


def select_item(a):
    str_lib = treeView.item(treeView.selection())
    listOfUsers.append(str_lib['values'][4])
    name = str_lib['text']
    info = str_lib['values']
    info.append(name)

    for i in info:
        userInfo.append(i)
    print(userInfo)
    print(listOfUsers)
def deleteUser():
    connection = sqlite3.connect("iplannerdb.db")
    connCur = connection.cursor()
    connCur.execute("DELETE FROM users WHERE oid = "+ str(listOfUsers[-1]))
    connection.commit()
    connection.close()

            #from UI
    selected_item = treeView.selection()[0]
    treeView.delete(selected_item)

    #deleteUser()

#create the function that first clears and deletes all the recent records
def clearTreeview():
    #create a for loop and in each iteration, delete a records
    tv = treeView.get_children()
    for j in tv:
        treeView.delete(j)

def refresh():
    _nameEntry.delete(0, END)
    _amountEntry.delete(0, END)
    _DOLEntry.delete(0, END)
    _DOREntry.delete(0, END)

def refreshAndShowInfo():
    clearTreeview()
    showUserDetails()
    refreshHistory()

def addUser():
    name = _nameEntry.get()
    amount = _amountEntry.get()
    DOL = _DOLEntry.get()
    DOR = _DOREntry.get()
    #Contact the DataBase
    user = database.storeData(name, amount, DOL, DOR)
    user.getUserData()
    refresh()
    clearTreeview()
    showUserDetails()
    _DOLEntry.insert(0,d1)
def delete():
    selected_item = treeView.selection()[0]
    treeView.delete(selected_item)
    print(selected_item)

    window = Tk()
    window.title("Update User Details")

    name = Label(root, text="Name")
    name.grid(row=0, column=0)
    amount = Label(root, text="Name")
    amount.grid(row=1, column=0)
    DOL = Label(root, text="Name")
    DOL.grid(row=2, column=0)
    DOR = Label(root, text="Name")
    DOR.grid(row=3, column=0)

    _name = Entry(root)
    _name.grid(row=0, column=1)
    _amount = Entry(root)
    _amount.grid(row=1, column=1)
    _DOL = Entry(root)
    _DOL.grid(row=2, column=1)
    _DOR = Entry(root)
    _DOR.grid(row=3, column=1)


    window.mainloop()

#Menus
MainMenu = Menu(root)
DashboardMenu = Menu(MainMenu, tearoff=0)
DashboardMenu.add_command(label = "View Dash Board", command=show_dashboard)
MainMenu.add_cascade(label = "Dash Board", menu=DashboardMenu)

PlansMenu = Menu(MainMenu, tearoff=0)
PlansMenu.add_command(label = "Add Plan")
MainMenu.add_cascade(label = "Add Plan" , menu=PlansMenu)

root.config(menu=MainMenu)
#create the frames
MainFrame = Frame(root)
MainFrame.pack()
TitleFrame = Frame(MainFrame)
TitleFrame.pack(side=TOP)
DataFrame = Frame(MainFrame)
DataFrame.pack(side=RIGHT)
EntryFrame = LabelFrame(MainFrame, text = "Enter User Details")
EntryFrame.pack(side=RIGHT)
HistoryFrame = LabelFrame(root, text="Payment History")
HistoryFrame.pack(side=TOP)
ButtonFrame = Frame(root)
ButtonFrame.pack(side=BOTTOM)

#function to refresh the history frame
def refreshHistory():
    payment.delete(0,END)
    connect = sqlite3.connect("iplannerdb.db")
    connectCur = connect.cursor()
    connectCur.execute("SELECT *, oid FROM history")
    resultSlip = connectCur.fetchall()

    for row in resultSlip:
        dateOFpayment = d1
        word = "paid on"
        data = [row[0],row[1],row[2], row[3], row[4]]
        data.append(word)
        data.append(dateOFpayment)
        payment.insert(END, data)
    connect.commit()
    connect.close()

scrollbarHistory = Scrollbar(HistoryFrame)
scrollbarHistory.grid(row=0, column=1, sticky='ns')
payment = Listbox(HistoryFrame, width=135, height=14,yscrollcommand = scrollbarHistory.set)
payment.grid(row=0, column=0, sticky='nw')

#display the data from the database in the history frame
connect = sqlite3.connect("iplannerdb.db")
connectCur = connect.cursor()
connectCur.execute("SELECT *, oid FROM history")
resultSlip = connectCur.fetchall()

for row in resultSlip:
    dateOFpayment = d1
    word = "paid on"
    data = [row[0],row[1],row[2], row[3], row[4]]
    data.append(word)
    data.append(dateOFpayment)
    payment.insert(END, data)
connect.commit()
connect.close()
scrollbarHistory.config(command = payment.yview)

#create the widgets
#title frame
titleLabel = Label(TitleFrame, text = "iPlanner", font=("arial",20,"bold"))
titleLabel.grid()
#Data frame
scrollbar = Scrollbar(DataFrame)
scrollbar.grid(row=0, column=1, sticky='ns')
treeView = Treeview(DataFrame, yscrollcommand=scrollbar.set)
treeView.grid(row=0, column=0)
treeView["columns"] = ("one", "two" , "three", "four", "five")
treeView.column("#0", width=150, minwidth=270, stretch=NO)
treeView.column("one", width=100, minwidth=270, stretch=NO)
treeView.column("two", width=150, minwidth=270, stretch=NO)
treeView.column("three", width=120, minwidth=270, stretch=NO)
treeView.column("four", width=80, minwidth=270, stretch=NO)
treeView.column("five", width=50, minwidth=270, stretch=NO)

treeView.heading("#0", text = "Name", anchor=W)
treeView.heading("one", text = "Amount", anchor=W)
treeView.heading("two", text = "Date Given Out", anchor=W)
treeView.heading("three", text = "Date to be received", anchor=W)
treeView.heading("four", text = "Status", anchor=W)
treeView.heading("five", text = "ID", anchor=W)
treeView.bind('<<TreeviewSelect>>', select_item)
scrollbar.config(command = treeView.yview)

#display the data from the DataBase
showUserDetails()

#button Frame
updateBtn = Button(ButtonFrame, text="Update", command=updateUser)
updateBtn.grid(row=0 , column=0, pady=5)
deleteBtn = Button(ButtonFrame, text="Delete", command=deleteUser)
deleteBtn.grid(row=0, column=1, pady=5)
exitBtn = Button(ButtonFrame, text="Refresh", command=refreshAndShowInfo)
exitBtn.grid(row=0, column=2, pady=5)
settleBtn = Button( ButtonFrame, text="Settle", command=settleUser)
settleBtn.grid(row=0, column=3, pady=5)
#Entry frame
_name = Label(EntryFrame, text="Name")
_name.grid(row=0, column=0, pady=3)
_amount = Label(EntryFrame, text="Amount")
_amount.grid(row=1, column=0, pady=3)
_DOL = Label(EntryFrame, text="DOL")
_DOL.grid(row=2, column=0, pady=3)
_DOR = Label(EntryFrame, text="DOR")
_DOR.grid(row=3, column=0, pady=3)

_nameEntry = Entry(EntryFrame)
_nameEntry.grid(row=0, column=1, pady=3)
_amountEntry = Entry(EntryFrame)
_amountEntry.grid(row=1, column=1, pady=3)
_DOLEntry = Entry(EntryFrame)
_DOLEntry.insert(0,d1)
_DOLEntry.grid(row=2, column=1, pady=3)
_DOREntry = Entry(EntryFrame)
_DOREntry.grid(row=3, column=1, pady=3)

saveUserData = Button(EntryFrame, text="Save User Data", width=20, command=addUser)
saveUserData.grid(column=1, row=4)

root.mainloop()
