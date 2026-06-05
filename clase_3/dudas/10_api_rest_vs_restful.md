# ¿Qué es una API REST y qué significa RESTful?

En casi todos los entornos de desarrollo modernos vas a escuchar sobre "APIs REST" o sistemas "RESTful", pero estas palabras suelen confundir al inicio. Vamos a desglosar qué significa cada cosa con un ejemplo sencillo de restaurante.

## 1. ¿Qué es una API? (El Mesero)

Imagina que estás en un restaurante.
- Tú eres el **Cliente** (la página web o aplicación móvil).
- La cocina es el **Servidor** (o base de datos) donde está la magia.
- **La API es el mesero**. Tú no vas a la cocina a hacerte la hamburguesa; tú le pides al mesero, él lleva tu orden a la cocina, y luego te trae la hamburguesa lista. 

Una API (Interfaz de Programación de Aplicaciones) es simplemente *el mensajero* que comunica un programa con otro.

## 2. ¿Qué es REST? (Las reglas del restaurante)

Podrías tener un restaurante donde el cliente grita su pedido, otro donde la orden se pasa por debajo de la puerta, u otro donde se usa lenguaje de señas. Sería un caos.

**REST** (Representational State Transfer) es un **conjunto arquitectónico de 6 reglas fundamentales**. Si un sistema sigue estas reglas, todo funciona en armonía:

1. **Interfaz Uniforme (Uniform Interface)**: Todos debemos hablar el mismo idioma universal. En lugar de inventar palabras, usamos los verbos estándar de la web (HTTP):
   - `GET`: "Tráigame esto" (Leer data)
   - `POST`: "Cree esta orden nueva" (Guardar nueva data)
   - `PUT / PATCH`: "Cámbieme estos ingredientes" (Actualizar data)
   - `DELETE`: "Cancele mi orden" (Eliminar data)
2. **Falta de estado (Stateless)**: Al mesero se le olvida quién eres en cada interacción. Cada vez que le hablas, tu mensaje debe llevar TODA la información para que entienda (tu nombre de mesa, el pedido exacto). El servidor no guarda memoria de tu "charla" continua; cada petición es un mundo nuevo.
3. **Cliente-Servidor (Client-Server)**: Tú (en tu mesa) te separas totalmente de la cocina (base de datos). El cliente no necesita saber cómo se fríen las papas, y a la cocina no le importa cómo luces vestido. Son mundos independientes que solo se conectan por el mesero.
4. **Cacheable (Uso de Caché)**: Si pides algo que nunca cambia (ejemplo, "tráigame el menú"), el mesero no va hasta la cocina a que impriman uno nuevo; saca uno de su delantal (Caché). La API debe avisar si una respuesta se puede "guardar y reutilizar" para ahorrar tiempo.
5. **Sistema en Capas (Layered System)**: Entre el mesero y la cocina puede haber un cajero, un supervisor o un sistema de seguridad probando el plato. A ti como cliente no te importa quién está en medio, tú solo te comunicas con el mesero y recibes tu comida igual.
6. **Código bajo demanda (Opcional)**: En raras ocasiones, el servidor no solo manda datos, sino pequeños "scripts" ejecutables al cliente (pero hoy en día casi no se usa para mantener todo simple).

## 3. Entonces, ¿qué significa RESTful?

Es súper sencillo:
- **REST** es la teoría (el libro de reglas).
- **RESTful** es el adjetivo que se le pone a algo que cumple esas reglas.

Si una API sigue al pie de la letra los verbos `GET/POST/PUT/DELETE` y opera sin estado, entonces decimos que es **una API RESTful**. 

En nuestras clases pasadas y actuales, la API que creamos para nuestros "items" es **RESTful**, porque respeta este orden universal para crear, leer, actualizar y eliminar recursos apoyándose en URLs lógicas en lugar de inventar métodos desordenados.
