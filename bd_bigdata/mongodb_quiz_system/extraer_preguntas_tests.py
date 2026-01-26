"""
Script para extraer preguntas de los PDFs de tests
y convertirlas al formato del sistema de quiz
"""

import re
import sys

# Mapeo manual de las preguntas extraídas de los PDFs
# Formato: test_number -> list of questions

TESTS_DATA = {
    "Test 1 - Fundamentos de Datos": [
        {
            "question": "¿Cuál es la unidad semántica mínima que puede almacenarse o comunicarse?",
            "options": {
                "a": "Dato.",
                "b": "Información.",
                "c": "Conocimiento.",
                "d": "Las respuestas A y B son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "El dato es la mínima expresión semántica que puede almacenarse."
        },
        {
            "question": "¿Qué métodos pueden utilizarse para la transformación de información a conocimiento?",
            "options": {
                "a": "Contextualización, agregación y cálculo.",
                "b": "Repercusión, conexión y conversación.",
                "c": "Categorización, corrección y agregación.",
                "d": "Análisis, investigación y discusión.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "Son los métodos que, entre otros, permiten la transformación adecuada de la información en conocimiento."
        },
        {
            "question": "¿Qué métrica de calidad describe la proporción en la que un conjunto de datos contiene a la población que representa?",
            "options": {
                "a": "Precisión.",
                "b": "Consistencia.",
                "c": "Completitud.",
                "d": "Interpretabilidad.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "c",
            "explanation": "Solo puede ser la completitud la métrica que indique lo representativo que son los datos con respecto a una población."
        },
        {
            "question": "¿Cuál de los siguientes es un ejemplo de método de captura manual?",
            "options": {
                "a": "Web scraping.",
                "b": "Encuestas.",
                "c": "Acceso a bases de datos relacionales.",
                "d": "Lectura de termómetro digital.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "Excepto las encuestas, los otros métodos pueden ser automatizados; la encuesta, por su parte, no."
        },
        {
            "question": "¿En qué categoría de captura de datos entra la lectura de información del acelerómetro y giroscopio de un teléfono móvil?",
            "options": {
                "a": "Captura manual.",
                "b": "Procesamiento de documentos.",
                "c": "Acceso a datos públicos.",
                "d": "Sensores.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "El acelerómetro y el giroscopio son los sensores que vienen integrados en el teléfono para capturar el movimiento del teléfono y su posición o inclinación, por ende, los sensores determinan la captura de este tipo de datos."
        },
        {
            "question": "¿Qué elemento es utilizado para delimitar valores en un fichero CSV?",
            "options": {
                "a": "Coma.",
                "b": "CRLF.",
                "c": "Comillas dobles.",
                "d": "Espacio.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "Dentro de los limitares posibles de CSV, la coma es uno de ellos."
        },
        {
            "question": "¿Sobre qué estructuras se basa el formato JSON?",
            "options": {
                "a": "Objetos y diccionarios.",
                "b": "Tablas hash.",
                "c": "Objetos y arrays.",
                "d": "Listas enlazadas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "c",
            "explanation": "Los objetos y los arrays son los elementos que conforman la estructura de JSON."
        },
        {
            "question": "¿Cuál de las siguientes condiciones sobre XML es verdadera?",
            "options": {
                "a": "Un documento solo puede tener un elemento raíz.",
                "b": "El contenido de un elemento debe ser otro elemento.",
                "c": "Todo elemento debe tener un atributo llamado «id».",
                "d": "Los atributos deben de ser de tipo numérico.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "Es la única afirmación que es cierta, un documento XML solo puede tener un único elemento raíz."
        },
        {
            "question": "¿Qué nombre recibe un conjunto de datos persistente utilizado por un sistema de software?",
            "options": {
                "a": "Archivo.",
                "b": "Base de datos.",
                "c": "Registro.",
                "d": "Las respuestas A y B son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "La persistencia se puede dar o bien en una base de datos o bien en un archivo."
        },
        {
            "question": "¿Cuál es la instrucción de SQL para consultar información?",
            "options": {
                "a": "SELECT.",
                "b": "INSERT.",
                "c": "UPDATE.",
                "d": "DELETE.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "La instrucción SELECT permite consultar información en cualquier base de datos."
        }
    ],

    "Test 2 - NoSQL y MongoDB": [
        {
            "question": "¿Qué tipo de base de datos NoSQL se caracteriza por operaciones de lectura y escritura básicas, además de ser apropiadas para entornos de gestión de caché?",
            "options": {
                "a": "Almacén clave-valor simple.",
                "b": "Almacén clave-valor sofisticado.",
                "c": "Base de datos relacional.",
                "d": "Almacén de documentos.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "Son el tipo de bases de datos que soportan operaciones de lectura y escritura básicas."
        },
        {
            "question": "¿En qué categoría de base de datos NoSQL se clasifica a MongoDB?",
            "options": {
                "a": "Almacén clave-valor simple.",
                "b": "Almacén clave-valor sofisticado.",
                "c": "Base de datos relacional.",
                "d": "Almacén de documentos.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "MongoDB es una base de datos basada en documentos."
        },
        {
            "question": "¿Cuál de las siguientes afirmaciones es correcta?",
            "options": {
                "a": "Cassandra se caracteriza porque todos sus nodos actúan por igual y se agrupan en anillo.",
                "b": "Cassandra y Neo4j están desarrolladas en Java.",
                "c": "Neo4j es una base de datos transaccional compatible con ACID y que almacena y procesa grafos nativos.",
                "d": "Todas las afirmaciones anteriores son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Todas estas afirmaciones son correctas."
        },
        {
            "question": "¿Cuál es el equivalente a un registro en MongoDB?",
            "options": {
                "a": "Base de datos.",
                "b": "Collection.",
                "c": "Tabla.",
                "d": "Documento.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "El documento es la mínima agrupación de datos en MongoDB."
        },
        {
            "question": "¿Cuál es el término equivalente a una tabla en MongoDB?",
            "options": {
                "a": "Base de datos.",
                "b": "Collection.",
                "c": "Registro.",
                "d": "Documento.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "La colección agrupa varios documentos y es lo más similar a las tablas en un modelo relacional."
        },
        {
            "question": "¿Cuándo se detalla el uso de la primera base de datos NoSQL?",
            "options": {
                "a": "En 2007, cuando Amazon liberó DynamoDB.",
                "b": "Con Carlo Strozzi en 1998.",
                "c": "En 1965 con MultiValue.",
                "d": "Eric Evans en 2009.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "c",
            "explanation": "Las bases de datos MultiValue fueron desarrolladas por TRW en 1965."
        },
        {
            "question": "¿Cuál de las siguientes es una ventaja de las bases de datos NoSQL?",
            "options": {
                "a": "No generan cuellos de botella.",
                "b": "Tecnología madura.",
                "c": "Responden a la necesidad de escalabilidades horizontal demandada cada vez por más empresas y, además, de manera sencilla.",
                "d": "Las respuestas A y C son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Estas dos afirmaciones describen dos problemas que resuelven las bases de datos NoSQL: el cuello de botella al almacenar los datos y la escalabilidad de dichas bases de datos cuando aumenta el volumen de datos."
        },
        {
            "question": "¿Cuál de las siguientes afirmaciones es correcta?",
            "options": {
                "a": "Todo sistema distribuido no puede garantizar a la vez que haya consistencia, disponibilidad y tolerancia a particiones.",
                "b": "Un sistema distribuido garantiza al menos disponibilidad y consistencia.",
                "c": "Un sistema distribuido que garantiza la consistencia y la tolerancia a particiones no sacrifica por ello la disponibilidad.",
                "d": "Todas las afirmaciones anteriores son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "Este es uno de los principios que describe el teorema CAP."
        },
        {
            "question": "¿Qué patrón de diseño de MongoDB permite incluir un documento dentro de otro?",
            "options": {
                "a": "Uno-a-uno con documentos embebidos.",
                "b": "Uno-a-uno con documentos referidos.",
                "c": "Uno-a-varios con documentos referidos.",
                "d": "Las respuestas B y C son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "Los documentos embebidos hacen referencia al uso de un documento dentro de otro, la relación es uno a uno en este caso."
        },
        {
            "question": "¿Qué patrón de diseño de MongoDB permite incluir una lista de referencias a otros documentos dentro de un documento principal?",
            "options": {
                "a": "Uno-a-uno con documentos embebidos.",
                "b": "Uno-a-uno con documentos referidos.",
                "c": "Uno-a-varios con documentos referidos.",
                "d": "Las respuestas B y C son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Este patrón describe el uso de referencias entre documentos para representar las relaciones. Estas relaciones pueden ser uno a uno o uno a muchos."
        }
    ],

    "Test 3 - MongoDB CRUD": [
        {
            "question": "¿Qué comando de la consola de MongoDB se utiliza para indicar la base de datos con la que se trabajará?",
            "options": {
                "a": "select.",
                "b": "find.",
                "c": "use.",
                "d": "Las respuestas A y C son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "c",
            "explanation": "use permite «usar» la base de datos con la que se quiere trabajar."
        },
        {
            "question": "¿Cuál de las siguientes afirmaciones es correcta?",
            "options": {
                "a": "MongoBooster es una herramienta GUI multiplataforma que facilita la construcción de consultas.",
                "b": "MongoDB Compass es una herramienta no propietaria para la manipulación externa de bases de datos MongoDB.",
                "c": "MongoBooster y MongoDB Compass proporcionan información estadística y de rendimiento de una base de datos MongoDB.",
                "d": "Todas las afirmaciones anteriores son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Las tres afirmaciones son correctas sobre los productos MongoBooster y MongoDB Compass."
        },
        {
            "question": "¿Cuál será el resultado al insertar un documento que posee un atributo más al resto de atributos de la colección?",
            "options": {
                "a": "Dará un fallo al insertar los datos porque el modelo de datos es diferente.",
                "b": "Insertará los datos a la colección.",
                "c": "Insertará los datos a la colección y creará el nuevo atributo vacío en el resto de documentos.",
                "d": "Insertará los datos a la colección, pero sin el nuevo atributo para cumplir con el modelo.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "Los documentos dentro de las colecciones no responden a ningún modelo de datos, por ello, se pueden insertar documentos con atributos diferentes."
        },
        {
            "question": "¿Qué comando puede utilizarse en MongoDB para la creación de un nuevo documento dentro de una collection?",
            "options": {
                "a": "save.",
                "b": "insert.",
                "c": "create.",
                "d": "Las respuestas A y B son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Tanto save como insert permiten crear un nuevo documento en una colección. La acción es la misma en determinados casos, pero cada opción tiene un comportamiento diferente."
        },
        {
            "question": "¿Cuál es el nombre del atributo especial en las collections de MongoDB que ayuda a identificar de manera única a cada documento?",
            "options": {
                "a": "_id.",
                "b": "_ID.",
                "c": "Primary_key.",
                "d": "Identifier.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "Este es el nombre del atributo; si en la consulta no se indica, lo crea MongoDB, y si se indica, el valor debe ser único entre los documentos."
        },
        {
            "question": "¿Qué método permite modificar los datos de un documento sin tener que incluir el documento completo como argumento?",
            "options": {
                "a": "save.",
                "b": "store.",
                "c": "update.",
                "d": "set.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "c",
            "explanation": "Al igual que en SQL, update permite actualizar el documento utilizando una condición y los nuevos a valores a actualizar."
        },
        {
            "question": "La operación MongoDB equivalente a JOIN en SQL es:",
            "options": {
                "a": "Se puede conseguir concatenando sentencias find en la misma operación.",
                "b": "El aggregation framework.",
                "c": "MongoDB no tiene operación equivalente a JOIN hasta su versión 3.2.",
                "d": "Ninguna de las anteriores es cierta.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "Hay funciones de agregación que nos permiten simular el JOIN de SQL."
        },
        {
            "question": "¿Qué situación tiene que darse para que el comando save actualice un documento?",
            "options": {
                "a": "Que el argumento contenga un identificador existente en la collection.",
                "b": "Que el segundo argumento en el comando sea el valor true.",
                "c": "Que el argumento se parezca en más de un 50 % a un documento en la collection.",
                "d": "save no puede utilizarse para actualizar documentos.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "save no permite ningún parámetro de búsqueda. Comprueba si existe un documento con el mismo _id que guardaste. Cuando existe, lo reemplaza. Cuando no existe tal documento, inserta el documento como uno nuevo. Cuando el documento que inserta no tiene _id campo, genera uno con un ObjectId recién creado antes de insertarlo."
        },
        {
            "question": "¿Qué comando se utiliza en MongoDB para eliminar un conjunto de documentos?",
            "options": {
                "a": "save.",
                "b": "delete.",
                "c": "remove.",
                "d": "unset.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "Delete permite borrar documentos que cumplan determinada condición. Remove, por su parte, borra el primero documento que cumpla dicha condición."
        },
        {
            "question": "¿Qué comando puede aplicarse sobre el resultado de una consulta en MongoDB para restringir el número de documentos retornados?",
            "options": {
                "a": "limit.",
                "b": "restrict.",
                "c": "skip.",
                "d": "sort.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "Al igual que en SQL, limit limita el número de registros que se visualizan en una consulta."
        }
    ],

    "Test 4 - Agregación MongoDB": [
        {
            "question": "¿Para qué son útiles las funciones de agregación?",
            "options": {
                "a": "Para agrupar datos.",
                "b": "Para realizar cálculos.",
                "c": "Para crear nuevas colecciones.",
                "d": "Todas las anteriores son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Las funciones de agregación, entre otras cosas, permiten agrupar datos, realizar cálculos y crear nuevas colecciones a partir de los resultados de sus operaciones."
        },
        {
            "question": "¿Qué método puede utilizarse en MongoDB para agregar información de documentos en una collection?",
            "options": {
                "a": "sum.",
                "b": "Aggregate, a partir de la versión 2.2.",
                "c": "Map-Reduce.",
                "d": "Las respuestas B y C son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Estos son los métodos que se han desarrollado en este tema."
        },
        {
            "question": "¿Cuál de las siguientes son operaciones específicas de agregación?",
            "options": {
                "a": "sum.",
                "b": "Map-Reduce.",
                "c": "count.",
                "d": "Las respuestas A y C son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Sum y count son funciones de agregación de por sí. Mongo las utiliza para cumplir operaciones específicas en Aggregate."
        },
        {
            "question": "¿Cuál es el objetivo principal de la función map?",
            "options": {
                "a": "Generar los pares clave-valor.",
                "b": "Realizar operaciones con los atributos de la colección.",
                "c": "Opinar sobre los pares clave-valor.",
                "d": "Crear una nueva colección.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "Map genera los pares clave-valor en función de los datos que procesa."
        },
        {
            "question": "¿Cuál es el objetivo principal de la función reduce?",
            "options": {
                "a": "Generar los pares clave-valor.",
                "b": "Realizar operaciones con los atributos de la colección.",
                "c": "Operar sobre los pares clave-valor, reduce lo que hace es operar sobre ellos para cumplir su objetivo como función de reducción.",
                "d": "Crear una nueva colección.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "c",
            "explanation": "Una vez generados los pares clave-valor, reduce lo que hace es operar sobre ellos para cumplir su objetivo como función de reducción."
        },
        {
            "question": "¿Qué comando se utiliza en una función map para generar el par clave-valor que será procesado posteriormente?",
            "options": {
                "a": "generate.",
                "b": "return.",
                "c": "emit.",
                "d": "yield.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "c",
            "explanation": "emit es la función que genera el par clave-valor que será procesado en el momento de generarse."
        },
        {
            "question": "¿Cuál de las siguientes es una ventaja del framework de agregación de MongoDB?",
            "options": {
                "a": "Rendimiento.",
                "b": "Potencia.",
                "c": "Simplicidad.",
                "d": "Las respuestas A y C son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Aggregation básicamente permite conseguir mejor rendimiento y simplicidad a la hora de hacer las agregaciones. Potencia no es que sea siempre un daño en una agregación, incluso habrá agregaciones que no sean lo suficientemente adecuadas para pensar en su uso."
        },
        {
            "question": "¿En qué está modelado el framework de agregación?",
            "options": {
                "a": "Funciones.",
                "b": "Etapas.",
                "c": "Sentencias SQL.",
                "d": "Agrupaciones.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "Recordemos que el framework de agregación está modelado en el concepto de tuberías de procesamiento de datos, es decir, los documentos entran en una tubería de varias etapas que transforman los documentos en un resultado agregado."
        },
        {
            "question": "¿Qué campo es obligatorio especificar en framework de agregación?",
            "options": {
                "a": "_id.",
                "b": "Object.",
                "c": "$sum.",
                "d": "$group.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "$group es el campo obligatorio que debe especificarse en el framework de agregación."
        },
        {
            "question": "¿Cuál de los siguientes es un operador del framework de agregación?",
            "options": {
                "a": "$gt.",
                "b": "$map.",
                "c": "$glear.",
                "d": "Todos los anteriores son correctos.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Los tres son operadores de agregación del framework."
        }
    ],

    "Test 5 - Backup, Índices, Replicación y Sharding": [
        {
            "question": "¿Qué comando de MongoDB permite crear una copia de respaldo de una base de datos?",
            "options": {
                "a": "mongorestore.",
                "b": "mongodump.",
                "c": "backup.",
                "d": "mongod.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "Este comando permite crear una copia de seguridad «dump» de la base de datos."
        },
        {
            "question": "¿Qué comando de MongoDB permite recuperar una base de datos a partir de una copia de seguridad?",
            "options": {
                "a": "mongorestore.",
                "b": "save.",
                "c": "mongos.",
                "d": "copydb.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "Este comando permite restaurar una base de datos que previamente ha sido guardada «dump»."
        },
        {
            "question": "¿Qué elementos de la base de datos mejoran el rendimiento de consultas a collection?",
            "options": {
                "a": "Índices.",
                "b": "Replica sets.",
                "c": "Query routers.",
                "d": "Las respuestas B y C son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "Los índices son elementos que permiten indexar los documentos de la base de datos para mejorar las búsquedas."
        },
        {
            "question": "¿Qué característica de MongoDB permite tener redundancia y aumentar la disponibilidad de los datos?",
            "options": {
                "a": "Seguridad.",
                "b": "Sharding.",
                "c": "Índices.",
                "d": "Replicación.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Recuerda que la replicación es una característica de MongoDB que permite la redundancia de datos e incrementa su disponibilidad."
        },
        {
            "question": "¿Cuál es el modelo básico de replicación en MongoDB?",
            "options": {
                "a": "Sharding.",
                "b": "Replica set.",
                "c": "Maestro-Esclavo.",
                "d": "Shards.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "c",
            "explanation": "La arquitectura básica de replicación en MongoDB sigue un modelo Maestro-Esclavo."
        },
        {
            "question": "¿Cómo se llama al refinamiento del modelo Maestro-Esclavo implementado en MongoDB?",
            "options": {
                "a": "Result set.",
                "b": "Replica set.",
                "c": "Sharding.",
                "d": "Replicación.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "Este método permite una recuperación a fallos de forma automática, y es la forma recomendada de implementar replicación de datos en MongoDB."
        },
        {
            "question": "¿Cómo se denomina al nodo de un replica set que no almacena datos y solamente puede votar en las elecciones de nodo primario?",
            "options": {
                "a": "Secundario.",
                "b": "Árbitro.",
                "c": "Shard.",
                "d": "Config server.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "Este es utilizado solamente para decidir qué nodo debe ser asignado como primario."
        },
        {
            "question": "¿Qué otro nombre recibe el método de escalabilidad horizontal, en el que los datos son separados y distribuidos entre varios servidores?",
            "options": {
                "a": "Escalabilidad vertical.",
                "b": "Elastic computing.",
                "c": "Sharding.",
                "d": "Replicación.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "c",
            "explanation": "Sharding o escalabilidad horizontal."
        },
        {
            "question": "¿Qué nombre reciben los nodos que almacenan datos en un sharded cluster?",
            "options": {
                "a": "Data stores.",
                "b": "Config servers.",
                "c": "Query routers.",
                "d": "Shards.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Están a cargo de almacenar la información. Cada shard es un replica set, por lo que brinda alta disponibilidad y consistencia de datos."
        },
        {
            "question": "¿Cuántos config servers debe haber en un entorno de producción?",
            "options": {
                "a": "Uno.",
                "b": "Tres.",
                "c": "Un máximo de cinco.",
                "d": "Depende del número de servidores disponibles.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "Los sharded clusters en un entorno de producción tienen exactamente tres config servers."
        }
    ],

    "Test 6 - Drivers MongoDB": [
        {
            "question": "¿Cuál es el objetivo de un driver?",
            "options": {
                "a": "«Traducir» las llamadas que se hacen desde un lenguaje de programación a un «lenguaje» que entienda la base de datos.",
                "b": "Proporcionar un objeto de conexión.",
                "c": "Proporcionar una serie de «funciones» que permitan al programador interactuar con la base de datos.",
                "d": "Todas las anteriores son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Todas las afirmaciones anteriores son características de los drivers."
        },
        {
            "question": "¿Dónde se debería acudir si se quiere desarrollar una aplicación con base de datos MongoDB para gestionar una conexión?",
            "options": {
                "a": "A la página oficial del lenguaje de programación con el que estamos desarrollando.",
                "b": "A la página de documentación oficial de MongoDB, en el apartado de drivers.",
                "c": "A la página oficial del sistema operativo donde estemos desarrollando.",
                "d": "Todas las anteriores son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "MongoDB proporciona información detallada de todos los drivers de conexión que existen, lo recomendable es utilizar dicha información para crear nuestras propias aplicaciones."
        },
        {
            "question": "¿Cuál de los siguientes lenguajes de programación soporta MongoDB?",
            "options": {
                "a": "C.",
                "b": "Java.",
                "c": "PHP.",
                "d": "Todos los anteriores son correctos.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Los tres lenguajes soportan programar para MongoDB."
        },
        {
            "question": "¿Cuál es la mejor forma de descargar el driver de Java?",
            "options": {
                "a": "Utilizando Maven.",
                "b": "Buscando en Google.",
                "c": "Repositorio.",
                "d": "Las respuestas A y C son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Tanto Maven como los repositorios oficiales ofrecen las librerías de Java necesarias para trabajar con MongoDB."
        },
        {
            "question": "Si no se especifica en el driver ningún parámetro, ¿dónde se realiza la conexión?",
            "options": {
                "a": "A localhost u puerto 27017.",
                "b": "Puerto 27017.",
                "c": "Localhost.",
                "d": "Es obligatorio definir un servidor y un puerto.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "Al instalar MongoDB, por defecto, este levanta una instancia de servidor en localhost sobre el puerto 27017. El driver por defecto conoce esta información y la usa para conectarse si el usuario no indica ninguna información de conexión diferente."
        },
        {
            "question": "¿Cuál es el formato de documentos utilizado por el driver de Java?",
            "options": {
                "a": "BSON.",
                "b": "JSON.",
                "c": "CSV.",
                "d": "XML.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "Java utiliza el formato BSON para manipular los documentos de MongoDB."
        },
        {
            "question": "¿Cuál es la mejor forma de instalar el driver de Node.js?",
            "options": {
                "a": "Usando Maven.",
                "b": "Buscando en Google.",
                "c": "Usando NPM.",
                "d": "Todas las anteriores son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "c",
            "explanation": "NPM es el instalador de paquetes útil para Node.js, por medio de este es posible instalar el driver para que Node.js conecte con MongoDB."
        },
        {
            "question": "¿Qué es PyMongo?",
            "options": {
                "a": "Una base de datos NoSQL.",
                "b": "El driver de MongoDB para Python.",
                "c": "Una base de datos SQL.",
                "d": "El driver de lenguaje de programación Py.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "La librería de Python para trabajar y conectar con MongoDB se llama PyMongo."
        },
        {
            "question": "¿Cómo podemos descargar el driver de Python para Mongo?",
            "options": {
                "a": "Utilizando NPM.",
                "b": "Utilizando Maven.",
                "c": "Buscando en Google.",
                "d": "Utilizando PIP.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "El driver de Python está disponible en el repositorio de paquetes de PIP, por ello es la forma más sencilla de instalar dicho driver para conectar con MongoDB desde Python."
        },
        {
            "question": "¿Cuál de estos comandos son válidos para acceder a una colección de mongo?",
            "options": {
                "a": "db.myCollection",
                "b": "db['myCollection']",
                "c": "db.getCollection('myCollection')",
                "d": "Todas son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Todos los comandos anteriores permiten acceder a una colección en MongoDB."
        }
    ],

    "Test 7 - Cassandra": [
        {
            "question": "Cassandra:",
            "options": {
                "a": "Es un sistema de almacenamiento de datos NoSQL desarrollado por Facebook.",
                "b": "Es un sistema de almacenamiento en tiempo real para aplicaciones en línea.",
                "c": "Está diseñado para manejar cargas de trabajo en múltiples nodos.",
                "d": "Todas las afirmaciones anteriores son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Todas estas afirmaciones definen lo que es Cassandra y lo que puede hacer como base de datos NoSQL."
        },
        {
            "question": "¿Cuáles son los componentes principales de Cassandra?",
            "options": {
                "a": "Cluster, keyspace, column y column & family.",
                "b": "Columna name, tables y keyspace.",
                "c": "Mem-Table, SSTable y Bloom Filter.",
                "d": "Las respuestas A y C son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "Además de los componentes que permiten el almacenamiento del dato y su manipulación, la tabla de memoria, la SSTable y BFilter son componentes claves que dan a Cassandra agilidad y robustez."
        },
        {
            "question": "¿Cuáles son las colecciones en CQL Cassandra?",
            "options": {
                "a": "Tupple, list y timestamp.",
                "b": "Map, list y set.",
                "c": "Counter, duration y date.",
                "d": "Ninguna respuesta anterior es correcta.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "Estas son las principales colecciones que utiliza Cassandra y que optimiza para facilitar su implementación en determinados contextos."
        },
        {
            "question": "¿Cuál es la principal característica de la colección list?",
            "options": {
                "a": "Almacenar datos de forma aleatoria.",
                "b": "Almacenar datos de forma ordenada y que se puedan repetir.",
                "c": "Almacenar elementos clave-valor.",
                "d": "Almacenar elementos para usarlos en un orden concreto.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Cuando el orden de los elementos importa, se utiliza list en Cassandra. La consulta de estos elementos es mediante su posición."
        },
        {
            "question": "¿Qué pasa con los datos eliminados en Cassandra?",
            "options": {
                "a": "Se borran inmediatamente de la base de datos.",
                "b": "Se almacenan temporalmente en la papelera de reciclaje de Cassandra.",
                "c": "Son marcados con una lápida.",
                "d": "Nunca se borran, están inactivos hasta que el usuario los vuelva a activar.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "c",
            "explanation": "Cassandra tiene un modo particular de eliminar los datos borrados. Estos no se eliminan de inmediato, sino que son marcados para que tareas posteriores se encarguen de su borrado real."
        },
        {
            "question": "¿Cuál de las siguientes afirmaciones es verdadera?",
            "options": {
                "a": "Cassandra escribe los datos en una caché clave-valor llamada Mem-Table.",
                "b": "Los datos en Mem-Table se ordenan por clave.",
                "c": "Existe una Mem-Table por cada ColumnFamily y de ella se recuperan los datos por la columna clave.",
                "d": "Todas las afirmaciones anteriores son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Las tres afirmaciones explican cómo utiliza Cassandra la memoria mediante la tabla Mem-Table."
        },
        {
            "question": "La instrucción ALTER KEYSPACE se puede utilizar para:",
            "options": {
                "a": "Definir un esquema.",
                "b": "Crear una tabla.",
                "c": "Ejecutar una consulta.",
                "d": "Modificar un keyspace.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "La instrucción ALTER modifica cualquier elemento que se indique a continuación, en este caso el keyspace."
        },
        {
            "question": "Al intentar borrar un elemento que no existe en una colección set, se produce:",
            "options": {
                "a": "La inserción de un nuevo elemento con dicho valor.",
                "b": "Un error en la operación de borrado.",
                "c": "Una operación que no se lleva a cabo y que tampoco genera error alguno.",
                "d": "Una mutación de la colección.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "c",
            "explanation": "No es un error intentar borrar un elemento que no existe en un set, simplemente la operación no se realiza y tampoco genera ningún mensaje de error."
        },
        {
            "question": "¿Qué es una UDT?",
            "options": {
                "a": "Un tipo de datos primitivo.",
                "b": "Un objeto con funciones especiales en Cassandra.",
                "c": "Un tipo de datos definido por el usuario.",
                "d": "Un proceso de carga de datos.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "c",
            "explanation": "La sigla UDT significa User Define Tupe, es decir, un tipo de datos definido por el usuario."
        },
        {
            "question": "¿Cuál de las siguientes instrucciones es correcta?",
            "options": {
                "a": "select * from client.agent where dept='AB';",
                "b": "drop index IF EXISTS clients.DeptIndex;",
                "c": "insert into University.Teacher(id,Name,Email,Description) values (2, 'Hamilton',['hamilton@hotmail.com'], ['Data Science']);",
                "d": "Todas las instrucciones anteriores son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Todas las instrucciones son correctas en este caso."
        }
    ],

    "Test 8 - Grafo (Neo4j)": [
        {
            "question": "¿Cuáles son los principales componentes de un grafo?",
            "options": {
                "a": "El esquema, los nodos, las relaciones y las propiedades.",
                "b": "Nodos, relaciones y propiedades.",
                "c": "Nodos y relaciones, las propiedades están implícitas en cada uno.",
                "d": "Ninguna de las anteriores es correcta.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "Un grafo se representa principalmente por nodos, relaciones y propiedades. Otros elementos, como los esquemas, son propios del concepto de base de datos."
        },
        {
            "question": "¿Qué afirmación define las características principales del modelo de grafos?",
            "options": {
                "a": "El modelo representa datos en nodos, relaciones y propiedades.",
                "b": "Las propiedades son pares clave-valor.",
                "c": "Las relaciones conectan los nodos.",
                "d": "Todas las anteriores son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Todas las afirmaciones definen las características de Neo4j vistas en este tema."
        },
        {
            "question": "¿Qué es CQL?",
            "options": {
                "a": "El lenguaje de consulta para Neo4j Graph Database.",
                "b": "Un lenguaje para insertar y borrar nodos y relaciones.",
                "c": "Un lenguaje enfocado a encontrar solo nodos dentro de un grafo.",
                "d": "Todas las afirmaciones anteriores son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "CQL o Cypher Query Language es el lenguaje que utiliza Neo4j para la manipulación de grafos."
        },
        {
            "question": "¿Qué hace la siguiente instrucción: MATCH ( n ) DETACH DELETE n?",
            "options": {
                "a": "Limpia la base de datos.",
                "b": "Borra todos los nodos y relaciones de la base de datos.",
                "c": "Borra solo los nodos existentes.",
                "d": "Borra los nodos y sus propiedades.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "Cuidado, esta instrucción borra tanto nodos como relaciones de la base de datos. De igual forma, incluye las propiedades de ambos elementos."
        },
        {
            "question": "La cláusula que borra etiquetas y propiedades es:",
            "options": {
                "a": "DELETE.",
                "b": "UNWIND.",
                "c": "REMOVE.",
                "d": "DROP.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "c",
            "explanation": "REMOVE permite eliminar tanto las etiquetas como las propiedades de nodos y relaciones. DELETE borra nodos o relaciones y DROP no existe en Neo4j."
        },
        {
            "question": "¿Qué significa n en la siguiente instrucción: MATCH ( n ) RETURN n.name, n.runs ORDER BY n.runs?",
            "options": {
                "a": "Cualquier nodo y relación.",
                "b": "Cualquier nodo.",
                "c": "Cualquier relación con las propiedades name y runs.",
                "d": "Los nodos cuya propiedad name tiene un valor.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "n representa cualquier nodo relacionado con otros nodos."
        },
        {
            "question": "¿La instrucción MATCH ( n ) RETURN n.name order by n.name qué retorna?",
            "options": {
                "a": "Un grafo con los nodos n.",
                "b": "Un listado.",
                "c": "Un listado y un grafo.",
                "d": "Una lista ordenada de las propiedades nombre de todos los nodos.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Al igual que en SQL, order by ordena un resultado, en este caso el retorno en la lista de nombres ordenada ascendentemente por defecto."
        },
        {
            "question": "¿La instrucción CREATE (Pepe)-[r:CANTA_EN{name=\"Padre\"}]-(Concierto) genera algún tipo de error al ser ejecutada?",
            "options": {
                "a": "No, crea los nodos Pepe y Concierto y su relación CANTAEN.",
                "b": "Sí, la propiedad de la relación es incorrecta.",
                "c": "Sí, no se indica una dirección o sentido de la relación.",
                "d": "Todas las respuestas anteriores son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "c",
            "explanation": "Siempre es necesario indicar el sentido de la relación. Si este no se indica, Neo4j genera un error preguntando por esta definición."
        },
        {
            "question": "La instrucción CREATE (Juan)-[r:HIJO_DE]->(Alma) crea:",
            "options": {
                "a": "Los nodos Juan y Alma y una relación entre ellos llamada HIJO_DE.",
                "b": "Una relación entre los nodos Juan y Alma llamada HIJO_DE.",
                "c": "Una relación saliente de Juan hacia Ana llamada HIJO_DE.",
                "d": "Ninguna de las anteriores es correcta.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "Juan y Alma son nodos, aunque existan se crearán dichos nodos y ambos se le asignará la relación HIJO_DE."
        },
        {
            "question": "Indica qué hace la siguiente instrucción: MATCH (a:Jugador), (b:Juego) WHERE a.name = \"Rabino\" AND b.name = \"Casino\" CREATE (a)-[r:TRABAJA_EN {partida1: victorias:5}]->(b) RETURN a,b",
            "options": {
                "a": "Crea los nodos a y b y asigna la relación TRABAJA_EN.",
                "b": "Crea la relación TRABAJA_EN sobre los nodos a y b.",
                "c": "Busca los nodos a y b que cumplan la condición del WHERE y luego asigna la relación TRABAJA_EN entre ellos.",
                "d": "Todas las respuestas anteriores son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "c",
            "explanation": "Al ejecutarse juntas MATCH y CREATE, los nodos que cumplan la condición WHERE serán quienes reciban la relación que se indica en el CREATE."
        }
    ],

    "Test 9 - Redis": [
        {
            "question": "Las siguientes son estructuras de Redis:",
            "options": {
                "a": "String, integer, float, sets y lists.",
                "b": "Lists, sets, hashes, stream y bit arrays.",
                "c": "HyperLogsLogs, hashes, sets, string y float.",
                "d": "Ninguna de las anteriores es correcta.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "Estos son algunos de los tipos de datos que utiliza Redis para almacenar y manipular los datos. Float, por su parte, no es un tipo de datos de Redis."
        },
        {
            "question": "¿Cuál de estas afirmaciones es verdadera?",
            "options": {
                "a": "No es necesario definir previamente un modelo de datos antes de usar o guardar datos en Redis.",
                "b": "Redis se caracteriza por el tratamiento de distintos tipos de datos, los cuales se pueden aplicar en distintos casos de uso.",
                "c": "Redis es una base de datos clave-valor.",
                "d": "Todas las anteriores son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Todas las afirmaciones son ciertas, hacen parte de las características relevantes de la base de datos."
        },
        {
            "question": "¿Cómo se llama el cliente de Redis?",
            "options": {
                "a": "Cliente Redis Long.",
                "b": "redis-cli.",
                "c": "cli-rediss.",
                "d": "Ninguna de las anteriores es correcta.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "Redis llama a su consola o terminal redis-cli, abreviatura de cliente redis en inglés."
        },
        {
            "question": "¿Cuál de estas instrucciones muestra todos los elementos de una lista llamada clientes?",
            "options": {
                "a": "LINDEX clientes 0.",
                "b": "LRANGE clientes 0 -1.",
                "c": "LRANGE clientes 0 *.",
                "d": "GET clientes 1.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "Los valores 0 y -1 indican que se muestren los valores desde la posición 0 hasta el final de la lista."
        },
        {
            "question": "¿Cuál de estas instrucciones permite añadir un elemento a la colección llamada frutas?",
            "options": {
                "a": "SADD frutas mango.",
                "b": "SADD mango frutas.",
                "c": "SMEMBERS frutas mango.",
                "d": "SISMEMBERS frutas mango.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "SADD permite añadir elementos a una colección, seguido se indica el nombre de la colección y luego el elemento a añadir."
        },
        {
            "question": "¿Qué hace la siguiente instrucción: SET user pep?",
            "options": {
                "a": "Establece un usuario en pep.",
                "b": "Crea un elemento llamado user con el valor pep.",
                "c": "Muestra el valor de user y pep.",
                "d": "Guarda el valor user en pep.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "b",
            "explanation": "SET crea un elemento, seguido se indica el nombre del elemento y luego su valor."
        },
        {
            "question": "¿Qué son las colecciones ordenadas?",
            "options": {
                "a": "Una colección cuyos elementos se ordenan por la clave.",
                "b": "Una colección cuyos elementos se ordenan por el orden en que se añaden los valores.",
                "c": "Una colección cuyos elementos se ordenan por los valores que se añaden a dicha colección, no por su clave.",
                "d": "Ninguna de las anteriores es correcta.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "c",
            "explanation": "Las colecciones ordenadas se ordenan por los valores que se añaden a dicha colección, no por su clave."
        },
        {
            "question": "El patrón pub/sub permite:",
            "options": {
                "a": "Publicar datos cada cierto tiempo en un puerto concreto.",
                "b": "Crea un canal para que los clientes se suscriban y reciban valores emitidos.",
                "c": "Publicar datos en stream para ser consumido.",
                "d": "Todas las anteriores son correctas.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Según la configuración que se le aplique al patrón, este permitirá hacer las tres operaciones que se indican previamente."
        },
        {
            "question": "Redis es una base de datos clave-valor que utiliza:",
            "options": {
                "a": "RAM y memoria flash.",
                "b": "Solo RAM.",
                "c": "RAM y memoria caché.",
                "d": "RAM SSD y Sweap.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "a",
            "explanation": "Redis posee funciones especializadas para usar tanto la memoria RAM como las memorias flash, incluso en SSD."
        },
        {
            "question": "¿Qué afirmación es verdadera?",
            "options": {
                "a": "Dentro de un cluster de Redis, un servidor determinado se denomina cliente.",
                "b": "Cada nodo puede ser un nodo primario (maestro), pero no un nodo secundario (esclavo).",
                "c": "La administración del cluster se realiza en una capa de la arquitectura del cluster de Redis.",
                "d": "El almacenamiento de datos de series de tiempo es otra tarea común en Redis.",
                "e": "Ninguna de las anteriores."
            },
            "correct": "d",
            "explanation": "Redis dispone de un módulo que permite tratar datos de series de tiempo."
        }
    ]
}

def format_questions_for_quiz_system():
    """
    Formatea las preguntas al estilo del sistema de quiz
    """
    all_formatted = []

    category_id = 10  # Empezamos desde 10 (después de las 9 categorías de MongoDB)

    for test_name, questions in TESTS_DATA.items():
        print(f"\n{'='*60}")
        print(f"Procesando: {test_name}")
        print(f"Total de preguntas: {len(questions)}")
        print(f"Categoría ID: {category_id}")

        formatted_questions = []
        for q in questions:
            formatted = {
                "category_id": category_id,
                "question_type": "conceptual",
                "question_text": q["question"],
                "option_a": q["options"]["a"],
                "option_b": q["options"]["b"],
                "option_c": q["options"]["c"],
                "option_d": q["options"]["d"],
                "option_e": q["options"].get("e", "No aplica"),
                "correct_answer": q["correct"],
                "explanation": q["explanation"],
                "dataset_reference": "N/A",
                "difficulty": "medium"
            }
            formatted_questions.append(formatted)

        all_formatted.append({
            "test_name": test_name,
            "category_id": category_id,
            "questions": formatted_questions
        })

        category_id += 1

    return all_formatted

if __name__ == "__main__":
    print("="*60)
    print("EXTRACCIÓN DE PREGUNTAS DE TESTS")
    print("="*60)

    formatted = format_questions_for_quiz_system()

    print(f"\n✅ Total de tests procesados: {len(formatted)}")
    total_questions = sum(len(t['questions']) for t in formatted)
    print(f"✅ Total de preguntas extraídas: {total_questions}")

    print("\n" + "="*60)
