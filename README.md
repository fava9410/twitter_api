# twitter_api

# Horas invertidas

- 1 hora investigando sobre flask
- 1 hora probando el api de twitter con Insomnia
- 5-7 horas creando el api como tal
- 2-3 pruebas unitarias

Total horas invertidas 12 horas aprox.

# Descripcion general
Es mi primer desarrollo en flask, por lo que tuve que aprender sobre la marcha, tengo experiencia con Django por lo que no fue tan dificil pero si tenias sus cositas, como el sql alchemy y la parte de los unit tests, incluso el api de twitter me presento problemas al principio por las credenciales, creo que quedaban mal copiadas cuando abria el pdf desde el correo.

La prueba fue bastante interesante, sin embargo quede insatisfecho ya que por motivos personales no pude terminarla o dejarla como queria, por ejemplo me faltaron las pruebas de integracion y por lo menos un front-end para consumir los api's, tenia pensado al menos hacer un html basico pero por tiempo no me dio (ademas que odio el front entonces le saque el cuerpo lo mas que pude para hacer otras cosas), por lo que debido a esto el aplicativo debe ser probado con herramientas como **Insomnia** o **Postman**, los endpoints con metodos _post_ y _put_ reciben los parametros como un **Multipart Form** no como json. Tambien me falto la documentacion pero confio que con lo simple del aplicativo no haga falta.

En cuento a la base de datos me pude conectar sin problemas, fui cuidadoso con la tabla a trabajar y por si acaso *adjunto un archivo sql que hice como backup de la tabla* (por si me la tiraba). Tuve problemas con los unit tests porque _flask-testing_ pide usar otra base de datos, por lo que perdi tiempo investigando otra forma y despues montando una en mi local, no me queria arriesgar la base de datos de Zemoga.

Para los queries a la base de datos utilice _sql alchemy_ como orm ya que va con defecto con flask y _marshmallow_ para la parte de serializado, queria hacer que cuando un registo se guarda (create or update) se sincronizara con la informacion del usuario en twitter, pero no me di maña para hacerlo en forma elegante para el update, por lo que por tiempo "machetie".

Gracias por la oportunidad, aprendi mucho y espero un feedback para saber en que puedo mejorar.

# Como ejecutar

Adjunto un archivo docker, por lo que basta con los siguientes 2 comandos:

```
docker build . -t twitter_api
docker run -p 5000:5000 twitter_api
```

Desde un navegador se puede acceder a http://localhost:5000/users y deberia retornar un json con todos los usuarios de la base de datos.


# TODO
- frontend
- documentacion
- mas pruebas unitarias