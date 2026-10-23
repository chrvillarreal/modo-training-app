# ARM Orchestrator v1.0 — auditoría y entrega verificable
Fecha de entrega: 23/10/2026 (Argentina). Fuente previa: ARM_Orchestrator_v1_Auditoria_2026-10-23.md. Esta entrega actualiza sus pendientes con evidencia nueva.

## Resultado
Se implementó un núcleo local supervisado en Python/SQLite y se auditaron los tres repositorios mediante inventario de ramas, PR, comparación con main, checks y pruebas de los candidatos prioritarios. No es un servicio multiagente permanente: ChatGPT Work sigue siendo el coordinador, y los contratos de Desarrollo y UX/QA quedan preparados para la siguiente integración.

No se modificó main, no hubo pushes, merges, despliegues, escrituras en bases productivas ni gastos. Los worktrees Git de Modo y NutriSport quedaron limpios. RM se recuperó por el conector debido al rechazo de clonación privada: 39 archivos de texto validados contra sus hashes Git; se omitió el ZIP binario, no necesario para estos tests.

## Versiones y PR
| Proyecto | Versión probada | PR abiertos | Diferencia del candidato frente a main |
|---|---|---|---|
| RM Training | design/study-preview-20261019 — 24a584cb520c9d8e4f4e51e0ee7b0e5d6f0fd312 | #2 y #4 | #4: 2 commits adelante, 0 detrás; sólo dos archivos design-preview |
| Modo Training | feat/rutina-agustin-link — 0bb492437d3f24d2b29c1ed608ffc8080b21230a | #1 | 1 adelante, 0 detrás; sólo agrega rutina-agustin.html |
| NutriSport | feat/nutrisport-pro-local-mvp — e852644c4ce29635024eedbbf3fb8acfc6ff8df8 | #1 Nhost y #2 local | #2: 11 adelante, 0 detrás, 41 archivos modificados |

Inventario completo: evidence/inventory.json (6 ramas RM, 5 Modo, 3 NutriSport). Comparaciones: evidence/comparisons.json. Las ramas históricas y Nhost se inventariaron/compararon; no se ejecutaron todas sus suites. El PR #1 de NutriSport no se integró ni modificó.

RM #2 diverge de main: 38 commits adelante y 2 detrás. No asumir que puede integrarse sin reconciliar mejoras posteriores. RM #4 mantiene las pantallas actuales y agrega un preview separado. Sus pruebas de estudio prueban el código compartido con main; la revisión adicional del preview se informa aparte.
Modo tiene una versión más avanzada en feature/modo-training-1.3 (prototype/modo-training-1.3.html), y un panel comercial local en feat/ai-operations-mvp (operations/index.html). Se leyeron ambos: no son backend multiusuario ni orquestador de agentes. No se extrapolan los defectos de index.html al prototipo 1.3. La rama main/Agustín conserva el index de demo.

## Pruebas ejecutadas
| Componente | Resultado | Evidencia |
|---|---|---|
| ARM Orchestrator | 20/20 tests Python | evidence/orchestrator-tests.log |
| RM unitarias | 7/7, exit 0 | evidence/rm-unit.log |
| RM navegador, suite existente | 32 comprobaciones, sin errores JS | evidence/rm-browser.log |
| RM rediseño | 24 combinaciones ruta/ancho sin overflow, notas persisten; textos corruptos detectados | evidence/rm-preview.json |
| Modo | 4 defectos reproducidos; inicio sin overflow a 320/390/1440 | evidence/modo-repro.json |
| NutriSport unitarias | 88/88, cuatro archivos | evidence/nutri-unit.log |
| NutriSport build | TypeScript y Vite correctos | evidence/nutri-build.log |
| NutriSport E2E original | 10/10, 16,9 s | evidence/nutri-e2e.log |
| NutriSport E2E con servidor estático alternativo | 10/10, 14,7 s | evidence/nutri-browser-results.json y nutri-e2e-adapted.log |

RM: once aulas a 390/1440, notas, prácticas, repaso diferido, penalización/omisión en examen, expiración, buscador y respaldo. Preview: inicio, catálogo, aula 11, práctica, notas y biblioteca a 320/390/430/1440; las peticiones externas se bloquearon. No se certifica reproducción de videos ni disponibilidad completa de R2.
NutriSport: CRUD, evaluación, navegación a seis anchos (320–1440), backup/restauración, rechazo de datos inválidos, IndexedDB denegado, métodos, seguimiento, PDF offline y actualización PWA conservando datos. Se usó información ficticia; estas pruebas no constituyen validación clínica de ecuaciones ni recomendaciones nutricionales.
Modo: los tests son reproducciones de defectos, no aceptación del producto. Inyección comprobada con marcador local inocuo; no se probó exfiltración ni se usaron registros reales.

Entorno: Node 24.19.0, Python 3.12.14, Chromium 153.0.8010.0. Descarga estándar de Chromium falló; se obtuvo un binario mediante paquete npm sin scripts de instalación. La suite original NutriSport requirió retirar variables proxy del proceso. La suite alternativa conserva los tests y cambia sólo servidor/configuración local; no modifica la app. El error inicial de implementación del registro ARM se corrigió y se conserva el log inicial separado.
Aislamiento: copias/worktrees y perfiles de navegador independientes. El host rechazó namespaces bwrap; no hubo sandbox de sistema operativo/red fuerte. Ninguna suite revisada usó un backend productivo. No confundir esta separación con aislamiento de código arbitrario.

## Hallazgos priorizados
P0: ninguno confirmado dentro del alcance; esto no demuestra ausencia global de vulnerabilidades.

| Prioridad | ID | Hallazgo / siguiente acción |
|---|---|---|
| P1 | MODO-01 | La página de Agustín es estática: cero controles para registrar cargas. |
| P1 | MODO-02 | R y mt_routine son globales: editar alumno 1 cambia lo mostrado para alumno 2. |
| P1 | MODO-03 | Nombre de alumno renderizado como HTML ejecuta un marcador JS local. Escapar según contexto o usar DOM seguro. |
| P2 | MODO-04 | JSON corrupto en mt_students interrumpe inicialización; falta recuperación. |
| P2 | RM-02 | Rediseño contiene caracteres U+FFFD y controles en textos/flechas; comprobado en navegador y blob exacto. |
| P1 | RM-03 | PR #2 diverge de main; reconciliar en copia y ejecutar su suite antes de cualquier integración. |
| P1 | ARM-01 | Lectura de despliegues del equipo bloqueada por autorización Vercel. |
| P1 | ARM-03 | Elegir base funcional Modo y autorizar destino persistente de ARM. |
| P2 | ARM-02 | Incorporar CI funcional en RM/Modo; comentarios Vercel no son suite QA. |
| P2 | RM-01 | Completar accesibilidad y recursos externos del rediseño. |
| P2 | NUTRI-01 | Identificar alojamiento NutriSport sin confundirlo con app de estudio nutricional. |

backlog.json contiene pasos, esperado, observado, evidencia y aceptación. Los defectos de producto se documentaron; no se aplicaron cambios persistentes ni se publicaron parches.

## Despliegues: evidencia y límite
El listado Vercel mostró RM y Modo y sus IDs conocidos. Consultar despliegues con el team correcto devolvió 403: requiere autorización para chrvillarreals-projects. La herramienta de autorización indicada por el error no está expuesta en esta sesión; no se sorteó esa restricción.
Como evidencia adicional, GitHub registra estado Vercel success en los SHAs exactos de RM #2/#4 y Modo #1. Esto certifica el estado informado del despliegue, no su disponibilidad actual ni su funcionamiento.
- RM #4: https://vercel.com/chrvillarreals-projects/rm-training/B4GL6NJmiExXahxqzY7hGHwS7aAm
- Modo #1: https://vercel.com/chrvillarreals-projects/modo-training-app/4zc6WbiYht1rxkuwihj4DFuowAnP
- NutriSport #2: check verify success en https://github.com/chrvillarreal/calculadora-nutricion-deportiva/actions/runs/39333240705/job/118336322727
No se identificó un proyecto Vercel inequívoco de la calculadora. Los proyectos de estudio nutricional son otra aplicación. Ausencia de commit statuses en NutriSport no significa suite fallida: el check verify sí pasó.

## Sistema entregado
arm.py, arm.sqlite y snapshot.json: tres proyectos; backlog, ejecuciones reales registradas y solicitud pendiente para publicación del paquete. Evidencias con hash, registro encadenado y pruebas de rechazo de acciones, duplicados, expiración y cambio de alcance.
No contiene ejecutor de shell, scheduler, agentes LLM permanentes ni conectores autenticados embebidos. Las aprobaciones no son autenticación humana: son registros para revisión, sin capacidad de escribir fuera. Esto evita presentar un prototipo como servicio autónomo completo.
Contratos agents/development.md y agents/ux-qa.md: entradas, límites, flujos y salida estructurada. README incluye comandos y plan técnico de siguiente fase.

## Intervención necesaria
1. Para completar auditoría remota: autorizar lectura del equipo chrvillarreals-projects en la integración Vercel. No se necesita permiso de despliegue.
2. Propuesta concreta para persistir ARM: publicar exactamente este paquete (código, tests, contratos y evidencias, excluyendo artefactos de prueba de alumnos) en operations/arm-orchestrator/ de una nueva rama feat/arm-orchestrator-v1 en modo-training-app, basada en main ee3b6f5ca6865707bf3374722d51c1cad4c174ed. Crear PR borrador, sin merge ni producción. No se hizo el push porque el usuario exige autorización antes de cambios persistentes. El destino puede cambiarse antes de aprobar.
3. Antes de corregir funciones Modo, decidir si la base será el prototipo 1.3 o la demo de main. Se recomienda evaluar 1.3 como candidato por sus series, asignación e historial local; todavía no afirmar sincronización entre dispositivos.

Aceptación parcial explícita: núcleo local verificable y auditoría de código/tests entregados; auditoría de despliegues actual y ejecución automática de agentes pendientes de acceso e integración autorizados.
