import sqlite3


def generate_vm_data(db_file):
    RAW_VM_LIST = [
        ('ID', 'Name', 'Status', 'Networks', 'Image', 'Flavor'),
        ('f79d1ffe-e284-4b86-926a-c6a6b23859d1', 'perla-08', 'ACTIVE', '',
         'CentOS7-tf_siesta_fann', 'perla-pv.xlarge'),
        ('3bacfad2-2256-4743-a55a-b176aa8f6679', 'perla-07',
         'ACTIVE', '', 'CentOS7-tf_siesta_fann', 'perla-pv.xlarge'),
        ('38d202c7-ecbf-43fb-a1ce-753e74be60c1', 'perla-06',
         'ACTIVE', '', 'CentOS7-tf_siesta_fann', 'perla-pv.xlarge'),
        ('a9b58c0f-9db8-4238-8ad3-647eecc54bb5', 'perla-05',
         'ACTIVE', '', 'CentOS7-tf_siesta_fann', 'perla-pv.xlarge'),
        ('32c19d53-52ba-404a-861e-508f6752750d', 'perla-04',
         'ACTIVE', '', 'CentOS7-tf_siesta_fann', 'perla-pv.xlarge'),
        ('7c3b8a56-6550-4eb4-8f32-94fdbd6f5221', 'perla-03',
         'ACTIVE', '', 'CentOS7-tf_siesta_fann', 'perla-pv.xlarge'),
        ('c10c77f7-64ee-4629-ab5c-1b1498d4c623', 'perla-02',
         'ACTIVE', '', 'CentOS7-tf_siesta_fann', 'perla-pv.xlarge'),
        ('b3c9e31c-d66d-41d2-8c76-c8f9c18848ff', 'perla-01', 'ACTIVE',
         'provider=194.102.58.51', 'CentOS7-tf_siesta_fann', 'perla-pv.xlarge')]

    connection = sqlite3.connect(db_file)

    cursor = connection.cursor()

    cursor.execute('''DROP TABLE IF EXISTS cloudifinServer''')

    cursor.execute('''CREATE TABLE cloudifinServer 
                   (ID text,
                   Name text,
                   Status text,
                   Networks text,
                   Image text,
                   Flavor text)''')

    for vm in RAW_VM_LIST[1:]:
        tuple_vm = vm
        cursor.execute(
            '''INSERT INTO cloudifinServer VALUES (?,?,?,?,?,?)''', tuple_vm)

    connection.commit()
    connection.close()


def get_user_vms(db_file):
    generate_vm_data(db_file)
    connection = sqlite3.connect(db_file)

    cursor = connection.cursor()

    data = cursor.execute(
        '''SELECT ID, Name FROM cloudifinServer''').fetchall()

    connection.close()

    return data


def main():
    generate_vm_data()


if __name__ == '__main__':
    main()
