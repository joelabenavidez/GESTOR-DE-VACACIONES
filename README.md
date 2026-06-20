Gestor de Vacaciones
Descripción

Gestor de Vacaciones es una aplicación desarrollada en Python que simula la automatización del proceso administrativo de solicitud y gestión de vacaciones dentro de una organización.

El sistema fue desarrollado como Trabajo Práctico Integrador para la materia Organización Empresarial de la Tecnicatura Universitaria en Programación (TUP).

La solución implementa un modelo basado en BPMN 2.0, permitiendo que empleados, administradores y gerencia interactúen con el sistema mediante menús y validaciones de negocio.

Funcionalidades
Empleados
Inicio de sesión mediante legajo y contraseña.
Solicitud de vacaciones.
Consulta de historial de solicitudes.
Consulta de saldo disponible.
Cancelación de vacaciones aprobadas.
Cambio de contraseña.
Administrador
Desbloqueo de usuarios.
Blanqueo de contraseña.
Consulta de empleados.
Listado completo de empleados.
Consulta de vacaciones aprobadas.
Cancelación administrativa de vacaciones.
Cierre del sistema.
Gerente
Consulta de empleados.
Visualización de estadísticas generales.
Consulta del calendario anual de vacaciones.
Consulta del registro de auditoría del sistema.
Acceso al menú de administración.
Reglas de Negocio Implementadas
Las vacaciones deben solicitarse con un mínimo de 30 días de anticipación.
No se pueden solicitar más días de los disponibles.
No se permiten solicitudes inferiores a 7 días.
No se permite dejar un remanente menor a 7 días.
No se permiten períodos de vacaciones superpuestos para un mismo empleado.
Se controla el cupo máximo de empleados ausentes por clase.
Los usuarios quedan bloqueados luego de tres intentos fallidos de contraseña.
Las vacaciones pueden cancelarse con al menos 30 días de anticipación.
El administrador puede cancelar vacaciones sin restricción de plazo.
Persistencia de Datos

El sistema utiliza archivos CSV como base de datos simulada.

empleados.csv

Contiene:

Legajo
Nombre
Clase
Antigüedad
Días disponibles
Contraseña cifrada
Estado de acceso
vacaciones_2026.csv

Contiene:

Legajo
Fecha de solicitud
Fecha de inicio
Fecha de fin
Cantidad de días
Días restantes
Estado de la solicitud
calendario.csv

Contiene:

Fecha
Empleados de Clase 1 ausentes
Empleados de Clase 2 ausentes
Empleados de Clase 3 ausentes
interacciones.txt

Registro de auditoría del sistema.

Tecnologías Utilizadas
Python 3
CSV
Datetime
Hashlib (SHA-256)
OS
Time
Calendar
Ejecución
Descargar o clonar el repositorio.
git clone https://github.com/USUARIO/gestor-vacaciones.git
Ingresar al directorio del proyecto.
cd gestor-vacaciones
Ejecutar el programa.
python main.py
Usuarios de Prueba
Gerente
Legajo	Contraseña
123623	soyelgerente
Administrador
Legajo	Contraseña
999999	123456
Empleados

Todos los empleados poseen inicialmente:

Contraseña: 123456

Ejemplos:

Legajo	Nombre
100010	Valeria Rios
100016	Andrea Benítez
100031	Héctor Silva
100037	Emiliano Correa
100050	Claudia Bravo

Estos registros permiten probar distintos escenarios:

Empleados sin saldo disponible.
Empleados bloqueados.
Diferentes clases de personal.
Diferentes antigüedades.
Distintos saldos de vacaciones.
Estructura del Proyecto
GestorVacaciones/
│
├── main.py
├── empleados.csv
├── vacaciones_2026.csv
├── calendario.csv
├── interacciones.txt
├── README.md
└── Informe.pdf
Modelado BPMN

El proceso fue modelado utilizando BPMN 2.0, diferenciando claramente:

Usuario
Sistema / Bot

El flujo contempla:

Inicio de sesión.
Validaciones de negocio.
Solicitud de vacaciones.
Consulta de historial.
Cancelación de solicitudes.
Gestión administrativa.
Gestión gerencial.
Autor

Joel Benavidez

Tecnicatura Universitaria en Programación (TUP)

Trabajo Práctico Integrador – Organización Empresarial

2026

Licencia

Proyecto desarrollado con fines exclusivamente académicos para la Tecnicatura Universitaria en Programación. No destinado a uso comercial.
