
#hechos en tupla (sujeto, predicado, objeto)
hechos={ 
    # Ontología de estilos de aprendizaje VARK
    ("visual", "es_un", "estilo"),
    ("auditivo", "es_un", "estilo"),
    ("lectura_escritura", "es_un", "estilo"),
    ("kinestesico", "es_un", "estilo"),
    ("multimodal", "es_un", "estilo"),

    # Condiciones de apoyo para cada estilo de aprendizaje
    ("visual", "requiere", "representacion_grafica"),
    ("auditivo", "requiere", "representacion_auditiva"),
    ("lectura_escritura", "requiere", "representacion_textual"),
    ("kinestesico", "requiere", "representacion_practica"),
    ("multimodal", "requiere", "varias_modalidades"),

    # Técnicas de aprendizaje efectivas para cada estilo
    ("visual", "tecnica", "mapas mentales"),
    ("auditivo", "tecnica", "grabacion de audios"),
    ("lectura_escritura", "tecnica", "apuntes y resúmenes"),
    ("kinestesico", "tecnica", "practicas fisicas"),
    ("multimodal", "tecnica", "combinacion de mapas, audios y practica"),

    # Sujetos de prueba (preferencias que el motor usará para inferir)
    ("estudiante_1", "prefiere", "representacion_grafica"),
    ("estudiante_2", "prefiere", "representacion_practica"),
    ("estudiante_3", "prefiere", "varias_modalidades"),
    }

#consulta de hechos, utiliza una tupla (sujeto, predicado, objeto) con valores 
# None como comodín para cualquier valor, respondiendo diferentes consultas sobre los hechos
def consultar_estilo(s=None, p=None, o=None):
        return [(a, b, c) for (a, b, c) in hechos 
                if s in (None, a) 
                and p in (None, b) 
                and o in (None, c)]

# 2. CONSULTAS DIRECTAS Y SUBCONJUNTOS-----------------------------------------------------------------
#regla 1, se extrae todas las x que sean estilos de aprendizaje 
tecnicas_validas = {x for (x, r, y) in hechos if r == "es_un" and y == "estilo"}

#regla 2, se extrae todas las x que requieran de y, y se guardan en un sub-conjunto
condiciones_apoyo = {(x, y) for (x, r, y) in hechos if r == "requiere"}

#regla 3, se extrae todas las x que tengan y como tecnica efectiva, y se guardan en un sub-conjunto
tecnicas_efectivas = {(x, y) for (x, r, y) in hechos if r == "tecnica"}

# 3. REGLAS DE INFERENCIA (Cláusulas de Horn: cabeza <- cuerpo)-----------------------------------------------
reglas = [
    # Regla 1: Si ?X prefiere ?R, y ?E es un estilo que requiere ?R -> ?X tiene estilo ?E
    {
        "cabeza": ("?X", "tiene_estilo", "?E"),
        "cuerpo": [
            ("?X", "prefiere", "?R"),
            ("?E", "es_un", "estilo"),
            ("?E", "requiere", "?R")
        ]
    },
    # Regla 2: Si ?X tiene estilo ?E, y ?E tiene tecnica ?T -> recomendar ?T a ?X
    {
        "cabeza": ("?X", "recomendar_tecnica", "?T"),
        "cuerpo": [
            ("?X", "tiene_estilo", "?E"),
            ("?E", "tecnica", "?T")
        ]
    }
]

# 4. MOTOR DE INFERENCIA (Unificación y Resolución SLD)---------------------
def es_variable(termino):
    return isinstance(termino, str) and termino.startswith("?")

def resolver_valor(termino, sustituciones):
    """Sigue la cadena de sustituciones hasta encontrar el valor final."""
    while es_variable(termino) and termino in sustituciones:
        termino = sustituciones[termino]
    return termino

def aplicar_sustitucion(tupla, sustituciones):
    return tuple(resolver_valor(elem, sustituciones) for elem in tupla)

def unificar(meta, objetivo, sustituciones):
    """Empareja dos tuplas (sujeto, predicado, objeto)."""
    nueva_sust = sustituciones.copy()
    for m, o in zip(meta, objetivo):
        m = resolver_valor(m, nueva_sust)
        o = resolver_valor(o, nueva_sust)

        if m == o:
            continue
        elif es_variable(m):
            nueva_sust[m] = o
        elif es_variable(o):
            nueva_sust[o] = m
        else:
            return None  # Fallo en la unificación
    return nueva_sust

def resolver_sld(metas, sustituciones=None):
    """Algoritmo SLD: encadenamiento hacia atrás con backtracking."""
    if sustituciones is None:
        sustituciones = {}

    # Caso base: no quedan metas pendientes (éxito)
    if not metas:
        yield sustituciones
        return

    # 1. Selección (izquierda a derecha)
    meta_actual = aplicar_sustitucion(metas[0], sustituciones)
    metas_restantes = metas[1:]

    # 2. Búsqueda en hechos
    for hecho in hechos:
        sust = unificar(meta_actual, hecho, sustituciones)
        if sust is not None:
            yield from resolver_sld(metas_restantes, sust)

    # 3. Búsqueda en reglas
    for regla in reglas:
        sust = unificar(meta_actual, regla["cabeza"], sustituciones)
        if sust is not None:
            nuevas_metas = regla["cuerpo"] + metas_restantes
            yield from resolver_sld(nuevas_metas, sust)

#prueba ------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # --- Prueba original sobre la ontología ---
    perfil = "visual"
    print("=== Consulta directa a la base de hechos ===")
    print(f"'{perfil}' es un estilo de aprendizaje: {perfil in tecnicas_validas}")
    print(f"Condiciones de apoyo para '{perfil}': {[y for (x, y) in condiciones_apoyo if x == perfil]}")
    print(f"Técnicas recomendadas para '{perfil}': {[y for (x, y) in tecnicas_efectivas if x == perfil]}")

    # --- Prueba del Motor de Inferencia SLD ---
    print("\n=== Resultados del Motor de Inferencia SLD ===")
    sujetos = ["estudiante_1", "estudiante_2", "estudiante_3"]

    for sujeto in sujetos:
        print(f"\nAnálisis para: {sujeto}")
        
        # Inferir estilo
        for sol in resolver_sld([(sujeto, "tiene_estilo", "?Estilo")]):
            print(f"  -> Estilo inferido: {resolver_valor('?Estilo', sol)}")

        # Inferir técnica recomendada (encadena Regla 2 -> Regla 1 -> Hechos)
        for sol in resolver_sld([(sujeto, "recomendar_tecnica", "?Tecnica")]):
            print(f"  -> Técnica recomendada: {resolver_valor('?Tecnica', sol)}")