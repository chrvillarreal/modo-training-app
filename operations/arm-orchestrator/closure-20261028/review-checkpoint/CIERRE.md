# Cierre de fase ARM — 28/10/2026, Argentina

Referencia: chrvillarreal/modo-training-app PR #2, commit c86bdfc133a1191d446a84984d758e50975f75fe. Todas las modificaciones de esta fase son locales. No se publicaron commits, no se fusionaron PR, no se modificaron producción ni datos productivos, no se hicieron llamadas a modelos de pago y no se duplicó el coordinador.

## Criterios de aceptación

1. **Flujo Desarrollo: cumplido en modo supervisado.** Tarea registrada, reproducción negativa, cambio mínimo en worktree independiente, regresión, evidencia con hash y revisión UX/QA. La CLI completa crea una tarea draft_patch, la asigna a development, abre run, registra evidencia, termina, exporta estado y verifica sin modificar el SQLite. No se presenta como agente automático instalado.
2. **UX/QA ARM: cumplido localmente.** El commit publicado pasa 21 tests. La revisión encontró creación accidental de SQLite al verificar rutas erróneas, datos corruptos sin JSON estable, esquema ajeno aceptado y una evidencia omitida. Borrador corregido: 27/27. Recuperación de evidencia exacta verificada; no se reescribe historial. Revisión por el mismo operador, con fase y scripts distintos; no es aprobación humana independiente.
3. **Backlog: los 11 ítems revisados.** Estado y siguiente acción en backlog-closure.json, más cuatro hallazgos nuevos. Las pruebas locales posibles y los borradores acotados están terminados. Los pendientes requieren publicación B, decisión de producto/editorial, acceso remoto o un diseño de integración revisado.
4. **Trazabilidad: cumplida con límites explícitos.** Esta fase tiene 78 ejecuciones registradas: {"passed": 64, "failed": 12, "blocked": 1, "running": 1}. Son comandos, inspecciones y pruebas, no un conteo de tests. Se conservan fallos y reproducciones negativas. executions.jsonl contiene comandos y SHA base; snapshot.json añade eventos y bloqueos del conector; candidate-hashes.json fija los borradores modificados. La cadena verifica.
5. **Informe de cierre y propuestas: cumplido.** Publicación de cualquier cambio nuevo sigue pendiente. No se reutiliza la aprobación de la fase anterior.

## Resultados reejecutados ahora

| Componente / versión | Resultado |
|---|---|
| ARM c86bdfc publicado | 21/21 antes del nuevo borrador |
| ARM borrador local | 27/27; verify sólo lectura y salida JSON consistente ante errores |
| RM 24a584c | 7/7 unitarias; 32 comprobaciones de curso; preview 24 combinaciones sin overflow y notas persistentes; 5 checks de teclado/menú/búsqueda |
| RM 77c90df, PR2 divergente | 16/16 unitarias; tres suites browser aprobadas en 320/360/390/430/1365, más storage e inyección según suite |
| Modo 0bb4924 | Cuatro defectos reproducidos; original falla regresión de inyección; borrador MODO03/04 pasa 6 comprobaciones |
| Modo 1.3 9f8b2c3 | 6 smoke checks: cuatro anchos, copias de asignación independientes y campos de cargas; sin afirmar sincronización |
| NutriSport e852644 | 88/88 unitarias y build; E2E original 9/10, con fallo PWA visible |
| NutriSport borrador local | Build y 10/10 E2E aprobados; test específico de primera instalación/actualización también aprobado |

Entorno actual: Python 3.12.14, Node 24.19.0, Chromium 154.0.8037.57 en Debian. No confundir con Chromium 153 histórico. Datos ficticios, worktrees y contextos de navegador separados; no es certificación de sandbox de SO/red. Los tests revisados trabajan localmente sin backend productivo.

## Hallazgos y límites que no se cierran

- RM conserva 154 U+FFFD y flechas corruptas en design-preview/index.html. Confirmado visualmente a 320 px y en fuente. El historial consultado no contiene un original limpio. No se inventaron textos del curso.
- RM PR2 está 38 commits adelante y 2 detrás de main. Simulación de reconciliación, sin mover ramas: conflictos en curso-arm.html, entrenamiento-base.html, entrenamiento.html y tests/browser.cjs. Suites verdes separadas no certifican una integración inexistente.
- Modo demo mantiene MODO01/MODO02. El borrador de seguridad no migra datos ni cambia rutinas globales; el modo de recuperación es de sesión y conserva originales. Guardado en múltiples claves no constituye transacción de backend.
- Base Modo pendiente: propuesta 1.3 por sus copias, cargas e historial local; falta decisión del usuario y contrato de sincronización/autorización de servidor antes de prometer uso entre dispositivos.
- Vercel: 403 del equipo. Se generó consentimiento para revisión del usuario, sin otorgar permisos. R2: HEAD bloqueado por proxy 403; no se intentó bypass. No se certifican streaming, disponibilidad desplegada ni alojamiento NutriSport.
- CI son documentos propuestos, no workflows activos ni checks remotos aprobados. Están condicionados a la base y archivos de test indicados.

## Incidencias operativas conservadas

La primera instalación npm falló por su caché predeterminada; reintento con caché en workspace y scripts deshabilitados pasó. Una inspección asumió package.json en RM PR2 y otra buscó study-ui.js inexistente; se corrigió la inspección, sin modificar productos por esos errores. La suite RM con servidor genérico falló porque las páginas heredadas carecen de meta charset; con el servidor UTF-8 equivalente al original pasó. El nuevo parche de dos meta charset pasa las mismas 32 comprobaciones aun con servidor genérico. El script preview ARM tenía rutas fijas de navegador/URL; se parametrizó y pasó sin cambiar sus observaciones. Las reproducciones negativas de ARM, inyección Modo y PWA Nutri se mantienen como failed, seguidas por su evidencia de corrección; no se borran ni se cuentan como tests aprobados.

## Aprobaciones agrupadas

- **B-ARM:** nueva actualización en la misma rama del PR #2 de Modo, sólo operations/arm-orchestrator: corrección de verify, tests, evidencia recuperada, script parametrizable, este cierre y propuestas documentales. Sin instalar CI ni tocar pantallas del producto.
- **B-NUTRI:** actualizar PR #2 existente de calculadora-nutricion-deportiva, base e852644, con PwaSettings.tsx y regresión stage-two.spec.ts. Parche en proposals/phase2-20261028/nutrisport-pwa.patch.
- **B-RM:** actualizar PR #4 existente de RM, base 24a584c, sólo dos meta charset. Parche rm-charset.patch. No reconciliar ni fusionar PR #2.

Cada push puede disparar automatizaciones o un preview ya configurados; no se solicita despliegue manual, producción, merge, gastos ni nivel C. B-MODO no se solicita todavía: antes debe elegirse base; su parche de seguridad queda concreto y revisable como alternativa para la demo. La aprobación de ARM no implica aprobar los otros dos proyectos.

El resto no está bloqueado por trabajo local pendiente: requiere esas decisiones/accesos o aprobar el diseño de integración RM antes de una fase de reconciliación funcional. Los originales arm.sqlite, snapshot.json, INFORME.md y evidencias del 23/10 se conservan.
