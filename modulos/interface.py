import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import difflib
import sys
from modulos.manipularArquivos import *

root = tk.Tk()
root.withdraw()

def carregar_arquivo():
    file_path = filedialog.askopenfilename(
        title='Selecione o arquivo Excel.',
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if not file_path:
        messagebox.showerror('Error', 'Nenhum arquivo selecionado. Encerrando o programa.')
        sys.exit()
    return file_path 

def carregar_anexo():
    resposta = messagebox.askyesno(
        'Anexo opcional',
        'Deseja enviar um anexo?'
    )
    
    if resposta:
        anexo_path = filedialog.askopenfilename(
            title='Selecione um arquivo para anexar.',
            filetypes=[("Arquivos", "*.*")]
        )
        return anexo_path if anexo_path else None
    else:
        return None
    
def escolher_pagina(workbook):
    paginas = workbook.sheetnames
    while True:
        pagina_selecionada = simpledialog.askstring('Seleção de Página', f'Selecione a página a ser processada:\n\n{", ".join(paginas)}')
        if pagina_selecionada is None:
            messagebox.showerror('Erro', 'Operação cancelada.')
            sys.exit()

        pagina_correspondente = difflib.get_close_matches(pagina_selecionada, paginas, n=1, cutoff=0.5)

        if pagina_correspondente:
            return pagina_correspondente[0]
        else:
            retry = messagebox.askretrycancel('Erro', f'Página "{pagina_selecionada}" não encontrada. Deseja tentar novamente?')
            if not retry:
                sys.exit()

def obter_num_mensagens():
    while True:
        try:
            num_mensagens = simpledialog.askinteger('Quantidade de mensagens', 'Quantas mensagens deseja enviar?')
            if num_mensagens is None:
                messagebox.showwarning('Atenção!', 'Digite um número válido!')
                sys.exit()
            if num_mensagens <= 0:
                raise ValueError('O número de mensagens deve ser positivo.')
            return num_mensagens
        except ValueError as e:
            messagebox.showerror('Erro', f'Valor inválido: {e}. Por favor, insira um número inteiro positivo.')

def obter_mensagens(num_mensagens):
    mensagens = []
    for i in range(num_mensagens):
        mensagem = simpledialog.askstring('Mensagem', f'Digite a mensagem {i+1}:')
        if mensagem is None:
            messagebox.showwarning('Atenção', 'Operação cancelada.')
            sys.exit()
        mensagens.append(mensagem)
    return mensagens

def reiniciar_envios(pagina_clientes, coluna_envio):
    ja_enviados, erro = verificar_numeros_enviados(pagina_clientes, coluna_envio)

    if erro:
        messagebox.showerror('Erro', erro)
        return

    if ja_enviados:
        resposta = messagebox.askyesno(
            'Reinicio de envios',
            'Já existem números enviados. Deseja resetar o status de envio?'
        )
        if resposta:
            resetar_status_envio(pagina_clientes, coluna_envio)
            messagebox.showinfo('Sucesso', 'Status de envio resetado.')
        else:
            messagebox.showinfo('Informação', 'O status de envio não foi alterado.')
    else:
        messagebox.showinfo('Informação', 'Nenhum número enviado ainda. Prosseguindo...')


