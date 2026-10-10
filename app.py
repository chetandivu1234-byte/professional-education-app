from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle
from kivy.core.audio import SoundLoader

import os

# -------------------------------------------------------------
# Theme
# -------------------------------------------------------------
APP_BG = (0.04, 0.07, 0.12, 1.0)
CARD_BG = (0.11, 0.17, 0.24, 1.0)
CARD_BG_2 = (0.15, 0.22, 0.30, 1.0)
SURFACE = (0.20, 0.27, 0.38, 1.0)
ACCENT = (0.11, 0.78, 0.76, 1.0)
ACCENT_2 = (0.59, 0.76, 1.0, 1.0)
ACCENT_3 = (0.98, 0.72, 0.28, 1.0)
ACCENT_4 = (0.98, 0.42, 0.39, 1.0)
TEXT = (0.96, 0.98, 1.0, 1.0)
TEXT_MUTED = (0.74, 0.80, 0.86, 1.0)

# -------------------------------------------------------------
# Utility
# -------------------------------------------------------------
def play_sound(name='click'):
    try:
        sound_dir = os.path.join(os.getcwd(), 'Assets', 'Sounds')
        candidates = [
            os.path.join(sound_dir, f'{name}.wav'),
            os.path.join(sound_dir, f'{name}.ogg'),
            os.path.join(sound_dir, f'{name}.mp3'),
        ]
        for path in candidates:
            if os.path.exists(path):
                sound = SoundLoader.load(path)
                if sound:
                    sound.play()
                return
    except Exception:
        pass


class HeaderBar(BoxLayout):
    def __init__(self, title, show_back=False, back_action=None, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=58, spacing=12, **kwargs)

        if show_back:
            back_btn = Button(
                text='<',
                bold=True,
                background_normal='',
                background_down='',
                background_color=(0.15, 0.21, 0.28, 1.0),
                color=TEXT,
                size_hint=(None, None),
                width=42,
                height=42,
            )
            with back_btn.canvas.before:
                Color(0.15, 0.21, 0.28, 1.0)
                back_btn.bg = RoundedRectangle(pos=back_btn.pos, size=back_btn.size, radius=[16])
            back_btn.bind(pos=lambda i, v: setattr(back_btn.bg, 'pos', v),
                          size=lambda i, v: setattr(back_btn.bg, 'size', v))
            if back_action:
                back_btn.bind(on_release=back_action)
            self.add_widget(back_btn)
        else:
            self.add_widget(BoxLayout(size_hint_x=None, width=42))

        title_label = Label(
            text=title,
            bold=True,
            color=TEXT,
            font_size='22sp',
            halign='center',
            valign='middle',
            size_hint_x=1,
        )
        title_label.bind(size=title_label.setter('text_size'))
        self.add_widget(title_label)

        self.add_widget(BoxLayout(size_hint_x=None, width=42))


class ModernCard(ButtonBehavior, BoxLayout):
    def __init__(self, title, subtitle='', icon='★', accent=ACCENT, callback=None, size=(170, 120), **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=[18, 14, 18, 14], **kwargs)
        self.size_hint = (None, None)
        self.size = size
        self.callback = callback

        with self.canvas.before:
            Color(*CARD_BG)
            self.background = RoundedRectangle(pos=self.pos, size=self.size, radius=[18])
        self.bind(pos=self._update_bg, size=self._update_bg)

        top = BoxLayout(size_hint_y=None, height=40)
        icon_label = Label(text=icon, font_size='26sp', color=TEXT, bold=True, size_hint_x=None, width=46)
        top.add_widget(icon_label)

        accent_box = BoxLayout(size_hint_x=1)
        with accent_box.canvas.before:
            Color(*accent)
            accent_box.bg = RoundedRectangle(pos=accent_box.pos, size=accent_box.size, radius=[12])
        accent_box.bind(pos=lambda i, v: setattr(accent_box.bg, 'pos', v),
                        size=lambda i, v: setattr(accent_box.bg, 'size', v))
        top.add_widget(accent_box)
        self.add_widget(top)

        title_label = Label(text=title, color=TEXT, bold=True, font_size='17sp', halign='left', valign='middle', size_hint_y=None, height=24)
        title_label.bind(size=title_label.setter('text_size'))
        self.add_widget(title_label)

        if subtitle:
            sub_label = Label(text=subtitle, color=TEXT_MUTED, font_size='12sp', halign='left', valign='middle', size_hint_y=None, height=18)
            sub_label.bind(size=sub_label.setter('text_size'))
            self.add_widget(sub_label)

    def _update_bg(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size

    def on_release(self):
        play_sound('click')
        if self.callback:
            self.callback(self)


class SettingRow(BoxLayout):
    def __init__(self, title, subtitle='', switch_value=False, callback=None, **kwargs):
        super().__init__(orientation='horizontal', spacing=12, padding=[18, 10, 18, 10], **kwargs)
        self.size_hint_y = None
        self.height = 72

        with self.canvas.before:
            Color(*CARD_BG_2)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[16])
        self.bind(pos=self._update_bg, size=self._update_bg)

        left = BoxLayout(orientation='vertical', size_hint_x=1, spacing=2)
        left.add_widget(Label(text=title, color=TEXT, bold=True, font_size='17sp'))
        if subtitle:
            left.add_widget(Label(text=subtitle, color=TEXT_MUTED, font_size='12sp'))
        self.add_widget(left)

        sw = Switch(active=switch_value)
        sw.size_hint = (None, None)
        sw.size = (56, 36)
        if callback:
            sw.bind(active=callback)
        self.add_widget(sw)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


# -------------------------------------------------------------
# Screens
# -------------------------------------------------------------
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=[20, 18, 20, 18], spacing=18)
        with root.canvas.before:
            Color(*APP_BG)
            root.bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda i, v: setattr(root.bg, 'pos', v),
                  size=lambda i, v: setattr(root.bg, 'size', v))

        root.add_widget(HeaderBar('StudyHub'))

        search = TextInput(
            hint_text='Search courses, books, lessons...',
            multiline=False,
            size_hint_y=None,
            height=52,
            foreground_color=TEXT,
            background_color=(0.11, 0.17, 0.24, 1.0),
            padding=[16, 12],
            cursor_color=ACCENT,
        )
        root.add_widget(search)

        feature_row = GridLayout(cols=2, spacing=16, size_hint_y=None)
        feature_row.bind(minimum_height=feature_row.setter('height'))
        cards = [
            ('My Courses', '12 active', '📘', ACCENT, self.open_board),
            ('Progress', '86% complete', '📊', ACCENT_2, self.open_dashboard),
            ('Schedule', 'Today plan', '🗓️', ACCENT_3, self.open_dashboard),
            ('Rewards', '7 badges', '🏆', ACCENT_4, self.open_profile),
        ]
        for title, subtitle, icon, accent, cb in cards:
            feature_row.add_widget(ModernCard(title, subtitle, icon, accent, callback=cb, size=(160, 120)))
        root.add_widget(feature_row)

        section = Label(text='Explore Learning', bold=True, color=TEXT, font_size='20sp', size_hint_y=None, height=30, halign='left')
        section.bind(size=section.setter('text_size'))
        root.add_widget(section)

        explore = GridLayout(cols=2, spacing=16, size_hint_y=None)
        explore.bind(minimum_height=explore.setter('height'))
        extras = [
            ('Board', 'CBSE / ICSE / IB', '🎓', ACCENT, lambda *_: self.manager.current = 'board'),
            ('Subjects', 'Math, science, art', '🧠', ACCENT_2, lambda *_: self.manager.current = 'subject'),
            ('Library', 'Books + resources', '📚', ACCENT_3, lambda *_: self.manager.current = 'books'),
            ('Settings', 'App preferences', '⚙️', ACCENT_4, lambda *_: self.manager.current = 'settings'),
        ]
        for title, subtitle, icon, accent, cb in extras:
            explore.add_widget(ModernCard(title, subtitle, icon, accent, callback=cb, size=(160, 120)))
        root.add_widget(explore)

        self.add_widget(root)

    def open_board(self, *_args):
        self.manager.current = 'board'

    def open_dashboard(self, *_args):
        self.manager.current = 'dashboard'

    def open_profile(self, *_args):
        self.manager.current = 'profile'


class BoardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=[20, 18, 20, 18], spacing=18)
        with root.canvas.before:
            Color(*APP_BG)
            root.bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda i, v: setattr(root.bg, 'pos', v),
                  size=lambda i, v: setattr(root.bg, 'size', v))

        root.add_widget(HeaderBar('Choose Board', show_back=True, back_action=lambda *_: self.manager.current = 'home'))

        grid = GridLayout(cols=2, spacing=16, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        boards = [
            ('CBSE', 'National curriculum', 'C', ACCENT),
            ('ICSE', 'Balanced learning', 'I', ACCENT_2),
            ('State Board', 'Regional syllabus', 'S', ACCENT_3),
            ('NIOS', 'Flexible learning', 'N', ACCENT_4),
            ('IB', 'Global focus', 'B', (0.51, 0.70, 1.0, 1.0)),
            ('International', 'World curriculum', 'W', (0.76, 0.52, 1.0, 1.0)),
        ]
        for title, subtitle, icon, color in boards:
            grid.add_widget(ModernCard(title, subtitle, icon, color, callback=lambda _c, t=title: self.select_board(t), size=(160, 120)))
        root.add_widget(grid)
        self.add_widget(root)

    def select_board(self, board_name):
        self.manager.board_name = board_name
        self.manager.current = 'class'


class ClassScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=[20, 18, 20, 18], spacing=18)
        with root.canvas.before:
            Color(*APP_BG)
            root.bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda i, v: setattr(root.bg, 'pos', v),
                  size=lambda i, v: setattr(root.bg, 'size', v))

        root.add_widget(HeaderBar('Choose Class', show_back=True, back_action=lambda *_: self.manager.current = 'board'))

        grid = GridLayout(cols=3, spacing=16, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        for i in range(1, 13):
            color = (0.12 + (i % 6) * 0.08, 0.20 + (i % 4) * 0.06, 0.28, 1.0)
            grid.add_widget(ModernCard(f'Class {i}', 'Academic year', str(i), color, callback=lambda _c, n=i: self.select_class(n), size=(110, 110)))
        root.add_widget(grid)
        self.add_widget(root)

    def select_class(self, class_number):
        self.manager.class_name = class_number
        self.manager.current = 'subject'


class SubjectScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subjects = ['Mathematics', 'Science', 'English', 'Hindi', 'Social Studies', 'Computer Science', 'Arts', 'Sports']

        root = BoxLayout(orientation='vertical', padding=[20, 18, 20, 18], spacing=18)
        with root.canvas.before:
            Color(*APP_BG)
            root.bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda i, v: setattr(root.bg, 'pos', v),
                  size=lambda i, v: setattr(root.bg, 'size', v))

        root.add_widget(HeaderBar('Choose Subject', show_back=True, back_action=lambda *_: self.manager.current = 'class'))

        grid = GridLayout(cols=2, spacing=16, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        for idx, subject in enumerate(self.subjects):
            accent = [ACCENT, ACCENT_2, ACCENT_3, ACCENT_4][idx % 4]
            grid.add_widget(ModernCard(subject, 'Study material', subject[:2].upper(), accent, callback=lambda _c, s=subject: self.select_subject(s), size=(160, 120)))
        root.add_widget(grid)
        self.add_widget(root)

    def select_subject(self, subject_name):
        self.manager.subject_name = subject_name
        self.manager.current = 'books'


class BooksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=[20, 18, 20, 18], spacing=18)
        with root.canvas.before:
            Color(*APP_BG)
            root.bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda i, v: setattr(root.bg, 'pos', v),
                  size=lambda i, v: setattr(root.bg, 'size', v))

        root.add_widget(HeaderBar('Books & Resources', show_back=True, back_action=lambda *_: self.manager.current = 'subject'))

        grid = GridLayout(cols=2, spacing=16, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        books = [
            ('Mathematics Mastery', 'Textbook', '📘', ACCENT),
            ('Science Explorer', 'Practical guide', '🔬', ACCENT_2),
            ('English Reader', 'Literature', '📖', ACCENT_3),
            ('Question Bank', 'MCQs + notes', '📝', ACCENT_4),
            ('Quick Revision', 'Summary', '⚡', (0.62, 0.78, 1.0, 1.0)),
            ('Mock Test Prep', 'Practice', '✅', (0.81, 0.59, 1.0, 1.0)),
        ]
        for title, subtitle, icon, color in books:
            grid.add_widget(ModernCard(title, subtitle, icon, color, callback=lambda _c, t=title: self.open_book(t), size=(160, 140)))
        root.add_widget(grid)
        self.add_widget(root)

    def open_book(self, book_name):
        self.manager.selected_book = book_name
        self.manager.current = 'reader'


class ReaderScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=[20, 16, 20, 16], spacing=10)
        with root.canvas.before:
            Color(*APP_BG)
            root.bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda i, v: setattr(root.bg, 'pos', v),
                  size=lambda i, v: setattr(root.bg, 'size', v))

        root.add_widget(HeaderBar('Reader', show_back=True, back_action=lambda *_: self.manager.current = 'books'))

        title = Label(text='Mathematics Mastery', bold=True, color=TEXT, font_size='20sp', halign='center', size_hint_y=None, height=30)
        title.bind(size=title.setter('text_size'))
        root.add_widget(title)

        page_panel = BoxLayout(orientation='vertical', padding=[18, 14, 18, 14], size_hint=(1, 1))
        with page_panel.canvas.before:
            Color(*CARD_BG_2)
            page_panel.bg = RoundedRectangle(pos=page_panel.pos, size=page_panel.size, radius=[20])
        page_panel.bind(pos=lambda i, v: setattr(page_panel.bg, 'pos', v),
                        size=lambda i, v: setattr(page_panel.bg, 'size', v))

        page_text = Label(
            text='Page 04\n\nChapter 1: Number Patterns\n\nThe purpose of mathematics is not just to solve problems, but to understand structure, patterns, and logic.',
            color=TEXT,
            font_size='18sp',
            halign='center',
            valign='middle',
            text_size=(self.width, None),
        )
        page_panel.add_widget(page_text)
        root.add_widget(page_panel)

        nav = BoxLayout(size_hint_y=None, height=52, spacing=14)
        prev = Button(text='Previous', background_normal='', background_down='', background_color=ACCENT, color=(0, 0, 0, 1), bold=True)
        prev.bind(on_release=lambda *_: play_sound('click'))
        nxt = Button(text='Next', background_normal='', background_down='', background_color=ACCENT_2, color=(0, 0, 0, 1), bold=True)
        nxt.bind(on_release=lambda *_: play_sound('click'))
        nav.add_widget(prev)
        nav.add_widget(nxt)
        root.add_widget(nav)

        self.add_widget(root)


class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=[20, 18, 20, 18], spacing=18)
        with root.canvas.before:
            Color(*APP_BG)
            root.bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda i, v: setattr(root.bg, 'pos', v),
                  size=lambda i, v: setattr(root.bg, 'size', v))

        root.add_widget(HeaderBar('Dashboard', show_back=True, back_action=lambda *_: self.manager.current = 'home'))

        stat_row = GridLayout(cols=2, spacing=16, size_hint_y=None)
        stat_row.bind(minimum_height=stat_row.setter('height'))
        stat_row.add_widget(ModernCard('Courses', '12 active', '📘', ACCENT, size=(160, 120)))
        stat_row.add_widget(ModernCard('Study Time', '4.5 hrs', '⏱️', ACCENT_2, size=(160, 120)))
        stat_row.add_widget(ModernCard('Quiz Score', '92%', '✅', ACCENT_3, size=(160, 120)))
        stat_row.add_widget(ModernCard('Streak', '18 days', '🔥', ACCENT_4, size=(160, 120)))
        root.add_widget(stat_row)

        self.add_widget(root)


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=[20, 18, 20, 18], spacing=18)
        with root.canvas.before:
            Color(*APP_BG)
            root.bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda i, v: setattr(root.bg, 'pos', v),
                  size=lambda i, v: setattr(root.bg, 'size', v))

        root.add_widget(HeaderBar('Profile', show_back=True, back_action=lambda *_: self.manager.current = 'home'))

        profile = BoxLayout(orientation='vertical', padding=[16, 16, 16, 16], spacing=10, size_hint_y=None, height=150)
        with profile.canvas.before:
            Color(*CARD_BG_2)
            profile.bg = RoundedRectangle(pos=profile.pos, size=profile.size, radius=[18])
        profile.bind(pos=lambda i, v: setattr(profile.bg, 'pos', v),
                     size=lambda i, v: setattr(profile.bg, 'size', v))
        profile.add_widget(Label(text='Aanya Sharma', color=TEXT, bold=True, font_size='22sp'))
        profile.add_widget(Label(text='Class 10 • Biology', color=TEXT_MUTED, font_size='14sp'))
        profile.add_widget(Label(text='Level: Bronze Scholar', color=ACCENT, font_size='14sp'))
        root.add_widget(profile)

        info = GridLayout(cols=2, spacing=16, size_hint_y=None)
        info.bind(minimum_height=info.setter('height'))
        info.add_widget(ModernCard('Certificates', '5 earned', '🏅', ACCENT, size=(160, 120)))
        info.add_widget(ModernCard('Achievements', 'Top 10%', '🎯', ACCENT_2, size=(160, 120)))
        root.add_widget(info)

        self.add_widget(root)


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=[20, 18, 20, 18], spacing=18)
        with root.canvas.before:
            Color(*APP_BG)
            root.bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda i, v: setattr(root.bg, 'pos', v),
                  size=lambda i, v: setattr(root.bg, 'size', v))

        root.add_widget(HeaderBar('Settings', show_back=True, back_action=lambda *_: self.manager.current = 'home'))

        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', spacing=14, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        settings = [
            ('Sound Effects', 'Enable app sound', True, self.toggle_sound),
            ('Night Mode', 'Dark interface', True, self.toggle_night),
            ('Wi‑Fi Download', 'Download over Wi‑Fi only', True, self.toggle_download),
            ('Auto Save Notes', 'Keep notes automatically', True, self.toggle_notes),
            ('Study Reminders', 'Daily task reminders', True, self.toggle_reminders),
            ('Push Notifications', 'Exam and task alerts', True, self.toggle_push),
        ]

        for title, subtitle, value, callback in settings:
            content.add_widget(SettingRow(title, subtitle, switch_value=value, callback=callback))

        extra = BoxLayout(orientation='horizontal', spacing=16)
        extra.add_widget(ModernCard('Theme', 'Customize view', '🎨', ACCENT, size=(160, 110)))
        extra.add_widget(ModernCard('Backup', 'Cloud sync', '☁️', ACCENT_2, size=(160, 110)))
        content.add_widget(extra)

        scroll.add_widget(content)
        root.add_widget(scroll)
        self.add_widget(root)

    def toggle_sound(self, instance, value):
        if value:
            play_sound('click')

    def toggle_night(self, instance, value):
        pass

    def toggle_download(self, instance, value):
        pass

    def toggle_notes(self, instance, value):
        pass

    def toggle_reminders(self, instance, value):
        pass

    def toggle_push(self, instance, value):
        pass


class EducationApp(App):
    title = 'StudyHub Education'

    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(BoardScreen(name='board'))
        sm.add_widget(ClassScreen(name='class'))
        sm.add_widget(SubjectScreen(name='subject'))
        sm.add_widget(BooksScreen(name='books'))
        sm.add_widget(ReaderScreen(name='reader'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.current = 'home'
        return sm


if __name__ == '__main__':
    EducationApp().run()


