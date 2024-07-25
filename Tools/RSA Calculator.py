import math
from egcd import egcd
import re
import tkinter as tk

style = {
    "bg": "black",
    "fg": "white",
    # "insertbackground": "white"  # Cursor color in the Entry field
}

# Create the main window
root = tk.Tk()
root.title("RSA Calculator")
root.configure(bg=style["bg"])

frame=tk.Frame(root, bg=style["bg"])
frame.pack()

buttons=tk.Frame(root, bg=style["bg"])
buttons.pack()

log_console = tk.Text(root, height=3, width=50, bg="black", fg="white", wrap=tk.WORD, state=tk.DISABLED    )
log_console.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Log to the console
def log(text):
    log_console.config(state=tk.NORMAL)
    log_console.insert(tk.END, str(text)+"\n")
    log_console.config(state=tk.DISABLED)

# Creates input fields
def create_input(label, row):
    # entry = tk.Entry(frame,background='black', foreground='white', width=50, **style)
    entry = tk.Entry(frame, width=50, **style)
    entry.grid(row=row, column=1)
    tk.Label(frame, **style, text=label+" =").grid(row=row, column=0)
    tk.Button(frame, **style, text="Clear", command=lambda: entry.delete(0, tk.END)).grid(row=row,column=2)
    return entry


# Defines input fields
crow=0
c=create_input("c", crow)
n=create_input("n", crow:=crow+1)
e=create_input("e", crow:=crow+1)
p=create_input("p", crow:=crow+1)
q=create_input("q", crow:=crow+1)
phi=create_input("phi", crow:=crow+1)
d=create_input("d", crow:=crow+1)
m=create_input("m", crow:=crow+1)

e.insert(0, "65537")


# Check if the values are correct
# Hacky as hell, but it works
def check():
    try:
        if int(n.get()) != int(p.get())*int(q.get()):
            log("Error: n != p*q")
            return False
    except:
        pass
    try:
        if int(phi.get()) != (int(p.get())-1)*(int(q.get())-1):
            log("Error: phi != (p-1)*(q-1)")
            return False
    except:
        pass
    try:
        if (int(d.get())*int(e.get())) % int(phi.get()) != 1:
            log("Error: d*e % phi != 1")
            return False
    except:
        pass
    return True

# Can a value be calculated?
def cc(list):
    val = [i.get() for i in list]
    count = [v for v in val if v]
    if len(count) == len(val) - 1:
        return True
    return False

# Calculate the values
def calc():
    for i in range(0,3):
        if not check():
            return
        if cc([n,p,q]):
            if n.get()=="":
                n.insert(0, str(int(p.get())*int(q.get())))
            if p.get()=="":
                p.insert(0, str(int(n.get())//int(q.get())))
            if q.get()=="":
                q.insert(0, str(int(n.get())//int(p.get())))
        if cc([phi,p,q]):
            if phi.get()=="":
                phi.insert(0, str((int(p.get())-1)*(int(q.get())-1)))
            if p.get()=="":
                p.insert(0, str(int(math.sqrt(int(phi.get())))+1))
            if q.get()=="":
                q.insert(0, str(int(math.sqrt(int(phi.get())))+1))
        if cc([d,e,phi]):
            if d.get()=="":
                d.insert(0, str(egcd(int(e.get()), int(phi.get()))[1]))
            if e.get()=="":
                e.insert(0, str(egcd(int(d.get()), int(phi.get()))[1]))
        
# Cipher
def cipher():
    if c.get() != "":
        log("Error: c already filled")
    elif m.get() != "" and n.get() != "" and e.get() != "":
        c.insert(0, str(pow(int(m.get()), int(e.get()), int(n.get()))))
    else:
        log("Error: m, n, or e not filled")

# Decipher
def decipher():
    if m.get() != "":
        log("Error: m already filled")
    elif c.get() != "" and n.get() != "" and d.get() != "":
        m.insert(0, str(pow(int(c.get()), int(d.get()), int(n.get()))))
        try:
            log(bytes.fromhex(hex(int(m.get()))[2:]).decode('utf-8'))
        except Exception as e:
            log(str(e))
    else:
        log("Error: c, n, or d not filled")

# Strip non int characters
def strip():
    for entry in [c, n, e, p, q, phi, d, m]:
        v=re.sub(r'[^0-9-]|','',entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, v)

def auto():
    strip()
    calc()
    if c.get()!="":
        decipher()
    else:
        cipher()
    


# Create a button
tk.Button(buttons, **style, text="strip", command=strip).grid(row=(crow:=crow+1), column=0, padx=5, pady=5)
tk.Button(buttons, **style, text="calc", command=calc).grid(row=crow, column=1, padx=5, pady=5)
tk.Button(buttons, **style, text="cipher", command=cipher).grid(row=crow, column=2, padx=5, pady=5)
tk.Button(buttons, **style, text="decipher", command=decipher).grid(row=crow, column=3, padx=5, pady=5)
tk.Button(buttons, **style, text="auto", command=auto).grid(row=crow, column=4, padx=5, pady=5)
tk.Button(buttons, **style, text="quit", command=root.quit).grid(row=crow, column=5, padx=5, pady=5)

# Run the application
root.mainloop()
