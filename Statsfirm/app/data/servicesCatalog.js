/**
 * STATSFIRM CO. — CATÁLOGO OFICIAL DE SERVICIOS Y PORTAFOLIO TECNOLÓGICO
 * Normativa: Documento 01.A (Identidad Corporativa) y Documento 05 (Catálogo de Servicios)
 * Diseñado con lenguaje de valor empresarial accesible para tomadores de decisiones no-ingenieros.
 */

const servicesCatalog = {
  company: {
    name: 'Statsfirm Co.',
    tagline: 'Transformación Empresarial de Alta Fidelidad en Datos, Software y Procesos',
    purpose: 'Liberar el potencial de las organizaciones resolviendo sus desafíos más complejos mediante la ingeniería de alta precisión, transformando la incertidumbre en ventaja competitiva verificable.',
    mission: 'Diseñar, construir e implementar capacidades empresariales de vanguardia en Datos, Inteligencia Artificial, Software y Procesos. Empoderamos a las empresas con tecnología soberana, gobernada y automatizada, acelerando su transición hacia modelos de negocio guiados por el valor real.',
    vision: 'Consolidarnos como la firma referente de ingeniería de datos y transformación empresarial en Iberoamérica, creando plataformas analíticas de clase mundial y productos de software propios desde nuestro laboratorio Innova Lab.',
    slaUptime: '99.9% garantizado contractualmente',
    slaResponseTime: '< 2 horas hábiles en atención comercial y < 15 min en soporte crítico'
  },

  // Mapeo de dolores empresariales a soluciones (IHC para No-Ingenieros)
  businessPains: [
    {
      id: 'pain-excel-chaos',
      icon: '📊',
      painQuestion: '¿Nuestros reportes en Excel nunca coinciden entre departamentos?',
      symptom: 'Ventas dice una cifra, Finanzas dice otra y Operaciones tiene un tercer reporte. Se pierden horas en reuniones discutiendo quién tiene la razón.',
      solutionTitle: 'Unificación en Única Fuente de Verdad (Data Lakehouse)',
      howItWorks: 'Conectamos automáticamente todos sus programas (facturación, CRM, inventarios) en una sola base central. La información se limpia y estandariza sola.',
      businessBenefit: 'Una sola cifra oficial e indiscutible para toda la empresa. Cero tiempo perdido conciliando archivos a mano.',
      recommendedServiceId: 'data-engineering',
      ctaText: 'Unificar los datos de mi empresa'
    },
    {
      id: 'pain-blind-decisions',
      icon: '👁️',
      painQuestion: '¿La dirección general toma decisiones "a ciegas" o con reportes viejos?',
      symptom: 'Para saber cómo va el mes hay que esperar 15 días a que el equipo cierre informes. Cuando se detecta un problema, ya es demasiado tarde para corregirlo.',
      solutionTitle: 'Tableros Ejecutivos de Control en Tiempo Real (Business Intelligence)',
      howItWorks: 'Diseñamos pantallas ejecutivas intuitivas accesibles desde su celular o computadora donde ve sus ventas, márgenes y clientes actualizados al minuto.',
      businessBenefit: 'Decisiones rápidas y con certeza total. Alertas inmediatas en su celular cuando una meta o margen esté en riesgo.',
      recommendedServiceId: 'bi-analytics',
      ctaText: 'Ver mis números en tiempo real'
    },
    {
      id: 'pain-inventory-churn',
      icon: '📉',
      painQuestion: '¿Tiene dinero atrapado en inventario o pierde clientes sin saber por qué?',
      symptom: 'Se compra producto de más que se queda en bodega, o falta stock cuando el cliente lo pide; además, clientes valiosos dejan de comprar sin aviso.',
      solutionTitle: 'Inteligencia Artificial Predictiva y Modelos de Demanda',
      howItWorks: 'Nuestros modelos matemáticos analizan su historial y predicen con semanas de anticipación cuánto va a vender y qué clientes están por irse.',
      businessBenefit: 'Reducción drástica de mermas y sobre-stock, y retención oportuna de clientes clave antes de que se vayan con la competencia.',
      recommendedServiceId: 'ai-data-science',
      ctaText: 'Predecir demanda y retener clientes'
    },
    {
      id: 'pain-bottlenecks',
      icon: '⏳',
      painQuestion: '¿Sus procesos internos son lentos y los clientes se quejan por demoras?',
      symptom: 'Aprobaciones manuales en cadenas infinitas de correos, trámites en papel o personal calificado haciendo tareas mecánicas y aburridas.',
      solutionTitle: 'Optimización y Automatización de Procesos (BPMN 2.0)',
      howItWorks: 'Radiografiamos cómo fluye el trabajo en su negocio, eliminamos los pasos inútiles y automatizamos las tareas repetitivas mediante software.',
      businessBenefit: 'Tiempos de entrega reducidos hasta en un 60% y colaboradores enfocados en generar valor y ventas en vez de llenar formatos.',
      recommendedServiceId: 'process-engineering',
      ctaText: 'Automatizar los procesos de mi equipo'
    },
    {
      id: 'pain-flaky-software',
      icon: '💻',
      painQuestion: '¿Sus sistemas se caen, son lentos o no se comunican entre sí?',
      symptom: 'Sistemas heredados que fallan en horas pico, interfaces complejas que los empleados evitan usar o gastos excesivos en servidores sin justificación.',
      solutionTitle: 'Ingeniería de Software & Nube de Alta Disponibilidad',
      howItWorks: 'Modernizamos sus aplicaciones para que sean tan rápidas y seguras como las de los bancos globales, funcionando en la nube con respaldo automático.',
      businessBenefit: 'Cero caídas operativas, experiencia impecable para sus clientes y costos de nube optimizados sin pagar por capacidad desperdiciada.',
      recommendedServiceId: 'software-cloud',
      ctaText: 'Modernizar mis sistemas y aplicaciones'
    }
  ],

  serviceLines: [
    {
      id: 'data-engineering',
      number: '01',
      title: 'Data Intelligence & Engineering',
      simpleName: 'La Tubería y Bodega Central de Información de su Negocio',
      hookText: '¿Sus datos están regados en mil sistemas y nadie sabe cuál es la cifra real?',
      icon: '🌊',
      forNonEngineers: {
        whatIsIt: 'Es el servicio que conecta todos los programas que usa su empresa (facturación, CRM, hojas de cálculo, bodegas) y los canaliza a una gran "bodega central" limpia, segura y organizada.',
        metaphor: 'Es como reemplazar cientos de tuberías viejas y con fugas por un acueducto moderno de acero inoxidable donde el agua (la información) siempre llega pura y con presión.',
        businessPainSolved: 'Elimina las discrepancias entre departamentos, erradica los Excel desactualizados y evita que pierda información crítica de clientes o ventas.',
        tangibleOutcome: 'Una sola fuente oficial de la verdad para toda la empresa, disponible 24/7 sin caídas y lista para ser consultada.'
      },
      capabilities: [
        'Conexión automática de programas y bases de datos sin intervención manual',
        'Limpieza y eliminación de registros duplicados o corruptos',
        'Almacenamiento seguro en la nube con copias de respaldo inmutables',
        'Cumplimiento estricto de privacidad y protección de datos corporativos (DAMA-BOK)',
        'Estructura lista para soportar auditorías y el crecimiento de su negocio'
      ],
      techStack: ['Apache Kafka', 'Apache Spark', 'Databricks', 'Snowflake', 'dbt Core', 'Delta Lake'],
      deliverables: 'Base central de datos unificada, automatizaciones de sincronización continua y catálogo de información empresarial.'
    },
    {
      id: 'bi-analytics',
      number: '02',
      title: 'Business Intelligence & Decision Analytics',
      simpleName: 'Tableros de Control Ejecutivos para Decidir con Certeza',
      hookText: '¿Espera semanas a fin de mes para saber si su negocio ganó o perdió dinero?',
      icon: '📈',
      forNonEngineers: {
        whatIsIt: 'Transformamos los datos limpios en tableros visuales, claros y elegantes (estilo cabina de avión) para que los líderes vean en segundos cómo marcha cada área.',
        metaphor: 'Es como cambiar el velocímetro roto de su auto por una pantalla de navegación digital de alta definición que le avisa con antelación si se está quedando sin combustible.',
        businessPainSolved: 'Evita decisiones basadas en corazonadas o reportes tardíos; cualquier directivo puede consultar sus indicadores desde su celular o laptop.',
        tangibleOutcome: 'Reducción del 80% en tiempo dedicado a crear informes manuales y claridad total sobre ventas, márgenes, cobranzas y rentabilidad.'
      },
      capabilities: [
        'Tableros ejecutivos en Power BI, Looker o Tableau adaptados a su negocio',
        'Árboles de Indicadores Clave (KPIs) acordados con la junta directiva',
        'Simuladores de escenarios comerciales ("¿Qué pasa si subo el precio un 5%?") ',
        'Alertas inteligentes a su correo o WhatsApp si un indicador cae',
        'Capacitación al equipo para que cualquier usuario cree sus propios reportes'
      ],
      techStack: ['Power BI', 'Google Looker', 'Tableau', 'Cube.js', 'SQL Server', 'DuckDB'],
      deliverables: 'Consolas analíticas ejecutivas en modo oscuro profesional, modelos de KPIs y capacitaciones directivas.'
    },
    {
      id: 'ai-data-science',
      number: '03',
      title: 'AI Engineering & Applied Data Science',
      simpleName: 'Inteligencia Artificial y Modelos Predictivos para su Negocio',
      hookText: '¿Quiere que la Inteligencia Artificial trabaje para aumentar sus ventas y recortar costos?',
      icon: '🤖',
      forNonEngineers: {
        whatIsIt: 'Desarrollamos fórmulas matemáticas y algoritmos de inteligencia artificial que aprenden del pasado de su negocio para predecir el futuro y automatizar decisiones complejas.',
        metaphor: 'Es como tener a un analista genio trabajando las 24 horas del día que le advierte qué productos se van a agotar antes de que ocurra y qué clientes necesitan atención urgente.',
        businessPainSolved: 'Elimina el exceso de inventario muerto, evita la pérdida silenciosa de clientes y optimiza rutas logísticas y asignación de precios.',
        tangibleOutcome: 'Modelos de predicción en producción que incrementan la rentabilidad neta y ahorran cientos de horas de cálculo.'
      },
      capabilities: [
        'Pronóstico de ventas y demanda con semanas o meses de anticipación',
        'Detección anticipada de clientes insatisfechos o propensos a retirarse (Churn)',
        'Optimización matemática de rutas de entrega, fletes e inventarios en bodega',
        'Asistentes de IA especializados que responden dudas con los documentos privados de su empresa',
        'Monitoreo continuo para garantizar que los modelos nunca pierdan precisión'
      ],
      techStack: ['Python 3.11', 'PyTorch', 'Scikit-learn', 'MLflow', 'FastAPI', 'LangChain'],
      deliverables: 'Modelos de predicción conectados a sus sistemas de gestión, paneles de control predictivo y reglas de negocio automatizadas.'
    },
    {
      id: 'software-cloud',
      number: '04',
      title: 'Software & Cloud Engineering',
      simpleName: 'Desarrollo de Software y Nube de Alta Disponibilidad',
      hookText: '¿Sus sistemas se cuelgan en días clave o sus clientes se quejan de plataformas lentas?',
      icon: '⚡',
      forNonEngineers: {
        whatIsIt: 'Construimos aplicaciones web, portales de clientes y servicios digitales con el mismo nivel de ingeniería que usan las empresas de tecnología más grandes del mundo.',
        metaphor: 'Es como construir un rascacielos con cimientos antisísmicos: sin importar cuántas miles de personas entren al mismo tiempo, el edificio no vibra ni se cae.',
        businessPainSolved: 'Elimina la frustración de plataformas que fallan, portales lentos que ahuyentan clientes y facturas desmedidas de servicios en la nube.',
        tangibleOutcome: 'Sistemas que nunca se caen, tiempos de carga ultra-rápidos en milisegundos y costos de servidores optimizados.'
      },
      capabilities: [
        'Portales para clientes y plataformas operativas internas a la medida',
        'Conexión segura entre sistemas mediante APIs modernas y de alta velocidad',
        'Migración y optimización de servidores en la nube (AWS, Google Cloud, Azure)',
        'Seguridad blindada contra accesos no autorizados y ciberataques',
        'Actualizaciones automáticas sin interrumpir la operación de su negocio'
      ],
      techStack: ['Go', 'Node.js', 'Python', 'React / Next.js', 'Kubernetes', 'Docker', 'AWS / Azure'],
      deliverables: 'Aplicaciones contenerizadas, infraestructura en la nube documentada y pipelines de despliegue continuo.'
    },
    {
      id: 'process-engineering',
      number: '05',
      title: 'Process Engineering & BPM',
      simpleName: 'Optimización y Automatización de Procesos de Trabajo',
      hookText: '¿Su equipo gasta la mitad de su jornada en trámites manuales, correos y firmas?',
      icon: '⚙️',
      forNonEngineers: {
        whatIsIt: 'Auditamos paso a paso cómo se hace el trabajo en su empresa, eliminamos los cuellos de botella y programamos flujos automatizados para que las tareas se ejecuten solas.',
        metaphor: 'Es como transformar una calle llena de semáforos dañados y desvíos confusos en una autopista de peaje electrónico donde todo avanza a máxima velocidad.',
        businessPainSolved: 'Acaba con los trámites estancados en el escritorio de alguien, evita reprocesos y reduce drásticamente las quejas por demoras en la atención.',
        tangibleOutcome: 'Procesos estandarizados en diagramas claros (BPMN 2.0) ejecutables en software, reduciendo los tiempos de ciclo en un 40% a 60%.'
      },
      capabilities: [
        'Descubrimiento real de cuellos de botella analizando los registros del sistema (Process Mining)',
        'Modelado oficial en estándar mundial BPMN 2.0 ejecutable en Camunda',
        'Formularios digitales que guían a los empleados y validan la información al instante',
        'Asignación clara de responsables para cada tarea (Matriz de responsabilidades)',
        'Medición en vivo del tiempo que tarda cada proceso de principio a fin'
      ],
      techStack: ['Camunda 7 & 8', 'BPMN 2.0 (ISO 19510)', 'Process Mining', 'TOGAF ADM', 'Camunda Forms'],
      deliverables: 'Flujos de procesos diagramados y automatizados en Camunda, formularios digitales y manuales operativos estandarizados.'
    }
  ],

  saasProducts: [
    {
      name: 'Statsfirm DataWeave',
      badge: 'Innova Lab Product',
      tagline: 'Rastreo y Calidad del Dato sin Fricción',
      desc: 'Plataforma que vigila automáticamente la salud de sus datos. Si un sistema externo envía información incompleta o dañada, DataWeave avisa antes de que afecte a sus reportes o clientes.',
      features: ['Vigilancia de datos 24/7', 'Alertas preventivas a su correo', 'Historial visual de dónde vino cada dato']
    },
    {
      name: 'Statsfirm ProcessMatrix',
      badge: 'Innova Lab Product',
      tagline: 'El Radar de Procesos de su Empresa en Vivo',
      desc: 'Conecta las actividades cotidianas de su negocio con diagramas visuales en tiempo real, mostrándole en qué departamento o persona se están acumulando los trámites y demoras.',
      features: ['Detección de cuellos de botella en vivo', 'Visor de tiempos de respuesta', 'Auditoría automática de procesos']
    },
    {
      name: 'Statsfirm MetricsEngine',
      badge: 'Innova Lab Product',
      tagline: 'Definición Única de Métricas para Toda la Compañía',
      desc: 'Garantiza que la fórmula con la que se calcula "Ventas Netas", "Margen Bruto" o "Rotación" sea exactamente la misma en todas las áreas de la compañía, sin sorpresas en junta directiva.',
      features: ['Glosario unificado de números', 'Conexión a Power BI y Excel', 'Respuestas ultra-rápidas']
    }
  ],

  engagementModels: [
    {
      id: 'squad-as-a-service',
      title: 'Squad as a Service (Célula de Élite Dedicada)',
      tagline: 'Un equipo completo de ingeniería a su servicio, sin lidiar con contrataciones',
      desc: 'Asignamos a su empresa un equipo multidisciplinario sincronizado (Líder Arquitecto, Ingenieros de Datos, Científicos de IA, Especialistas de Negocio y Scrum Master) trabajando en entregas tangibles cada 15 días.',
      idealFor: 'Empresas que necesitan velocidad inmediata y excelencia técnica sin los costos ni demoras de reclutar y capacitar personal interno.'
    },
    {
      id: 'fixed-scope',
      title: 'Fixed-Scope Transformation (Proyecto Cerrado por Hitos)',
      tagline: 'Alcance, cronograma e inversión cerrados con garantía de entrega',
      desc: 'Diseñamos un plan de trabajo con objetivos específicos (ej. construir el Data Lakehouse o automatizar un proceso clave) con entregables definidos, fechas fijas y costo acordado de antemano.',
      idealFor: 'Empresas con un requerimiento puntual o presupuesto anual cerrado que buscan un retorno de inversión garantizado.'
    }
  ]
};

module.exports = servicesCatalog;
