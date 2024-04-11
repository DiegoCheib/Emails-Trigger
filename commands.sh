#!/bin/bash

#!/bin/bash

# Cria o ambiente virtual
python3 -m venv env

# Ativa o ambiente virtual
source env/bin/activate

# Instala as dependências
pip install -r requirements.txt

# Inicia a aplicação
python main.py