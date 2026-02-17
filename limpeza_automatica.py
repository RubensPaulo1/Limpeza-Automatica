import os
import subprocess
import sys
import shutil
import psutil
import socket
import curses
from curses import wrapper
from datetime import datetime

def download_Limpeza():

    arquivos =  os.path.join(os.path.expanduser("~"), "Downloads")

    for arquivo in os.listdir(arquivos):
        
        file_path = os.path.join(arquivos, arquivo)

        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Arquivo {arquivo} removido")

def temp_Limpeza():

    arquivos =  os.getenv("TEMP")
  
  

    for arquivo in os.listdir(arquivos):
        
        file_path = os.path.join(arquivos, arquivo)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            print(f"Arquivo {arquivo} removido")
        except PermissionError:
            print(f"Erro ao remover arquivo {arquivo}: {arquivo}")

def agendamento_Limpeza(dia, horario):

    if dia == "1":
        dia = "MON"
    elif dia == "2":
        dia = "TUE"
    elif dia == "3":
        dia = "WED"
    elif dia == "4":
        dia = "THU"
    elif dia == "5":
        dia = "FRI"
    elif dia == "6":
        dia = "SAT"
    elif dia == "7":
        dia = "SUN"

    caminho_script = os.path.abspath(sys.argv[0])
    comando = [
        "schtasks",
        "/create",
        "/tn", "WinToolkitTask",
        "/tr", f'"{caminho_script}"',
        "/sc", "weekly",
        "/d", dia,
        "/st", horario,
        "/f"
    ]

    resultado = subprocess.run(comando, capture_output=True, text=True)
    if resultado.returncode == 0:
        print("Agendamento realizado com sucesso")
    else:
        print("Erro ao agendar a limpeza")
        print(resultado.stderr)

def init_colors():
    """Inicializa as cores do curses"""
    curses.start_color()
    curses.use_default_colors()
    
    # Define pares de cores personalizados
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)      # Título
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)     # Sucesso/Info
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)    # Aviso
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)       # Erro/Destaque
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)      # Menu
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLUE)      # Selecionado
    curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK)   # Destaque secundário

def draw_header(stdscr):
    """Desenha o cabeçalho da aplicação"""
    height, width = stdscr.getmaxyx()
    
    # Linha superior decorativa
    stdscr.addstr(0, 0, "═" * width, curses.color_pair(1))
    
    # Título centralizado
    title = "🛠️  SISTEMA DE LIMPEZA AUTOMÁTICA  🛠️"
    x = (width - len(title)) // 2
    stdscr.addstr(1, x, title, curses.color_pair(1) | curses.A_BOLD)
    
    # Data e hora
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    stdscr.addstr(2, width - len(now) - 2, now, curses.color_pair(2))
    
    # Linha inferior do cabeçalho
    stdscr.addstr(3, 0, "═" * width, curses.color_pair(1))

def draw_system_info(stdscr):
    """Desenha as informações do sistema"""
    height, width = stdscr.getmaxyx()
    
    # Box de informações do sistema
    info_y = 5
    info_x = 2
    
    # Título da seção
    stdscr.addstr(info_y, info_x, "╔" + "═" * 48 + "╗", curses.color_pair(5))
    stdscr.addstr(info_y + 1, info_x, "║" + " " * 20 + "INFORMAÇÕES DO SISTEMA" + " " * 20 + "║", 
                  curses.color_pair(5) | curses.A_BOLD)
    stdscr.addstr(info_y + 2, info_x, "╠" + "═" * 48 + "╣", curses.color_pair(5))
    
    # Informações do disco
    try:
        disco = psutil.disk_usage("/")
        disco_total = disco.total / (1024 ** 3)
        disco_usado = disco.used / (1024 ** 3)
        disco_livre = disco.free / (1024 ** 3)
        disco_percent = (disco_usado / disco_total) * 100
        
        stdscr.addstr(info_y + 3, info_x, "║ 💾 DISCO:", curses.color_pair(7))
        stdscr.addstr(info_y + 3, info_x + 50, "║", curses.color_pair(5))
        stdscr.addstr(info_y + 4, info_x, f"║   Total: {disco_total:.2f} GB", curses.color_pair(2))
        stdscr.addstr(info_y + 4, info_x + 50, "║", curses.color_pair(5))
        stdscr.addstr(info_y + 5, info_x, f"║   Usado: {disco_usado:.2f} GB ({disco_percent:.1f}%)", 
                      curses.color_pair(3) if disco_percent > 80 else curses.color_pair(2))
        stdscr.addstr(info_y + 5, info_x + 50, "║", curses.color_pair(5))
        stdscr.addstr(info_y + 6, info_x, f"║   Livre: {disco_livre:.2f} GB", curses.color_pair(2))
        stdscr.addstr(info_y + 6, info_x + 50, "║", curses.color_pair(5))
        stdscr.addstr(info_y + 7, info_x, "╠" + "═" * 48 + "╣", curses.color_pair(5))
    except:
        stdscr.addstr(info_y + 3, info_x, "║ Erro ao obter informações do disco", curses.color_pair(4))
        stdscr.addstr(info_y + 3, info_x + 50, "║", curses.color_pair(5))
        stdscr.addstr(info_y + 7, info_x, "╠" + "═" * 48 + "╣", curses.color_pair(5))
    
    # Informações da RAM
    try:
        ram = psutil.virtual_memory()
        ram_total = ram.total / (1024 ** 3)
        ram_usada = ram.used / (1024 ** 3)
        ram_livre = ram.free / (1024 ** 3)
        ram_percent = ram.percent
        
        stdscr.addstr(info_y + 8, info_x, "║ 🧠 MEMÓRIA RAM:", curses.color_pair(7))
        stdscr.addstr(info_y + 8, info_x + 50, "║", curses.color_pair(5))
        stdscr.addstr(info_y + 9, info_x, f"║   Total: {ram_total:.2f} GB", curses.color_pair(2))
        stdscr.addstr(info_y + 9, info_x + 50, "║", curses.color_pair(5))
        stdscr.addstr(info_y + 10, info_x, f"║   Usada: {ram_usada:.2f} GB ({ram_percent:.1f}%)", 
                      curses.color_pair(3) if ram_percent > 80 else curses.color_pair(2))
        stdscr.addstr(info_y + 10, info_x + 50, "║", curses.color_pair(5))
        stdscr.addstr(info_y + 11, info_x, f"║   Livre: {ram_livre:.2f} GB", curses.color_pair(2))
        stdscr.addstr(info_y + 11, info_x + 50, "║", curses.color_pair(5))
        stdscr.addstr(info_y + 12, info_x, "╠" + "═" * 48 + "╣", curses.color_pair(5))
    except:
        stdscr.addstr(info_y + 8, info_x, "║ Erro ao obter informações da RAM", curses.color_pair(4))
        stdscr.addstr(info_y + 8, info_x + 50, "║", curses.color_pair(5))
        stdscr.addstr(info_y + 12, info_x, "╠" + "═" * 48 + "╣", curses.color_pair(5))
    
    # Informações da CPU e Rede
    try:
        cpu = psutil.cpu_percent(interval=0.1)
        stdscr.addstr(info_y + 13, info_x, f"║ ⚡ CPU: {cpu:.1f}%", 
                      curses.color_pair(3) if cpu > 80 else curses.color_pair(2))
        stdscr.addstr(info_y + 13, info_x + 50, "║", curses.color_pair(5))
        
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        stdscr.addstr(info_y + 14, info_x, f"║ 🌐 Hostname: {hostname}", curses.color_pair(2))
        stdscr.addstr(info_y + 14, info_x + 50, "║", curses.color_pair(5))
        stdscr.addstr(info_y + 15, info_x, f"║ 📡 IP: {ip}", curses.color_pair(2))
        stdscr.addstr(info_y + 15, info_x + 50, "║", curses.color_pair(5))
    except:
        stdscr.addstr(info_y + 13, info_x, "║ Erro ao obter informações", curses.color_pair(4))
        stdscr.addstr(info_y + 13, info_x + 50, "║", curses.color_pair(5))
    
    stdscr.addstr(info_y + 16, info_x, "╚" + "═" * 48 + "╝", curses.color_pair(5))

def draw_menu(stdscr, selected):
    """Desenha o menu principal"""
    height, width = stdscr.getmaxyx()
    
    menu_y = 5
    menu_x = width - 55
    
    # Box do menu
    stdscr.addstr(menu_y, menu_x, "╔" + "═" * 50 + "╗", curses.color_pair(5))
    stdscr.addstr(menu_y + 1, menu_x, "║" + " " * 18 + "MENU PRINCIPAL" + " " * 18 + "║", 
                  curses.color_pair(5) | curses.A_BOLD)
    stdscr.addstr(menu_y + 2, menu_x, "╠" + "═" * 50 + "╣", curses.color_pair(5))
    
    # Opções do menu
    opcoes = [
        "[1] Definir Limpeza Automática",
        "[2] Limpeza Manual",
        "[3] Sair"
    ]
    
    for i, opcao in enumerate(opcoes):
        y = menu_y + 3 + i
        if i == selected:
            stdscr.addstr(y, menu_x, f"║ ▶ {opcao:<45} ║", curses.color_pair(6) | curses.A_BOLD)
        else:
            stdscr.addstr(y, menu_x, f"║   {opcao:<47} ║", curses.color_pair(5))
    
    stdscr.addstr(menu_y + 6, menu_x, "╚" + "═" * 50 + "╝", curses.color_pair(5))
    
    # Instruções
    stdscr.addstr(menu_y + 8, menu_x, "Use ↑↓ para navegar, ENTER para selecionar", 
                  curses.color_pair(2) | curses.A_DIM)

def draw_message(stdscr, message, color_pair=2):
    """Desenha uma mensagem na parte inferior"""
    height, width = stdscr.getmaxyx()
    y = height - 2
    stdscr.addstr(y, 2, " " * (width - 4), curses.color_pair(0))
    x = (width - len(message)) // 2
    stdscr.addstr(y, x, message, curses.color_pair(color_pair))
    stdscr.refresh()

def menu_agendamento(stdscr):
    """Menu de agendamento de limpeza"""
    stdscr.clear()
    draw_header(stdscr)
    
    height, width = stdscr.getmaxyx()
    
    # Título
    title = "AGENDAMENTO DE LIMPEZA AUTOMÁTICA"
    x = (width - len(title)) // 2
    stdscr.addstr(5, x, title, curses.color_pair(1) | curses.A_BOLD)
    
    # Dias da semana
    dias = [
        "[1] Segunda-feira",
        "[2] Terça-feira",
        "[3] Quarta-feira",
        "[4] Quinta-feira",
        "[5] Sexta-feira",
        "[6] Sábado",
        "[7] Domingo"
    ]
    
    menu_y = 8
    menu_x = (width - 30) // 2
    
    stdscr.addstr(menu_y - 1, menu_x, "╔" + "═" * 28 + "╗", curses.color_pair(5))
    stdscr.addstr(menu_y, menu_x, "║" + " " * 8 + "DIA DA SEMANA" + " " * 7 + "║", 
                  curses.color_pair(5) | curses.A_BOLD)
    stdscr.addstr(menu_y + 1, menu_x, "╠" + "═" * 28 + "╣", curses.color_pair(5))
    
    for i, dia in enumerate(dias):
        stdscr.addstr(menu_y + 2 + i, menu_x, f"║ {dia:<26} ║", curses.color_pair(5))
    
    stdscr.addstr(menu_y + 9, menu_x, "╚" + "═" * 28 + "╝", curses.color_pair(5))
    
    # Antes de ler entrada, garante que não haja teclas "sobrando" no buffer
    curses.flushinp()
    stdscr.timeout(-1)  # bloqueante enquanto o usuário digita
    
    # Input do dia
    stdscr.addstr(menu_y + 11, menu_x + 2, "Digite o dia (1-7): ", curses.color_pair(2))
    stdscr.clrtoeol()
    stdscr.refresh()
    curses.echo()
    curses.curs_set(1)
    dia_bytes = stdscr.getstr(menu_y + 11, menu_x + 24, 2)  # até 2 dígitos (ex: '1', '07')
    curses.noecho()
    curses.curs_set(0)
    dia = dia_bytes.decode('utf-8').strip()
    
    # Input do horário
    curses.flushinp()
    stdscr.addstr(menu_y + 13, menu_x + 2, "Digite o horário (HH:MM): ", curses.color_pair(2))
    stdscr.clrtoeol()
    stdscr.refresh()
    curses.echo()
    curses.curs_set(1)
    horario_bytes = stdscr.getstr(menu_y + 13, menu_x + 30, 5)
    curses.noecho()
    curses.curs_set(0)
    horario = horario_bytes.decode('utf-8').strip()
    
    # Restaura timeout padrão (não bloqueante) para a tela principal
    stdscr.timeout(100)
    
    # Executar agendamento
    try:
        agendamento_Limpeza(dia, horario)
        draw_message(stdscr, "✓ Limpeza Automática agendada com sucesso!", 2)
    except Exception as e:
        draw_message(stdscr, f"✗ Erro ao agendar: {str(e)}", 4)
    
    stdscr.getch()

def menu_limpeza_manual(stdscr):
    """Menu de limpeza manual"""
    stdscr.clear()
    draw_header(stdscr)
    
    height, width = stdscr.getmaxyx()
    selected = 0
    
    opcoes = [
        "[1] Limpar Downloads",
        "[2] Limpar Temp",
        "[3] Limpar Todos os Temporários",
        "[4] Voltar"
    ]
    
    while True:
        stdscr.clear()
        draw_header(stdscr)
        
        # Título
        title = "LIMPEZA MANUAL"
        x = (width - len(title)) // 2
        stdscr.addstr(5, x, title, curses.color_pair(1) | curses.A_BOLD)
        
        # Menu
        menu_y = 8
        menu_x = (width - 40) // 2
        
        stdscr.addstr(menu_y, menu_x, "╔" + "═" * 38 + "╗", curses.color_pair(5))
        stdscr.addstr(menu_y + 1, menu_x, "║" + " " * 12 + "OPÇÕES DE LIMPEZA" + " " * 9 + "║", 
                      curses.color_pair(5) | curses.A_BOLD)
        stdscr.addstr(menu_y + 2, menu_x, "╠" + "═" * 38 + "╣", curses.color_pair(5))
        
        for i, opcao in enumerate(opcoes):
            y = menu_y + 3 + i
            if i == selected:
                stdscr.addstr(y, menu_x, f"║ ▶ {opcao:<34} ║", curses.color_pair(6) | curses.A_BOLD)
            else:
                stdscr.addstr(y, menu_x, f"║   {opcao:<36} ║", curses.color_pair(5))
        
        stdscr.addstr(menu_y + 7, menu_x, "╚" + "═" * 38 + "╝", curses.color_pair(5))
        
        stdscr.addstr(menu_y + 9, menu_x + 2, "Use ↑↓ para navegar, ENTER para selecionar", 
                      curses.color_pair(2) | curses.A_DIM)
        
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            selected = (selected - 1) % len(opcoes)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(opcoes)
        elif key == ord('\n') or key == ord('\r'):
            if selected == 0:  # Limpar Downloads
                stdscr.clear()
                draw_header(stdscr)
                draw_message(stdscr, "Limpando Downloads...", 2)
                stdscr.refresh()
                try:
                    download_Limpeza()
                    draw_message(stdscr, "✓ Downloads limpos com sucesso!", 2)
                except Exception as e:
                    draw_message(stdscr, f"✗ Erro: {str(e)}", 4)
                stdscr.getch()
            elif selected == 1:  # Limpar Temp
                stdscr.clear()
                draw_header(stdscr)
                draw_message(stdscr, "Limpando arquivos temporários...", 2)
                stdscr.refresh()
                try:
                    temp_Limpeza()
                    draw_message(stdscr, "✓ Arquivos temporários limpos com sucesso!", 2)
                except Exception as e:
                    draw_message(stdscr, f"✗ Erro: {str(e)}", 4)
                stdscr.getch()
            elif selected == 2:  # Limpar Todos
                stdscr.clear()
                draw_header(stdscr)
                draw_message(stdscr, "Limpando todos os temporários...", 2)
                stdscr.refresh()
                try:
                    temp_Limpeza()
                    download_Limpeza()
                    draw_message(stdscr, "✓ Limpeza completa realizada com sucesso!", 2)
                except Exception as e:
                    draw_message(stdscr, f"✗ Erro: {str(e)}", 4)
                stdscr.getch()
            elif selected == 3:  # Voltar
                break

def main_curses(stdscr):
    """Função principal da GUI com curses"""
    # Configurações iniciais
    curses.curs_set(0)  # Esconde o cursor
    stdscr.keypad(True)  # Habilita teclas especiais
    stdscr.timeout(100)  # Timeout para atualização em tempo real
    
    init_colors()
    
    selected = 0
    
    while True:
        stdscr.clear()
        
        # Desenha os elementos da tela
        draw_header(stdscr)
        draw_system_info(stdscr)
        draw_menu(stdscr, selected)
        
        # Atualiza informações do sistema periodicamente
        height, width = stdscr.getmaxyx()
        if height >= 25 and width >= 100:
            stdscr.refresh()
        
        # Captura teclas
        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            selected = (selected - 1) % 3
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % 3
        elif key == ord('\n') or key == ord('\r'):
            if selected == 0:  # Agendamento
                menu_agendamento(stdscr)
            elif selected == 1:  # Limpeza Manual
                menu_limpeza_manual(stdscr)
            elif selected == 2:  # Sair
                stdscr.clear()
                draw_message(stdscr, "Encerrando aplicação...", 2)
                stdscr.refresh()
                curses.napms(1000)
                break
        elif key == ord('q') or key == ord('Q'):
            break

def main():
    """Função main que inicia a GUI"""
    wrapper(main_curses)

        
if __name__ == "__main__":
    main()