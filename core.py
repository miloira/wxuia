import re

import uiautomation as uia

from utils import set_clipboard_text, set_clipboard_file


class ProxySettingBackDialog:

    def __init__(self, parent: "ProxySettings"):
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


class ProxySettings:

    def __init__(self, parent: "WechatLogin"):
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
        return ProxySettingBackDialog(self)

    def close(self):
        self.click(self.close_button)


class WechatLogin:

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
        return ProxySettings(self)

    def show(self):
        return self.window_control.Show()

    def close(self):
        return self.click(self.close_button)


class WeChat:

    def __init__(self):
        self.window = uia.WindowControl(RegexName="[Weixin|微信]")
        self.search_edit = self.window.EditControl(Name="搜索")

    def send(self, who, content, msg_type):
        self.window.SetActive()
        self.search_edit.SendKeys(who)
        self.window.SendKeys("{Enter}")
        chat_edit = self.window.EditControl(Name=who)
        chat_edit.SendKeys("{Ctrl}a{Del}")

        if msg_type == "text":
            set_clipboard_text(content)
        elif msg_type in ["image", "video", "file"]:
            set_clipboard_file([content])

        chat_edit.SendKeys("{Ctrl}v")
        self.window.SendKeys("{Enter}")
        self.window.ListControl(Name="消息").GetChildren()

    def send_text(self, who, content):
        return self.send(who, content, "text")

    def send_typing_text(self, who, content, delay=0.01):
        self.window.SetActive()
        self.search_edit.SendKeys(who)
        self.window.SendKeys("{Enter}")
        chat_edit = self.window.EditControl(Name=who)
        chat_edit.SendKeys("{Ctrl}a{Del}")
        chat_edit.SendKeys(content, interval=delay)
        self.window.SendKeys("{Enter}")

    def send_image(self, who, image_path):
        return self.send(who, image_path, "image")

    def send_video(self, who, video_path):
        return self.send(who, video_path, "video")

    def send_file(self, who, file_path):
        return self.send(who, file_path, "file")

    def call(self, who, msg_type, members=None):
        self.window.SetActive()
        self.search_edit.SendKeys(who)
        self.window.SendKeys("{Enter}")
        tool_bar = self.window.ButtonControl(Name="发送(S)").GetParentControl().GetChildren()[0]
        if msg_type == "private_voice":
            tool_bar.ButtonControl(Name="语音聊天").Click()
        elif msg_type == "room_voice":
            tool_bar.ButtonControl(Name="多人通话").Click()
            select_group_members_window = self.window.WindowControl(Name="微信选择成员")
            select_member_text = select_group_members_window.TextControl(Name="选择成员")
            finish_button = select_member_text.GetParentControl().GetChildren()[-1]
            cancel_button = select_member_text.GetParentControl().GetChildren()[-2]

            checkbox_list = select_group_members_window.ListControl(Name="请勾选需要添加的联系人").GetChildren()
            for checkbox in checkbox_list:
                if checkbox.Name in members:
                    checkbox.Click()

            selected_members_text = select_member_text.GetParentControl().GetChildren()[-3]
            members_count = re.findall(r"已选择(\d+)个联系人", selected_members_text.Name)[0]
            if members_count > 1:
                finish_button.Click()
            else:
                raise Exception("至少选择2个联系人")
        elif msg_type == "video_live":
            tool_bar.ButtonControl(Name="视频号直播").Click()
        elif msg_type == "video":
            tool_bar.ButtonControl(Name="视频聊天").Click()

    def call_voice(self, contact):
        return self.call(contact, "voice")

    def call_video(self, contact):
        return self.call(contact, "video")

    def call_room_voice(self, room, members):
        return self.call(room, "room_voice", members)

    def call_video_live(self, room):
        return self.call(room, "video_live")


if __name__ == '__main__':
    # login_window = WechatLogin()
    # proxy_settings_window = login_window.open_proxy_settings()
    # proxy_settings_window.set_use_proxy(True)
    # proxy_settings_window.set_address("address")
    # proxy_settings_window.set_port("8080")
    # proxy_settings_window.set_account("account")
    # proxy_settings_window.set_passwprd("password")
    # proxy_settings_back_dialog = proxy_settings_window.back()
    # proxy_settings_back_dialog.not_save()

    wechat = WeChat()
    wechat.send_text("文件传输助手", "测试")
