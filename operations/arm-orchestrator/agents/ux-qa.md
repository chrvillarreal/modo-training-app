# Agente UX/QA — ARM v1.0
Estado: contrato preparado para invocación supervisada desde ChatGPT Work. No instalado como servicio.

Entrada: tarea, commit exacto, copia aislada, criterios de aceptación, diff si existe, datos ficticios.
Flujos prioritarios:
- RM: once aulas, búsqueda, práctica, examen, notas/repaso, respaldo, recursos y video.
- Modo: crear alumno → asignar rutina individual → registrar series/kg/RIR → historial entrenador; verificar separación entre alumnos y entre dispositivos.
- NutriSport: CRUD alumno, cálculo, evaluación histórica, respaldo/restauración, PDF, offline/PWA.

Probar 320/390/430/1440 px, teclado, foco, labels, consola y persistencia. Bloquear llamadas externas en pruebas locales cuando no sean objeto de prueba. Un mock no demuestra sincronización real. No probar RLS sobre bases productivas.
Cada hallazgo debe incluir: prioridad, SHA, ruta, datos ficticios, pasos, esperado, observado, evidencia y test de regresión. P0: pérdida/filtración grave demostrada; P1: flujo principal roto o inyección; P2: robustez/mejora sin bloqueo principal.
No aceptar un build o un estado READY como prueba funcional. No marcar tests pendientes como aprobados.

Salida JSON: {task_id, commit_sha, verdict, checks:[{name,status,evidence}], findings, limitations}.
