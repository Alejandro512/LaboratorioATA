## 1. administrators

| Campo          | Tipo      | Descripción                                                                                     | Rol / Función                                                | Relación |
|----------------|-----------|-------------------------------------------------------------------------------------------------|--------------------------------------------------------------|----------|
| `_id`          | ObjectId  | Identificador único generado por MongoDB para cada administrador.                               | Clave primaria interna para la colección.                   | —        |
| `name`         | String    | Nombre de pila del administrador (p.ej. “María”).                                               | Mostrar en listados y búsquedas.                            | —        |
| `lastname`     | String    | Apellidos del administrador (p.ej. “González Pérez”).                                           | Mostrar en listados y búsquedas.                            | —        |
| `email`        | String    | Correo electrónico único usado como login.                                                      | Credencial de inicio de sesión y notificaciones.            | —        |
| `salt`         | String    | Semilla única para generar el hash de la contraseña (bcrypt).                                   | Asegurar que cada hash sea único.                           | —        |
| `passwordHash` | String    | Contraseña cifrada usando `salt`.                                                               | Verificar identidad al iniciar sesión.                      | —        |
| `role`         | String    | Siempre `"administrator"`, define nivel de acceso.                                              | Control de permisos en la app.                              | —        |
| `createdAt`    | Date      | Fecha y hora en que se creó la cuenta (ISO 8601).                                               | Auditoría de creación de cuentas.                           | —        |
| `status`       | String    | Estado de la cuenta: `active`, `suspended` o `deleted`.                                         | Controlar si puede autenticarse o no.                       | —        |

---

## 2. technicians

| Campo          | Tipo      | Descripción                                                                                     | Rol / Función                                                | Relación |
|----------------|-----------|-------------------------------------------------------------------------------------------------|--------------------------------------------------------------|----------|
| `_id`          | ObjectId  | Identificador único generado por MongoDB para cada técnico.                                     | Clave primaria interna para la colección.                   | —        |
| `name`         | String    | Nombre de pila del técnico (p.ej. “Juan”).                                                      | Mostrar en listados y asignaciones.                         | —        |
| `lastname`     | String    | Apellidos del técnico (p.ej. “Ramírez López”).                                                  | Mostrar en listados y asignaciones.                         | —        |
| `email`        | String    | Correo electrónico único usado como login.                                                      | Credencial de inicio de sesión y notificaciones.            | —        |
| `phone`        | String    | Número de contacto (p.ej. “+593987654321”).                                                     | Llamadas o SMS para asignaciones urgentes.                  | —        |
| `salt`         | String    | Semilla única para generar el hash de la contraseña.                                            | Asegurar que cada hash sea único.                           | —        |
| `passwordHash` | String    | Contraseña cifrada usando `salt`.                                                               | Verificar identidad al iniciar sesión.                      | —        |
| `role`         | String    | Siempre `"technician"`, define nivel de acceso.                                                 | Control de permisos en la app.                              | —        |
| `createdAt`    | Date      | Fecha y hora en que se dio de alta el técnico.                                                  | Auditoría de creación de cuentas.                           | —        |
| `status`       | String    | Estado de la cuenta: `active`, `suspended` o `deleted`.                                         | Controlar si puede autenticarse o no.                       | —        |

---

## 3. users

| Campo          | Tipo      | Descripción                                                                                     | Rol / Función                                                | Relación |
|----------------|-----------|-------------------------------------------------------------------------------------------------|--------------------------------------------------------------|----------|
| `_id`          | ObjectId  | Identificador único generado por MongoDB para cada usuario.                                     | Clave primaria interna para la colección.                   | —        |
| `name`         | String    | Nombre de pila del usuario (p.ej. “Ana”).                                                       | Mostrar en listados y notificaciones.                       | —        |
| `lastname`     | String    | Apellidos del usuario (p.ej. “Morales Vega”).                                                   | Mostrar en listados y notificaciones.                       | —        |
| `email`        | String    | Correo electrónico único usado como login.                                                      | Credencial de inicio de sesión y notificaciones.            | —        |
| `salt`         | String    | Semilla única para generar el hash de la contraseña.                                            | Asegurar que cada hash sea único.                           | —        |
| `passwordHash` | String    | Contraseña cifrada usando `salt`.                                                               | Verificar identidad al iniciar sesión.                      | —        |
| `company`      | String    | Nombre de la empresa o cliente (p.ej. “AgroIndustrial S.A.”).                                   | Segmentar datos y permisos por compañía.                    | —        |
| `role`         | String    | Siempre `"user"`, define nivel de acceso.                                                       | Control de permisos en la app.                              | —        |
| `createdAt`    | Date      | Fecha y hora de registro del usuario.                                                           | Auditoría de creación de cuentas.                           | —        |
| `status`       | String    | Estado de la cuenta: `active`, `suspended` o `deleted`.                                         | Controlar si puede autenticarse o no.                       | —        |

---

## 4. sensors

| Campo            | Tipo       | Descripción                                                                                    | Rol / Función                                              | Relación        |
|------------------|------------|------------------------------------------------------------------------------------------------|------------------------------------------------------------|-----------------|
| `_id`            | ObjectId   | Identificador único generado por MongoDB para cada sensor.                                     | Clave primaria interna para la colección.                 | —               |
| `serial`         | String     | Número de serie único asignado por el fabricante (p.ej. “SN-00123”).                           | Identificar físicamente el dispositivo.                    | —               |
| `type`           | String     | Tipo de medición (`humidity`, `temperature`, etc.).                                            | Diferenciar comportamiento y unidades de lectura.          | —               |
| `location`       | String     | Ubicación textual o coordenadas GPS (p.ej. “-0.1807, -78.4678”).                                | Mostrar en mapas y filtrar lecturas por zona.              | —               |
| `ownerUserId`    | ObjectId   | Referencia al propietario o responsable del sensor.                                            | Asociar sensor a un cliente.                               | → `users._id`   |
| `installedAt`    | Date       | Fecha y hora de instalación del sensor.                                                        | Calcular antigüedad y programar mantenimientos.            | —               |
| `status`         | String     | Estado operativo (`online`, `offline`, `maintenance`).                                         | Definir si acepta lecturas o requiere atención.            | —               |
| `thresholds`     | Object     | Objeto con `{ min: Number, max: Number }` que define límites para generar alertas.             | Detectar valores fuera de rango automáticamente.           | —               |

---

## 5. sensorReadings

| Campo        | Tipo              | Descripción                                                                                 | Rol / Función                                               | Relación                  |
|--------------|-------------------|---------------------------------------------------------------------------------------------|-------------------------------------------------------------|---------------------------|
| `_id`        | ObjectId          | Identificador único generado por MongoDB para cada lectura.                                 | Clave primaria interna para la colección.                  | —                         |
| `sensorId`   | ObjectId          | ID del sensor que produjo la lectura (p.ej. `ObjectId("…")`).                               | Saber a qué dispositivo pertenece cada medición.            | → `sensors._id`           |
| `timestamp`  | Date              | Fecha y hora exacta de la medición.                                                        | Ordenar cronológicamente las lecturas.                      | —                         |
| `value`      | Number            | Valor cuantitativo medido (p.ej. `23.5`).                                                  | Analizar tendencias y compararlo con umbrales.              | —                         |
| `unit`       | String            | Unidad de medida (`%`, `°C`, `ppm`, etc.).                                                 | Interpretar correctamente el valor registrado.              | —                         |
| `quality`    | String            | Estado de calidad de la lectura (`ok`, `suspect`, `calibration_needed`).                   | Filtrar o ignorar lecturas de baja confianza.               | —                         |
| `alertId`    | ObjectId \| null  | Si la lectura disparó una alerta, referencia su `_id`; si no, `null`.                      | Vincular lecturas con eventos de alerta.                    | → `alerts._id` opcional   |

---

## 6. alerts

| Campo             | Tipo              | Descripción                                                                                       | Rol / Función                                                   | Relación                                                   |
|-------------------|-------------------|---------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|------------------------------------------------------------|
| `_id`             | ObjectId          | Identificador único generado por MongoDB para cada alerta.                                        | Clave primaria interna para la colección.                      | —                                                          |
| `sensorId`        | ObjectId          | ID del sensor que originó la alerta.                                                              | Conocer qué dispositivo tuvo el incidente.                     | → `sensors._id`                                            |
| `triggerReadingId`| ObjectId \| null  | ID de la lectura que disparó la alerta; si fue manual, `null`.                                     | Vincular el evento con la causa exacta.                        | → `sensorReadings._id` opcional                           |
| `severity`        | String            | Nivel de gravedad (`info`, `warning`, `critical`).                                                | Priorizar atención según criticidad.                           | —                                                          |
| `message`         | String            | Descripción detallada del incidente (p.ej. “Temperatura > 50 °C”).                               | Informar al equipo de soporte y a los usuarios.                | —                                                          |
| `state`           | String            | Estado actual de la alerta (`open`, `acknowledged`, `resolved`).                                  | Controlar flujo de resolución y notificaciones.                | —                                                          |
| `createdAt`       | Date              | Fecha y hora de creación de la alerta.                                                            | Auditoría temporal de eventos.                                 | —                                                          |
| `resolvedAt`      | Date \| null      | Fecha y hora en que la alerta fue marcada como resuelta; si sigue abierta, `null`.                | Calcular tiempos de respuesta y SLA.                           | —                                                          |

---

## 7. tickets

| Campo            | Tipo             | Descripción                                                                                  | Rol / Función                                                    | Relación                   |
|------------------|------------------|----------------------------------------------------------------------------------------------|------------------------------------------------------------------|----------------------------|
| `_id`            | ObjectId         | Identificador único generado por MongoDB para cada ticket.                                   | Clave primaria interna para la colección.                       | —                          |
| `requesterId`    | ObjectId         | ID del usuario que solicitó el ticket.                                                       | Conectar ticket con el cliente afectado.                         | → `users._id`             |
| `assignedTechId` | ObjectId         | ID del técnico asignado para resolver el ticket.                                            | Saber quién es responsable de la intervención.                   | → `technicians._id`       |
| `alertId`        | ObjectId         | ID de la alerta que motivó este ticket.                                                     | Contextualizar problema en un evento previo.                     | → `alerts._id`            |
| `subject`        | String           | Asunto breve para identificar el problema (p.ej. “Fallo de sensor”).                        | Listados y filtros rápidos.                                      | —                          |
| `description`    | String           | Descripción extensa del problema proporcionada por el usuario.                              | Proveer detalle para diagnóstico.                                | —                          |
| `priority`       | String           | Nivel de prioridad (`low`, `medium`, `high`, `critical`).                                   | Ordenar cola de trabajo según urgencia.                          | —                          |
| `status`         | String           | Estado del ticket (`open`, `in_progress`, `resolved`, `closed`).                            | Controlar ciclo de vida y notificaciones.                       | —                          |
| `history`        | Array            | Array de objetos que registra cambios de estado y comentarios (`{ date, userId, note }`).   | Auditar acciones sobre el ticket.                               | —                          |
| `meeting`        | Object           | `{ date: Date, link: String }` para agendar videollamadas de soporte.                      | Facilitar coordinación remota.                                   | —                          |
| `createdAt`      | Date             | Fecha y hora de creación del ticket.                                                        | Auditoría temporal de solicitudes.                               | —                          |

---

## 8. maintenanceLogs

| Campo           | Tipo       | Descripción                                                                                  | Rol / Función                                                    | Relación                       |
|-----------------|------------|----------------------------------------------------------------------------------------------|------------------------------------------------------------------|--------------------------------|
| `_id`           | ObjectId   | Identificador único generado por MongoDB para cada registro de mantenimiento.                | Clave primaria interna para la colección.                       | —                              |
| `sensorId`      | ObjectId   | ID del sensor intervenido.                                                                   | Registrar qué dispositivo recibió servicio.                     | → `sensors._id`               |
| `performedBy`   | ObjectId   | ID del técnico que realizó el mantenimiento.                                                 | Rastrear responsable de la intervención.                        | → `technicians._id`           |
| `type`          | String     | Tipo de mantenimiento: `preventive` o `corrective`.                                          | Diferenciar acciones planificadas vs. reactivas.                | —                              |
| `notes`         | String     | Detalles y observaciones sobre la intervención.                                             | Documento para auditoría y seguimiento.                         | —                              |
| `partsReplaced` | Array      | Lista de piezas reemplazadas durante el servicio (p.ej. `[“sensor cap”, “battery”]`).      | Control de inventario y coste.                                  | —                              |
| `startDate`     | Date       | Fecha y hora de inicio de la intervención.                                                  | Calcular duración y programación de recursos.                   | —                              |
| `endDate`       | Date       | Fecha y hora de fin de la intervención.                                                     | Calcular duración y coste.                                      | —                              |
| `performedAt`   | Date       | Fecha y hora en que el registro fue guardado en la base de datos.                           | Auditoría de registro de eventos.                               | —                              |

---

## 9. reports  *DEFINIR BIEN PARA LA BDD QUE DEBE LLEVAR EL REWPORTE Y COMO ALMACENAR*

| Campo             | Tipo        | Descripción                                                                                  | Rol / Función                                                    | Relación                                                     |
|-------------------|-------------|----------------------------------------------------------------------------------------------|------------------------------------------------------------------|--------------------------------------------------------------|
| `_id`             | ObjectId    | Identificador único generado por MongoDB para cada reporte.                                  | Clave primaria interna para la colección.                       | —                                                            |
| `generatedById`   | ObjectId    | ID de quien solicitó o generó el reporte.                                                    | Indicar autoría del documento.                                  | → `administrators._id` / `technicians._id` / `users._id`    |
| `generatedByRole` | String      | Rol de quien generó el reporte (`administrator`, `technician`, `user`).                      | Validar permisos de acceso a datos.                             | —                                                            |
| `parameters`      | Object      | Parámetros usados para generar el reporte (p.ej. fechas, sensores, filtros).                 | Reproducir condiciones exactas de generación.                   | —                                                            |
| `fileUrl`         | String      | Ruta o URL donde se almacenó el archivo generado (p.ej. enlace a S3).                         | Acceder al documento final.                                     | —                                                            |
| `format`          | String      | Formato de salida del archivo (`pdf`, `csv`, `xlsx`).                                        | Saber cómo procesar o descargar el archivo.                     | —                                                            |
| `createdAt`       | Date        | Fecha y hora en que se creó el registro de reporte.                                           | Auditoría temporal de generados.                                | —                                                            |

---
## Manejo seguro de `salt` + `passwordHash`

1. **Generar un salt único por usuario**  
   ```js
   import bcrypt from 'bcrypt';
   const salt = await bcrypt.genSalt(12);       // 12 rondas ≈ buen balance seguridad/rendimiento
   const passwordHash = await bcrypt.hash(plainPassword, salt);
