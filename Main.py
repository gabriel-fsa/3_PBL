import os
import datetime
import hashlib
import pickle
import getpass


def cls():
    """
    This function clears the terminal screen when called.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def verification_directories_files():
    path = './user_data'
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except OSError:
            print('Erro na criação do diretório {}'.format(path))

    path = './user_file'
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except OSError:
            print('Erro na criação do diretório {}'.format(path))

    if not os.path.isfile('./user_data/users.txt'):
        with open('./user_data/users.txt', 'w') as file:
            file.write(
                'users file created {}:{}:{}\n'.format(datetime.datetime.now().hour, datetime.datetime.now().minute,
                                                       datetime.datetime.now().second))
            file.write('day: {}/{}/{}\n'.format(datetime.datetime.now().day, datetime.datetime.now().month,
                                                datetime.datetime.now().year))

    if not os.path.isfile('log.txt'):
        with open('log.txt', 'w') as file:
            file.write(
                'Log file created {}:{}:{}\n'.format(datetime.datetime.now().hour, datetime.datetime.now().minute,
                                                     datetime.datetime.now().second))


def hash_password(password, salt):
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password, salt_user):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt_user.encode() + user_password.encode()).hexdigest()


def read_int(num='', erro=False, condicao=(), apagar=True):
    """
    Essa função é semelhante ao int(input()), pois além de retornar um número, há possibilidade de colocar uma condição, ou seja, só irá prosseguir o programa quando for digitado o
    número correspondente, e caso não for digitado um número, mostrar uma mensagem de erro e pedirá para o usuário insira novamente o número.
    :param num: número a ser retornado
    :param erro: Valor booleano para usar a condição.
    :param condicao: Tupla usada para condicionar o valor digitado, o programa só irá proseguir caso for digitado um valor contido na tupla.
    :param apagar: Valor booleano na qual caso o que foi digitado não for o esperado, não vai apagar a tela e voltará para o usuário digita novamente.
    :return: retorna o valor digitado, desde que, ou o parâmetro erro seja igual a False, ou o que esteja na condição.
    """
    if erro == False:
        while True:
            try:
                aux = int(input(num))
            except:
                if apagar:
                    cls()
                print('Digite um número!')
            else:
                return aux
    else:
        while True:
            try:
                aux = int(input(num))
            except:
                if apagar:
                    cls()
                print('Digite um número!')
            else:
                if aux in condicao:
                    return aux
                if apagar:
                    cls()
                print('Valor inválido!')


class User:
    def __init__(self):
        self._name = ''
        self._user = ''
        self._password = ''
        self._logged_user = False
        self._task = Task(self._user, self._password)

    def sign_up(self):
        cls()
        verification_directories_files()
        with open('./user_data/users.txt', 'r') as users:
            self._name = str(input('Digite seu nome: '))
            while True:
                self._user = str(input('Digite um nome de usuário: '))
                i = 0
                users_list = users.readlines()[2:]
                for i in range(int((len(users_list)) / 2)):
                    if self._user == users_list[2 * i][:-1]:
                        cls()
                        print('Nome de usuário já existente! ')
                        i = -1
                        break
                if i != -1:
                    break

        _salt = os.urandom(64).hex()
        _password = getpass.getpass('Digite a senha: ')
        self._password = hash_password(_password, _salt)

        with open('./user_data/users.txt', 'a') as users:
            users.write('{}\n'.format(self._user))
            users.write('{}&{}\n'.format(self._name, self._password))

        path = './user_file/{}'.format(hashlib.sha256(self._user.encode()).hexdigest())
        try:
            os.mkdir(path)
        except OSError:
            print('Erro na criação do diretório {}'.format(path))
        path = path + '/log.txt'
        with open(path, 'w') as file:
            file.write('File created {}:{}:{} in {}/{}/{}\n'.format(datetime.datetime.now().hour,
                                                                    datetime.datetime.now().minute,
                                                                    datetime.datetime.now().second,
                                                                    datetime.datetime.now().day,
                                                                    datetime.datetime.now().month,
                                                                    datetime.datetime.now().year))
        print('Cadrastro concluido com sucesso!')

    def log_in(self):
        while True:
            verification_directories_files()
            cls()

            valid_user = False
            _name = ''
            _password = ''
            _user = str(input('Digite seu nome de usuário: '))
            i = 0
            with open('./user_data/users.txt', 'r') as users:
                users_list = users.readlines()[2:]
                for i in range(int((len(users_list)) / 2)):
                    if _user == users_list[2 * i][:-1]:
                        _name = users_list[2 * i + 1].split('&')[0]
                        break
            _password = getpass.getpass('Digite sua senha: ')
            cls()
            hashed_password = users_list[2 * i + 1][:-1].split('&')[1]
            _salt = hashed_password.split(':')[1]
            valid_user = check_password(hashed_password, _password, _salt)
            if not valid_user:
                print('Usuário e/ou senha incorreta!')
            else:
                print('Login feito com sucesso!')
                self._user = _user
                self._name = _name
                self._password = _password
                self._logged_user = True
                cls()
                break

    def __del__(self):
        ...


class Task:

    def __init__(self, user, password):
        self.user = user
        self.password = password


while True:
    menu = read_int('1 - Cadrastar novo usuário \n2 - Logar no sistema \n3 - Sair', True, (1, 2, 3))

    if menu == 1:
        user = User()
        user.sign_up()
        del user
    elif menu == 2:
        user = User()
        user.log_in()

    elif menu == 3:
        ...