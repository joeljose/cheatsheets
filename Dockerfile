FROM python:3.12-slim
RUN pip install --no-cache-dir reportlab
WORKDIR /app
COPY src/ src/
CMD ["sh", "-c", "python src/tmux_cheatsheet.py && python src/vim_cheatsheet.py"]
