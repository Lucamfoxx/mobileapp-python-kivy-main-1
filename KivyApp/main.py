import os
import threading
import csv
import pandas as pd
from fpdf import FPDF
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
import openai  # Certifique-se de ter a biblioteca openai instalada

# Defina sua chave de API OpenAI aqui
openai.api_key = "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"

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

        # Limpar os campos após salvar as informações
        self.limpar_campos()

        # Mudar para a tela UserInfo
        self.root.current = 'user'

    def limpar_campos(self):
        # Adicione aqui a lógica para limpar os campos de entrada após salvar as informações
        pass

    def obter_informacoes_usuario(self):
        arquivo_csv = "usuarios.csv"
        df = pd.read_csv(arquivo_csv, delimiter=',')
        df.columns = df.columns.str.strip()

        target_user_id = self.userID  # Substitua pelo userID desejado

        user_row = df[df['userID'] == target_user_id]

        if not user_row.empty:
            user_info = {
                'userID': user_row['userID'].values[0],
                'nome': user_row['nome'].values[0],
                'idade': user_row['idade'].values[0],
                'peso': user_row['peso'].values[0],
                'altura': user_row['altura'].values[0],
                'atividade': user_row['atividade'].values[0],
                'sexo': user_row['sexo'].values[0],
            }
            return user_info
        else:
            print(f"UserID {target_user_id} não encontrado no DataFrame.")
            return None

    def on_dieta_button_press(self):
        user_info = self.obter_informacoes_usuario()
        if user_info:
            self.dieta(user_info)

    def on_treino_button_press(self):
        user_info = self.obter_informacoes_usuario()
        if user_info:
            self.treino(user_info)

    def on_rotina_button_press(self):
        user_info = self.obter_informacoes_usuario()
        if user_info:
            self.rotina(user_info)

    def dieta(self, user_info):
        # Lógica para lidar com a função dieta
        prompt = f"""Idade: {user_info['idade']}\n Peso: {user_info['peso']}\n altura(m): {user_info['altura']}
        \napenas me de 5 refeições bem detalhadas (24h) em tópicos."""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an excellent nutritionist."},
                {"role": "user", "content": prompt},
            ]
        )

        dieta_text = response.choices[0].message['content'].strip()
        self.save_to_pdf(user_info, dieta_text, 'Dieta')

    def treino(self, user_info):
        
        prompt = f"""Idade: {user_info['idade']}\n Peso: {user_info['peso']}\n altura(m): {user_info['altura']}
        \napenas me de 3 treinos com o objetivo de hipertrofia bem detalhados completo em tópicos."""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an excellent nutritionist"},
                {"role": "user", "content": prompt},
            ]
        )

        treino_text = response.choices[0].message['content'].strip()
        self.save_to_pdf(user_info, treino_text, 'Treino')

    def rotina(self, user_info):
        prompt = f"Idade: {user_info['idade']}\n Peso: {user_info['peso']}\n altura(m): {user_info['altura']}\napenas me de uma rotina de bons Habitos (24H) detalhada com base nisso em topicos,"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an excellent nutritionist."},
                {"role": "user", "content": prompt},
            ]
        )

        rotina_text = response.choices[0].message['content'].strip()
        self.save_to_pdf(user_info, rotina_text, 'Rotina')



    def save_to_pdf(self, user_info, content, filename):
        # Lógica para salvar em arquivo PDF
        user_folder = user_info['nome']
        os.makedirs(user_folder, exist_ok=True)
        filename = os.path.join(user_folder, f"{filename}_{user_info['nome']}.pdf")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, content)
        pdf.output(filename)
        print(f"Arquivo '{filename}' salvo com sucesso.")

if __name__ == "__main__":
    HealthApp().run()
