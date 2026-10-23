# ARM Orchestrator v1.0 — entrega local supervisada
Python 3.12+, biblioteca estándar; sin cuentas adicionales, sin claves API, sin consumo de modelos pagos.

## Qué funciona
Registro SQLite de los tres proyectos, tareas P0/P1/P2, asignación determinista Desarrollo/UX-QA, estados de ejecución, evidencias con SHA-256, solicitudes de aprobación vinculadas al contenido y SHA, expiración y eventos encadenados con hash. Exportación JSON.
ChatGPT Work actúa como coordinador humano-supervisado y usa las integraciones existentes. Este paquete NO ejecuta agentes LLM ni tareas periódicas por sí mismo.

## Ejecutar
Desde la carpeta descomprimida:
```bash
python3 -m unittest discover -s tests -v
python3 arm.py --db arm.sqlite status
python3 arm.py --db arm.sqlite verify
python3 arm.py --db demo.sqlite task --project rm-training --title 'Revisar flujo' --priority P1 --action review --branch audit/review --sha 24a584cb520c9d8e4f4e51e0ee7b0e5d6f0fd312
```
`start TASK_ID` abre una ejecución; `finish RUN_ID passed|failed|blocked evidencia.log` registra el resultado del operador. No ejecuta comandos y no verifica automáticamente que un log sea verdadero: corresponde a QA adjuntar resultados reales.
`request-approval TASK_ID` solicita revisión de una tarea sensible. La API Python `decide` registra referencia de una decisión humana; no es autenticación de identidad y no habilita un ejecutor externo. En v1 ninguna aprobación local dispara pushes, despliegues ni publicaciones.

## Seguridad y límites
Las tareas desconocidas se rechazan. Main, merge, producción, datos productivos, gastos y comunicaciones están bloqueados. Los datos son locales y no están cifrados: no almacenar secretos ni información de alumnos. Los hashes detectan cambios accidentales; una persona con acceso al archivo puede reescribir la cadena, por lo que no es una bitácora criptográficamente autenticada.
Los tests de los productos se corrieron en copias/worktrees separados; no hubo contenedor de seguridad de red: bwrap no permite crear namespaces en este host. No presentar esa separación de archivos como aislamiento fuerte.
No hay sincronización, cron, servidor público ni permisos nuevos. El SQLite incluido contiene la auditoría de esta entrega y aprobaciones pendientes, ninguna autorización concedida.

## Siguiente implementación
1. Aprobar el destino persistente del código ARM y el alcance de publicación en rama; conservar main intacta.
2. Adaptador de lectura GitHub/Vercel con paginación, SHA fijo y manejo explícito de acceso denegado.
3. Ejecutor de tests en sandbox de red y filesystem real, con timeout y lista cerrada de comandos; no ejecutar scripts arbitrarios del repo sin revisión.
4. Invocación de Desarrollo y UX/QA con sus contratos, salida estructurada y revisión cruzada. Usar ChatGPT Work sin añadir API de pago.
5. Integrar aprobación autenticada por acción/diff/SHA, un uso y vencimiento, antes de habilitar cualquier escritura remota.
6. Sólo después: agente de Producto/Backlog; más tarde Contenido/Comercial, sin envío automático.

Ver INFORME.md, backlog.json, evidence/, agents/ y snapshot.json.
