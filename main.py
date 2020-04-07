from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.utils import get_color_from_hex
from RDS_connector import rds_connect_lsy
import pandas as pd
import numpy as np
from datetime import datetime

class LabelButton(ButtonBehavior, Label):
    pass
# we are screens
class LoginScreen(Screen): # if you want to call this class in loginscreen.kv use root instead of app
    pass
class SettingScreen(Screen):
    pass
class PersonalScreen(Screen):
    pass
class HomeScreen(Screen):
    pass
class VerificationScreen(Screen):
    pass
class DoctorScreen(Screen):
    pass
class VeriScreen(Screen):
    pass
class DocdiagScreen(Screen):
    pass
class DocemerScreen(Screen):
    pass
class PatdiagScreen(Screen):
    pass
class PatemerScreen(Screen):
    pass

# put GUI behind all these kind of class because main.kv need to call them.
GUI = Builder.load_file("main.kv") # display what you configure in main.kv, main.kv will be the self.root

class MainApp(App):
    def build(self):
        return GUI

    def change_screen(self, screen_name):
        # get the screen manager from the .kv file
        screen_manager = self.root.ids.screen_manager
        screen_manager.current = screen_name

    # prepare for personal screen
    def prepare_psn_screen(self):

        where = ''' '{}' '''.format(self.input_user_name)
        sql_txt = '''select * from user_info where name = ''' + where
        re = pd.read_sql_query(sql_txt, con=self.connector)
        # generate id
        if(re['id'].values[0] == None):
            id = ''
        else:
            id = re.iloc[0]['id']
        # id = re.iloc[0]['id']
        # generate gender
        '''if re['gender'].values[0] == None:
            print('yes')'''
        if(re['gender'].values[0] == None):
            self.gender = ''
        else:
            self.gender = re.iloc[0]['gender']
        # generate age
        '''if(re['birthday'].values[0] == None):
            self.age = ''
        else:
            self.age = str(date.today().year - re.iloc[0]['birthday'].year)'''
        if(re['birthday'].values[0] == None):
            self.birthday = ''
        else:
            self.birthday = re.iloc[0]['birthday']
        # generate address
        if(re['address'].values[0] == None):
            self.address = ''
        else:
            self.address = re.iloc[0]['address']
        # generate blood type
        if(re['blood_type'].values[0] == None):
            self.blood_type = ''
        else:
            self.blood_type = re.iloc[0]['blood_type']
        # generate penicillin allergy
        if(re['penicillin_allergy'].values[0] == None):
            self.pen_all = ''
        else:
            self.pen_all = re.iloc[0]['penicillin_allergy']
        # pass value to personalscreen.kv
        self.root.ids.personal_screen.ids.username_label.text = str(id) + '#' + str(self.input_user_name)
        self.root.ids.personal_screen.ids.gender_ti.text = self.gender
        self.root.ids.personal_screen.ids.age_ti.text = str(self.birthday)
        self.root.ids.personal_screen.ids.address_ti.text = self.address
        self.root.ids.personal_screen.ids.blood_ti.text = self.blood_type
        self.root.ids.personal_screen.ids.pen_it.text = self.pen_all

    # check if the user could login = submit
    def validate_user_name(self):

        input_user_name = self.root.ids.login_screen.ids.user_name_field.text
        input_pass_word = self.root.ids.login_screen.ids.pass_word_field.text
        self.input_user_name = input_user_name # assemble self.input_user_name

        # check if the input_user_name is null
        if input_user_name == '':
            self.root.ids.login_screen.ids.login_info_label.text = 'user name cannot be null'
            self.root.ids.login_screen.ids.login_info_label.color = get_color_from_hex("#ff0000")
            self.login_user = ''
            return self

        # query in the database
        cn = rds_connect_lsy()
        self.connector = cn.conn # assemble self.connector
        where = ''' '{}' '''.format(input_user_name)
        sql_txt = '''select password from user_info where name = ''' + where

        # check if there is no such user in the database
        if len(pd.read_sql_query(sql_txt, con=cn.conn).index) == 0:
            self.root.ids.login_screen.ids.login_info_label.text = 'no match username'
            self.root.ids.login_screen.ids.login_info_label.color = get_color_from_hex("#ff0000")
            cn.conn.commit()
            self.login_user = ''
            return self
        db_pass_word = pd.read_sql_query(sql_txt, con=cn.conn).iloc[0]['password']
        # check the password
        if db_pass_word != input_pass_word:
            self.root.ids.login_screen.ids.login_info_label.text = 'user name and password do not match'
            self.root.ids.login_screen.ids.login_info_label.color = get_color_from_hex("#ff0000")
            cn.conn.commit()
            self.login_user = ''
            return self
        # prepare for personal_screen
        else:
            print('right password')


        self.login_user = input_user_name
        self.prepare_psn_screen()
        self.change_screen('personal_screen')
        cn.conn.commit()

        return self

    def create_new_account(self):

        input_user_name = self.root.ids.login_screen.ids.user_name_field.text
        input_pass_word = self.root.ids.login_screen.ids.pass_word_field.text
        self.input_user_name = input_user_name # assemble self.input_user_name

        # check if the input_user_name is null
        if input_user_name == '':
            self.root.ids.login_screen.ids.login_info_label.text = 'user name cannot be null'
            self.root.ids.login_screen.ids.login_info_label.color = get_color_from_hex("#ff0000")
            self.login_user = ''
            return

        # check if the password is null
        if input_pass_word == '':
            self.root.ids.login_screen.ids.login_info_label.text = 'password cannot be null'
            self.root.ids.login_screen.ids.login_info_label.color = get_color_from_hex("#ff0000")
            self.login_user = ''
            return

        # connect to the database
        cn = rds_connect_lsy()
        self.connector = cn.conn # assemble self.connector
        # check if the new name is duplicated
        sql_txt = '''select name from user_info'''
        l = pd.read_sql_query(sql_txt, con=cn.conn)['name'].values
        if input_user_name in l:
            self.root.ids.login_screen.ids.login_info_label.text = 'this user name is existed, please change a new user name'
            self.root.ids.login_screen.ids.login_info_label.color = get_color_from_hex("#ff0000")
            print('this user name is existed, please change a new user name')
            self.login_user = ''
            cn.conn.commit()
            return

        # insert into AWS RDS
        cursor = cn.conn.cursor()
        sql_txt = "insert into user_info (name, password) values ('{}', '{}');".format(input_user_name, input_pass_word)
        cursor.execute(sql_txt)

        # login_user
        self.login_user = input_user_name

        # go to personal screen for detailed information
        self.prepare_psn_screen() # prepare for that screen first
        self.change_screen('personal_screen')
        cn.conn.commit()

        return

    # confirm user information in personal screen
    def confirm_user_info(self):

        # get value from personalscreen.kv
        id = int(self.root.ids.personal_screen.ids.username_label.text.split('#')[0])
        input_user_name = self.root.ids.personal_screen.ids.username_label.text.split('#')[1]
        gender = self.root.ids.personal_screen.ids.gender_ti.text
        # check datatime format
        try:
            datetime.strptime(self.root.ids.personal_screen.ids.age_ti.text, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            self.root.ids.personal_screen.ids.confirm_check_label.text = 'wrong birthday format: the right should be yyyy-mm-dd HH:MM:SS '
            self.root.ids.personal_screen.ids.confirm_check_label.color = get_color_from_hex("#ff0000")
            return
        birthday = datetime.strptime(self.root.ids.personal_screen.ids.age_ti.text, '%Y-%m-%d %H:%M:%S')
        address = self.root.ids.personal_screen.ids.address_ti.text
        blood_type = self.root.ids.personal_screen.ids.blood_ti.text
        pen_all = self.root.ids.personal_screen.ids.pen_it.text

        '''print(id)
        print(input_user_name)
        print(gender)
        print(birthday)
        print(address)
        print(blood_type)
        print(pen_all)'''

        # insert into database
        cn = rds_connect_lsy()
        cursor = cn.conn.cursor()
        # sql_txt = "insert into user_info (name, password) values ('{}', '{}');".format(input_user_name, input_pass_word)
        sql_txt = "update user_info set gender= '{}', \
                                        birthday= '{}', \
                                        address = '{}', \
                                        pos = 'patient', \
                                        blood_type = '{}', \
                                        penicillin_allergy = '{}' \
                                        where id = {};".format(gender, birthday, address, blood_type, pen_all, id)
        cursor.execute(sql_txt)
        cn.conn.commit()

        self.change_screen('home_screen')

        self.patient_id = id
        self.patient_name = input_user_name

        return

    def doctor_login(self):

        # get veri_code
        veri_code = self.root.ids.veri_screen.ids.veri_code_ti.text

        # check the veri_code
        sql_list_veri_code = "select veri_code from doctor_info"
        cn = rds_connect_lsy()
        re = pd.read_sql_query(sql_list_veri_code, con=cn.conn)
        veri_code_list = re.values.tolist()
        if [veri_code] in veri_code_list:
            where = veri_code
            sql_txt = "select * from doctor_info where veri_code = " + where
            re = pd.read_sql_query(sql_txt, con=cn.conn)
            if (re['id'].values[0] == None):
                id = ''
            else:
                id = re.iloc[0]['id']
            if (re['name'].values[0] == None):
                name = ''
            else:
                name = re.iloc[0]['name']
            if (re['depart'].values[0] == None):
                depart = ''
            else:
                depart = re.iloc[0]['depart']
            if (re['address'].values[0] == None):
                addr = ''
            else:
                addr = re.iloc[0]['address']

            self.root.ids.doctor_screen.ids.doct_info_label.text = str(id) + '#' + str(name) + ' information'
            self.root.ids.doctor_screen.ids.doctor_depart.text = str(depart)
            self.root.ids.doctor_screen.ids.doctor_addr.text = str(addr)
            self.doctor_login_id = id

            cn.conn.commit()

            self.change_screen('doctor_screen')

        else:
            self.root.ids.veri_screen.ids.error_label.text = 'no match verification code'
            self.root.ids.veri_screen.ids.error_label.color = get_color_from_hex("#ff0000")
            cn.conn.commit()
            return

    #
    # for doctors to select patients
    def select_patients(self):
        # get doctor id
        doct_id = int(self.root.ids.doctor_screen.ids.doct_info_label.text.split('#')[0])
        # get patients list
        sql_txt = "select p.id, p.name from user_info p  \
                            left join doctor_patient d \
                            on p.id = d.patient_id \
                            where d.doct_id = {};".format(doct_id)
        cn = rds_connect_lsy()
        re = pd.read_sql_query(sql_txt, con=cn.conn)
        # check if re is null
        if len(re.values.tolist()) == 0:
            self.root.ids.doctor_screen.ids.error_label.text = 'no assigned patients'
            self.root.ids.doctor_screen.ids.error_label.color = get_color_from_hex("#ff0000")
            cn.conn.commit()
            return
        else:
            patient_list = []
            for instance in re.values.tolist():
                patient_list.append(str(instance[0]) + '#' + str(instance[1]))
        cn.conn.commit()

        # create and assemble dropdown button
        self.dropdown1 = DropDown()
        for patient in patient_list:
            drop_btn = Button(text=str(patient), size_hint_y=None, height=55)
            # drop_btn.bind(on_release=lambda drop_btn: print(dropdown1.select(drop_btn.text)))
            drop_btn.bind(on_release=lambda drop_btn: self.go_to_doctor_diagnosis(drop_btn.text))
            self.dropdown1.add_widget(drop_btn)

        return self.dropdown1.open(self.root.ids.doctor_screen.ids.diag_button)

    # in doctor_screen when doctor click dropdown buttons in 'diagnosis button'
    def go_to_doctor_diagnosis(self, text):
        # get patient id from dropdown
        self.selected_patient_id_by_doctor = text.split('#')[0]
        self.selected_patient_name_by_doctor = text.split('#')[1]
        # work with database
        sql_txt = "select diag.*, doct.name from diagnosis diag\
                    left join doctor_info doct\
                    on diag.doct_id = doct.id \
                    where diag.patient_id = {} \
                    order by diag.begin_time asc;".format(self.selected_patient_id_by_doctor)
        cn = rds_connect_lsy()
        re = pd.read_sql_query(sql_txt, con=cn.conn)
        content = re.values.tolist()
        if len(content) == 0:
            self.root.ids.doctor_screen.ids.error_label.text = 'this patient has no submission yet'
            self.root.ids.doctor_screen.ids.error_label.color = get_color_from_hex("#ff0000")
            cn.conn.commit()
            return
        else:
            output = ''
            for index, item in enumerate(content):
                output = output + str(index) + ') datetime: ' + str(item[2]) + \
                         ' description: ' + str(item[4]) + '\ndatetime: ' + str(item[3]) +\
                         ' by doctor: ' + str(item[6]) + ' suggestions: ' + str(item[5]) + '\n'
                self.patient_latest_submit = str(item[2])
            self.root.ids.docdiag_screen.ids.patient_diagnosis.text = output
            self.change_screen('docdiag_screen')

        cn.conn.commit()
        return self.dropdown1.dismiss(self.root.ids.doctor_screen.ids.diag_button)

    # in doctor_screen when doctor click dropdown buttons in 'diagnosis button'
    def go_to_patient_diagnosis(self):
        # get patient id from dropdown
        patient_id = self.patient_id
        # work with database
        sql_txt = "select diag.*, doct.name from diagnosis diag\
                            left join doctor_info doct\
                            on diag.doct_id = doct.id \
                            where diag.patient_id = {} \
                            order by diag.begin_time asc;".format(patient_id)
        cn = rds_connect_lsy()
        re = pd.read_sql_query(sql_txt, con=cn.conn)
        content = re.values.tolist()
        if len(content) == 0:
            output = ''
        else:
            output = ''
            for index, item in enumerate(content):
                output = output + str(index) + ') datetime: ' + str(item[2]) + \
                         ' description: ' + str(item[4]) + '\ndatetime: ' + str(item[3]) +\
                         ' by doctor: ' + str(item[6]) + ' suggestions: ' + str(item[5]) + '\n'
        self.root.ids.patdiag_screen.ids.doctor_diagnosis.text = output
        cn.conn.commit()
        self.change_screen('patdiag_screen')

        return


    # in patdiag_screen when patient click submit button
    def submit_patient_diagnosis(self):

        # prepare for the information
        txt = self.root.ids.patdiag_screen.ids.patient_diagnosis.text
        patient_id = self.patient_id
        patient_name = self.patient_name
        begin_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # work with AWS mysql
        cn = rds_connect_lsy()
        cursor = cn.conn.cursor()
        sql_txt = "insert into diagnosis (patient_id, begin_time, patient_txt) \
                    values ({}, '{}', '{}');".format(patient_id, begin_time, txt)
        cursor.execute(sql_txt)
        cn.conn.commit()

        self.root.ids.patdiag_screen.ids.patient_diagnosis.text = ''

        self.change_screen('home_screen')

        return

    # in docdiag_screen when doctor click submit button
    def submit_doctor_diagnosis(self):
        # prepare
        begin_time = self.patient_latest_submit
        patient_id = self.selected_patient_id_by_doctor
        doctor_id = self.doctor_login_id
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        doctor_text = self.root.ids.docdiag_screen.ids.doctor_diagnosis.text
        # work with database
        cn = rds_connect_lsy()
        cursor = cn.conn.cursor()
        sql_txt = " update diagnosis set doct_id = {}, \
                    end_time = '{}', \
                    doctor_txt = '{}'\
                    where patient_id = {} \
                    and begin_time = '{}';".format(doctor_id, end_time, doctor_text, patient_id, begin_time)
        cursor.execute(sql_txt)
        cn.conn.commit()

        self.root.ids.docdiag_screen.ids.doctor_diagnosis.text = ''

        self.change_screen('doctor_screen')

        return

MainApp().run()