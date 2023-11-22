import os
import threading
import csv
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp

Window.size = (350, 580)

class SplashScreen(Screen):
    pass

class CadastroScreen(Screen):
    pass


class UserInfoscreen(Screen):
    pass

class HealthApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.userID = self.obter_ultimo_userid()  # Obtém o último userID

    def obter_ultimo_userid(self):
        arquivo_csv = "usuarios.csv"
        if os.path.isfile(arquivo_csv):
            with open(arquivo_csv, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for linha in reader:
                    pass
                return int(linha[0]) + 1
        else:
            return 1

    def build(self):
        kv = Builder.load_file("telas.kv")
        return kv

    @mainthread
    def update_ui(self, dt):
        # Atualizações da interface do usuário aqui
        pass

    def perform_background_task(self):
        # Código da tarefa demorada aqui
        # ...

        # Agende a atualização da interface do usuário no thread principal
        Clock.schedule_once(lambda dt: self.update_ui(dt), 0)

    def on_start(self):
        # Inicia a tarefa demorada em um thread secundário
        threading.Thread(target=self.perform_background_task).start()

    def salvar_informacoes_csv(self):
        nome = self.root.get_screen('Cadastro').ids.nome_user.text

        try:
            idade = int(self.root.get_screen('Cadastro').ids.Idade.text)
            if not 10 <= idade <= 100:
                raise ValueError("Idade deve estar entre 10 e 100")
        except ValueError as e:
            print(f"Erro na idade: {e}")
            return

        try:
            peso = float(self.root.get_screen('Cadastro').ids.Peso_user.text)
            if peso <= 0:
                raise ValueError("Peso deve ser um número positivo")
        except ValueError as e:
            print(f"Erro no peso: {e}")
            return

        try:
            altura = float(self.root.get_screen('Cadastro').ids.altura_user.text)
            if altura <= 0:
                raise ValueError("Altura deve ser um número positivo")
        except ValueError as e:
            print(f"Erro na altura: {e}")
            return

        sexo = self.root.get_screen('Cadastro').ids.sexo_user.text
        atividade = self.root.get_screen('Cadastro').ids.atividade_user.text

        self.userID += 1
        nova_linha = f"{self.userID},{nome},{idade},{peso},{altura},{sexo},{atividade}"

        arquivo_csv = "usuarios.csv"

        if not os.path.isfile(arquivo_csv):
            with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(['userID', 'nome', 'idade', 'peso', 'altura', 'atividade', 'sexo'])

        with open(arquivo_csv, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(nova_linha.split(','))

        self.limpar_campos()
        
        # Mudar para a tela UserInfo
        self.root.current = 'user'

    def limpar_campos(self):
        # Adicione aqui a lógica para limpar os campos de entrada após salvar as informações
        pass

    def on_dieta_button_press(self):
        # Lógica para lidar com o pressionamento do botão Dieta
        pass

    def on_treino_button_press(self):
        # Lógica para lidar com o pressionamento do botão Treino
        pass

    def on_rotina_button_press(self):
        # Lógica para lidar com o pressionamento do botão Rotina
        pass

if __name__ == "__main__":
    HealthApp().run()
