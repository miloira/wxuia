import uiautomation as uia


class ProxySettingBackDialogWindow:

    def __init__(self, parent: "ProxySettingsWindow"):
        self.parent = parent
        self.window_control = self.parent.window_control.WindowControl(Name="Weixin", ClassName="mmui::XDialog")
        self.save_button = self.window_control.ButtonControl(Name="保存")
        self.not_save_button = self.window_control.ButtonControl(Name="不保存")

    @property
    def content(self):
        return self.window_control.GroupControl().GetChildren()[0].Name

    def click(self, button_control):
        self.window_control.SetActive()
        button_control.Click()

    def save(self):
        self.click(self.save_button)

    def not_save(self):
        self.click(self.not_save_button)


class ProxySettingsWindow:

    def __init__(self, parent: "LoginWindow"):
        self.parent = parent
        self.window_control = self.parent.window_control
        self.tool_bar = self.parent.tool_bar
        self.back_button = self.tool_bar.ButtonControl(Name="返回")
        self.close_button = self.tool_bar.ButtonControl(Name="关闭")
        self.use_proxy_checkbox = self.window_control.CheckBoxControl(Name="使用代理")
        self.address_edit = self.window_control.EditControl(Name="地址")
        self.port_edit = self.window_control.EditControl(Name="端口")
        self.account_edit = self.window_control.EditControl(Name="账户")
        self.password_edit = self.window_control.EditControl(Name="密码")
        self.save_button = self.window_control.ButtonControl(Name="保存")

    def click(self, button_control):
        self.window_control.SetActive()
        button_control.Click()

    def set_use_proxy(self, status=False):
        toggle_state = self.use_proxy_checkbox.GetTogglePattern().ToggleState
        if status:
            if toggle_state == 0:
                self.use_proxy_checkbox.Click()
        else:
            if toggle_state == 1:
                self.use_proxy_checkbox.Click()

    def input_edit(self, edit_control, content):
        edit_control.Click()
        edit_control.SendKeys("{Ctrl}a{Del}")
        edit_control.SendKeys(content)

    def set_address(self, address):
        self.input_edit(self.address_edit, address)

    def set_port(self, port):
        self.input_edit(self.port_edit, port)

    def set_account(self, account):
        self.input_edit(self.account_edit, account)

    def set_passwprd(self, password):
        self.input_edit(self.password_edit, password)

    def save(self):
        self.click(self.save_button)

    def back(self):
        self.click(self.back_button)
        return ProxySettingBackDialogWindow(self)

    def close(self):
        self.click(self.close_button)


class LoginWindow:

    def __init__(self):
        self.window_control = uia.WindowControl(Name="微信", ClassName="mmui::LoginWindow")
        self.tool_bar = self.window_control.ToolBarControl(ClassName="mmui::TitleBar")
        self.close_button = self.tool_bar.ButtonControl(Name="关闭")
        self.proxy_settings_button = self.tool_bar.ButtonControl(Name="网络代理设置")
        self.current_account_text = self.window_control.TextControl(RegexName="当前登录用户.*?")
        self.login_button = self.window_control.ButtonControl(Name="登录")
        self.enter_wechat_button = self.window_control.ButtonControl(Name="进入微信")
        self.rescan_qrcode_button = self.window_control.ButtonControl(Name="重新扫码")
        self.switch_account_button = self.window_control.ButtonControl(Name="切换账号")
        self.only_transfer_files_button = self.window_control.ButtonControl(Name="仅传输文件")

    def click(self, button_control):
        self.window_control.SetActive()
        button_control.Click()

    def enter(self):
        return self.click(self.enter_wechat_button)

    def switch_account(self):
        return self.click(self.switch_account_button)

    def transfer_files(self):
        return self.click(self.only_transfer_files_button)

    def open_proxy_settings(self):
        self.click(self.proxy_settings_button)
        return ProxySettingsWindow(self)

    def show(self):
        return self.window_control.Show()

    def close(self):
        return self.click(self.close_button)


login_window = LoginWindow()
proxy_settings_window = login_window.open_proxy_settings()
proxy_settings_window.set_use_proxy(True)
proxy_settings_window.set_address("address")
proxy_settings_window.set_port("8080")
proxy_settings_window.set_account("account")
proxy_settings_window.set_passwprd("password")
proxy_settings_back_dialog = proxy_settings_window.back()
proxy_settings_back_dialog.not_save()
