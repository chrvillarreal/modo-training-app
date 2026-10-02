# Arquitectura funcional propuesta

## Entrenador
Inicio
├── Alumnos
│   └── Ficha
│       ├── Datos / anamnesis
│       ├── Objetivos
│       ├── Rutina activa
│       ├── Historial de sesiones
│       └── Progreso
├── Rutinas
│   ├── Plantillas
│   ├── Duplicar
│   ├── Personalizar
│   └── Asignar
├── Biblioteca
│   └── Ejercicio
├── Calendario
└── Progreso

## Alumno — próxima fase
Inicio
├── Entrenamiento de hoy
│   ├── Ejercicio
│   ├── Series / reps / carga
│   ├── RIR/RPE
│   └── Finalizar sesión
├── Historial
└── Progreso

## Modelo de datos futuro
profiles, coach_athlete_links, athletes, assessments, exercise_library, routine_templates, routines, routine_days, routine_exercises, assigned_plans, training_sessions, session_exercises, session_sets, progress_metrics, coach_notes, media.

## Regla de historial
Una sesión completada no debe depender de que la plantilla actual siga igual. Guardar snapshot/versionado de lo prescripto y lo ejecutado.
