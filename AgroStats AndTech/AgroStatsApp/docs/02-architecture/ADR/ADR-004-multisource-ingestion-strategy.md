# ADR-004: Estrategia de Conectores Polimórficos de Ingesta para Múltiples Fuentes Oficiales
**Fecha**: 2026-09-14  
**Estado**: Aceptado  
**Fase PDCO**: PLAN → DEVELOPMENT  
**Autores**: Equipo de Ingeniería de Software y Ciencia de Datos — Agro Stat & Tech Co.  

---

## Contexto
El sistema debe extraer información de un ecosistema gubernamental heterogéneo:
- DANE: API Socrata (datos.gov.co) para precios mayoristas (`SIPSA_P`), volúmenes de abastecimiento municipal (`SIPSA_A`) e insumos agropecuarios (`SIPSA_I`).
- MinAgricultura / Agronet: Evaluaciones Agropecuarias Municipales (EVA).
- IDEAM: Portal DHIME y API OData de datos abiertos para series climatológicas diarias (precipitación, temperaturas extremas, humedad).
- NASA POWER / CHIRPS: Reanálisis satelital para radiación solar incidente y evapotranspiración.
- Gremios e instituciones bursátiles (BMC, Fedearroz, Fenalce).

Se requiere que la adición de una nueva fuente no implique refactorizar los casos de uso ni el pipeline de curaduría (principio Open/Closed). Además, debe implementarse tolerancia a fallos de red con reintentos exponenciales (RNF-005).

## Decisión
Se implementa una arquitectura de **Conectores Polimórficos** basada en el patrón GoF **Factory Method** y **Strategy**:
1. **Puerto de Salida `ExternalSourceExtractorPort`**: Contrato base que define el método abstracto `extract_batch(start_date, end_date, filters) -> RawBatch`.
2. **Adaptadores Concretos Especializados**:
   - `SocrataSipsaExtractor`: Maneja paginación de Socrata con tokens de aplicación, cláusulas `$where` y conversiones de tipos.
   - `IdeamClimaExtractor`: Realiza peticiones a la API de estaciones meteorológicas del IDEAM.
   - `NasaPowerExtractor`: Consulta la API REST de NASA POWER con coordenadas lat/long de las zonas agrícolas prioritarias.
3. **Resiliencia de Red**: Cada adaptador integra un decorador de reintentos con backoff exponencial (`tenacity` o lógica nativa controlada) que tolera caídas temporales de las APIs de origen (RNF-005).
4. **Firma Criptográfica SHA-256**: Cada lote crudo extraído genera un hash SHA-256 para verificar la inmutabilidad y garantizar la no repetición de ingesta del mismo lote (RNF-006).

## Consecuencias

### Positivas:
- **Modularidad Total**: Agregar una fuente (ej. Fedegan) solo requiere crear una clase que herede de `ExternalSourceExtractorPort`.
- **Aislamiento de Errores**: Si la API del IDEAM presenta latencia o caída temporal, el pipeline de precios del DANE continúa ejecutándose normalmente.
- **Trazabilidad de Auditoría**: Cada registro en el lago de datos mantiene el identificador exacto de la fuente de origen y el hash del lote crudo.

### Negativas / Trade-offs:
- Requiere mantener configuraciones independientes (tokens de API, límites de tasa de peticiones) para cada servicio externo en `config.py`.
