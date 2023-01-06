import sys
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QHBoxLayout,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)
from time import sleep
from database import Database
from general import stat_list


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fire Emblem Child Calculator")
        self.new_window = 'main'
        self.boon = 'HP'
        self.bane = 'Str'
        self.gender = 'm'
        self.boba_error_message = None
        self.db = None
        self.give_kid = ''
        self.give_kid_pair = None
        self.find_max = ''
        self.find_max_unavailable = None
        self.margin = 0
        self.hp_weight = None
        self.str_weight = None
        self.mag_weight = None
        self.skl_weight = None
        self.spd_weight = None
        self.lck_weight = None
        self.def_weight = None
        self.res_weight = None
        self.tot_weight = None

        self.advance()

    def create_main_layout(self):
        self.resize(400, 150)
        self.center()
        main_text = QLabel()
        main_text.setText('Which game do you want to use?')

        select_game = QComboBox()
        select_game.addItems(['Fates', 'Awakening', 'Genealogy'])
        select_game.currentTextChanged.connect(self.set_window)
        self.new_window = select_game.itemText(0)
        select_game.setMaximumWidth(300)

        boon = QComboBox()
        boon.addItems(stat_list)
        boon.currentTextChanged.connect(self.set_boon)
        self.boon = boon.itemText(0)
        boon.setMaximumWidth(150)

        bane = QComboBox()
        bane.addItems(stat_list)
        bane.setCurrentIndex(1)
        bane.currentTextChanged.connect(self.set_bane)
        self.bane = bane.itemText(1)
        bane.setMaximumWidth(150)

        boon_bane = QHBoxLayout()
        boon_bane.addWidget(boon)
        boon_bane.addWidget(bane)

        gender = QComboBox()
        gender.addItems(['Male', 'Female'])
        gender.currentTextChanged.connect(self.set_gender)
        self.set_gender(gender.itemText(0))
        gender.setMaximumWidth(200)

        self.boba_error_message = QLabel()
        self.boba_error_message.setStyleSheet('color: red')

        confirm_button = QPushButton()
        confirm_button.setText('OK')
        confirm_button.clicked.connect(self.after_main)
        confirm_button.setMaximumWidth(200)

        layout = QVBoxLayout()

        widgets = [
            main_text,
            select_game,
            boon_bane,
            gender,
            self.boba_error_message,
            confirm_button
        ]

        for w in widgets:
            if isinstance(w, QHBoxLayout):
                layout.addLayout(w)
            else:
                layout.addWidget(w)

        return layout

    def create_fates_window(self):
        self.db = Database.load_file('fates_growths.txt', (self.boon, self.bane), self.gender)
        self.resize(800, 600)
        self.setWindowTitle('Fates Child Calculator')
        self.center()

        main_text = QLabel()
        main_text.setText('Fates Child Calculator')

        # give kid method
        give_kid_text = QLabel()
        give_kid_text.setText('Choose kid to view with chosen parent:')

        give_kid_kid = QComboBox()
        give_kid_kid.addItems(self.db.kids)
        self.give_kid = give_kid_kid.itemText(0)
        give_kid_kid.currentTextChanged.connect(self.set_give_kid)

        self.give_kid_pair = QComboBox()
        give_dad = self.db.char[self.give_kid]['base'].dad
        self.give_kid_pair.addItems(give_dad.pair)

        # find max method
        find_max_text = QLabel()
        find_max_text.setText('Choose kid to maximize stat growths:')

        find_max_kid = QComboBox()
        find_max_kid.addItems(self.db.kids)
        self.find_max = find_max_kid.itemText(0)
        find_max_kid.currentTextChanged.connect(self.set_find_max)

        self.find_max_unavailable = QListWidget()
        find_max_dad = self.db.char[self.find_max]['base'].dad
        self.find_max_unavailable.addItems(self.db.char[find_max_dad].pair)
        self.find_max_unavailable.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        find_max_margin = QSpinBox()
        find_max_margin.setRange(0, 20)
        self.margin = find_max_margin.value()
        find_max_margin.setPrefix('Margin: ')
        find_max_margin.valueChanged.connect(self.set_margin)

        self.hp_weight = QSpinBox()
        self.hp_weight.setRange(0, 3)
        self.hp_weight.setPrefix('HP weight: ')

        self.str_weight = QSpinBox()
        self.str_weight.setRange(0, 3)
        self.str_weight.setPrefix('Str weight: ')

        self.mag_weight = QSpinBox()
        self.mag_weight.setRange(0, 3)
        self.mag_weight.setPrefix('Mag weight: ')

        self.skl_weight = QSpinBox()
        self.skl_weight.setRange(0, 3)
        self.skl_weight.setPrefix('Skl weight: ')

        self.spd_weight = QSpinBox()
        self.spd_weight.setRange(0, 3)
        self.spd_weight.setPrefix('Spd weight: ')

        self.lck_weight = QSpinBox()
        self.lck_weight.setRange(0, 3)
        self.lck_weight.setPrefix('Lck weight: ')

        self.def_weight = QSpinBox()
        self.def_weight.setRange(0, 3)
        self.def_weight.setPrefix('Def weight: ')

        self.res_weight = QSpinBox()
        self.res_weight.setRange(0, 3)
        self.res_weight.setPrefix('Res weight: ')

        self.tot_weight = QSpinBox()
        self.tot_weight.setRange(0, 3)
        self.tot_weight.setPrefix('Tot weight: ')

        find_max_weights_left = QVBoxLayout()
        find_max_weights_left.addWidget(self.hp_weight)
        find_max_weights_left.addWidget(self.mag_weight)
        find_max_weights_left.addWidget(self.spd_weight)
        find_max_weights_left.addWidget(self.def_weight)

        find_max_weights_right = QVBoxLayout()
        find_max_weights_right.addWidget(self.str_weight)
        find_max_weights_right.addWidget(self.skl_weight)
        find_max_weights_right.addWidget(self.lck_weight)
        find_max_weights_right.addWidget(self.res_weight)

        find_max_weights = QHBoxLayout()
        find_max_weights.addLayout(find_max_weights_left)
        find_max_weights.addLayout(find_max_weights_right)

        # exit
        exit_button = QPushButton()
        exit_button.setText('Exit')
        exit_button.clicked.connect(self.return_to_main)

        give_kid_box = QVBoxLayout()
        give_kid_box.addWidget(give_kid_text)
        give_kid_box.addWidget(give_kid_kid)
        give_kid_box.addWidget(self.give_kid_pair)

        find_max_box = QVBoxLayout()
        find_max_box.addWidget(find_max_text)
        find_max_box.addWidget(find_max_kid)
        find_max_box.addWidget(self.find_max_unavailable)
        find_max_box.addWidget(find_max_margin)
        find_max_box.addLayout(find_max_weights)
        find_max_box.addWidget(self.tot_weight)

        data_boxes = QHBoxLayout()
        data_boxes.addLayout(give_kid_box)
        data_boxes.addLayout(find_max_box)

        widgets = [
            main_text,
            data_boxes,
            exit_button
        ]

        layout = QVBoxLayout()

        for w in widgets:
            if isinstance(w, QHBoxLayout):
                layout.addLayout(w)
            else:
                layout.addWidget(w)

        return layout

    def create_awakening_window(self):
        self.db = Database.load_file('awakening_growths.txt', (self.boon, self.bane), self.gender)
        self.resize(800, 600)
        self.setWindowTitle('Awakening Child Calculator')
        self.center()

        main_text = QLabel()
        main_text.setText('Awakening Gaming')

        exit_button = QPushButton()
        exit_button.setText('Exit')
        exit_button.clicked.connect(self.return_to_main)

        widgets = [
            main_text,
            exit_button
        ]

        layout = QVBoxLayout()

        for w in widgets:
            if isinstance(w, QHBoxLayout):
                layout.addLayout(w)
            else:
                layout.addWidget(w)

        return layout

    def set_window(self, new_window):
        self.new_window = new_window

    def set_boon(self, boon):
        self.boon = boon

    def set_bane(self, bane):
        self.bane = bane

    def set_gender(self, gender):
        if gender == 'Female':
            self.gender = 'f'
        elif gender == 'Male':
            self.gender = 'm'
        else:
            raise ValueError

    def set_give_kid(self, give_kid):
        self.give_kid = give_kid
        give_dad = self.db.char[self.give_kid]['base'].dad
        self.give_kid_pair.clear()
        self.give_kid_pair.addItems(self.db.char[give_dad].pair)

    def set_find_max(self, find_max):
        self.find_max = find_max
        self.find_max_unavailable.clear()
        find_max_dad = self.db.char[self.find_max]['base'].dad
        self.find_max_unavailable.addItems(self.db.char[find_max_dad].pair)

    def set_margin(self, margin):
        self.margin = margin

    def return_to_main(self):
        self.new_window = 'main'
        self.advance()

    def after_main(self):
        if self.boon == self.bane:
            self.boba_error_message.setText('Boon must be different from bane!')
        else:
            self.advance()

    def advance(self):
        if self.new_window == 'main':
            layout = self.create_main_layout()
        elif self.new_window == 'Fates':
            layout = self.create_fates_window()
        elif self.new_window == 'Awakening':
            layout = self.create_awakening_window()
        else:
            return

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def center(self):

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
