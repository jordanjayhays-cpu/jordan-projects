# PEPE Energía DataLens · notas del rediseño (v4 → v5)

Archivo: `PEPE_Energia_DataLens_v5.html` (un solo HTML, D3.js desde cdnjs, sin build).
Original conservado: `PEPE_Energia_Dashboard_v4 (original).html`.
Todas las cifras son las de la v4. No se ha inventado ningún dato. Lo único retirado es el ruido
aleatorio (`Math.random`) del gráfico de picos horarios, que cambiaba en cada carga.

## Qué cambia y por qué

| Principio | v4 | v5 |
|---|---|---|
| Arco narrativo (Dykes, sesión 7) | 13 pestañas por tema (Consumo, Plantas, ESG…) | 6 vistas que cuentan una historia: Resumen → Plantas → Cuándo → Anomalías → Carbono y coste → Qué hacer |
| Una idea por gráfico (Knaflic) | Títulos descriptivos: "Consumo mensual 2025 vs 2024" | Títulos que dicen el hallazgo: "El consumo bajó todos los meses de 2025, salvo en diciembre" |
| Paleta de realce (sesión 3, Strachnyi) | 12 colores, donut arcoíris, semáforos en cada tabla | 4 colores con significado fijo: naranja = foco, gris = contexto, rojo = alerta, verde = objetivo o mejora |
| Gestalt: proximidad y región común (sesión 2) | Rejilla de tarjetas sin jerarquía | Cada vista abre con titular, cifras clave y gráficos agrupados por pregunta; caja negra alrededor del pico en el mapa de calor |
| Etiquetas directas (Jones) | Leyendas debajo de cada gráfico | Las series llevan su nombre al final de la línea; cifras encima de las barras |
| Sin gráficos engañosos | Radares, gauges, donut, treemap, Sankey en lienzo | Barras ordenadas, puntos con línea de referencia, pendiente, mapa de calor con una sola escala |
| Interacción con sentido (Rosling) | Filtros que ocultan datos | Resaltar, no filtrar: al pasar por una planta se atenúan las demás en toda la vista; la tabla sigue ordenable |
| Honestidad con el dato | "DUMMY" en una etiqueta | Pie de página con datos, fuentes, previsiones marcadas con asterisco y límites |
| Movimiento | Fundido de 0,3 s por sección | Entrada en cascada de tarjetas, líneas que se dibujan, barras que crecen, contador en cifras clave; se respeta `prefers-reduced-motion` |

## Qué conserva de la v4

- Marca y tipografía (Montserrat, naranja PEPE, cabecera negra).
- Tabla de plantas ordenable por columna.
- Selector de planta en el mapa de calor.
- Asistente de datos (chat) con las mismas respuestas, redactadas más cortas.
- Hoja de ruta por fases y las ocho palancas con inversión, ahorro y retorno.

## Qué se ha quitado y dónde está ahora

- Radares (plantas, benchmarks, ESG): sustituidos por filas con punto PEPE, sector y mejor de su clase.
- Gauges y matriz de semáforos: sus cifras están en la tabla de plantas y en las tarjetas de cifras clave.
- Treemap y Sankey: sustituidos por barras apiladas de mix y de alcance 1/2, que se leen con una escala.
- Pestaña "Conclusiones": sus seis puntos están repartidos como titulares de los gráficos.
- Filtros Anual / Q4 / Diciembre: sólo la vista anual. Si hacen falta, es fácil añadir un selector de periodo.

## Para revisar antes de usarlo con un cliente

- Verificar las cifras de origen (siguen siendo de demostración).
- Confirmar el nombre de la empresa, el logo y la fecha.
- Decidir si el chat se queda: responde sólo con las cifras del panel.
