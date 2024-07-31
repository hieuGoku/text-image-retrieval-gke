pip install -U poetry

# add torch cpu version https://qiita.com/XPT60/items/894841b57995bef1e81c
poetry source add -p explicit pytorch https://download.pytorch.org/whl/cpu
poetry add --source --no-cache pytorch torch torchvision
poetry add fastapi ...
