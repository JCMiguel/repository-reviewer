import customtkinter as ctk
from .misc import StdoutRedirector


class LogsFrame(ctk.CTkFrame):
    PADX = 20
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.logs_lbl = ctk.CTkLabel(self, text="Results and logs", anchor="w", font=ctk.CTkFont(weight="bold"))
        self.logs_lbl.pack(side="top", padx=LogsFrame.PADX, pady=(10,0))
        self.logs_box = ctk.CTkTextbox(self, width=2000, height=150, activate_scrollbars=True)
        self.logs_box.pack(side="top", padx=LogsFrame.PADX, pady=(10, 20))
        self.logs_box.configure(state="disabled")
        self.show_logs_checkbox = None
        self.stdout_redirector = StdoutRedirector(self.logs_box)

    def Get_enabling_checkBox(self, parent) -> ctk.CTkCheckBox:
        if (self.show_logs_checkbox is None):
            self.show_logs_checkbox = ctk.CTkCheckBox(parent, text="Show results and logs", command=self._checkbox_event)
        if bool(self.grid_info()): # This method led to know if the widget is visible now and so then syncronise the checkbox
            self.show_logs_checkbox.select()
        return self.show_logs_checkbox

    def _checkbox_event(self):
        value = self.show_logs_checkbox.get()
        # Redirect the standar output between default stdout and self.logs_box
        self.stdout_redirector.enable( value )
        # Handle visibility on the front
        self.grid() if value else self.grid_remove()
        print("_checkbox_event( view_enabled={} )".format(value))
