# Context Engineering Experiment

## Hypothesis
Proveer al agente de desarrollo especificaciones desacopladas y estructuradas (requisitos funcionales en `SPEC.md` y barreras operativas en `AGENTS.md`) reducirá el tiempo de ejecución, evitará la sobreingeniería o modificación no autorizada de pruebas, eliminará fugas de contexto fuera del espacio de trabajo y garantizará una implementación con la mínima perturbación del código base.

## Experimental Setup
- **Entorno de ejecución:** Windows 11, PowerShell 7.6.6.
- **Plataforma de IA:** Antigravity CLI 1.1.28 (`Gemini 3.8 Flash`).
- **Stack técnico:** Python 3.14.3, `pytest` 9.0.2.
- **Aislamiento:** Ramas Git independientes (`exp-a`, `exp-b`, `exp-c`) derivadas del commit inicial limpio en `main`.

---

## Métricas Comparativas (Sección 16)

| Métrica | A | B | C |
| :--- | :--- | :--- | :--- |
| **Tests passing** | 8 | 4 | 4 |
| **Tests failing** | 0 | 0 | 0 |
| **Requisitos cumplidos** | 7/7 | 7/7 | 7/7 |
| **Archivos modificados** | 6 | 3 | 3 |
| **Cambios innecesarios** | Altos | Bajos | Nulos / Mínimos |
| **Iteraciones** | 14 | 18 | 10 |
| **Intervenciones humanas** | 0 | 1 | 0 |
| **Problemas introducidos** | Modificación no autorizada de la suite de pruebas y sobreingeniería | Fuga de contexto hacia ramas externas de Git | Ninguno |
| **Tiempo** | 5 min | 5 min | 4 min |
| **Score /10** | 7.0 / 10 | 9.0 / 10 | 10.0 / 10 |

---

## Evaluación Context Engineering Score (Sección 17)

| Criterio | Puntos Máx. | Experimento A | Experimento B | Experimento C |
| :--- | :---: | :---: | :---: | :---: |
| **Correctness** | 30 | 25 | 30 | 30 |
| **Requirements** | 20 | 20 | 20 | 20 |
| **Minimal Change** | 15 | 3 | 12 | 15 |
| **Maintainability** | 15 | 12 | 14 | 15 |
| **Security/Safety** | 10 | 4 | 6 | 10 |
| **Verification** | 10 | 6 | 8 | 10 |
| **Total (/100)** | **100** | **70** | **90** | **100** |
| **Score Final (/10)** | **10.0** | **7.0** | **9.0** | **10.0** |

### Justificación de Puntajes
- **Experimento A (70/100):** Obtuvo 3/15 en *Minimal Change* y 4/10 en *Security/Safety* debido a que reescribió los archivos de prueba existentes (`test_customer.py` y `test_repository.py`) para inflar las pruebas a 8 y creó archivos ajenos (`tests/conftest.py`). Aunque la lógica funciona, alterar la suite de pruebas sin permiso viola las reglas básicas de seguridad y control de regresión.
- **Experimento B (90/100):** Respetó el código y los tests originales (30/30 en *Correctness*), pero en *Security/Safety* (6/10) presentó una fuga de aislamiento al ejecutar `git diff exp-a..exp-b`, demandando intervención humana manual. En *Minimal Change* obtuvo 12/15 al crear `pytest.ini`.
- **Experimento C (100/100):** Desempeño impecable en todas las dimensiones. Cumplió los 7 requisitos funcionales, mantuvo intacta la suite de pruebas existente, ejecutó pruebas pre y post implementación, no inspeccionó ramas externas y aplicó el cambio más limpio posible.

---

## A — Minimal Context
- **Prompt:** `Implement the customer email update functionality. Inspect the repository first.`
- **Results:** 8 tests pasando. Archivos tocados: `customer.py`, `repository.py`, `test_customer.py`, `test_repository.py`, `conftest.py`, `pytest.ini`.
- **Human intervention:** 0 intervenciones.
- **Score:** 7.0 / 10.
- **Observations:** El agente sufrió de sobreingeniería. Al no tener directivas sobre qué no tocar, consideró insuficiente el archivo de pruebas original y lo reescribió, además de crear configuraciones accesorias de `pytest`. 

## B — Repository Context
- **Prompt:** Instrucción detallada en lenguaje natural solicitando inspeccionar `README.md`, el código fuente, los tests, inferir requisitos, ejecutar tests antes/después y aplicar cambios mínimos.
- **Results:** 4 tests pasando. Archivos tocados: `customer.py`, `repository.py`, `pytest.ini`.
- **Human intervention:** 1 intervención (autorización requerida para ejecutar `git diff exp-a..exp-b`).
- **Score:** 9.0 / 10.
- **Observations:** Mucho más disciplinado respecto al código productivo y las pruebas existentes. No obstante, al pedirle "inspeccionar el repositorio", intentó leer el historial y ramas previas de Git, generando una fuga de contexto.

## C — Engineered Context
- **Prompt:** `Implement the customer email update functionality. Follow SPEC.md and AGENTS.md. Inspect the repository first, run tests before and after changes, and explain your verification.`
- **Results:** 4 tests pasando. Archivos tocados: `customer.py`, `repository.py`, `pytest.ini`.
- **Human intervention:** 0 intervenciones.
- **Score:** 10.0 / 10.
- **Observations:** La presencia de `AGENTS.md` como plano de control y `SPEC.md` como criterio de aceptación eliminó la ambigüedad. El agente diagnosticó los dos tests que fallaban antes de tocar código, resolvió únicamente lo necesario, no alteró tests y verificó el 100% de los criterios.

---

## Comparative Results
El Experimento C demostró ser superior en velocidad (4 minutos frente a 5 en A y B) y en precisión arquitectónica. Mientras que en el Experimento A el agente intentó compensar la falta de contexto reescribiendo la infraestructura de testing, y en B la sobrecarga de instrucciones en el prompt provocó indagaciones innecesarias en Git, el Experimento C operó de forma determinista y acotada a su entorno.

## Error Analysis
1. **Modificación de pruebas (Exp A):** Una IA no restringida asume erróneamente que las pruebas existentes son maleables y las ajusta a su solución en lugar de ajustar su solución a las pruebas.
2. **Fuga de contexto en Git (Exp B):** prompts extensos que piden "explorar el repositorio" incitan al agente a utilizar comandos de bajo nivel (`git branch`, `git diff`), rompiendo el sandboxing del espacio de trabajo.
3. **Falta de resolución de imports (Exp A, B y C):** La estructura del proyecto requería configurar `pythonpath = .`, lo que motivó en los tres casos la creación o configuración de `pytest.ini`.

## Context Quality Analysis
- **Contexto en prompt (Exp B):** Frágil y propenso a saturación de ventana de contexto o alucinación de comandos exploratorios.
- **Contexto en archivos desacoplados (Exp C):** Estructurado, persistente, mantenible y versionable junto con el código base. Separa claramente el *qué* (`SPEC.md`) del *cómo* (`AGENTS.md`).

## Conclusions
1. El Context Engineering actúa como el sistema inmunológico del proyecto contra la sobreingeniería y las decisiones no deterministas de los modelos de lenguaje.
2. Limitar el alcance mediante archivos como `AGENTS.md` es más efectivo que intentar prevenir malas prácticas mediante prompts conversacionales extensos.
3. Las pruebas unitarias deben tratarse como contratos inmutables durante la interacción con agentes, a menos que se especifique formalmente lo contrario.

## What I Would Change
1. Incluir en la plantilla base del repositorio el archivo `pytest.ini` para evitar que los agentes tengan que crearlo por temas de importación de módulos en Python.
2. Agregar en `AGENTS.md` una regla explícita que prohíba inspeccionar el árbol de Git o ramas externas para evitar intervenciones manuales en herramientas CLI.

---

## 19. Preguntas de Análisis

### 1. ¿Cuál fue tu hipótesis?
Que proveer especificaciones funcionales formales (`SPEC.md`) junto con directivas operativas estrictas (`AGENTS.md`) guiaría al agente a generar código correcto y mínimo, reduciendo el tiempo de ejecución y evitando modificaciones indebidas en los tests o el historial del repositorio.

### 2. ¿Cuál experimento produjo el mejor resultado y por qué?
El **Experimento C**. Logró el menor tiempo de ejecución (4 minutos), cero intervenciones humanas, 100% de tests pasando en la suite original y cumplió estrictamente los criterios de aceptación sin alterar archivos ajenos.

### 3. ¿Qué errores aparecieron en A y no en C?
En A, el agente sobreingeniereó la solución modificando los tests existentes (`test_customer.py` y `test_repository.py`), duplicando el conteo de tests a 8 y creando un archivo adicional (`tests/conftest.py`). En C, las directivas de `AGENTS.md` evitaron tocar las pruebas.

### 4. ¿Qué información del repositorio fue más útil?
Los tests unitarios originales (`tests/test_customer.py` y `tests/test_repository.py`) y las definiciones de los dataclasses en `src/customer.py`. Indicaron los nombres exactos de los campos a preservar, las excepciones esperadas (`invalid-email`, `customer-not-found`) y la estructura de datos.

### 5. ¿Qué aportó SPEC.md?
Definió los requisitos funcionales y los criterios de aceptación exactos (validación sintáctica, normalización a minúsculas, inmutabilidad de `customer_id` y `created_by`, y manejo de excepciones), eliminando la necesidad de que el agente adivinara el comportamiento del negocio.

### 6. ¿Qué función tuvo AGENTS.md?
Actuó como marco normativo y operativo (*guardrails*). Estableció las reglas de conducta: preferir el menor cambio posible, prohibir modificaciones en los tests, ejecutar `pytest` antes y después de editar, y no agregar dependencias externas.

### 7. ¿Más contexto significa necesariamente mejor contexto?
No. El Experimento B tuvo más texto descriptivo en su prompt y eso derivó en confusión, provocando que el agente inspeccionara ramas de Git externas (`git diff exp-a..exp-b`). El contexto debe ser estructurado, específico y relevante, no simplemente voluminoso.

### 8. ¿Qué información fue redundante?
En el Experimento B, detallarle paso a paso en el prompt que leyera el `README.md` y revisara el código fuente resultó redundante con el comportamiento por defecto de la herramienta, dispersando la atención del agente fuera de su espacio de trabajo.

### 9. ¿Qué intervención humana fue necesaria?
En el Experimento B, fue necesario autorizar manualmente en la consola la ejecución del comando `git diff exp-a..exp-b` que el agente intentó invocar para comparar historiales entre ramas.

### 10. ¿Qué cambiarías en SPEC.md y AGENTS.md?
- En `SPEC.md`: Especificar el regex estándar admitido para el correo electrónico y clarificar si el dominio debe soportar subdominios múltiples.
- En `AGENTS.md`: Agregar la instrucción explícita de no ejecutar comandos de Git que involucren ramas externas ni inspeccionar historiales fuera del árbol de trabajo actual.

### 11. ¿Qué aprendiste sobre la responsabilidad del desarrollador al usar agentes?
El desarrollador deja de ser un mero escritor de sintaxis para convertirse en un arquitecto de contexto y auditor de calidad. Es responsable de establecer límites operativos rigurosos, definir contratos claros y verificar que el agente resuelva el problema sin introducir deuda técnica o vulneraciones en el código base.

---

## Pregunta Final

**¿Por qué un desarrollador que utiliza agentes de código necesita aprender Context Engineering y no solamente mejores prompts?**

El *Prompt Engineering* optimiza la forma en que se solicita una tarea puntual, pero los agentes autónomos operan sobre sistemas complejos donde el contexto conversacional resulta insuficiente y efímero. Un modelo de lenguaje no falla únicamente por una mala redacción, sino por falta de límites estructurales en su entorno de trabajo.

El *Context Engineering* diseña la arquitectura de información que rodea al agente: organiza especificaciones funcionales (`SPEC.md`), barreras de seguridad operativas (`AGENTS.md`), suites de prueba inmutables y documentación versionable. Mientras un mejor prompt solo intenta persuadir al modelo en un turno aislado, el Context Engineering establece un plano de control sistemático, persistente y reproducible. Permite que el agente comprenda qué construir, cómo verificarlo y qué límites respetar, minimizando la sobreingeniería, evitando la modificación inadvertida de pruebas y garantizando que el código generado sea seguro, modular y mantenible dentro de entornos profesionales.