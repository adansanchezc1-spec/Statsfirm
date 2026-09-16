# ADR-001: Adopción de Arquitectura Hexagonal (Ports & Adapters)
**Fecha**: 2026-09-14  
**Estado**: Aceptado  
**Fase PDCO**: PLAN → DEVELOPMENT  
**Autores**: Equipo de Ingeniería de Software y Ciencia de Datos — Agro Stat & Tech Co.  

---

## Contexto
La plataforma Agrostat procesa datos agrícolas y climatológicos para pronóstico de mercado y control bioestadístico. Los requerimientos no funcionales (RNF-007, RNF-008) exigen alta mantenibilidad, testabilidad unitaria sin dependencias de red o de base de datos, y capacidad para migrar de almacenamiento local a la nube o intercambiar librerías analíticas sin reescribir la lógica de negocio. 

Las alternativas tradicionales (arquitectura en capas 3-tier clásica o frameworks acoplados tipo Django ORM) tienden a propagar dependencias de base de datos dentro del dominio, dificultando las pruebas y violando el principio de Inversión de Dependencias (DIP).

## Decisión
Se adopta la **Arquitectura Hexagonal (Puertos y Adaptadores)** formulada por Alistair Cockburn:
1. El **Núcleo de Dominio** (`domain/`) contendrá únicamente entidades, value objects y servicios puros (matemática bioestadística, validaciones DAMA-BOK, reglas de Nelson). No importará librerías de persistencia (DuckDB, Pandas, SQL) ni frameworks web (FastAPI).
2. Los **Puertos** (`ports/`) definirán contratos abstractos (`abc.ABC`) para los puntos de entrada (Driving Ports) y de salida (Driven Ports).
3. Los **Casos de Uso** (`application/use_cases/`) orquestarán los flujos de negocio comunicándose exclusivamente con los puertos.
4. Los **Adaptadores** (`adapters/`) implementarán los detalles técnicos concretos (FastAPI, CLI Click/Typer, repositorios DuckDB/Parquet, clientes HTTP Socrata/OData).

## Consecuencias

### Positivas:
- **Testabilidad Máxima**: El 100% de la lógica bioestadística y de validación de calidad se prueba con tests unitarios instantáneos sin levantar servicios ni bases de datos.
- **Independencia de Frameworks y Proveedores**: El motor SQL (DuckDB) puede sustituirse por PostgreSQL o Snowflake en el futuro cambiando únicamente el adaptador de salida.
- **Múltiples Interfaces de Ejecución**: La misma lógica del pipeline puede ejecutarse indistintamente desde un cron job, un CLI o una API REST.

### Negativas / Trade-offs:
- Mayor número de clases e interfaces abstractas (*overhead* inicial de diseño y tipado).
- Necesidad de DTOs y conversores (mappers) entre las capas externas y el dominio interno.
