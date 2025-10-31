FROM jupyterhub/jupyterhub:latest

# Install required packages
RUN pip install --no-cache-dir \
    jupyterlab \
    pvlib \
    pandas \
    numpy \
    matplotlib \
    scikit-learn \
    seaborn

# Install PyTorch with GPU support
RUN pip install --no-cache-dir \
    torch \
    torchvision \
    torchaudio

# Install additional ML/TS packages
RUN pip install --no-cache-dir \
    pytorch-forecasting \
    lightning \
    tensorboard \
    optuna \
    optuna-integration[pytorch_lightning] \
    statsmodels \
    openpyxl

USER ubuntu
WORKDIR /home/ubuntu