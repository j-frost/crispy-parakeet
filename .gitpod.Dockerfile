FROM gitpod/workspace-full

USER gitpod

RUN git clone https://github.com/momo-lab/xxenv-latest.git "$(pyenv root)"/plugins/xxenv-latest 

RUN pyenv latest install 3.9
