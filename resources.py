from flask_restful import Resource, reqparse, fields, marshal_with, abort
import controlador_juegos  # Importamos tu controlador existente

# --- Configuración de Serialización (Cómo se verá el JSON) ---
juego_fields = {
    'id': fields.Integer,
    'titulo': fields.String,
    'genero': fields.String,
    'plataforma': fields.String,
    'precio': fields.Float
}

# --- Configuración del Parser (Validación de datos de entrada) ---
parser = reqparse.RequestParser()
parser.add_argument('titulo', type=str, required=True, help="El título es obligatorio")
parser.add_argument('genero', type=str, required=True, help="El género es obligatorio")
parser.add_argument('plataforma', type=str, required=True, help="La plataforma es obligatoria")
parser.add_argument('precio', type=float, required=True, help="El precio es obligatorio")

# --- Helper: Convertir Tupla a Diccionario ---
def tupla_a_dict(juego_tupla):
    if not juego_tupla:
        return None
    return {
        'id': juego_tupla[0],
        'titulo': juego_tupla[1],
        'genero': juego_tupla[2],
        'plataforma': juego_tupla[3],
        'precio': juego_tupla[4]
    }

# === RECURSO: Lista de Juegos (GET, POST) ===
class JuegoList(Resource):
    @marshal_with(juego_fields)
    def get(self):
        """Obtiene la lista completa de videojuegos."""
        juegos_raw = controlador_juegos.obtener_juegos()
        # Convertimos la lista de tuplas a lista de diccionarios
        juegos = [tupla_a_dict(j) for j in juegos_raw]
        return juegos, 200

    @marshal_with(juego_fields)
    def post(self):
        """Crea un nuevo videojuego."""
        args = parser.parse_args()
        # Insertamos usando tu controlador existente
        controlador_juegos.insertar_juego(args['titulo'], args['genero'], args['plataforma'], args['precio'])
        
        # NOTA: Tu controlador actual no devuelve el ID creado. 
        # Para una API real, deberías modificar insertar_juego para retornar el ID.
        # Aquí devolvemos los datos recibidos como confirmación (simulando el objeto creado).
        nuevo_juego = args
        nuevo_juego['id'] = 0 # Placeholder porque no tenemos el ID real
        return nuevo_juego, 201

# === RECURSO: Juego Individual (GET, PUT, DELETE) ===
class JuegoResource(Resource):
    @marshal_with(juego_fields)
    def get(self, id):
        """Obtiene un videojuego por su ID."""
        juego_tupla = controlador_juegos.obtener_juego_por_id(id)
        if not juego_tupla:
            abort(404, message=f"El juego con id {id} no existe")
        return tupla_a_dict(juego_tupla), 200

    @marshal_with(juego_fields)
    def put(self, id):
        """Actualiza un videojuego existente."""
        args = parser.parse_args()
        # Verificamos si existe antes de actualizar
        juego_tupla = controlador_juegos.obtener_juego_por_id(id)
        if not juego_tupla:
            abort(404, message=f"El juego con id {id} no existe")
            
        controlador_juegos.actualizar_juego(
            args['titulo'], args['genero'], args['plataforma'], args['precio'], id
        )
        
        # Devolvemos el juego actualizado
        juego_actualizado = args
        juego_actualizado['id'] = id
        return juego_actualizado, 200

    def delete(self, id):
        """Elimina un videojuego."""
        juego_tupla = controlador_juegos.obtener_juego_por_id(id)
        if not juego_tupla:
            abort(404, message=f"El juego con id {id} no existe")
            
        controlador_juegos.eliminar_juego(id)
        return '', 204