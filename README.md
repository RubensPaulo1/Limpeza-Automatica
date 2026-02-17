# 🛠️ Sistema de Limpeza Automática - Windows

Aplicação em Python com interface interativa no terminal para monitoramento do sistema e limpeza de arquivos temporários.

<img width="1129" height="793" alt="Captura de tela 2026-02-17 173341" src="https://github.com/user-attachments/assets/91cec5c9-279c-4836-835b-ca37f72d2d91" />
<img width="1123" height="790" alt="Captura de tela 2026-02-17 173352" src="https://github.com/user-attachments/assets/5608ab48-f118-4455-ba08-52ca3a269892" />
<img width="1120" height="788" alt="Captura de tela 2026-02-17 173405" src="https://github.com/user-attachments/assets/db291429-6286-4a8b-8ad7-84ed34bad2a8" />


##Funcionalidades

###Monitoramento em Tempo Real
O sistema exibe informações atualizadas do computador:

- Uso do Disco
- Uso da Memória RAM
- Uso da CPU
- Hostname
- IP da máquina
- Data e hora em tempo real

---

###Limpeza Manual

Permite:

- Limpar pasta **Downloads**
- Limpar pasta **Temp**
- Limpar ambas as pastas

###Agendamento de Limpeza Automática

Integração com o **Agendador de Tarefas do Windows (schtasks)**.

É possível:

- Escolher o dia da semana
- Definir o horário
- Criar uma tarefa semanal automática

---

##Interface

- Interface visual feita com `curses`
- Sistema de cores no terminal
- Navegação com ↑ ↓
- Seleção com ENTER
- Atualização contínua das informações

---

##Tecnologias Utilizadas

- Python 3
- os
- shutil
- subprocess
- psutil
- socket
- curses
- datetime

---

## 📦 Instalação

Clone o repositório:

```bash
git clone https://github.com/RubensPaulo1/Limpeza-Automatica.git
cd seurepositorio
