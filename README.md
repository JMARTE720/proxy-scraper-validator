# Proxy Scraper & Validator

Este proyecto descarga proxies desde fuentes públicas, detecta su tipo (HTTP, SOCKS4, SOCKS5), y valida si están activos. Los proxies válidos se guardan en la carpeta `proxies/` por tipo.

## Uso

```bash
python main.py
```

Selecciona el modo de ejecución: una vez o en bucle.

## Requisitos

- Python 3.7+
- requests

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

## Archivos generados

- `proxies/http.txt`
- `proxies/socks4.txt`
- `proxies/socks5.txt`

## Licencia

MIT
