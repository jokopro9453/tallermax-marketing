# Piloto de anuncios de Meta

Claude maneja la campaña con `scripts/anuncios.py`: lee los resultados todos los
días y **pausa** lo que no rinde. Nunca crea campañas, nunca cambia un
presupuesto ni el límite de gasto, y sólo mira las campañas cuyo nombre empieza
con **`TMX`**. Las reglas y los números están en `campana.json`, y el script los
explica arriba del todo.

```bash
python3 scripts/anuncios.py revisar --cuenta act_<id>            # sólo informa
python3 scripts/anuncios.py revisar --cuenta act_<id> --aplicar  # informa y pausa
python3 scripts/anuncios.py activar <id_anuncio> --cuenta act_<id>
python3 scripts/probar_anuncios.py                               # 22 pruebas, sin tocar Meta
```

## Tres seguros, de afuera hacia adentro

1. **Límite de gasto de la cuenta, en $35.000.** Lo aplica Meta, y el token de
   Claude no puede cambiarlo porque no tiene permiso sobre los pagos.
2. **Presupuesto TOTAL de la campaña, en $35.000**, con fecha de término. Un
   presupuesto total no se pasa nunca. Si alguien lo cambia a diario o lo sube
   sobre el tope, el script pausa la campaña.
3. **El script sólo pausa solo.** Activar un anuncio lo hace sólo si se le pide
   expresamente, y sólo dentro del tope y antes de la fecha de término.

## Configuración (una vez, la hace Joaquín)

**1. Límite de gasto.** Administrador de anuncios → *Facturación y pagos* →
*Configuración de pagos* → *Límite de gasto de la cuenta* → **$35.000**. Cuenta
desde el momento en que se pone.

**2. La app, conectada al portafolio.** En developers.facebook.com, en la misma
app del token de Instagram, agregar el caso de uso **«Crear y administrar
anuncios con la API de marketing»**. La app tiene que estar en el portafolio
comercial: *Configuración del negocio → Cuentas → Apps*.

**3. Usuario del sistema.** En business.facebook.com/settings → *Usuarios →
Usuarios del sistema → Agregar*:
* Nombre `claude-anuncios`, rol **Empleado**.
* *Asignar activos → Cuentas publicitarias →* la cuenta de Tallermax, con
  **«Administrar campañas»** y nada más. Sin «Administrar cuenta
  publicitaria»: así el token no puede tocar pagos ni el límite de gasto.
* *Asignar activos → Apps →* la app.
* *Generar token:* la app, caducidad **Nunca**, permisos **`ads_management`** y
  **`ads_read`**. Meta lo muestra **una sola vez**: copiarlo directo al paso 4,
  sin pegarlo en ningún chat.

**4. Un entorno aparte en la nube.** En claude.ai → Code → entornos, crear
`tallermax-anuncios` (separado del de Instagram, para que el publicador no
pueda tocar los anuncios ni el piloto pueda publicar):
* *Network secret:* host **`graph.facebook.com`**, cabecera `Authorization`,
  valor `Bearer <el token>`.
* *Acceso a la red:* permitir `graph.facebook.com`.

**5. Pasarle a Claude el número de la cuenta publicitaria** (`act_…`). Aparece
arriba a la izquierda en el Administrador de anuncios. No es secreto.

Con eso Claude crea la rutina diaria y hace una primera pasada **sin
`--aplicar`**, para comprobar que lee bien antes de que pueda pausar nada.

## La campaña (la crea Joaquín en el Administrador de anuncios)

| | |
|---|---|
| Nombre | **`TMX · Talleres fundadores`**. El prefijo `TMX` es obligatorio: es lo que el piloto reconoce. |
| Objetivo | **Interacción** → dónde: **Apps de mensajes → WhatsApp** → meta: maximizar conversaciones |
| Presupuesto | **Presupuesto de campaña Advantage+, TOTAL, $35.000** (no diario) |
| Fechas | **lun 27 oct 00:00 → jue 13 nov 23:59** |
| Horario | Programar anuncios: lun–vie **12:30–14:30** y **19:30–22:30**, sáb **10:00–13:00** |
| Un conjunto | Quilpué, Villa Alemana, Viña del Mar y Valparaíso (+15 km). 28 a 60 años. Sin intereses: el anuncio filtra solo. Ubicaciones Advantage+. |
| Anuncios | **Usar publicación existente**: reel «Ingreso con fotos», carrusel «Tu sistema hoy» y reel «Evidencia por correo». **Un solo destino: WhatsApp** (si se marca más de uno, sale el error #2446493). |
| Mensaje inicial | «Hola, quiero probar Tallermax 7 días gratis» |
