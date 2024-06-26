import numpy as np

class Dataset_Raw:
    def __init__(self, traces_file_path, textin_file_path, textout_file_path, keys_file_path,dataset_num, key_array=None, key_string=""):
        self.dataset_num : int = dataset_num
        self.traces_file_path = traces_file_path
        self.textin_file_path = textin_file_path
        self.textout_file_path = textout_file_path
        self.keys_file_path = keys_file_path
        self.key_array = key_array if key_array is not None else np.array([])
        self.key_string = key_string
    
    # Getters
    @property
    def dataset_num(self):
        return self._dataset_num

    @property
    def traces_file_path(self):
        return self._traces_file_path

    @property
    def textin_file_path(self):
        return self._textin_file_path

    @property
    def textout_file_path(self):
        return self._textout_file_path

    @property
    def key_array(self):
        return self._key_array

    @property
    def key_string(self):
        return self._key_string

    # Setters
    @dataset_num.setter
    def dataset_num(self, value):
        self._dataset_num = value

    @traces_file_path.setter
    def traces_file_path(self, value):
        self._traces_file_path = value

    @textin_file_path.setter
    def textin_file_path(self, value):
        self._textin_file_path = value

    @textout_file_path.setter
    def textout_file_path(self, value):
        self._textout_file_path = value

    @key_array.setter
    def key_array(self, value):
        self._key_array = np.array(value)

    @key_string.setter
    def key_string(self, value):
        self._key_string = value

    def load_traces(self):
        try:
            self.traces = np.load(self.traces_file_path)
        except Exception as e:
            print(f"Error loading traces: {e}")
            self.traces = None

    def load_textin(self):
        try:
            with open(self.textin_file_path, 'r') as file:
                self.textin = file.read()
        except Exception as e:
            print(f"Error loading textin: {e}")
            self.textin = None

    def load_textout(self):
        try:
            with open(self.textout_file_path, 'r') as file:
                self.textout = file.read()
        except Exception as e:
            print(f"Error loading textout: {e}")
            self.textout = None

    def display_info(self):
        print(f"Traces File Path: {self.traces_file_path}")
        print(f"Textin File Path: {self.textin_file_path}")
        print(f"Textout File Path: {self.textout_file_path}")
        print(f"Keys File Path: {self.keys_file_path}")
        print(f"Key Array: {self.key_array}")
        print(f"Key String: {self.key_string}")

    def set_key_array(self, key_array):
        self.key_array = np.array(key_array)

    def set_key_string(self, key_string):
        self.key_string = key_string

    def is_last_row_all_zeros(self):
        try:
            # load the file .npy
            data = np.load(self.traces_file_path)

            # Obtaining the last row
            last_row = data[-1, :]

            # verify if all the elements of the last row are 0s
            if np.all(last_row == 0):
                # Remove the last row
                data = data[:-1, :]
                # Saving the modified file
                np.save(self.traces_file_path, data)
                print("Last row with 0s removed and file saved.")
                return True
            else:
                return False
        except Exception as e:
            print(f"Error loading the file to remove row of 0s: {e}")
            return False

    def binary_array_to_hex_string(self):
        try:
            # Converting the array to string
            bit_string = ''.join(format(x, '08b') for x in self.key_array)

            # Is multiple of 4?
            if len(bit_string) % 4 != 0:
                raise ValueError("The length of the string is not multiple of 4")

            # Convertir bits to hexadecimal
            hex_string = '{:0{}X}'.format(int(bit_string, 2), len(bit_string) // 4)

            # To lowercase to mantain the convention of AESkeys.
            key_string = hex_string.lower()
            
            self.key_string = key_string
            print(f"Self.keystring = {self.key_string}")

        except Exception as e:
            print(f"Error converting binary array to hex string: {e}")
            return None
        

