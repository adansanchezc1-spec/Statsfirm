| # | Fuente | Dataset / recurso | Año / periodo | Granularidad | Variables principales | Frecuencia | Análisis posible | Link |
|---:|---|---|---|---|---|---|---|---|
| 1 | **UPRA** | Evaluaciones Agropecuarias Municipales (EVA) | 2019–2025 | Municipio × producto/actividad × periodo | Área, producción, rendimiento, cultivos, inventarios pecuarios | Semestral / anual | Crecimiento, participación, concentración, rendimiento, tendencias |  |
| 2 | **DANE** | SIPSA – Abastecimiento de alimentos | 2018–2025 | Fecha × origen × municipio × mercado × producto | Cantidad abastecida, origen, destino, producto, grupo | Periódica | Flujos de abastecimiento, concentración, estacionalidad, tendencias |  |
| 3 | **DANE** | SIPSA – Precios mayoristas | 2025–2026 | Fecha × mercado mayorista × producto | Precio, producto, mercado | Diaria / mensual | Tendencia, volatilidad, CV, estacionalidad, variación |  |
| 4 | **DANE** | Cuenta Satélite de la Agroindustria | 2022–2024 preliminar | Cadena × fase × año | Producción, consumo intermedio, VAB, variables económicas | Anual | Crecimiento, participación, productividad, valor agregado |  |
| 5 | **DANE** | Estadísticas de Exportaciones | 2025–2026 | Mes × producto/arancel × departamento × destino | FOB USD, kg, país destino, departamento, subpartida | Mensual | Crecimiento, concentración, diversificación, USD/kg |  |
| 6 | **DANE** | Microdatos de Exportaciones (EXPO) | 2025–2026 | Operación × producto × destino × origen × tiempo | Subpartida, país, departamento, kg, FOB, transporte | Mensual / registro | Panel producto-destino, concentración, crecimiento |  |
| 7 | **ICA** | Estimaciones poblacionales y Censo Pecuario Nacional (PowerBI / XLSX) | 2025–2026 | Municipio (DIVIPOLA 5 dígitos) × especie × categoría × año | Bovinos, porcinos, bufalinos, ovinos, caprinos, avícola, equinos | Anual | Distribución territorial, concentración (HHI), densidad pecuaria | [Ver Ficha Metodológica 06](6-fichas_tecnicas_metodologicas_fuentes.md#ficha-tecnica-y-metodologica-06-ica---censo-pecuario-nacional-e-inventario-pecuario) |
| 8 | **UPRA** | SIPRA – Sistema de Información para la Planificación Rural Agropecuaria | Actual | Polígono municipal (DIVIPOLA `DDMMM`) × cadena × capa | Aptitud (A1-A3, No Apta), fronteras agrícolas, zonificación | Variable | Análisis espacial, aptitud, especialización territorial | [Ver Geoportal SIPRA](https://sipra.upra.gov.co/nacional) |
| 9 | **UPRA** | RECIA – Infraestructura agropecuaria | 2025–2026 | Infraestructura × municipio (DIVIPOLA `DDMMM`) | Tipo, ubicación, características y capacidad instalada | Actualización progresiva | Cobertura, concentración, accesibilidad, brechas de acopio | [Ver Ficha Metodológica 08](6-fichas_tecnicas_metodologicas_fuentes.md#ficha-tecnica-y-metodologica-08-upra---recia-red-de-infraestructura-agropecuaria) |
| 10 | **AgroNET** | Estadísticas pecuarias e índice de agroinsumos | 2025–2026 | Mes × municipio/departamento × producto/insumo | Precio de leche, volumen recolectado, precios fertilizantes | Mensual | Tendencias, volatilidad, presión de costos sobre margen | [Ver Ficha Metodológica 09](6-fichas_tecnicas_metodologicas_fuentes.md#ficha-tecnica-y-metodologica-09-agronet---estadisticas-pecuarias-e-insumos) |
| 11 | **Datos Abiertos** | Exportaciones Agrícolas y Bioinsumos (`gaic-b8aw`) | 2025–2026 | Municipio / Departamento × producto / bioinsumo | Subpartidas, volumen, FOB USD, tipo insumo | Mensual | Ingesta Socrata, penetración bioinsumos, agroexportación | [Ver Ficha Metodológica 11](6-fichas_tecnicas_metodologicas_fuentes.md#ficha-tecnica-y-metodologica-11-datos-abiertos---exportaciones-agricolas-y-bioinsumos-gaic-b8aw) |



| Dimensión | Granularidad necesaria | Fuente |
|---|---|---|
| **Oferta agrícola** | Producto × municipio × tiempo | EVA |
| **Producción** | Producto × municipio × tiempo | EVA |
| **Rendimiento** | Producto × municipio × tiempo | EVA |
| **Oferta pecuaria** | Especie × municipio × tiempo | ICA |
| **Abastecimiento** | Producto × origen × mercado × tiempo | SIPSA Abastecimiento |
| **Precios** | Producto × mercado × tiempo | SIPSA Precios |
| **Estacionalidad** | Producto × territorio/mercado × tiempo | EVA + SIPSA |
| **Valor agregado** | Cadena × fase × año | Cuenta Satélite |
| **Exportaciones** | Producto × destino × origen × tiempo | DANE EXPO |
| **Mercados internacionales** | Producto × país × tiempo | DANE EXPO |
| **Infraestructura** | Infraestructura × territorio | RECIA |
| **Aptitud territorial** | Territorio × cadena × capa | SIPRA |
| **Costos productivos** | Producto × territorio × tiempo | AgroNET |
| **Demanda interna directa** | Producto × mercado/consumidor × tiempo | **Pendiente de fuente específica** |
| **Demanda internacional directa** | Producto × país comprador × tiempo | **Complementar EXPO con fuentes internacionales** |