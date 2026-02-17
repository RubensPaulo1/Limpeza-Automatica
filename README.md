# 🛠️ Sistema de Limpeza Automática - Windows

Aplicação em Python com interface interativa no terminal para monitoramento do sistema e limpeza de arquivos temporários.

---

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
git clone https://github.com/seuusuario/seurepositorio.git
cd seurepositorio
