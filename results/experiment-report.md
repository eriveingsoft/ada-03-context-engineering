# Reporte de Análisis de Context Engineering

## Métricas Comparativas

| Métrica | Experimento A (Contexto Mínimo) | Experimento B (Contexto de Repositorio) | Experimento C (Contexto Diseñado) |
| :--- | :--- | :--- | :--- |
| **Tiempo de ejecución** | 5 min | 5 min | 4 min |
| **Tests iniciales (pasando/fallando)** | 2 pasando / 2 fallando | 2 pasando / 2 fallando | 2 pasando / 2 fallando |
| **Tests finales (pasando/fallando)** | 8 pasando / 0 fallando | 4 pasando / 0 fallando | 4 pasando / 0 fallando |
| **Archivos modificados / creados** | 6 archivos (`customer.py`, `repository.py`, `test_customer.py`, `test_repository.py`, `pytest.ini`, `conftest.py`) | 3 archivos (`customer.py`, `repository.py`, `pytest.ini`) | 3 archivos (`customer.py`, `repository.py`, `pytest.ini`) |
| **Cambios innecesarios** | Altos (modificó archivos de prueba existentes, creó `conftest.py`) | Bajos (únicamente generó `pytest.ini`) | Nulos / Mínimos (siguió estrictamente el principio de menor cambio posible) |
| **Intervenciones humanas** | 0 | 0 | 0 |
| **Anomalías detectadas** | Sobreingeniería, alteró la suite de pruebas sin autorización | Fuga de contexto al intentar inspeccionar ramas históricas de Git | Ninguna; se apegó directamente a `SPEC.md` y `AGENTS.md` |

---

## Análisis Cualitativo

### Experimento A: Contexto Mínimo
Al proporcionarle únicamente el objetivo y una instrucción imprecisa de inspeccionar el repositorio, el agente resolvió la lógica central del dominio pero mostró una sobreingeniería marcada. Modificó la suite de pruebas (`test_customer.py` y `test_repository.py`), incrementando el conteo de pruebas de 4 a 8, y generó `tests/conftest.py` junto con `pytest.ini`. A pesar de que la solución funcionaba, violó el principio de mínima perturbación en el código base.

### Experimento B: Contexto de Repositorio
Al contar con instrucciones explícitas paso a paso (leer el README, inspeccionar fuentes, inspeccionar pruebas, inferir requerimientos, ejecutar pruebas antes y después, y realizar el cambio mínimo), el agente respetó la suite existente y evitó modificar los archivos de prueba. Sin embargo, la instrucción abierta de "inspeccionar el repositorio" provocó que explorara el historial de ramas de Git (`git branch -a`, `git diff exp-a..exp-b`), generando una fuga de contexto imprevista y requiriendo intervención humana manual para autorizar el comando.

### Experimento C: Contexto Diseñado
Equipado con especificaciones funcionales explícitas (`SPEC.md`) y directivas operativas de comportamiento (`AGENTS.md`), el agente logró el tiempo de ejecución más rápido (4 minutos) con cero intervenciones humanas. Respetó estrictamente las interfaces públicas, no modificó los archivos de prueba, realizó validaciones previas y posteriores a la implementación, y verificó todos los criterios de aceptación sin realizar indagaciones externas en el historial de Git.

---

## Conclusiones
1. El context engineering actúa como un plano de control para los agentes de IA: sin restricciones operativas y de límites claros (`AGENTS.md`), los agentes tienden a aplicar sobreingeniería en las soluciones o a modificar las pruebas para adaptarlas a su propio código.
2. Instrucciones genéricas como "inspeccionar el repositorio" pueden derivar en fugas de contexto hacia el historial del sistema de control de versiones, exigiendo intervención humana adicional.
3. Desacoplar los requisitos funcionales del negocio (`SPEC.md`) de las reglas de comportamiento del agente (`AGENTS.md`) maximiza la precisión de la implementación, reduciendo al mínimo los efectos secundarios y el tiempo de ejecución.