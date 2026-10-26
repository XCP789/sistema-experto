
#hechos en tupla (sujeto, predicado, objeto)
hechos={ 
#ontologia de estilos de aprendizaje VARK
    ("visual", "es_un", "estilo"),
    ("auditivo", "es_un", "estilo"),
    ("lectura_escritura", "es_un", "estilo"),
    ("kinestesico", "es_un", "estilo"),
    ("multimodal", "es_un", "estilo"),

#condiciones de apoyo para cada estilo de aprendizaje
    ("visual", "requiere", "representacion_grafica"),
    ("auditivo", "requiere", "representacion_auditiva"),
    ("lectura_escritura", "requiere", "representacion_textual"),
    ("kinestesico", "requiere", "representacion_practica"),
    ("multimodal", "requiere", "varias_modalidades"),

#técnicas de aprendizaje efectivas para cada estilo
    ("visual", "tecnica", "mapas mentales"),
    ("auditivo", "tecnica", "grabacion de audios"),
    ("lectura_escritura", "tecnica", "apuntes y resúmenes"),
    ("kinestesico", "tecnica", "practicas fisicas")
    }

#consulta de hechos, utiliza una tupla (sujeto, predicado, objeto) con valores 
# None como comodín para cualquier valor, respondiendo diferentes consultas sobre los hechos
def consultar_estilo(s=None, p=None, o=None):
        return [(a, b, c) for (a, b, c) in hechos 
                if s in (None, a) 
                and p in (None, b) 
                and o in (None, c)]

# reglas logicas para inferir hechos a partir de los hechos existentes. 
# se extrae x, y dependiendo su relacion con el predicado r, y se guardan en un sub-conjunto

#regla 1, se extrae todas las x que sean estilos de aprendizaje 
tecnicas_validas = {x for (x, r, y) in hechos if r == "es_un" and y == "estilo"}

#regla 2, se extrae todas las x que requieran de y, y se guardan en un sub-conjunto
condiciones_apoyo = {(x, y) for (x, r, y) in hechos if r == "requiere"}

#regla 3, se extrae todas las x que tengan y como tecnica efectiva, y se guardan en un sub-conjunto
tecnicas_efectivas = {(x, y) for (x, r, y) in hechos if r == "tecnica"}

#prueba 
if __name__ == "__main__": 
        perfil = "visual"
        #pregunta si el perfil es un estilo de aprendizaje
        print(f"'{perfil}' es un estilo de aprendizaje: {perfil in tecnicas_validas}")

        #para consultar, repite la consulta por cada estilo de aprendizaje 
        # hasta que obtenga las condiciones de apoyo y técnicas recomendadas
        condiciones = [y for (x, y) in condiciones_apoyo if x == perfil]
        print(f"Condiciones de apoyo para '{perfil}': {condiciones}")

        tecnicas = [y for (x, y) in tecnicas_efectivas if x == perfil]
        print(f"Técnicas recomendadas para '{perfil}': {tecnicas}")
