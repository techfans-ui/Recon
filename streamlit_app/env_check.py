import os
for k,v in os.environ.items():
    if 'STREAMLIT' in k.upper() or 'ASGI' in k.upper() or k.lower().endswith('asgi'):
        print(f"{k}={v}")
print('done')
