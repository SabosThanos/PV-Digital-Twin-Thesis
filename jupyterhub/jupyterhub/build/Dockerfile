FROM jupyterhub/jupyterhub:latest

# Create jovyan user 
RUN useradd -m jovyan

# Install required packages
RUN pip install --no-cache-dir \
    jupyterlab \
    pvlib \
    pandas \
    numpy \
    matplotlib \
    scikit-learn

# # Install TensorFlow with GPU support
# RUN pip install --no-cache-dir \
#     tensorflow[and-cuda]

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

USER jovyan
WORKDIR /home/jovyan