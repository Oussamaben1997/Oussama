from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import json
import os

# إعداد لون الخلفية
Window.clearcolor = (1, 1, 1, 1)

class OsamaApp(App):
    def build(self):
        self.data_file = "osama_final_build.json"
        main = BoxLayout(orientation='vertical', padding=[15, 10, 15, 10], spacing=12)
        
        # --- الصف الأول ---
        row1 = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height=110)
        self.price_in = self.create_input("price", row1)
        self.som_in = self.create_input("som", row1)
        self.dz_in = self.create_input("DZ", row1, readonly=True)
        main.add_widget(row1)

        # --- الصف الثاني ---
        row2 = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height=110)
        self.usdt_in = self.create_input("USDT", row2)
        self.dz_sell_in = self.create_input("DZ SELL", row2, readonly=True)
        main.add_widget(row2)

        # زر الحساب
        btn = Button(
            text="account", 
            size_hint_y=None, height=70, 
            background_color=(0.1, 0.5, 0.8, 1), 
            bold=True, font_size=24
        )
        btn.bind(on_press=self.run_dynamic_calculations)
        main.add_widget(btn)

        # --- الصف الثالث (المربع الكبير مع خاصية الإخفاء) ---
        self.row3 = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height=110)
        
        # المربع تم تكبيره هنا
        self.check_bottom = self.create_colored_checkbox(self.row3)
        
        self.dynamic_box = BoxLayout(orientation='horizontal', spacing=8)
        self.ex1_in = self.create_input("Buy (Div)", self.dynamic_box)
        self.ex2_in = self.create_input("Sell (Mult)", self.dynamic_box)
        
        self.row3.add_widget(self.dynamic_box)
        main.add_widget(self.row3)

        main.add_widget(Label(size_hint_y=1))
        
        self.load_all_data()
        self.toggle_inputs(self.check_bottom, self.check_bottom.active)
        
        return main

    def create_colored_checkbox(self, layout):
        # تكبير حجم الحاوية والمربع إلى 70x70
        cb_container = BoxLayout(size_hint=(None, None), size=(70, 70), pos_hint={'center_y': .4})
        cb = CheckBox(color=[0, 0, 0, 1], size_hint=(None, None), size=(70, 70))
        cb.bind(active=self.toggle_inputs)
        cb_container.add_widget(cb)
        layout.add_widget(cb_container)
        return cb

    def toggle_inputs(self, checkbox, value):
        with checkbox.canvas.before:
            if value:
                Color(1, 0, 0, 1) # أحمر
                self.dynamic_box.opacity = 1
                self.dynamic_box.disabled = False
            else:
                Color(1, 1, 1, 1) # أبيض
                self.dynamic_box.opacity = 0
                self.dynamic_box.disabled = True
            Rectangle(pos=checkbox.pos, size=checkbox.size)
        self.save_all_data()

    def create_input(self, label_text, layout, readonly=False):
        box = BoxLayout(orientation='vertical', spacing=2)
        lbl = Label(text=label_text, color=(0,0,0,1), bold=True, font_size=18, size_hint_y=None, height=35)
        box.add_widget(lbl)
        
        ti = TextInput(
            multiline=False, 
            readonly=readonly, 
            halign='center', 
            font_size=45, 
            padding=[2, 5, 2, 5],
            input_filter='float'
        )
        if readonly:
            ti.background_color = (0.95, 0.95, 1, 1)
        
        ti.bind(text=lambda instance, val: self.save_all_data())
        box.add_widget(ti)
        layout.add_widget(box)
        return ti

    def run_dynamic_calculations(self, instance):
        try:
            s = float(self.som_in.text or 0)
            p = float(self.price_in.text or 0)
            buy_val = float(self.ex1_in.text or 1)
            if buy_val != 0:
                self.dz_in.text = "{:.2f}".format((s * p) / buy_val)
            
            u = float(self.usdt_in.text or 0)
            sell_val = float(self.ex2_in.text or 1)
            self.dz_sell_in.text = "{:.2f}".format(u * sell_val)
            self.save_all_data()
        except:
            pass

    def save_all_data(self):
        data = {
            "price": self.price_in.text, "som": self.som_in.text, "dz": self.dz_in.text,
            "usdt": self.usdt_in.text, "dz_sell": self.dz_sell_in.text,
            "n1": self.ex1_in.text, "n2": self.ex2_in.text,
            "c_bottom": self.check_bottom.active
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f)

    def load_all_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    self.price_in.text = data.get("price", "")
                    self.som_in.text = data.get("som", "")
                    self.dz_in.text = data.get("dz", "")
                    self.usdt_in.text = data.get("usdt", "")
                    self.dz_sell_in.text = data.get("dz_sell", "")
                    self.ex1_in.text = data.get("n1", "240")
                    self.ex2_in.text = data.get("n2", "280")
                    self.check_bottom.active = data.get("c_bottom", False)
            except:
                pass

if __name__ == '__main__':
    OsamaApp().run()
      
