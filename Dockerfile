FROM conda/miniconda3

WORKDIR /app
RUN conda create -y -n myenv python=3.10
COPY requirements.txt .

RUN conda install --file requirements.txt
COPY . /app
