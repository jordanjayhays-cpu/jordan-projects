# fiovana · notas del rediseño de dos paneles

Carpeta: `fiovana-dashboards/`. Originales conservados con el sufijo "(original)". Sistema de diseño: el mismo de PEPE Energía v5 (Montserrat, naranja = foco, gris = contexto, rojo = alerta, verde = objetivo), para que todos los entregables de DataLens se parezcan.

## Vecinos Felices · presupuesto 26-27 (v10 → v11)

| Qué | v10 | v11 |
|---|---|---|
| Estructura | 7 pestañas por grupo contable + palancas | 4 preguntas: cómo vamos, en qué partidas, cuándo se gasta, qué decidir |
| Mes de corte | barra de progreso fija en mes 8 | control "mes cerrado" de 1 a 12 que recalcula todo el panel |
| Datos mensuales | patrón previsto + ruido aleatorio en cada carga | patrón previsto sin ruido: cada carga muestra lo mismo |
| Detalle de facturas | generador de facturas con proveedores reales inventados (Iberdrola, Mapfre, Otis…) | retirado; es información que debe venir de la contabilidad real |
| Alarmas | semáforo rojo para cualquier partida al 100%, incluido el seguro pagado en enero | estados que distinguen pago anual, pago periódico, estacional, adelantada y sobre presupuesto |
| Fondo de reserva | mezclado en el total (89% "ejecutado") | separado: presupuesto operativo 108.094 € y fondo 10.027 € intacto |
| Gráficos | 18 (donut, treemap, mapa de calor, top 10, desviación mensual, gauges…) | 9, cada uno con una frase de titular |
| Nuevo | — | caja de la comunidad mes a mes con cuota fija: toca fondo en septiembre; apoya la palanca de cuotas estacionales |
| Supuestos visibles | 40 viviendas escondido en el código | 40 viviendas y rangos de ahorro declarados en pantalla y en el pie |

Verificar antes de usar con la comunidad: número real de viviendas y coeficientes; rangos de ahorro de las palancas (son estimaciones del administrador); si el fondo de reserva se cobra dentro de la cuota.

## Propuesta comercial (v1 → v2)

| Qué | v1 | v2 |
|---|---|---|
| Formato | 8 pestañas de un "dashboard" | una página que se lee de arriba abajo, como una propuesta |
| Idea | 4 KPIs sin jerarquía | una frase: dashboard propio desde 1.000 € una vez, frente a 35.000 € al año de una plataforma |
| Benchmark | barras del máximo de cada competidor (200.000 $) frente a nuestro precio | rangos completos mínimo a máximo en escala logarítmica, fuentes citadas |
| Coste a un año | creación + 12 meses frente a SaaS mínimo y freelancer mínimo | igual, pero diciendo que las alternativas van por su mínimo |
| Gráficos retirados | donut de rondas de revisión, barras de SLA, barras de precio por plan | la tabla comparativa lo cubre |
| Inconsistencia corregida | mantenimiento a medida: 450 €/mes en una tabla y 350 €/mes en otra | 450 € en ambos sitios; confirmar |
| Añadido | — | bloque "siguiente paso" con una garantía propuesta (si la primera versión no responde a la pregunta, no se factura el segundo 50%). Es una propuesta de redacción; fiovana decide si la ofrece |

Verificar antes de enviar: moneda de las referencias (dólares mostrados como euros 1 a 1), el precio de mantenimiento a medida, y si se quiere ofrecer la garantía.
