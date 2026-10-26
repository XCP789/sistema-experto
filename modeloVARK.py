
hechos={ 
    ("visual", "es_un", "estilo"),
    ("auditivo", "es_un", "estilo"),
    ("lectura_escritura", "es_un", "estilo"),
    ("kinestesico", "es_un", "estilo"),
    ("multimodal", "es_un", "estilo"),

    ("visual", "requiere", "representacion_grafica"),
    ("auditivo", "requiere", "representacion_auditiva"),
    ("lectura_escritura", "requiere", "representacion_textual"),
    ("kinestesico", "requiere", "representacion_practica"),
    ("multimodal", "requiere", "varias_modalidades"),

    ("visual", "tecnica", "mapas mentales"),
    ("auditivo", "tecnica", "grabacion de audios"),
    ("lectura_escritura", "tecnica", "apuntes y resúmenes"),
    ("kinestesico", "tecnica", "practicas fisicas")
    }

def consultar_estilo(s=None, p=None, o=None):
        return [(a, b, c) for (a, b, c) in hechos 
                if s in (None, a) 
                and p in (None, b) 
                and o in (None, c)]

tecnicas_validas = {x for (x, r, y) in hechos if r == "es_un" and y == "estilo"}

condiciones_apoyo = {(x, y) for (x, r, y) in hechos if r == "requiere"}

tecnicas_efectivas = {(x, y) for (x, r, y) in hechos if r == "tecnica"}

#prueba 
if __name__ == "__main__": 
        perfil = "visual"
        print(f"'{perfil}' es un estilo de aprendizaje: {perfil in tecnicas_validas}")

        condiciones = [y for (x, y) in condiciones_apoyo if x == perfil]
        print(f"Condiciones de apoyo para '{perfil}': {condiciones}")

        tecnicas = [y for (x, y) in tecnicas_efectivas if x == perfil]
        print(f"Técnicas recomendadas para '{perfil}': {tecnicas}")
