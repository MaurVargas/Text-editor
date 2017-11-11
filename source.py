from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from string import punctuation
import time
import keyword


class Application(Frame):
    """
    This is the main class of the application

    self.master = the Tk object
    self.notebook = ttk.Notebook widget to work with tabs
    """
    
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        self.config(height=650, width=600, bg='blue')
        self.pack_propagate(0)
        self.pack(fill=BOTH, expand=1)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=BOTH, expand=1)
        first_tab = self.createTab()

        #the 'X' button calls self.onExit method
        self.master.protocol('WM_DELETE_WINDOW', self.onExit)              
        self.initUI()

    def initUI(self):       
        self.master.title('MEditor')
        # Creates the menu object
        the_menu = Menu(self.master)
        self.master.config(menu=the_menu)

        file_menu = Menu(the_menu, tearoff=0)
        file_menu.add_command(label='New File   ', command=self.onNewFile)
        file_menu.add_command(label='Open       ', command=self.onOpen)
        file_menu.add_separator()
        file_menu.add_command(label='Save       ', command=self.onSave)
        file_menu.add_command(label='Save as    ', command=self.onSaveAs)
        file_menu.add_separator()
        file_menu.add_command(label='Close      ', command=self.onClose)
        file_menu.add_command(label='Exit       ', command=self.onExit)
        the_menu.add_cascade(label='File', menu=file_menu)

        edit_menu = Menu(the_menu, tearoff=0)
        edit_menu.add_command(label='Undo            Ctrl+Z ', command=self.onUndo)
        edit_menu.add_command(label='Redo             ', command=self.onRedo)
        edit_menu.add_separator()
        edit_menu.add_command(label='Cut             Ctrl+X ', command=self.onCut)
        edit_menu.add_command(label='Copy            Ctrl+C ', command=self.onCopy)
        edit_menu.add_command(label='Paste           Ctrl+V ', command=self.onPaste)
        the_menu.add_cascade(label='Edit', menu=edit_menu)

        style_menu = Menu(the_menu, tearoff=0)
        style_menu.add_command(label='Enable  Highlight   ', command=self.onEnableHighlight)
        style_menu.add_command(label='Disable  Highlight  ', command=self.onDisableHighlight)
        style_menu.add_command(label='Choose Font Colors  ', command=self.onChooseFontColors,
                               state='disable')     #yet to be implemented
        the_menu.add_cascade(label='Style', menu=style_menu)

        self.popup_menu = Menu(self.master, tearoff=0)
        self.popup_menu.add_command(label='Change Name', command=self.changeName)
        self.popup_menu.add_command(label='Close Tab', command=self.onClose)
        self.popup_menu.add_command(label='New Tab', command=self.onNewFile)

        self.notebook.bind('<Button-3>', self.doPopup)

    def createTab(self, tab_name='New tab', file_name=None, highlight=True):
        """create a new tab."""
        new_tab = Tab(self.notebook, file_name=file_name, highlight=highlight)
        self.notebook.add(new_tab, text=tab_name)
        last_added = self.notebook.index('end')
        self.notebook.select([last_added - 1])
        return new_tab

    def closeWidget(self, widget, event=None):
        """close widget."""
        widget.destroy()

    def readFile(self, filename, event=None):
        """read the file."""
        f = open(filename, 'r')
        text = f.read()
        f.close()
        return text

    def changeTabName(self, name, widget, event=None):
        """change the tab name."""
        if name == '':
            return
        elif len(name) > 10:
            name = name[:8] + '..'
        elif len(name) < 10:
            name = name + ' '*(10 - len(name))
        print(name, len(name))
        self.notebook.tab('current', text=name)
        self.closeWidget(widget)
 
    def doPopup(self, event=None):
        """pops the popup menu"""
        time.sleep(0.1)
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()
           
    def onNewFile(self):
        """Create a blank new file."""
        self.createTab()
  
    def onOpen(self):
        """Open a new file."""
        ftypes = [('Python files', '*.py'), ('all files', '*')]
        file = filedialog.askopenfilename(filetypes = ftypes)
        try:
            text = self.readFile(file)
        except:
            print('file {} not found'.format(file))
            return
        name = str(file.split('/')[-1])
        if len(name) > 10:
            name = name[:8] + '..'
        else:
            name = name + ' '*(10 - len(name))
        #deletes current_tab if it is empty
        current_tab = self.notebook.children[(self.notebook.select().split('.')[3])]
        test_text = current_tab.getText()
        if test_text == '\n':
            current_tab.destroy()
        if str(file)[-3:] != '.py':
            new_tab = self.createTab(tab_name=name, file_name=file, highlight=False)
        else:
            new_tab = self.createTab(tab_name=name, file_name=file, highlight=True)
        new_tab.insertText(text)
        new_tab.highlight_all()
       
    def onSave(self):
        """Saves the text in the current tab."""
        current_tab = self.notebook.children[(self.notebook.select().split('.')[3])]
        if current_tab.getFileName() == None:
            self.onSaveAs()
        else:
            text = current_tab.getText()
            f = open(current_tab.getFileName(), 'w')
            f.write(text)
            f.close()
            current_tab.change_saved()
        
    def onSaveAs(self):
        """Choose a directory to save the file."""
        current_tab = self.notebook.children[(self.notebook.select().split('.')[3])]
        text = current_tab.getText()
        #Open window to save
        ftypes = [("Python file","*.py"), ('all files', '*')]
        file_name = filedialog.asksaveasfilename(filetypes = ftypes)
        #Update the tab file name
        current_tab.setFileName(file_name)
        current_tab.change_saved()
        #Write the text in a new file
        f = open(file_name, 'w')
        f.write(text)
        f.close()
        
    def onClose(self):
        """
        Closes the current tab
        Pops a warning window if the tab has not been saved
        """
        current_tab = self.notebook.children[(self.notebook.select().split('.')[3])]
        if current_tab.isSaved():
            current_tab.destroy()
        else:
            #pops a warning window
            var = messagebox.askyesno('Question', 'Do you want to save the file before closing?',
                                      icon=messagebox.QUESTION)
            if var:
                self.onSave()
                current_tab.destroy()
            else:
                current_tab.destroy()
            
    def onExit(self):
        """
        exit the application
        asks in case not all files are saved
        """               
        for tab in self.notebook.tabs():
            tab_frame = self.notebook.children[(tab.split('.')[3])]
            if not tab_frame.isSaved():        
                #pops a warning window
                var = messagebox.askyesno('Warning', 'Not all files were saved. Are you sure you want to exit?',
                                          icon=messagebox.WARNING)
                if var:
                    self.master.destroy()
                    return
                else:
                    return
        self.master.destroy()
        
    def onUndo(self):
        """Undo the last edit."""
        current_tab = self.notebook.children[(self.notebook.select().split('.')[3])]
        current_tab.undo()
    
    def onRedo(self):
        """Redo the last edit."""
        current_tab = self.notebook.children[(self.notebook.select().split('.')[3])]
        current_tab.redo()
        
    def onCut(self):
        """Cut the selected text."""
        current_tab = self.notebook.children[(self.notebook.select().split('.')[3])]
        current_tab.cut()
        
    def onCopy(self):
        """Copy selected text."""
        current_tab = self.notebook.children[(self.notebook.select().split('.')[3])]
        current_tab.copy()
        
    def onPaste(self):
        """paste selected text"""
        current_tab = self.notebook.children[(self.notebook.select().split('.')[3])]
        current_tab.paste()

    def changeName(self):
        """pops a window and change the current tab name"""
        new_window = Toplevel(self.master, height=100, width=300, takefocus=True)
        new_window.resizable(False, False)

        frame = Frame(new_window, padx=5, pady=5)
        frame.pack()

        label = Label(frame, text='Enter the new tab name', padx=10, pady=10)
        label.grid(row=2, column=1, rowspan=2, columnspan=5)

        name_entry = Entry(frame, width=20)
        name_entry.grid(row=4, column=1, rowspan=2, columnspan=5)
        name_entry.focus_set()

        CancelButton = Button(frame, text='Cancel', command=lambda: self.closeWidget(new_window), width=10, padx=5)
        OkButton = Button(frame, text='Ok', command=lambda: self.changeTabName(name_entry.get(), new_window), width=10, padx=5)
        CancelButton.grid(row=7, column=4, columnspan=2)
        OkButton.grid(row=7, column=2, columnspan=2)

    def onEnableHighlight(self):
        """enable python text highlight if it is currently disabled"""
        current_tab = self.notebook.children[(self.notebook.select().split('.')[3])]
        if not current_tab.isHighlighted():
            current_tab.change_highlight()
            current_tab.highlight_all()
        
    def onDisableHighlight(self):
        """disable python text highlight if it is currently enabled"""
        current_tab = self.notebook.children[(self.notebook.select().split('.')[3])]
        if current_tab.isHighlighted():
            current_tab.change_highlight()
            current_tab.disable_highlight()

    #still not implemented
    def onChooseFontColors(self):
        pass
            
class Tab(Frame):
    """
    tabs to manage different text files
    
    self.master = Application notebook
    self.file_name = the current file name for the text
    self.text = the main text widget
    self.label = the line display on the botton of the widget
    self.saved = True if the text has been saved
                 False otherwise
    self.highlight = True if the text is highlighted for python,
                     False otherwise
    KW = Python keywords list, used to highlight the text
    BUILTIN = Python builtin words list, used to highlight  the text
    """
    
    KW = keyword.kwlist
    BUILTIN = ['abs', 'all', 'any', 'basestring', 'bin', 'bool', 'bytearray',
               'callable', 'chr', 'classmethod', 'cmp', 'compile', 'complex',
               'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'execfile',
               'file', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals',
               'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance',
               'issubclass', 'iter', 'len', 'list', 'locals', 'long', 'map', 'max',
               'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow',
               'print', 'property', 'range', 'reduce', 'reload', 'repr', 'reversed',
               'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str',
               'sum', 'super', 'tuple', 'type', 'unichr', 'unicode', 'vars', 'xrange',
               'zip', '__import__']
    
    def __init__(self, master, file_name=None, highlight=True):
        Frame.__init__(self, master)
        self.master = master
        self.file_name = file_name
        self.saved = True
        self.highlight = highlight
        self.text_frame = Frame(self)
        self.text_frame.pack(side=TOP, fill=BOTH, expand=1)
        self.text = Text(self.text_frame)
        self.text.config(autoseparators=True, wrap=NONE, tabs='1c')
        self.text.pack(side=LEFT, fill=BOTH, expand=1, padx=5, pady=5)
        self.text.focus_set()
        #Add scrollbar to the text
        scrollbar = Scrollbar(self.text_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text.yview)
        #Add line and column indexes at the bottom
        index = self.text.index('insert').split('.')
        line_display = Frame(self, height = 10)
        line_display.pack(side=BOTTOM, fill=X)
        self.label = Label(line_display, text='Line: {}  Column: {}   '.format(index[0], index[1]))
        self.label.pack(side=RIGHT)

        self.text.event_add('<<update_highlight>>', '<KeyRelease>', '<Button-1>')
        self.text.bind('<<update_highlight>>', self.highlight_n_update)
        self.text.bind('<Button-3>', self.doPopup)
        self.text.bind('<Key>', self.change_not_saved)
        self.text.bind('<Tab>', self.set_tab)
        
        self.popup_menu = Menu(self, tearoff=0)
        self.popup_menu.add_command(label='Undo       ', command=self.undo)
        self.popup_menu.add_command(label='Redo       ', command=self.redo)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label='Cut        ', command=self.cut, state='disable')
        self.popup_menu.add_command(label='Copy       ', command=self.copy, state='disable')
        self.popup_menu.add_command(label='Paste      ', command=self.paste, state='disable')

        self.text.tag_config('kw', foreground='orange')
        self.text.tag_config('builtin', foreground='purple')
        self.text.tag_config('funcs', foreground='blue')
        self.text.tag_config('strings',  foreground='green')
        self.text.tag_config('comment', foreground='red')

    def set_tab(self, event=None):
        """tab key adds four space characters to the text"""
        index = self.text.index('insert')
        self.text.insert(index, '    ')
        return 'break'  #default behavior of Tab key doesn't happen    

    def highlight_all(self):
        """highlight all lines when a new .py file is opened"""
        if self.highlight:
            lines = self.text.index('end').split('.')[0]
            for line in range(int(lines)):
                self.highlight_n_update(cline=str(line))

    def disable_highlight(self):
        """remove all the text highlight"""
        if not self.highlight:
            self.text.tag_remove('kw', '1.0', 'end')
            self.text.tag_remove('builtin', '1.0', 'end')
            self.text.tag_remove('comment', '1.0', 'end')
            self.text.tag_remove('funcs', '1.0', 'end')
            self.text.tag_remove('strings', '1.0', 'end')
            
    def highlight_n_update(self, event=None, cline=None):
        """
        highlight text every time a key is pressed
        for keywords, highlight orange
        for builtin, highlight purple
        for comments, highlight red
        for strings, highlight green

        update the line and column display in the bottom
        """
        #line display
        index = self.text.index('insert').split('.')
        self.label.config(text='Line: {}  Column: {}   '.format(index[0], index[1]))

        if not self.highlight:
            return     # exit function if highlight option is disabled
        if cline == None:
            cline = self.text.index('insert').split('.')[0]
        line_start = '%s.0' %cline
        line_end = '%s.end' %cline
        
        self.text.tag_remove('kw', line_start, line_end)
        self.text.tag_remove('builtin', line_start, line_end)
        self.text.tag_remove('comment', line_start, line_end)
        self.text.tag_remove('funcs', line_start, line_end)
        self.text.tag_remove('strings', line_start, line_end)

        text = self.text.get(line_start, line_end)   
        #string green highlight and comment red highlight
        if '"' in text or "'" in text or '#' in text:
            L = []
            string1_mode = False    #string with single quotation
            string2_mode = False    #string with double quotation
            char = ''
            count_comment = 0
            for e in text:
                char += e
                if e == "'":
                    if not string1_mode and not string2_mode:
                        string1_mode = True
                        L.append(char[:-1])
                        char = ''
                    elif string1_mode and not string2_mode:
                        string1_mode = False
                        L.append("'" + char)
                        char = ''
                    else: pass
                elif e == '"':
                    if not string2_mode and not string1_mode:
                        string2_mode = True
                        L.append(char[:-1])
                        char = ''
                    elif string2_mode and not string1_mode:
                        string2_mode = False
                        L.append('"' + char)
                        char = ''
                    else: pass
                #comment highlight
                elif e == '#':
                    count_comment += 1
                    if not string1_mode and not string2_mode:
                        before_comment = '#'.join(text.split('#')[0:count_comment])
                        start = len(before_comment)
                        self.text.tag_add('comment', '%s.%d'%(cline, start), line_end)
                        break
            if string1_mode: L.append(char + "'")
            elif string2_mode: L.append(char + '"')
            start, end = 0, 0
            for i in range(len(L)):
                end = start + len(L[i])
                if not i%2 == 0:
                    self.text.tag_add('strings', '%s.%d'%(cline, start), '%s.%d'%(cline, end))
                start = end
                
        #Don't bother trying to highlight line after comment
        try:
            if before_comment.count("'")%2 == 0 and before_comment.count('"')%2 == 0:
                text = before_comment
        except UnboundLocalError: pass
        words = text.split(' ')
        start, end = 0, 0
        previous_word = ''
        for word in words:
            end = start + len(word)
            #funcs blue highlight
            if previous_word == 'class' or previous_word == 'def':
                has_punctuation = False
                for i in range(len(word)):
                    if word[i] in punctuation and not word[i] == '_':
                        has_punctuation = True
                        break
                if has_punctuation:
                    self.text.tag_add('funcs', '%s.%d'%(cline, start), '%s.%d'%(cline, start + i))
                else:
                    self.text.tag_add('funcs', '%s.%d'%(cline, start), '%s.%d'%(cline, end))
            #keywords orange highlight
            elif word in self.KW:
                self.text.tag_add('kw', '%s.%d'%(cline, start), '%s.%d'%(cline, end))
            #builtin purple highlight
            else:
                separated_words = word.split('(')
                sep_start = start
                for sep_word in separated_words:
                    sep_end = sep_start + len(sep_word)
                    if sep_word in self.BUILTIN:
                        self.text.tag_add('builtin', '%s.%d'%(cline, sep_start), '%s.%d'%(cline, sep_end))
                    sep_start = sep_end + 1
            previous_word = word
            start += len(word) + 1

    def test_disable_enable(self):
        """tests to see if some menu options should be
        disabled or enabled
        """
        try:
            test = self.text.get('sel.first', 'sel.last')
            self.popup_menu.entryconfig('Cut        ', state='normal')
            self.popup_menu.entryconfig('Copy       ', state='normal')
        except:
            self.popup_menu.entryconfig('Cut        ', state='disable')
            self.popup_menu.entryconfig('Copy       ', state='disable')
        try:
            test = self.selection_get(selection='CLIPBOARD')
            self.popup_menu.entryconfig('Paste      ', state='normal')
        except:
            self.popup_menu.entryconfig('Paste      ', state='disable')
        
    def doPopup(self, event=None):
       """pops the popup menu"""
       self.test_disable_enable()
       time.sleep(0.1)
       try:
           self.popup_menu.tk_popup(event.x_root, event.y_root)
       finally:
           self.popup_menu.grab_release()
    
    def insertText(self, text):
        """insert text in the text tab. Does not overwright old text."""
        self.text.insert(END, text)

    def getText(self):
        """return the text on self text"""
        return self.text.get('1.0', END)

    def getFileName(self):
        """return the file name of the tab"""
        return self.file_name

    def setFileName(self, file):
        """set a new name to the tab file name"""
        self.file_name = file

    def setName(self, name):
        """set a new name to the tab, name is a string"""
        assert type(name) == str
        self.name = name

    def isSaved(self):
        """return True if the file is saved, return False otherwise"""
        return self.saved

    def isHighlighted(self):
        """return True if the text is highlighted for python"""
        return self.highlight

    def change_highlight(self):
        """set self.highlight to True if self.highlight is False
        set self.highlight to False if self.highlight is True
        """
        if self.highlight:
            self.highlight = False
        else:
            self.highlight = True
        
    def undo(self):
        """undo command."""
        try: self.text.edit_undo()
        except: pass
        
    def redo(self):
        """redo command."""
        try: self.text.edit_redo()
        except: pass

    def copy(self):
        """copy command."""
        self.clipboard_clear()
        text = self.text.get('sel.first', 'sel.last')
        self.clipboard_append(text)

    def cut(self):
        """cut command."""
        self.copy()
        self.text.delete('sel.first', 'sel.last')

    def paste(self):
        """paste command."""
        text = self.selection_get(selection='CLIPBOARD')
        self.text.insert('insert', text)

    def change_saved(self, event=None):
        """
        Get's activated when the user saves the file
        change the self.saved from False to True.
        """
        self.saved = True

    def change_not_saved(self, event=None):
        """
        Get's activated when the user press a key in the text widget
        change the self.saved from True to False
        """
        self.saved = False 

        
def main():
    root = Tk()
    App = Application(root)
    x = 100
    y = 50
    #root.iconbitmap('shark.ico')
    root.geometry("+{}+{}".format(x, y))
    root.mainloop()
    
if __name__ == '__main__':
    main()
