# Obtener Data de Libros por ISBN

Se ejecuta en Python en un servidor flask

## Instalación de librerías


```bash
pip install Flask requests googletrans==4.0.0-rc1
```

## Uso
Iniciarlo mediante el siguiente comando (o poniendo play en el vsc).

```python
python app.py
```

## Ejecución

Se ejectuta por defecto en el siguiente link
```
http://localhost:5000/api/book?isbn=9789707704664
```
en donde ISBN es el parametro de entrada para que devuelva los parametros del libro en un rest.
```json
{
    "authors": [
        "Mario Vargas Llosa"
    ],
    "publish_date": "2006",
    "title": "Travesuras de la niña mala"
}
```
