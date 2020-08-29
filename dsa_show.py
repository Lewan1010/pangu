
from tkinter import *
import time
import json

class DSA():
    def __init__(self, json_path):
      self.dsa_cfg_all = self.get_json(json_path)
      return

    def get_mask(self, bit_num):
      return (1 << bit_num) - 1
   
    def get_dsa_fild_value(self, dsa, end, start):
      return (dsa >> start) & (self.get_mask(end - start + 1))

    def get_json(self, path):
      fp = open(path,'r', encoding ='utf8')
      pyData = json.load(fp)
      fp.close()
      return pyData

    def dsa_parse(self, cur_dsa_cfg, key, dsa):
        buffer = ""
        dsa_fields = cur_dsa_cfg[key].keys()
        for dsa_field in dsa_fields:
            dsatype = self.get_dsa_fild_value(dsa, cur_dsa_cfg[key][dsa_field][0][1], cur_dsa_cfg[key][dsa_field][0][2])
            if dsatype != cur_dsa_cfg[key][dsa_field][0][3]:
                continue
            for dsa_item in cur_dsa_cfg[key][dsa_field]:
                field_name = dsa_item[0]
                field_start = dsa_item[2]
                field_end = dsa_item[1]
                field_value = self.get_dsa_fild_value(dsa, field_end, field_start)
                buffer += field_name + ": " + str(field_value) + "\n"
        return  buffer

class MY_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    #设置窗口
    def set_init_window(self):
        self.each_words_label = {}
        self.each_words_label_text = {}
        self.result_data_text = {}
        self.dsa_type_radio = {}
        self.dsa_type_radios_start_rows = 0
        self.each_dsa_words_start_rows = 4
        self.each_dsa_word_span_row = 1

        self.init_window_name.title("DSA解析工具_v1.2")  #窗口名
        self.init_window_name.geometry('800x512+10+10')                
        #标签
        self.dsa = DSA("dsa.json")
        self.var = StringVar()
        self.init_dsa_types(self.dsa.dsa_cfg_all)

        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.result_data_Text = Text(self.init_window_name, font=('Arial', 12), width=70, height=48)  #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        
        #按钮
        self.str_tans_to_dsa_button = Button(self.init_window_name, text="解析", bg="lightblue", width=8, command=self.str_tans_to_dsa)
        self.str_tans_to_dsa_button.grid(row=1, column=11)

    def init_dsa_types(self, dsa_cfg):
        dsa_types = dsa_cfg.keys()
        radio_rows = self.dsa_type_radios_start_rows 
        radio_span_rows = 2
        for dsa_type in dsa_types:
            #radio 
            self.dsa_type_radio[dsa_type] = Radiobutton(self.init_window_name, text=dsa_type, 
                 variable=self.var, value=dsa_type, command=self.get_selected_dsa)
            self.dsa_type_radio[dsa_type].grid(row = radio_rows, column = 1, rowspan=radio_span_rows, columnspan=2, sticky=W)
            radio_span_rows += 1
            #radio words
            self.init_each_dsa_words(dsa_type, dsa_cfg[dsa_type].keys())
            
    def init_each_dsa_words(self, dsa_type, each_dsa_word):
        word_span_rows = self.each_dsa_word_span_row
        start_row = self.each_dsa_words_start_rows
        self.each_words_label[dsa_type] = {}
        self.each_words_label_text[dsa_type] = {}
        for key_word in each_dsa_word:
            self.each_words_label[dsa_type][key_word] = Label(self.init_window_name, text = key_word)
            self.each_words_label[dsa_type][key_word].grid(row = start_row, column = 2, rowspan=word_span_rows)
            self.each_words_label_text[dsa_type][key_word] = Text(self.init_window_name,  font=('courier-new', 16), width=16, height=1)
            self.each_words_label_text[dsa_type][key_word].grid(row = start_row, column=3, rowspan=word_span_rows)
            word_span_rows += 2

    def set_dynamic_dsa_words_visible(self, dsa_type_to_set):
        dsa_cfg = self.dsa.dsa_cfg_all
        dsa_types = dsa_cfg.keys()
        for dsa_type in dsa_types:
            key_words = dsa_cfg[dsa_type].keys()
            for key_word in key_words:
                self.each_words_label[dsa_type][key_word].grid_remove()
                self.each_words_label_text[dsa_type][key_word].grid_remove()
        
        key_words = dsa_cfg[dsa_type_to_set].keys()
        for key_word in key_words:
            self.each_words_label[dsa_type_to_set][key_word].grid()
            self.each_words_label_text[dsa_type_to_set][key_word].grid() 

    def get_selected_dsa(self):
        cur_selected_dsa_type = self.var.get()
        if cur_selected_dsa_type:
            self.set_dynamic_dsa_words_visible(cur_selected_dsa_type)
        return cur_selected_dsa_type

    def write_log_to_Text(self, str):
        print(str)

    def byte_is_digit(self, digit):
        digit_array = b'09afAF'
        is_digit = False
        digit_len = len(digit_array)
        for i in range(0, int(digit_len/2)):
            if digit_array[2*i] <= digit and digit_array[2*i + 1] >= digit :
                is_digit = True
                break 
        return is_digit

    def bytes_is_nums(self, src_byte_array):
        src_len = len(src_byte_array)
        for i in range(0, src_len):
            if not self.byte_is_digit(src_byte_array[i]):
                return False
        return True

    def byte_trans_to_digit(self, src_byte):
        std_digit_array = b'aA0'
        std_digit_base = bytearray([10, 10, 0])
        digit = 0
        std_digit_len = len(std_digit_array)
        for i in range(0, std_digit_len):
            if (src_byte >= std_digit_array[i]):
                digit = src_byte - std_digit_array[i] + std_digit_base[i]
                break
        return digit

    #保证输入的字节是合法的16进制数字
    def bytes_trans_to_nums(self, src_byte_array):
        nums = 0
        base = 1
        new_src_byte_array = bytearray(src_byte_array)
        new_src_byte_array.reverse()
        src_len = len(new_src_byte_array)
        for i in range(0, src_len):
            nums += base * self.byte_trans_to_digit(new_src_byte_array[i])
            base *= 16
        return nums

    def write_data_to_show_text(self, src):
        if src:
            try:
                #输出到界面
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, src)
                self.write_log_to_Text("INFO:str_tans_to_dsa success")
            except:
                self.result_data_Text.delete(1.0,END)
                self.result_data_Text.insert(1.0,"Parse dsa failed!")
        else:
            self.write_log_to_Text("ERROR:str_tans_to_dsa failed")

    #功能函数
    def str_tans_to_dsa(self):
        dsa_cfg = self.dsa.dsa_cfg_all
        cur_dsa_type = self.get_selected_dsa()
        if not cur_dsa_type:
            self.write_data_to_show_text("Please select dsa type!")
            return
        dsa_words = dsa_cfg[cur_dsa_type].keys()
        str_total = ""
        for dsa_word in dsa_words:
            str_total += dsa_word + ":\n"
            src = self.each_words_label_text[cur_dsa_type][dsa_word].get(1.0, END).strip().replace("\n","").encode()
            if not self.bytes_is_nums(src):
                except_buffer = "Invalid dsa on " + dsa_word
                self.write_data_to_show_text(except_buffer)
                return
            elif len(src) > 8:
                except_buffer = "The data is over 32 bits on " + dsa_word
                self.write_data_to_show_text(except_buffer)
                return 

            elif len(src) == 0:
                except_buffer = "Please input a dsa on " + dsa_word
                self.write_data_to_show_text(except_buffer)
                return

            src_dsa = self.bytes_trans_to_nums(src)
            result_dsa = self.dsa.dsa_parse(dsa_cfg[cur_dsa_type], dsa_word, src_dsa)
            str_total += result_dsa
            str_total += "\n"
        self.write_data_to_show_text(str_total)
        return

    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time

def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

if ( __name__ == "__main__"):
   gui_start()
